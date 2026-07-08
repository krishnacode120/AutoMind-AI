"""Rule-based vehicle predictor."""

from app.prediction.base_predictor import VehiclePredictor
from app.schemas.alert import AlertReport, AlertSeverity, AlertType
from app.schemas.health import HealthReport
from app.schemas.maintenance import MaintenancePriority, MaintenanceReport
from app.schemas.prediction import PredictionResult
from app.utils.time_utils import utc_now


class RuleBasedPredictor(VehiclePredictor):
    """Deterministic predictor based on reports and alerts."""

    def predict(
        self,
        health_report: HealthReport,
        alert_report: AlertReport,
        maintenance_report: MaintenanceReport,
    ) -> PredictionResult:
        """Generate a deterministic prediction."""
        if health_report.health_score < 40:
            return self._result(
                predicted_failure="High",
                confidence=0.92,
                recommended_action="Immediate Service",
                estimated_remaining_km=0.0,
            )

        if self._has_critical_engine_alert(alert_report):
            return self._result(
                predicted_failure="Engine System Risk",
                confidence=0.88,
                recommended_action="Immediate Engine Inspection",
                estimated_remaining_km=0.0,
            )

        if maintenance_report.overall_priority == MaintenancePriority.URGENT:
            return self._result(
                predicted_failure="Urgent Maintenance Required",
                confidence=0.86,
                recommended_action="Immediate Service",
                estimated_remaining_km=0.0,
            )

        if maintenance_report.overall_priority == MaintenancePriority.HIGH:
            return self._result(
                predicted_failure="Maintenance Needed Soon",
                confidence=0.74,
                recommended_action="Schedule Service",
                estimated_remaining_km=self._minimum_remaining_km(
                    maintenance_report,
                ),
            )

        if alert_report.highest_severity == AlertSeverity.WARNING:
            return self._result(
                predicted_failure="Minor Service Risk",
                confidence=0.62,
                recommended_action="Inspect Warning Conditions",
                estimated_remaining_km=self._minimum_remaining_km(
                    maintenance_report,
                ),
            )

        return self._result(
            predicted_failure="No Immediate Failure Predicted",
            confidence=0.55,
            recommended_action="Continue Monitoring",
            estimated_remaining_km=self._minimum_remaining_km(
                maintenance_report,
            ),
        )

    def supports_training(self) -> bool:
        """Return whether this predictor supports training."""
        return False

    def model_name(self) -> str:
        """Return the predictor model name."""
        return "rule-based-v1"

    def _result(
        self,
        predicted_failure: str,
        confidence: float,
        recommended_action: str,
        estimated_remaining_km: float | None,
    ) -> PredictionResult:
        """Create a prediction result."""
        return PredictionResult(
            prediction_type="rule",
            confidence=confidence,
            predicted_failure=predicted_failure,
            recommended_action=recommended_action,
            estimated_remaining_km=estimated_remaining_km,
            timestamp=utc_now(),
        )

    def _has_critical_engine_alert(self, alert_report: AlertReport) -> bool:
        """Return whether critical engine risk alerts are present."""
        critical_engine_alerts = {
            AlertType.HIGH_ENGINE_TEMP,
            AlertType.ENGINE_OVERLOAD,
        }
        return any(
            alert.type in critical_engine_alerts
            and alert.severity == AlertSeverity.CRITICAL
            for alert in alert_report.alerts
        )

    def _minimum_remaining_km(
        self,
        maintenance_report: MaintenanceReport,
    ) -> float | None:
        """Return the lowest available remaining-km estimate."""
        estimates = [
            task.estimated_km_remaining
            for task in maintenance_report.tasks
            if task.estimated_km_remaining is not None
        ]

        if not estimates:
            return None

        return min(estimates)
