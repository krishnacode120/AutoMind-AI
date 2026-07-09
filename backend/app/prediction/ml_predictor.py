"""Machine-learning vehicle predictor backed by trained artifacts."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import joblib

from app.prediction.base_predictor import VehiclePredictor
from app.prediction.rule_predictor import RuleBasedPredictor
from app.schemas.alert import AlertReport
from app.schemas.health import HealthReport
from app.schemas.maintenance import MaintenanceReport
from app.schemas.prediction import PredictionResult
from app.utils.time_utils import utc_now

logger = logging.getLogger(__name__)


class MLPredictor(VehiclePredictor):
    """Predictor that uses the persisted best ML model."""

    _cached_model: Any | None = None
    _cached_feature_names: list[str] | None = None
    _cache_initialized: bool = False
    _cache_error: str | None = None

    def __init__(
        self,
        *,
        fallback_to_rule: bool = False,
        models_dir: str | Path | None = None,
    ) -> None:
        """Initialize predictor and load trained model once."""
        self._fallback_to_rule = fallback_to_rule
        self._rule_predictor = RuleBasedPredictor()
        self._models_dir = (
            Path(models_dir).resolve()
            if models_dir is not None
            else Path(__file__).resolve().parents[1] / "ml" / "models"
        )
        self._model_path = self._models_dir / "best_model.pkl"
        self._metadata_path = self._models_dir / "model_metadata.json"
        self._ensure_model_loaded()

    def predict(
        self,
        health_report: HealthReport,
        alert_report: AlertReport,
        maintenance_report: MaintenanceReport,
    ) -> PredictionResult:
        """Generate an ML prediction, or fallback when configured."""
        if self._is_model_available():
            prediction = self._predict_from_model(
                health_report=health_report,
                alert_report=alert_report,
                maintenance_report=maintenance_report,
            )
            logger.info("Prediction generated via ML model")
            return prediction

        message = self._missing_artifact_message()
        if self._fallback_to_rule:
            logger.warning(
                "Fallback to rule predictor occurs: %s",
                message,
            )
            fallback_result = self._rule_predictor.predict(
                health_report,
                alert_report,
                maintenance_report,
            )
            return fallback_result.model_copy(
                update={"prediction_type": "rule-fallback"}
            )

        raise RuntimeError(message)

    def supports_training(self) -> bool:
        """Return whether this predictor supports training."""
        return True

    def model_name(self) -> str:
        """Return the predictor model name."""
        return "ml-best-model"

    def _predict_from_model(
        self,
        health_report: HealthReport,
        alert_report: AlertReport,
        maintenance_report: MaintenanceReport,
    ) -> PredictionResult:
        """Run model inference and transform output into schema."""
        model = self.__class__._cached_model
        feature_names = self.__class__._cached_feature_names
        if model is None or feature_names is None:
            raise RuntimeError(self._missing_artifact_message())

        feature_row = self._build_feature_row(
            feature_names=feature_names,
            health_report=health_report,
            alert_report=alert_report,
            maintenance_report=maintenance_report,
        )

        predicted_label = int(model.predict([feature_row])[0])
        positive_probability = float(model.predict_proba([feature_row])[0][1])
        confidence = (
            positive_probability
            if predicted_label == 1
            else 1.0 - positive_probability
        )

        predicted_failure = (
            "Failure Predicted"
            if predicted_label == 1
            else "No Immediate Failure Predicted"
        )
        recommended_action = (
            "Immediate Service"
            if predicted_label == 1
            else "Continue Monitoring"
        )

        return PredictionResult(
            prediction_type="ml",
            confidence=round(confidence, 6),
            predicted_failure=predicted_failure,
            recommended_action=recommended_action,
            estimated_remaining_km=self._minimum_remaining_km(
                maintenance_report,
            ),
            timestamp=utc_now(),
        )

    def _build_feature_row(
        self,
        feature_names: list[str],
        health_report: HealthReport,
        alert_report: AlertReport,
        maintenance_report: MaintenanceReport,
    ) -> dict[str, Any]:
        """Construct metadata-ordered feature values with safe defaults."""
        base_features: dict[str, Any] = {
            "health_score": health_report.health_score,
            "health_status": health_report.health_status,
            "alert_count": alert_report.alert_count,
            "highest_alert_severity": (
                alert_report.highest_severity.value
                if alert_report.highest_severity is not None
                else None
            ),
            "maintenance_priority": maintenance_report.overall_priority.value,
            "maintenance_task_count": maintenance_report.task_count,
            "prediction_type": "ml",
            "prediction_confidence": None,
            "predicted_failure": None,
            "estimated_remaining_km": self._minimum_remaining_km(
                maintenance_report,
            ),
            "driving_profile": None,
            "injected_faults": None,
            "fault_count": 0,
        }

        # Telemetry-derived features are unavailable in current interface and
        # are intentionally left as missing values for model preprocessing.
        return {
            feature_name: base_features.get(feature_name)
            for feature_name in feature_names
        }

    def _ensure_model_loaded(self) -> None:
        """Load model and metadata once per process."""
        if self.__class__._cache_initialized:
            return

        try:
            if not self._model_path.exists():
                raise FileNotFoundError(
                    f"Missing model artifact: {self._model_path}"
                )
            if not self._metadata_path.exists():
                raise FileNotFoundError(
                    f"Missing model metadata: {self._metadata_path}"
                )

            metadata = json.loads(
                self._metadata_path.read_text(encoding="utf-8")
            )
            feature_names = metadata.get("feature_names")
            if not isinstance(feature_names, list) or not feature_names:
                raise ValueError(
                    "Invalid metadata: 'feature_names' must be a non-empty list"
                )

            self.__class__._cached_model = joblib.load(self._model_path)
            self.__class__._cached_feature_names = [str(name) for name in feature_names]
            self.__class__._cache_error = None
            logger.info(
                "ML model loaded successfully from %s",
                self._model_path,
            )
        except Exception as error:
            self.__class__._cached_model = None
            self.__class__._cached_feature_names = None
            self.__class__._cache_error = str(error)
        finally:
            self.__class__._cache_initialized = True

    def _is_model_available(self) -> bool:
        return (
            self.__class__._cached_model is not None
            and self.__class__._cached_feature_names is not None
        )

    def _missing_artifact_message(self) -> str:
        """Build clear model availability error message."""
        if self.__class__._cache_error:
            return f"ML predictor unavailable: {self.__class__._cache_error}"
        return (
            "ML predictor unavailable: missing best_model.pkl "
            "or model_metadata.json."
        )

    def _minimum_remaining_km(
        self,
        maintenance_report: MaintenanceReport,
    ) -> float | None:
        """Return lowest remaining-km estimate across maintenance tasks."""
        estimates = [
            task.estimated_km_remaining
            for task in maintenance_report.tasks
            if task.estimated_km_remaining is not None
        ]
        if not estimates:
            return None
        return float(min(estimates))
