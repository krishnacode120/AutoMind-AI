"""Vehicle simulator enums."""

from enum import Enum


class VehicleState(str, Enum):
    """Supported vehicle operating states."""

    OFF = "OFF"
    STARTING = "STARTING"
    IDLE = "IDLE"
    ACCELERATING = "ACCELERATING"
    CRUISING = "CRUISING"
    BRAKING = "BRAKING"
    STOPPED = "STOPPED"


class DrivingMode(str, Enum):
    """Supported vehicle driving modes."""

    CITY = "CITY"
    HIGHWAY = "HIGHWAY"
    SPORT = "SPORT"
    ECO = "ECO"
