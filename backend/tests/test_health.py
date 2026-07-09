"""Tests for health calculation service."""

from dataclasses import replace

from app.services.health_service import VehicleHealthService


def test_health_service_returns_excellent_for_healthy_telemetry(
    telemetry_stub,
) -> None:
    """Healthy telemetry should produce a high health score."""
    report = VehicleHealthService().calculate_health(telemetry_stub)
    assert report.health_score >= 90
    assert report.health_status in {"Excellent", "Good"}


def test_health_service_penalizes_critical_values(telemetry_stub) -> None:
    """Critical telemetry should reduce health and add recommendations."""
    degraded = replace(
        telemetry_stub,
        engine_temperature=140.0,
        fuel_level=5.0,
        battery_voltage=10.1,
        oil_life=5.0,
        brake_wear=95.0,
        coolant_level=5.0,
        tire_pressure_fl=20.0,
    )
    report = VehicleHealthService().calculate_health(degraded)
    assert report.health_score < 50
    assert report.health_status in {"Poor", "Critical"}
    assert len(report.recommendations) > 0
