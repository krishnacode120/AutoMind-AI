"""Simulation controller data models."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class SimulationSnapshot:
    """Complete simulation snapshot assembled from simulator engines."""

    timestamp: datetime
    vehicle_state: str
    driving_mode: str
    speed: float
    rpm: int
    gear: int
    distance_delta: float
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
