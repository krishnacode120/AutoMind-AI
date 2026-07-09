"""Conversation memory module."""

from typing import Any
import uuid


class ConversationMemory:
    """Manages short-term conversation state using in-memory storage."""

    def __init__(self) -> None:
        """Initialize the in-memory session dictionary."""
        self._sessions: dict[str, list[dict[str, Any]]] = {}

    def create_session(self) -> str:
        """Create a new session ID and initialize its history."""
        session_id = str(uuid.uuid4())
        self._sessions[session_id] = []
        return session_id

    def append_message(self, session_id: str, role: str, content: str) -> None:
        """Append a message to a session's history."""
        if session_id not in self._sessions:
            self._sessions[session_id] = []
            
        self._sessions[session_id].append({
            "role": role,
            "content": content
        })

    def get_history(self, session_id: str) -> list[dict[str, Any]]:
        """Retrieve the message history for a session."""
        return self._sessions.get(session_id, [])

    def clear_session(self, session_id: str) -> None:
        """Clear the message history for a specific session."""
        if session_id in self._sessions:
            del self._sessions[session_id]
