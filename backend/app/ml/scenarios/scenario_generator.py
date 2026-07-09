"""Scenario generation for ML dataset samples."""

from random import Random

from app.ml.scenarios.driving_profiles import (
    DEFAULT_PROFILE_WEIGHTS,
    DRIVING_PROFILES,
    DrivingProfile,
)
from app.ml.scenarios.scenario import FaultType, Scenario


DEFAULT_FAULT_PROBABILITIES: dict[FaultType, float] = {
    FaultType.LOW_FUEL: 0.02,
    FaultType.LOW_BATTERY: 0.02,
    FaultType.HIGH_ENGINE_TEMPERATURE: 0.10,
    FaultType.HIGH_BRAKE_WEAR: 0.08,
    FaultType.LOW_COOLANT: 0.02,
    FaultType.HIGH_ENGINE_LOAD: 0.10,
    FaultType.LOW_TIRE_PRESSURE: 0.02,
}


class ScenarioGenerator:
    """Generate randomized driving scenarios and controlled faults."""

    def __init__(
        self,
        profile_weights: dict[str, float] | None = None,
        fault_probabilities: dict[FaultType | str, float] | None = None,
        random_seed: int | None = 0,
    ) -> None:
        """Initialize scenario sampling configuration."""
        self._random = Random(random_seed)
        self._profile_weights = profile_weights or DEFAULT_PROFILE_WEIGHTS
        self._fault_probabilities = self._normalize_fault_probabilities(
            fault_probabilities or DEFAULT_FAULT_PROBABILITIES,
        )
        self._validate_profile_weights()
        self._validate_fault_probabilities()

    def generate(self) -> Scenario:
        """Generate one scenario."""
        return Scenario(
            profile=self._select_profile(),
            faults=self._select_faults(),
        )

    def _select_profile(self) -> DrivingProfile:
        """Randomly select a driving profile from configured weights."""
        names = list(self._profile_weights)
        weights = [self._profile_weights[name] for name in names]
        selected_name = self._random.choices(names, weights=weights, k=1)[0]
        return DRIVING_PROFILES[selected_name]

    def _select_faults(self) -> tuple[FaultType, ...]:
        """Select independent controlled faults for one sample."""
        return tuple(
            fault_type
            for fault_type, probability in self._fault_probabilities.items()
            if self._random.random() < probability
        )

    def _normalize_fault_probabilities(
        self,
        probabilities: dict[FaultType | str, float],
    ) -> dict[FaultType, float]:
        """Convert string keys to FaultType keys."""
        return {
            self._fault_type(key): probability
            for key, probability in probabilities.items()
        }

    def _fault_type(self, value: FaultType | str) -> FaultType:
        """Return a FaultType from enum or string input."""
        if isinstance(value, FaultType):
            return value

        return FaultType(value)

    def _validate_profile_weights(self) -> None:
        """Validate configured profile names and weights."""
        if not self._profile_weights:
            raise ValueError("At least one driving profile weight is required")

        for name, weight in self._profile_weights.items():
            if name not in DRIVING_PROFILES:
                raise ValueError(f"Unknown driving profile: {name}")
            if weight < 0:
                raise ValueError("Profile weights cannot be negative")

    def _validate_fault_probabilities(self) -> None:
        """Validate configured fault probabilities."""
        for probability in self._fault_probabilities.values():
            if probability < 0.0 or probability > 1.0:
                raise ValueError("Fault probabilities must be between 0 and 1")
