"""Driving profile definitions for ML dataset scenarios."""

from dataclasses import dataclass

from app.simulator.enums import DrivingMode


@dataclass(frozen=True)
class DrivingProfile:
    """Driving profile used to guide simulator state transitions."""

    name: str
    driving_mode: DrivingMode
    acceleration_steps: int
    cruising_steps: int
    braking_steps: int
    stopped_steps: int

    @property
    def cycle_length(self) -> int:
        """Return the number of samples in one profile cycle."""
        return (
            self.acceleration_steps
            + self.cruising_steps
            + self.braking_steps
            + self.stopped_steps
        )


CITY_PROFILE = DrivingProfile(
    name="City",
    driving_mode=DrivingMode.CITY,
    acceleration_steps=10,
    cruising_steps=8,
    braking_steps=12,
    stopped_steps=4,
)

HIGHWAY_PROFILE = DrivingProfile(
    name="Highway",
    driving_mode=DrivingMode.HIGHWAY,
    acceleration_steps=18,
    cruising_steps=28,
    braking_steps=10,
    stopped_steps=1,
)

SPORT_PROFILE = DrivingProfile(
    name="Sport",
    driving_mode=DrivingMode.SPORT,
    acceleration_steps=8,
    cruising_steps=14,
    braking_steps=8,
    stopped_steps=1,
)

ECO_PROFILE = DrivingProfile(
    name="Eco",
    driving_mode=DrivingMode.ECO,
    acceleration_steps=18,
    cruising_steps=16,
    braking_steps=14,
    stopped_steps=3,
)

TRAFFIC_PROFILE = DrivingProfile(
    name="Traffic",
    driving_mode=DrivingMode.CITY,
    acceleration_steps=5,
    cruising_steps=4,
    braking_steps=8,
    stopped_steps=7,
)

MOUNTAIN_PROFILE = DrivingProfile(
    name="Mountain",
    driving_mode=DrivingMode.SPORT,
    acceleration_steps=14,
    cruising_steps=10,
    braking_steps=18,
    stopped_steps=2,
)

DRIVING_PROFILES: dict[str, DrivingProfile] = {
    profile.name: profile
    for profile in (
        CITY_PROFILE,
        HIGHWAY_PROFILE,
        SPORT_PROFILE,
        ECO_PROFILE,
        TRAFFIC_PROFILE,
        MOUNTAIN_PROFILE,
    )
}

DEFAULT_PROFILE_WEIGHTS: dict[str, float] = {
    "City": 0.24,
    "Highway": 0.20,
    "Sport": 0.14,
    "Eco": 0.16,
    "Traffic": 0.14,
    "Mountain": 0.12,
}
