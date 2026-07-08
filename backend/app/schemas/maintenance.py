"""Maintenance recommendation schemas."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class MaintenancePriority(str, Enum):
    """Supported maintenance priority levels."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"


class MaintenanceTask(BaseModel):
    """Single recommended maintenance task."""

    id: str
    title: str
    description: str
    priority: MaintenancePriority
    estimated_km_remaining: float | None = Field(default=None, ge=0)
    estimated_days_remaining: int | None = Field(default=None, ge=0)
    recommended_action: str
    component: str


class MaintenanceReport(BaseModel):
    """Vehicle maintenance recommendation report."""

    overall_priority: MaintenancePriority
    task_count: int = Field(ge=0)
    tasks: list[MaintenanceTask]
    timestamp: datetime
