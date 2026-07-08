"""Prediction result schema."""

from datetime import datetime

from pydantic import BaseModel, Field


class PredictionResult(BaseModel):
    """Vehicle prediction result."""

    prediction_type: str
    confidence: float = Field(ge=0.0, le=1.0)
    predicted_failure: str
    recommended_action: str
    estimated_remaining_km: float | None = Field(default=None, ge=0)
    timestamp: datetime
