"""Deterministic vehicle health calculation service."""

from typing import Protocol

from app.schemas.health import HealthReport
from app.utils.time_utils import utc_now


BASE_HEALTH_SCORE = 100.0
MIN_HEALTH_SCORE = 0.0
MAX_HEALTH_SCORE = 100.0

TEMPERATURE_THRESHOLD = 100.0
TEMPERATURE_MAX = 140.0
TEMPERATURE_MAX_PENALTY = 20.0

FUEL_THRESHOLD = 20.0
FUEL_MAX_PENALTY = 10.0

BATTERY_THRESHOLD = 12.2
BATTERY_MIN = 10.0
BATTERY_MAX_PENALTY = 15.0

OIL_THRESHOLD = 30.0
OIL_MAX_PENALTY = 20.0

BRAKE_WEAR_THRESHOLD = 70.0
BRAKE_WEAR_MAX = 100.0
BRAKE_WEAR_MAX_PENALTY = 15.0

TIRE_PRESSURE_MIN = 32.0
TIRE_PRESSURE_MAX = 35.0
TIRE_PRESSURE_TOLERANCE = 8.0
TIRE_PRESSURE_MAX_PENALTY = 10.0

COOLANT_THRESHOLD = 40.0
COOLANT_MAX_PENALTY = 10.0


class TelemetryLike(Protocol):
    """Telemetry attributes required for health calculation."""

    engine_temperature: float
    fuel_level: float
    battery_voltage: float
    oil_life: float
    brake_wear: float
    tire_pressure_fl: float
    tire_pressure_fr: float
    tire_pressure_rl: float
    tire_pressure_rr: float
    coolant_level: float


class VehicleHealthService:
    """Calculate deterministic health reports from telemetry."""

    def calculate_health(self, telemetry: TelemetryLike) -> HealthReport:
        """Calculate a health report from telemetry values."""
        penalties = self._calculate_penalties(telemetry)
        health_score = self._score_from_penalties(penalties)

        return HealthReport(
            health_score=health_score,
            health_status=self._health_status(health_score),
            penalties=penalties,
            recommendations=self._recommendations(penalties),
            timestamp=utc_now(),
        )

    def _calculate_penalties(
        self,
        telemetry: TelemetryLike,
    ) -> dict[str, float]:
        """Calculate all health penalties."""
        return {
            "temperature": self._high_penalty(
                value=telemetry.engine_temperature,
                threshold=TEMPERATURE_THRESHOLD,
                maximum=TEMPERATURE_MAX,
                max_penalty=TEMPERATURE_MAX_PENALTY,
            ),
            "fuel": self._low_penalty(
                value=telemetry.fuel_level,
                threshold=FUEL_THRESHOLD,
                minimum=0.0,
                max_penalty=FUEL_MAX_PENALTY,
            ),
            "battery": self._low_penalty(
                value=telemetry.battery_voltage,
                threshold=BATTERY_THRESHOLD,
                minimum=BATTERY_MIN,
                max_penalty=BATTERY_MAX_PENALTY,
            ),
            "oil_life": self._low_penalty(
                value=telemetry.oil_life,
                threshold=OIL_THRESHOLD,
                minimum=0.0,
                max_penalty=OIL_MAX_PENALTY,
            ),
            "brake_wear": self._high_penalty(
                value=telemetry.brake_wear,
                threshold=BRAKE_WEAR_THRESHOLD,
                maximum=BRAKE_WEAR_MAX,
                max_penalty=BRAKE_WEAR_MAX_PENALTY,
            ),
            "tire_pressure": self._tire_pressure_penalty(telemetry),
            "coolant": self._low_penalty(
                value=telemetry.coolant_level,
                threshold=COOLANT_THRESHOLD,
                minimum=0.0,
                max_penalty=COOLANT_MAX_PENALTY,
            ),
        }

    def _score_from_penalties(self, penalties: dict[str, float]) -> int:
        """Return a bounded health score from penalties."""
        score = BASE_HEALTH_SCORE - sum(penalties.values())
        bounded_score = self._clamp(score, MIN_HEALTH_SCORE, MAX_HEALTH_SCORE)
        return round(bounded_score)

    def _health_status(self, health_score: int) -> str:
        """Return health category for a score."""
        if health_score >= 90:
            return "Excellent"
        if health_score >= 75:
            return "Good"
        if health_score >= 60:
            return "Fair"
        if health_score >= 40:
            return "Poor"

        return "Critical"

    def _recommendations(self, penalties: dict[str, float]) -> list[str]:
        """Return simple recommendations for applied penalties."""
        recommendations: list[str] = []

        if penalties["fuel"] > 0:
            recommendations.append("Refuel vehicle.")
        if penalties["oil_life"] > 0:
            recommendations.append("Replace engine oil.")
        if penalties["battery"] > 0:
            recommendations.append("Inspect battery.")
        if penalties["tire_pressure"] > 0:
            recommendations.append("Check tire pressure.")
        if penalties["brake_wear"] > 0:
            recommendations.append("Inspect braking system.")
        if penalties["temperature"] > 0:
            recommendations.append("Inspect engine cooling system.")
        if penalties["coolant"] > 0:
            recommendations.append("Check coolant level.")

        return recommendations

    def _high_penalty(
        self,
        value: float,
        threshold: float,
        maximum: float,
        max_penalty: float,
    ) -> float:
        """Calculate penalty when value exceeds a threshold."""
        if value <= threshold:
            return 0.0

        ratio = (value - threshold) / (maximum - threshold)
        return round(self._clamp(ratio, 0.0, 1.0) * max_penalty, 2)

    def _low_penalty(
        self,
        value: float,
        threshold: float,
        minimum: float,
        max_penalty: float,
    ) -> float:
        """Calculate penalty when value falls below a threshold."""
        if value >= threshold:
            return 0.0

        ratio = (threshold - value) / (threshold - minimum)
        return round(self._clamp(ratio, 0.0, 1.0) * max_penalty, 2)

    def _tire_pressure_penalty(self, telemetry: TelemetryLike) -> float:
        """Calculate tire pressure penalty across all tires."""
        tire_pressures = (
            telemetry.tire_pressure_fl,
            telemetry.tire_pressure_fr,
            telemetry.tire_pressure_rl,
            telemetry.tire_pressure_rr,
        )
        largest_deviation = max(
            self._tire_pressure_deviation(pressure)
            for pressure in tire_pressures
        )
        ratio = largest_deviation / TIRE_PRESSURE_TOLERANCE
        return round(
            self._clamp(ratio, 0.0, 1.0) * TIRE_PRESSURE_MAX_PENALTY,
            2,
        )

    def _tire_pressure_deviation(self, pressure: float) -> float:
        """Return distance outside the normal tire pressure range."""
        if pressure < TIRE_PRESSURE_MIN:
            return TIRE_PRESSURE_MIN - pressure
        if pressure > TIRE_PRESSURE_MAX:
            return pressure - TIRE_PRESSURE_MAX

        return 0.0

    def _clamp(self, value: float, minimum: float, maximum: float) -> float:
        """Clamp a value to an inclusive range."""
        return max(minimum, min(value, maximum))
