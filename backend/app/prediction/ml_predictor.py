"""Vehicle predictor using locally trained, trusted model artifacts."""

import json
import logging
from functools import lru_cache
from pathlib import Path
from typing import Any

import joblib

from app.ml.features import MODEL_FEATURES
from app.prediction.base_predictor import VehiclePredictor
from app.prediction.rule_predictor import RuleBasedPredictor
from app.schemas.alert import AlertReport
from app.schemas.health import HealthReport
from app.schemas.maintenance import MaintenanceReport
from app.schemas.prediction import PredictionResult
from app.utils.time_utils import utc_now

logger = logging.getLogger(__name__)


@lru_cache(maxsize=4)
def _load_artifacts(directory: str, model_mtime: int, metadata_mtime: int):
    """Cache by location and revision, including models trained after startup."""
    path = Path(directory)
    metadata = json.loads((path / "model_metadata.json").read_text(encoding="utf-8"))
    features = metadata.get("feature_names")
    if not isinstance(features, list) or set(features) != set(MODEL_FEATURES):
        raise ValueError(
            "Incompatible model features; retrain using the current pipeline"
        )
    model = joblib.load(path / "best_model.pkl")
    if list(model.classes_) != [0, 1]:
        raise ValueError("Model must be trained with binary labels 0 and 1")
    return model, features


class MLPredictor(VehiclePredictor):
    """Run inference with the same report features used by offline training."""

    def __init__(
        self, *, fallback_to_rule: bool = False, models_dir: str | Path | None = None
    ) -> None:
        self._fallback_to_rule = fallback_to_rule
        self._models_dir = (
            Path(models_dir).resolve()
            if models_dir
            else Path(__file__).resolve().parents[1] / "ml" / "models"
        )

    def predict(
        self,
        health_report: HealthReport,
        alert_report: AlertReport,
        maintenance_report: MaintenanceReport,
    ) -> PredictionResult:
        """Predict current rule-defined failure risk, or use the configured fallback."""
        try:
            model_path = self._models_dir / "best_model.pkl"
            metadata_path = self._models_dir / "model_metadata.json"
            model, features = _load_artifacts(
                str(self._models_dir),
                model_path.stat().st_mtime_ns,
                metadata_path.stat().st_mtime_ns,
            )
            row = self._feature_row(health_report, alert_report, maintenance_report)
            values = [{name: row[name] for name in features}]
            label = int(model.predict(values)[0])
            probability = float(model.predict_proba(values)[0][1])
            return PredictionResult(
                prediction_type="ml",
                confidence=probability if label else 1 - probability,
                predicted_failure="Failure Predicted"
                if label
                else "No Immediate Failure Predicted",
                recommended_action="Immediate Service"
                if label
                else "Continue Monitoring",
                estimated_remaining_km=row["estimated_remaining_km"],
                timestamp=utc_now(),
            )
        except Exception as exc:
            if not self._fallback_to_rule:
                raise RuntimeError(f"ML predictor unavailable: {exc}") from exc
            logger.debug("Using rule fallback: %s", exc)
            return (
                RuleBasedPredictor()
                .predict(health_report, alert_report, maintenance_report)
                .model_copy(update={"prediction_type": "rule-fallback"})
            )

    def supports_training(self) -> bool:
        """Training is provided by the offline CLI."""
        return True

    def model_name(self) -> str:
        """Return the predictor identifier."""
        return "ml-best-model"

    @staticmethod
    def _feature_row(
        health: HealthReport, alerts: AlertReport, maintenance: MaintenanceReport
    ) -> dict[str, Any]:
        estimates = [
            task.estimated_km_remaining
            for task in maintenance.tasks
            if task.estimated_km_remaining is not None
        ]
        return {
            "health_score": health.health_score,
            "health_status": health.health_status,
            "alert_count": alerts.alert_count,
            "highest_alert_severity": alerts.highest_severity.value
            if alerts.highest_severity
            else None,
            "maintenance_priority": maintenance.overall_priority.value,
            "maintenance_task_count": maintenance.task_count,
            "estimated_remaining_km": min(estimates) if estimates else None,
        }
