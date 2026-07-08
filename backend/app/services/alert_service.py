"""Deterministic vehicle alert generation service."""

from typing import Protocol

from app.rules import alert_rules
from app.schemas.alert import Alert, AlertReport, AlertSeverity, AlertType
from app.schemas.health import HealthReport
from app.utils.time_utils import utc_now


class TelemetryLike(Protocol):
    """Telemetry attributes required for alert generation."""

    engine_temperature: float
    fuel_level: float
    battery_voltage: float
    oil_life: float
    coolant_level: float
    brake_wear: float
    tire_pressure_fl: float
    tire_pressure_fr: float
    tire_pressure_rl: float
    tire_pressure_rr: float
    engine_load: float


class VehicleAlertService:
    """Generate deterministic alerts from telemetry and health reports."""

    def generate_alerts(
        self,
        telemetry: TelemetryLike,
        health_report: HealthReport,
    ) -> AlertReport:
        """Generate an alert report."""
        alerts = self._build_alerts(telemetry, health_report)
        return AlertReport(
            alert_count=len(alerts),
            highest_severity=self._highest_severity(alerts),
            alerts=alerts,
        )

    def _build_alerts(
        self,
        telemetry: TelemetryLike,
        health_report: HealthReport,
    ) -> list[Alert]:
        """Build all alerts for the given telemetry and health report."""
        alerts: list[Alert] = []

        if telemetry.engine_temperature > alert_rules.HIGH_ENGINE_TEMP_THRESHOLD:
            alerts.append(
                self._alert(
                    severity=AlertSeverity.CRITICAL,
                    alert_type=AlertType.HIGH_ENGINE_TEMP,
                    title="High engine temperature",
                    description="Engine temperature is above the critical threshold.",
                    recommendation="Inspect cooling system.",
                )
            )

        if telemetry.fuel_level < alert_rules.LOW_FUEL_THRESHOLD:
            alerts.append(
                self._alert(
                    severity=AlertSeverity.WARNING,
                    alert_type=AlertType.LOW_FUEL,
                    title="Low fuel level",
                    description="Fuel level is below the warning threshold.",
                    recommendation="Refuel vehicle.",
                )
            )

        if telemetry.battery_voltage < alert_rules.LOW_BATTERY_THRESHOLD:
            alerts.append(
                self._alert(
                    severity=AlertSeverity.WARNING,
                    alert_type=AlertType.LOW_BATTERY,
                    title="Low battery voltage",
                    description="Battery voltage is below the warning threshold.",
                    recommendation="Check battery.",
                )
            )

        if telemetry.oil_life < alert_rules.LOW_OIL_LIFE_THRESHOLD:
            alerts.append(
                self._alert(
                    severity=AlertSeverity.WARNING,
                    alert_type=AlertType.LOW_OIL_LIFE,
                    title="Low oil life",
                    description="Oil life is below the warning threshold.",
                    recommendation="Replace engine oil.",
                )
            )

        if telemetry.coolant_level < alert_rules.LOW_COOLANT_THRESHOLD:
            alerts.append(
                self._alert(
                    severity=AlertSeverity.WARNING,
                    alert_type=AlertType.LOW_COOLANT,
                    title="Low coolant level",
                    description="Coolant level is below the warning threshold.",
                    recommendation="Inspect cooling system.",
                )
            )

        if telemetry.brake_wear > alert_rules.HIGH_BRAKE_WEAR_THRESHOLD:
            alerts.append(
                self._alert(
                    severity=AlertSeverity.WARNING,
                    alert_type=AlertType.HIGH_BRAKE_WEAR,
                    title="High brake wear",
                    description="Brake wear is above the warning threshold.",
                    recommendation="Inspect brake pads.",
                )
            )

        if self._has_low_tire_pressure(telemetry):
            alerts.append(
                self._alert(
                    severity=AlertSeverity.WARNING,
                    alert_type=AlertType.LOW_TIRE_PRESSURE,
                    title="Low tire pressure",
                    description="One or more tires are below the safe pressure threshold.",
                    recommendation="Check tire pressure.",
                )
            )

        if telemetry.engine_load > alert_rules.ENGINE_OVERLOAD_THRESHOLD:
            alerts.append(
                self._alert(
                    severity=AlertSeverity.CRITICAL,
                    alert_type=AlertType.ENGINE_OVERLOAD,
                    title="Engine overload",
                    description="Engine load is above the critical threshold.",
                    recommendation="Reduce engine load immediately.",
                )
            )

        if health_report.health_score < alert_rules.CRITICAL_HEALTH_SCORE_THRESHOLD:
            alerts.append(
                self._alert(
                    severity=AlertSeverity.CRITICAL,
                    alert_type=AlertType.VEHICLE_HEALTH_CRITICAL,
                    title="Critical vehicle health",
                    description="Overall vehicle health score is critical.",
                    recommendation="Inspect vehicle immediately.",
                )
            )

        return alerts

    def _alert(
        self,
        severity: AlertSeverity,
        alert_type: AlertType,
        title: str,
        description: str,
        recommendation: str,
    ) -> Alert:
        """Create an alert with a current timestamp."""
        return Alert(
            severity=severity,
            type=alert_type,
            title=title,
            description=description,
            recommendation=recommendation,
            timestamp=utc_now(),
        )

    def _has_low_tire_pressure(self, telemetry: TelemetryLike) -> bool:
        """Return whether any tire pressure is below threshold."""
        tire_pressures = (
            telemetry.tire_pressure_fl,
            telemetry.tire_pressure_fr,
            telemetry.tire_pressure_rl,
            telemetry.tire_pressure_rr,
        )
        return any(
            pressure < alert_rules.LOW_TIRE_PRESSURE_THRESHOLD
            for pressure in tire_pressures
        )

    def _highest_severity(
        self,
        alerts: list[Alert],
    ) -> AlertSeverity | None:
        """Return the highest severity present in alerts."""
        if not alerts:
            return None

        if any(alert.severity == AlertSeverity.CRITICAL for alert in alerts):
            return AlertSeverity.CRITICAL

        if any(alert.severity == AlertSeverity.WARNING for alert in alerts):
            return AlertSeverity.WARNING

        return AlertSeverity.INFO
