"""Tests for alert generation service."""

from dataclasses import replace
from datetime import datetime, timezone

from app.schemas.health import HealthReport
from app.services.alert_service import VehicleAlertService


def test_alert_service_generates_no_alerts_for_healthy_inputs(
    telemetry_stub,
) -> None:
    """Healthy telemetry should produce empty alerts."""
    health_report = HealthReport(
        health_score=95,
        health_status="Excellent",
        penalties={},
        recommendations=[],
        timestamp=datetime.now(timezone.utc),
    )
    report = VehicleAlertService().generate_alerts(telemetry_stub, health_report)
    assert report.alert_count == 0
    assert report.highest_severity is None


def test_alert_service_generates_critical_alerts(telemetry_stub) -> None:
    """Critical telemetry should raise critical alerts."""
    risky = replace(telemetry_stub, engine_temperature=130.0, engine_load=99.0)
    health_report = HealthReport(
        health_score=20,
        health_status="Critical",
        penalties={"temperature": 20.0},
        recommendations=["Inspect now"],
        timestamp=datetime.now(timezone.utc),
    )
    report = VehicleAlertService().generate_alerts(risky, health_report)
    assert report.alert_count >= 2
    assert report.highest_severity is not None
    assert report.highest_severity.value == "CRITICAL"
