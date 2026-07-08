"""Alert schemas."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class AlertSeverity(str, Enum):
    """Supported alert severity levels."""

    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


class AlertType(str, Enum):
    """Supported alert types."""

    HIGH_ENGINE_TEMP = "HIGH_ENGINE_TEMP"
    LOW_FUEL = "LOW_FUEL"
    LOW_BATTERY = "LOW_BATTERY"
    LOW_OIL_LIFE = "LOW_OIL_LIFE"
    LOW_COOLANT = "LOW_COOLANT"
    LOW_TIRE_PRESSURE = "LOW_TIRE_PRESSURE"
    HIGH_BRAKE_WEAR = "HIGH_BRAKE_WEAR"
    ENGINE_OVERLOAD = "ENGINE_OVERLOAD"
    VEHICLE_HEALTH_CRITICAL = "VEHICLE_HEALTH_CRITICAL"


class Alert(BaseModel):
    """Single vehicle alert."""

    severity: AlertSeverity
    type: AlertType
    title: str
    description: str
    recommendation: str
    timestamp: datetime


class AlertReport(BaseModel):
    """Collection of generated vehicle alerts."""

    alert_count: int = Field(ge=0)
    highest_severity: AlertSeverity | None
    alerts: list[Alert]
