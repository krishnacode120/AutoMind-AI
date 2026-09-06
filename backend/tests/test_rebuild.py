"""Regression coverage for the rebuilt vehicle workspace."""

import pytest
from pydantic import ValidationError
from app.ai.conversation_memory import ConversationMemory
from app.ai.intent_parser import IntentParser
from app.schemas.vehicle import VehicleCreate


def test_memory_limits_and_copy_isolation():
    memory = ConversationMemory(max_sessions=2, max_messages=2)
    for index in range(3):
        memory.append_message("a", "user", str(index))
    assert [item["content"] for item in memory.get_history("a")] == ["1", "2"]
    history = memory.get_history("a")
    history[0]["content"] = "changed"
    assert memory.get_history("a")[0]["content"] == "1"
    memory.append_message("b", "user", "b")
    memory.append_message("c", "user", "c")
    assert not memory.has_session("a")
    assert memory.has_session("b") and memory.has_session("c")


def test_memory_expiration(monkeypatch):
    import app.ai.conversation_memory as module

    monkeypatch.setattr(module, "monotonic", lambda: 0.0)
    memory = ConversationMemory(ttl_seconds=10)
    session = memory.create_session()
    memory.append_message(session, "user", "hello")
    monkeypatch.setattr(module, "monotonic", lambda: 11.0)
    assert memory.get_history(session) == []
    assert not memory.has_session(session)


@pytest.mark.parametrize(
    "message,intent",
    [
        ("This is confusing", "unknown"),
        ("Show alerts", "alerts"),
        ("Who are you?", "general"),
        ("What is the speed?", "telemetry"),
        ("my carpet", "unknown"),
    ],
)
def test_intent_uses_words(message, intent):
    assert IntentParser().parse(message).intent == intent


@pytest.mark.parametrize("odometer", [float("inf"), float("nan")])
def test_vehicle_rejects_nonfinite_distance(odometer):
    with pytest.raises(ValidationError):
        VehicleCreate(
            name="Test",
            manufacturer="Toyota",
            model="Corolla",
            year=2024,
            fuel_type="Petrol",
            transmission="Automatic",
            odometer=odometer,
        )
