"""Vehicle state machine."""

from app.simulator.enums import DrivingMode, VehicleState


class VehicleStateMachine:
    """Manage valid vehicle state transitions."""

    _TRANSITIONS: dict[VehicleState, set[VehicleState]] = {
        VehicleState.OFF: {VehicleState.STARTING},
        VehicleState.STARTING: {VehicleState.IDLE},
        VehicleState.IDLE: {
            VehicleState.ACCELERATING,
            VehicleState.OFF,
        },
        VehicleState.ACCELERATING: {VehicleState.CRUISING},
        VehicleState.CRUISING: {VehicleState.BRAKING},
        VehicleState.BRAKING: {VehicleState.STOPPED},
        VehicleState.STOPPED: {VehicleState.IDLE},
    }

    def __init__(
        self,
        initial_state: VehicleState = VehicleState.OFF,
        driving_mode: DrivingMode = DrivingMode.CITY,
    ) -> None:
        """Initialize the state machine."""
        self._current_state = initial_state
        self._driving_mode = driving_mode

    def current_state(self) -> VehicleState:
        """Return the current vehicle state."""
        return self._current_state

    def current_mode(self) -> DrivingMode:
        """Return the current driving mode."""
        return self._driving_mode

    def set_mode(self, driving_mode: DrivingMode) -> None:
        """Set the driving mode without changing vehicle state."""
        self._driving_mode = driving_mode

    def start_engine(self) -> VehicleState:
        """Advance engine startup from OFF to STARTING, then IDLE."""
        if self._current_state == VehicleState.STARTING:
            return self._transition_to(VehicleState.IDLE)

        return self._transition_to(VehicleState.STARTING)

    def stop_engine(self) -> VehicleState:
        """Move from IDLE to OFF."""
        return self._transition_to(VehicleState.OFF)

    def accelerate(self) -> VehicleState:
        """Move from IDLE to ACCELERATING."""
        return self._transition_to(VehicleState.ACCELERATING)

    def cruise(self) -> VehicleState:
        """Move from ACCELERATING to CRUISING."""
        return self._transition_to(VehicleState.CRUISING)

    def brake(self) -> VehicleState:
        """Move from CRUISING to BRAKING."""
        return self._transition_to(VehicleState.BRAKING)

    def stop(self) -> VehicleState:
        """Advance stopping from BRAKING to STOPPED, then IDLE."""
        if self._current_state == VehicleState.STOPPED:
            return self._transition_to(VehicleState.IDLE)

        return self._transition_to(VehicleState.STOPPED)

    def reset(self) -> None:
        """Reset state and mode to their defaults."""
        self._current_state = VehicleState.OFF
        self._driving_mode = DrivingMode.CITY

    def _transition_to(self, next_state: VehicleState) -> VehicleState:
        """Transition to the next state when allowed."""
        allowed_states = self._TRANSITIONS[self._current_state]
        if next_state not in allowed_states:
            raise ValueError(
                "Invalid transition from "
                f"{self._current_state.value} to {next_state.value}"
            )

        self._current_state = next_state
        return self._current_state
