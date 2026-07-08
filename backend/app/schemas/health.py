"""Vehicle health report schema."""

from datetime import datetime

from pydantic import BaseModel, Field


class HealthReport(BaseModel):
    """Calculated vehicle health report."""

    health_score: int = Field(ge=0, le=100)
    health_status: str
    penalties: dict[str, float]
    recommendations: list[str]
    timestamp: datetime
