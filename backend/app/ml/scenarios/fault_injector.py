"""Controlled fault injection for ML dataset telemetry samples."""

from random import Random

from app.ml.scenarios.scenario import FaultType, Scenario
from app.models.telemetry import Telemetry


class FaultInjector:
    """Apply realistic controlled faults to telemetry samples."""

    def __init__(self, random_seed: int | None = 0) -> None:
        """Initialize the fault injector."""
        self._random = Random(random_seed)

    def inject(self, telemetry: Telemetry, scenario: Scenario) -> Telemetry:
        """Apply scenario faults to telemetry and return it."""
        for fault in scenario.faults:
            self._apply_fault(telemetry, fault)

        return telemetry

    def _apply_fault(self, telemetry: Telemetry, fault: FaultType) -> None:
        """Apply one configured fault type."""
        if fault == FaultType.LOW_FUEL:
            telemetry.fuel_level = self._between(3.0, 14.5)
        elif fault == FaultType.LOW_BATTERY:
            telemetry.battery_voltage = self._between(10.8, 12.0)
        elif fault == FaultType.HIGH_ENGINE_TEMPERATURE:
            telemetry.engine_temperature = self._between(106.0, 125.0)
        elif fault == FaultType.HIGH_BRAKE_WEAR:
            telemetry.brake_wear = self._between(85.0, 100.0)
        elif fault == FaultType.LOW_COOLANT:
            telemetry.coolant_level = self._between(15.0, 29.5)
        elif fault == FaultType.HIGH_ENGINE_LOAD:
            telemetry.engine_load = self._between(96.0, 100.0)
            telemetry.throttle_position = max(
                telemetry.throttle_position,
                self._between(80.0, 95.0),
            )
        elif fault == FaultType.LOW_TIRE_PRESSURE:
            self._inject_low_tire_pressure(telemetry)

    def _inject_low_tire_pressure(self, telemetry: Telemetry) -> None:
        """Set one or more tire pressures to a realistic low range."""
        tire_fields = (
            "tire_pressure_fl",
            "tire_pressure_fr",
            "tire_pressure_rl",
            "tire_pressure_rr",
        )
        affected_count = self._random.randint(1, len(tire_fields))
        affected_fields = self._random.sample(tire_fields, affected_count)

        for field in affected_fields:
            setattr(telemetry, field, self._between(24.0, 29.5))

    def _between(self, minimum: float, maximum: float) -> float:
        """Return a rounded random value within a realistic range."""
        return round(self._random.uniform(minimum, maximum), 2)
