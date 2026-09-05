"""Types and models for the BON AI system."""

from typing import Any

from pydantic import BaseModel, Field, ConfigDict


class BONRequest(BaseModel):
    """Request payload for the BON assistant."""

    model_config = ConfigDict(str_strip_whitespace=True)
    vehicle_id: int = Field(gt=0)
    message: str = Field(min_length=1, max_length=4000)
    session_id: str = Field(min_length=1, max_length=100)


class BONResponse(BaseModel):
    """Response payload from the BON assistant."""

    answer: str
    intent: str
    confidence: float
    context_used: dict[str, Any] = Field(default_factory=dict)
    timestamp: str


class IntentResult(BaseModel):
    """Parsed intent classification."""

    intent: str
    confidence: float
    entities: dict[str, Any] = Field(default_factory=dict)
