"""Vehicle physics engine."""

from app.simulator.enums import VehicleState
from app.simulator.physics_models import PhysicsSnapshot
from app.simulator.state_machine import VehicleStateMachine


MIN_SPEED = 0.0
MAX_ACCELERATION_DELTA = 8.0
MAX_BRAKING_DELTA = -10.0
SECONDS_PER_HOUR = 3600.0

ENGINE_OFF_RPM = 0
STARTING_RPM = 600
IDLE_RPM = 750
RPM_VARIATION = 40
MAX_RPM_STEP = 450

NEUTRAL_GEAR = 0
MAX_SPEED = 180.0

GEAR_SPEED_LIMITS: tuple[tuple[float, int], ...] = (
    (20.0, 1),
    (40.0, 2),
    (60.0, 3),
    (90.0, 4),
    (120.0, 5),
)

GEAR_SPEED_RANGES: dict[int, tuple[float, float]] = {
    1: (0.0, 20.0),
    2: (20.0, 40.0),
    3: (40.0, 60.0),
    4: (60.0, 90.0),
    5: (90.0, 120.0),
    6: (120.0, MAX_SPEED),
}

GEAR_RPM_RANGES: dict[int, tuple[int, int]] = {
    1: (1000, 3000),
    2: (1500, 3200),
    3: (1700, 3400),
    4: (1800, 3500),
    5: (1800, 3200),
    6: (1700, 2800),
}


class PhysicsEngine:
    """Calculate vehicle movement from state machine state."""

    def __init__(self, state_machine: VehicleStateMachine) -> None:
        """Initialize the physics engine."""
        self._state_machine = state_machine
        self.current_speed = MIN_SPEED
        self.current_rpm = ENGINE_OFF_RPM
        self.current_gear = NEUTRAL_GEAR
        self.total_distance = 0.0
        self._update_count = 0

    def update(self) -> PhysicsSnapshot:
        """Update physics values and return a snapshot."""
        self._update_count += 1
        state = self._state_machine.current_state()
        previous_speed = self.current_speed

        if state == VehicleState.OFF:
            self._set_stationary_state(ENGINE_OFF_RPM)
        elif state == VehicleState.STARTING:
            self._set_stationary_state(STARTING_RPM)
        elif state == VehicleState.IDLE:
            self._set_stationary_state(IDLE_RPM)
        elif state == VehicleState.STOPPED:
            self._set_stationary_state(IDLE_RPM)
        elif state == VehicleState.ACCELERATING:
            self._accelerate()
        elif state == VehicleState.CRUISING:
            self._cruise()
        elif state == VehicleState.BRAKING:
            self._brake()

        acceleration = self.current_speed - previous_speed
        distance_delta = self.current_speed / SECONDS_PER_HOUR
        self.total_distance += distance_delta

        return PhysicsSnapshot(
            speed=round(self.current_speed, 2),
            rpm=self.current_rpm,
            gear=self.current_gear,
            acceleration=round(acceleration, 2),
            distance_delta=round(distance_delta, 6),
            engine_running=state != VehicleState.OFF,
        )

    def _set_stationary_state(self, rpm: int) -> None:
        """Set speed and gear for non-moving states."""
        self.current_speed = MIN_SPEED
        self.current_rpm = rpm
        self.current_gear = NEUTRAL_GEAR

    def _accelerate(self) -> None:
        """Increase speed, gear, and RPM gradually."""
        self.current_speed = min(
            self.current_speed + MAX_ACCELERATION_DELTA,
            MAX_SPEED,
        )
        self.current_gear = self._gear_for_speed(self.current_speed)
        target_rpm = self._target_rpm_for_speed(self.current_speed)
        self.current_rpm = self._approach_rpm(target_rpm)

    def _cruise(self) -> None:
        """Keep speed stable with small deterministic RPM variation."""
        self.current_gear = self._gear_for_speed(self.current_speed)
        target_rpm = self._target_rpm_for_speed(self.current_speed)
        target_rpm += self._rpm_variation()
        self.current_rpm = self._approach_rpm(target_rpm)

    def _brake(self) -> None:
        """Reduce speed, gear, and RPM gradually."""
        self.current_speed = max(
            self.current_speed + MAX_BRAKING_DELTA,
            MIN_SPEED,
        )
        self.current_gear = self._gear_for_speed(self.current_speed)
        if self.current_speed == MIN_SPEED:
            self.current_rpm = IDLE_RPM
            self.current_gear = NEUTRAL_GEAR
            return

        target_rpm = self._target_rpm_for_speed(self.current_speed)
        self.current_rpm = self._approach_rpm(target_rpm)

    def _gear_for_speed(self, speed: float) -> int:
        """Return automatic gear for the current speed."""
        if speed <= MIN_SPEED:
            return NEUTRAL_GEAR

        for speed_limit, gear in GEAR_SPEED_LIMITS:
            if speed <= speed_limit:
                return gear

        return 6

    def _target_rpm_for_speed(self, speed: float) -> int:
        """Calculate target RPM from speed and active gear."""
        gear = self._gear_for_speed(speed)
        if gear == NEUTRAL_GEAR:
            return IDLE_RPM

        min_speed, max_speed = GEAR_SPEED_RANGES[gear]
        min_rpm, max_rpm = GEAR_RPM_RANGES[gear]
        speed_span = max_speed - min_speed
        rpm_span = max_rpm - min_rpm
        speed_ratio = (speed - min_speed) / speed_span
        bounded_ratio = max(0.0, min(speed_ratio, 1.0))

        return round(min_rpm + (rpm_span * bounded_ratio))

    def _approach_rpm(self, target_rpm: int) -> int:
        """Move current RPM toward target RPM without sudden jumps."""
        rpm_delta = target_rpm - self.current_rpm
        bounded_delta = max(-MAX_RPM_STEP, min(rpm_delta, MAX_RPM_STEP))
        return round(self.current_rpm + bounded_delta)

    def _rpm_variation(self) -> int:
        """Return a small deterministic RPM variation for cruising."""
        return RPM_VARIATION if self._update_count % 2 == 0 else -RPM_VARIATION
