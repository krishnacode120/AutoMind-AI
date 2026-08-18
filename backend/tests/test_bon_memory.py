"""Unit tests for BON Assistant conversation memory retention and multi-turn context."""

from app.ai.bon import BONAssistant
from app.ai.types import BONRequest


def test_bon_assistant_memory_retention() -> None:
    """Test that BON assistant retains conversation history across turns."""
    assistant = BONAssistant()
    session_id = "test-session-multi-turn"

    # Turn 1
    req1 = BONRequest(vehicle_id=1, message="Hello", session_id=session_id)
    res1 = assistant.process(req1)
    assert res1.intent == "general"

    # Turn 2
    req2 = BONRequest(vehicle_id=1, message="How is my health?", session_id=session_id)
    res2 = assistant.process(req2)
    assert res2.intent == "health"

    # Verify history in memory
    history = assistant.memory.get_history(session_id)
    assert len(history) == 4  # 2 user msgs + 2 assistant msgs
    assert history[0]["content"] == "Hello"
    assert history[2]["content"] == "How is my health?"

    # Check that session exists
    assert assistant.memory.has_session(session_id) is True

    # Clear session
    assistant.memory.clear_session(session_id)
    assert assistant.memory.has_session(session_id) is False
    assert len(assistant.memory.get_history(session_id)) == 0
