"""Failure label generation for ML datasets."""

from app.schemas.alert import AlertReport, AlertSeverity
from app.schemas.health import HealthReport
from app.schemas.maintenance import MaintenancePriority, MaintenanceReport
from app.schemas.prediction import PredictionResult


class FailureLabelGenerator:
    """Generate deterministic binary labels from existing rule outputs."""

    def generate(
        self,
        health_report: HealthReport,
        alert_report: AlertReport,
        maintenance_report: MaintenanceReport,
        prediction: PredictionResult,
    ) -> int:
        """Return 1 when existing rules indicate a failure condition."""
        if health_report.health_status == "Critical":
            return 1

        if alert_report.highest_severity == AlertSeverity.CRITICAL:
            return 1

        if maintenance_report.overall_priority in {
            MaintenancePriority.HIGH,
            MaintenancePriority.URGENT,
        }:
            return 1

        if prediction.estimated_remaining_km == 0.0:
            return 1

        return 0
