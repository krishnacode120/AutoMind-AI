"""Bounded, user-requested simulation using the existing vehicle engines."""

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


def simulate_drive(db: Session, vehicle_id: int, samples: int = 60) -> list[Telemetry]:
    """Persist one finite sample drive; no background runner is started."""
    if not 1 <= samples <= 300:
        raise ValueError("Samples must be between 1 and 300")
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
        snapshots.append(controller.step())
    return PersistenceEngine(db).save_many(vehicle_id, snapshots)
