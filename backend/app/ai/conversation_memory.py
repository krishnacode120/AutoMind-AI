"""Bounded, expiring conversation state for a single application process."""

import uuid
from collections import OrderedDict
from threading import RLock
from time import monotonic
from typing import Any


class ConversationMemory:
    """Keep recent messages without unbounded process memory growth."""

    def __init__(
        self,
        max_sessions: int = 1000,
        max_messages: int = 100,
        ttl_seconds: float = 3600,
    ) -> None:
        if max_sessions < 1 or max_messages < 1 or ttl_seconds <= 0:
            raise ValueError("Memory limits must be positive")
        self._sessions: OrderedDict[str, list[dict[str, Any]]] = OrderedDict()
        self._updated: dict[str, float] = {}
        self._lock = RLock()
        self._max_sessions = max_sessions
        self._max_messages = max_messages
        self._ttl = ttl_seconds

    def _prune(self) -> None:
        now = monotonic()
        for session in list(self._sessions):
            if now - self._updated[session] >= self._ttl:
                self.clear_session(session)
        while len(self._sessions) > self._max_sessions:
            session, _ = self._sessions.popitem(last=False)
            self._updated.pop(session, None)

    def create_session(self) -> str:
        session_id = str(uuid.uuid4())
        with self._lock:
            self._sessions[session_id] = []
            self._updated[session_id] = monotonic()
            self._prune()
        return session_id

    def append_message(self, session_id: str, role: str, content: str) -> None:
        with self._lock:
            self._prune()
            history = self._sessions.setdefault(session_id, [])
            history.append({"role": role, "content": content})
            del history[: -self._max_messages]
            self._updated[session_id] = monotonic()
            self._sessions.move_to_end(session_id)
            self._prune()

    def get_history(self, session_id: str) -> list[dict[str, Any]]:
        with self._lock:
            self._prune()
            return [dict(message) for message in self._sessions.get(session_id, [])]

    def has_session(self, session_id: str) -> bool:
        with self._lock:
            self._prune()
            return session_id in self._sessions

    def clear_session(self, session_id: str) -> None:
        with self._lock:
            self._sessions.pop(session_id, None)
            self._updated.pop(session_id, None)
