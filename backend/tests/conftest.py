"""Shared test fixtures for backend test suite."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

import pytest

from app.schemas.alert import AlertReport
from app.schemas.health import HealthReport
from app.schemas.maintenance import MaintenancePriority, MaintenanceReport


@dataclass
class TelemetryStub:
    """Minimal telemetry object matching service protocol fields."""

    engine_temperature: float = 92.0
    fuel_level: float = 55.0
    battery_voltage: float = 12.6
    oil_life: float = 80.0
    brake_wear: float = 30.0
    tire_pressure_fl: float = 33.0
    tire_pressure_fr: float = 33.0
    tire_pressure_rl: float = 33.0
    tire_pressure_rr: float = 33.0
    coolant_level: float = 75.0
    engine_load: float = 42.0


@pytest.fixture
def telemetry_stub() -> TelemetryStub:
    """Return a healthy baseline telemetry object."""
    return TelemetryStub()


@pytest.fixture
def health_report() -> HealthReport:
    """Return a baseline health report fixture."""
    return HealthReport(
        health_score=85,
        health_status="Good",
        penalties={},
        recommendations=[],
        timestamp=datetime.now(timezone.utc),
    )


@pytest.fixture
def alert_report() -> AlertReport:
    """Return an empty alert report fixture."""
    return AlertReport(
        alert_count=0,
        highest_severity=None,
        alerts=[],
    )


@pytest.fixture
def maintenance_report() -> MaintenanceReport:
    """Return a baseline maintenance report fixture."""
    return MaintenanceReport(
        overall_priority=MaintenancePriority.LOW,
        task_count=0,
        tasks=[],
        timestamp=datetime.now(timezone.utc),
    )
