"""Tests for read-only vehicle insight aggregation."""

from app.prediction.predictor_factory import PredictorFactory
from app.services.vehicle_insight_service import VehicleInsightService


class _TelemetryService:
    """Minimal telemetry lookup replacement for a focused unit test."""

    def __init__(self, telemetry) -> None:
        self._telemetry = telemetry

    def get_latest(self, db, vehicle_id):
        """Return the configured telemetry sample."""
        return self._telemetry


def test_vehicle_insights_builds_all_reports(monkeypatch, telemetry_stub) -> None:
    """Latest telemetry should produce each frontend-facing report."""
    from app.services import vehicle_insight_service

    monkeypatch.setattr(
        vehicle_insight_service,
        "telemetry_service",
        _TelemetryService(telemetry_stub),
    )
    service = VehicleInsightService(PredictorFactory())

    reports = service.build(db=None, vehicle_id=1)

    assert reports.health.health_score >= 90
    assert reports.alerts.alert_count == 0
    assert reports.maintenance.task_count == 0
    assert reports.prediction.predicted_failure == "No Immediate Failure Predicted"
