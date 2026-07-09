"""Types and models for the BON AI system."""

from typing import Any
from pydantic import BaseModel, Field


class BONRequest(BaseModel):
    """Request payload for the BON assistant."""
    vehicle_id: int
    message: str
    session_id: str


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
