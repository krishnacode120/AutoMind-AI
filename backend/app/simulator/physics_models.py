"""Physics engine data models."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PhysicsSnapshot:
    """Snapshot of calculated vehicle physics values."""

    speed: float
    rpm: int
    gear: int
    acceleration: float
    distance_delta: float
    engine_running: bool
