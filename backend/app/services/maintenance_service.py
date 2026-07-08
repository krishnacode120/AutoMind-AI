"""Deterministic vehicle maintenance recommendation service."""

from typing import Protocol

from app.schemas.alert import AlertReport, AlertType
from app.schemas.health import HealthReport
from app.schemas.maintenance import (
    MaintenancePriority,
    MaintenanceReport,
    MaintenanceTask,
)
from app.utils.time_utils import utc_now


OIL_LIFE_THRESHOLD = 30.0
OIL_KM_MULTIPLIER = 100.0

BRAKE_WEAR_THRESHOLD = 70.0
BRAKE_KM_MULTIPLIER = 50.0

BATTERY_VOLTAGE_THRESHOLD = 12.2
BATTERY_DAYS_REMAINING = 30

LOW_TIRE_PRESSURE_THRESHOLD = 30.0
COOLANT_THRESHOLD = 40.0
LOW_FUEL_THRESHOLD = 15.0


class TelemetryLike(Protocol):
    """Telemetry attributes required for maintenance planning."""

    oil_life: float
    brake_wear: float
    battery_voltage: float
    tire_pressure_fl: float
    tire_pressure_fr: float
    tire_pressure_rl: float
    tire_pressure_rr: float
    coolant_level: float
    fuel_level: float


class VehicleMaintenanceService:
    """Generate deterministic maintenance recommendations."""

    def generate_maintenance_plan(
        self,
        telemetry: TelemetryLike,
        health_report: HealthReport,
        alert_report: AlertReport,
    ) -> MaintenanceReport:
        """Generate a maintenance report from telemetry, health, and alerts."""
        tasks = self._build_tasks(telemetry, alert_report)
        return MaintenanceReport(
            overall_priority=self._overall_priority(tasks),
            task_count=len(tasks),
            tasks=tasks,
            timestamp=health_report.timestamp or utc_now(),
        )

    def _build_tasks(
        self,
        telemetry: TelemetryLike,
        alert_report: AlertReport,
    ) -> list[MaintenanceTask]:
        """Build deterministic maintenance tasks."""
        tasks: list[MaintenanceTask] = []

        if telemetry.oil_life < OIL_LIFE_THRESHOLD:
            tasks.append(self._engine_oil_task(telemetry.oil_life))

        if telemetry.brake_wear > BRAKE_WEAR_THRESHOLD:
            tasks.append(self._brake_task(telemetry.brake_wear))

        if telemetry.battery_voltage < BATTERY_VOLTAGE_THRESHOLD:
            tasks.append(self._battery_task())

        if self._has_low_tire_pressure(telemetry):
            tasks.append(self._tire_task())

        if telemetry.coolant_level < COOLANT_THRESHOLD:
            tasks.append(self._coolant_task())

        if self._has_alert(alert_report, AlertType.HIGH_ENGINE_TEMP):
            tasks.append(self._engine_temperature_task())

        if telemetry.fuel_level < LOW_FUEL_THRESHOLD:
            tasks.append(self._fuel_task())

        return tasks

    def _engine_oil_task(self, oil_life: float) -> MaintenanceTask:
        """Return an engine oil maintenance task."""
        return MaintenanceTask(
            id="engine-oil",
            title="Replace engine oil",
            description="Oil life is below the recommended threshold.",
            priority=MaintenancePriority.HIGH,
            estimated_km_remaining=max(0.0, oil_life * OIL_KM_MULTIPLIER),
            estimated_days_remaining=None,
            recommended_action="Replace engine oil.",
            component="Engine Oil",
        )

    def _brake_task(self, brake_wear: float) -> MaintenanceTask:
        """Return a brake maintenance task."""
        return MaintenanceTask(
            id="brakes",
            title="Inspect braking system",
            description="Brake wear is above the recommended threshold.",
            priority=MaintenancePriority.HIGH,
            estimated_km_remaining=max(
                0.0,
                (100.0 - brake_wear) * BRAKE_KM_MULTIPLIER,
            ),
            estimated_days_remaining=None,
            recommended_action="Inspect brake pads.",
            component="Brakes",
        )

    def _battery_task(self) -> MaintenanceTask:
        """Return a battery maintenance task."""
        return MaintenanceTask(
            id="battery",
            title="Inspect battery",
            description="Battery voltage is below the recommended threshold.",
            priority=MaintenancePriority.MEDIUM,
            estimated_km_remaining=None,
            estimated_days_remaining=BATTERY_DAYS_REMAINING,
            recommended_action="Check battery.",
            component="Battery",
        )

    def _tire_task(self) -> MaintenanceTask:
        """Return a tire maintenance task."""
        return MaintenanceTask(
            id="tires",
            title="Check tire pressure",
            description="One or more tires are below the safe pressure threshold.",
            priority=MaintenancePriority.MEDIUM,
            estimated_km_remaining=None,
            estimated_days_remaining=None,
            recommended_action="Inflate and inspect tires.",
            component="Tires",
        )

    def _coolant_task(self) -> MaintenanceTask:
        """Return a coolant maintenance task."""
        return MaintenanceTask(
            id="coolant",
            title="Inspect cooling system",
            description="Coolant level is below the recommended threshold.",
            priority=MaintenancePriority.MEDIUM,
            estimated_km_remaining=None,
            estimated_days_remaining=None,
            recommended_action="Inspect cooling system.",
            component="Coolant",
        )

    def _engine_temperature_task(self) -> MaintenanceTask:
        """Return an urgent engine temperature maintenance task."""
        return MaintenanceTask(
            id="engine-temperature",
            title="Immediate engine temperature inspection",
            description="High engine temperature alert is active.",
            priority=MaintenancePriority.URGENT,
            estimated_km_remaining=0.0,
            estimated_days_remaining=0,
            recommended_action="Immediate inspection.",
            component="Engine",
        )

    def _fuel_task(self) -> MaintenanceTask:
        """Return a refueling maintenance task."""
        return MaintenanceTask(
            id="fuel",
            title="Refuel vehicle",
            description="Fuel level is below the recommended threshold.",
            priority=MaintenancePriority.LOW,
            estimated_km_remaining=None,
            estimated_days_remaining=None,
            recommended_action="Refuel vehicle.",
            component="Fuel",
        )

    def _has_low_tire_pressure(self, telemetry: TelemetryLike) -> bool:
        """Return whether any tire pressure is below threshold."""
        tire_pressures = (
            telemetry.tire_pressure_fl,
            telemetry.tire_pressure_fr,
            telemetry.tire_pressure_rl,
            telemetry.tire_pressure_rr,
        )
        return any(pressure < LOW_TIRE_PRESSURE_THRESHOLD for pressure in tire_pressures)

    def _has_alert(
        self,
        alert_report: AlertReport,
        alert_type: AlertType,
    ) -> bool:
        """Return whether an alert report contains an alert type."""
        return any(alert.type == alert_type for alert in alert_report.alerts)

    def _overall_priority(
        self,
        tasks: list[MaintenanceTask],
    ) -> MaintenancePriority:
        """Return the highest maintenance priority across all tasks."""
        priorities = [task.priority for task in tasks]

        if MaintenancePriority.URGENT in priorities:
            return MaintenancePriority.URGENT
        if MaintenancePriority.HIGH in priorities:
            return MaintenancePriority.HIGH
        if MaintenancePriority.MEDIUM in priorities:
            return MaintenancePriority.MEDIUM

        return MaintenancePriority.LOW
