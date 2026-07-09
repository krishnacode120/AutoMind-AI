"""Tests for maintenance recommendation service."""

from dataclasses import replace

from app.schemas.alert import Alert, AlertReport, AlertSeverity, AlertType
from app.schemas.health import HealthReport
from app.services.maintenance_service import VehicleMaintenanceService
from app.utils.time_utils import utc_now


def test_maintenance_service_returns_low_priority_without_issues(
    telemetry_stub,
) -> None:
    """Healthy telemetry should produce low-priority maintenance."""
    report = VehicleMaintenanceService().generate_maintenance_plan(
        telemetry_stub,
        HealthReport(
            health_score=90,
            health_status="Good",
            penalties={},
            recommendations=[],
            timestamp=utc_now(),
        ),
        AlertReport(alert_count=0, highest_severity=None, alerts=[]),
    )
    assert report.overall_priority.value == "LOW"
    assert report.task_count == 0


def test_maintenance_service_creates_urgent_engine_task(telemetry_stub) -> None:
    """Critical engine alert should produce an urgent maintenance task."""
    report = VehicleMaintenanceService().generate_maintenance_plan(
        replace(telemetry_stub, oil_life=10.0),
        HealthReport(
            health_score=55,
            health_status="Poor",
            penalties={"oil_life": 10.0},
            recommendations=["Replace engine oil."],
            timestamp=utc_now(),
        ),
        AlertReport(
            alert_count=1,
            highest_severity=AlertSeverity.CRITICAL,
            alerts=[
                Alert(
                    severity=AlertSeverity.CRITICAL,
                    type=AlertType.HIGH_ENGINE_TEMP,
                    title="High engine temperature",
                    description="Critical threshold exceeded",
                    recommendation="Immediate inspection",
                    timestamp=utc_now(),
                )
            ],
        ),
    )
    assert report.task_count >= 1
    assert report.overall_priority.value in {"URGENT", "HIGH"}
