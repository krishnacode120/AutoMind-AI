"""Sensor engine data models."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SensorSnapshot:
    """Snapshot of calculated vehicle sensor readings."""

    engine_temperature: float
    battery_voltage: float
    fuel_level: float
    oil_life: float
    coolant_level: float
    tire_pressure_fl: float
    tire_pressure_fr: float
    tire_pressure_rl: float
    tire_pressure_rr: float
    brake_wear: float
    engine_load: float
    throttle_position: float
