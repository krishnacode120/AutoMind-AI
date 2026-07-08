"""Simulation controller for coordinating simulator engines."""

from app.simulator.enums import DrivingMode, VehicleState
from app.simulator.physics_engine import PhysicsEngine
from app.simulator.sensor_engine import SensorEngine
from app.simulator.simulation_models import SimulationSnapshot
from app.simulator.state_machine import VehicleStateMachine
from app.utils.time_utils import utc_now


class SimulationController:
    """Coordinate state, physics, and sensor engines."""

    def __init__(
        self,
        state_machine: VehicleStateMachine,
        physics_engine: PhysicsEngine,
        sensor_engine: SensorEngine,
    ) -> None:
        """Initialize the simulation controller."""
        self._state_machine = state_machine
        self._physics_engine = physics_engine
        self._sensor_engine = sensor_engine

    def step(self) -> SimulationSnapshot:
        """Advance the simulation one step and return a combined snapshot."""
        physics_snapshot = self._physics_engine.update()
        sensor_snapshot = self._sensor_engine.update(physics_snapshot)

        return SimulationSnapshot(
            timestamp=utc_now(),
            vehicle_state=self._state_machine.current_state().value,
            driving_mode=self._state_machine.current_mode().value,
            speed=physics_snapshot.speed,
            rpm=physics_snapshot.rpm,
            gear=physics_snapshot.gear,
            distance_delta=physics_snapshot.distance_delta,
            engine_temperature=sensor_snapshot.engine_temperature,
            battery_voltage=sensor_snapshot.battery_voltage,
            fuel_level=sensor_snapshot.fuel_level,
            oil_life=sensor_snapshot.oil_life,
            coolant_level=sensor_snapshot.coolant_level,
            tire_pressure_fl=sensor_snapshot.tire_pressure_fl,
            tire_pressure_fr=sensor_snapshot.tire_pressure_fr,
            tire_pressure_rl=sensor_snapshot.tire_pressure_rl,
            tire_pressure_rr=sensor_snapshot.tire_pressure_rr,
            brake_wear=sensor_snapshot.brake_wear,
            engine_load=sensor_snapshot.engine_load,
            throttle_position=sensor_snapshot.throttle_position,
        )

    def start(self) -> VehicleState:
        """Delegate engine startup to the state machine."""
        return self._state_machine.start_engine()

    def stop(self) -> VehicleState:
        """Delegate stopping to the state machine."""
        return self._state_machine.stop()

    def accelerate(self) -> VehicleState:
        """Delegate acceleration to the state machine."""
        return self._state_machine.accelerate()

    def cruise(self) -> VehicleState:
        """Delegate cruising to the state machine."""
        return self._state_machine.cruise()

    def brake(self) -> VehicleState:
        """Delegate braking to the state machine."""
        return self._state_machine.brake()

    def set_mode(self, driving_mode: DrivingMode) -> None:
        """Delegate driving mode changes to the state machine."""
        self._state_machine.set_mode(driving_mode)
