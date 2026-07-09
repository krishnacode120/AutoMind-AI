"""Tests for BON request and response contracts."""

from app.ai.types import BONRequest, BONResponse


def test_bon_request_schema_fields() -> None:
    """BON request should enforce required fields."""
    request = BONRequest(
        vehicle_id=1,
        message="How is my vehicle health?",
        session_id="session-1",
    )
    assert request.vehicle_id == 1
    assert request.session_id == "session-1"


def test_bon_response_schema_fields() -> None:
    """BON response schema should retain response payload fields."""
    response = BONResponse(
        answer="Your vehicle health is stable.",
        intent="health_query",
        confidence=0.92,
        context_used={"health": {"status": "Good"}},
        timestamp="2026-01-01T00:00:00Z",
    )
    assert response.intent == "health_query"
    assert response.context_used["health"]["status"] == "Good"
