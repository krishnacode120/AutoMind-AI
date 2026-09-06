"""Bounded, user-requested simulation using the existing vehicle engines."""

from dataclasses import replace
from typing import Literal

from sqlalchemy.orm import Session

from app.core.exceptions import GlobalException
from app.models.vehicle import Vehicle
from app.models.telemetry import Telemetry
from app.simulator.enums import VehicleState
from app.simulator.physics_engine import PhysicsEngine
from app.simulator.sensor_engine import SensorEngine
from app.simulator.state_machine import VehicleStateMachine
from app.simulator.simulation_controller import SimulationController
from app.simulator.persistence_engine import PersistenceEngine


SimulationScenario = Literal["normal", "overheating", "low_fuel", "worn_brakes"]


def simulate_drive(
    db: Session,
    vehicle_id: int,
    samples: int = 60,
    scenario: SimulationScenario = "normal",
) -> list[Telemetry]:
    """Persist one finite sample drive; no background runner is started."""
    if not 1 <= samples <= 300:
        raise ValueError("Samples must be between 1 and 300")
    if scenario not in ("normal", "overheating", "low_fuel", "worn_brakes"):
        raise ValueError("Unknown simulation scenario")
    if db.get(Vehicle, vehicle_id) is None:
        raise GlobalException("Vehicle not found", 404)
    state = VehicleStateMachine()
    physics = PhysicsEngine(state)
    controller = SimulationController(state, physics, SensorEngine(physics))
    controller.start()
    controller.start()
    snapshots = []
    for index in range(samples):
        phase = index % 60
        current = state.current_state()
        if current == VehicleState.IDLE:
            controller.accelerate()
        elif current == VehicleState.ACCELERATING and phase >= 10:
            controller.cruise()
        elif current == VehicleState.CRUISING and phase >= 40:
            controller.brake()
        elif current == VehicleState.BRAKING and physics.current_speed == 0:
            controller.stop()
        elif current == VehicleState.STOPPED:
            controller.stop()
        snapshot = controller.step()
        progress = (index + 1) / samples
        # Each run is an independent synthetic scenario, recorded at generation time.
        # Retain the physics engine and cumulative vehicle odometer.
        if scenario == "overheating":
            snapshot = replace(
                snapshot,
                engine_temperature=95 + 40 * progress,
                coolant_level=35 - 20 * progress,
            )
        elif scenario == "low_fuel":
            snapshot = replace(snapshot, fuel_level=15 - 12 * progress)
        elif scenario == "worn_brakes":
            snapshot = replace(snapshot, brake_wear=75 + 20 * progress, oil_life=15)
        snapshots.append(snapshot)
    return PersistenceEngine(db).save_many(vehicle_id, snapshots)
