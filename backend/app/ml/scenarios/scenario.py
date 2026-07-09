"""Scenario models for ML dataset generation."""

from dataclasses import dataclass
from enum import Enum

from app.ml.scenarios.driving_profiles import DrivingProfile


class FaultType(str, Enum):
    """Supported controlled dataset fault types."""

    LOW_FUEL = "low_fuel"
    LOW_BATTERY = "low_battery"
    HIGH_ENGINE_TEMPERATURE = "high_engine_temperature"
    HIGH_BRAKE_WEAR = "high_brake_wear"
    LOW_COOLANT = "low_coolant"
    HIGH_ENGINE_LOAD = "high_engine_load"
    LOW_TIRE_PRESSURE = "low_tire_pressure"


@dataclass(frozen=True)
class Scenario:
    """Single generated data scenario."""

    profile: DrivingProfile
    faults: tuple[FaultType, ...] = ()

    @property
    def has_fault(self) -> bool:
        """Return whether the scenario includes injected faults."""
        return bool(self.faults)
