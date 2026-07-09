"""Tests for WebSocket connection manager behavior."""

import pytest

from app.websocket.connection_manager import ConnectionManager


class MockWebSocket:
    """Minimal async websocket mock for manager tests."""

    def __init__(self, fail_send: bool = False) -> None:
        self.accepted = False
        self.fail_send = fail_send
        self.messages: list[str] = []

    async def accept(self) -> None:
        self.accepted = True

    async def send_text(self, message: str) -> None:
        if self.fail_send:
            raise RuntimeError("Send failed")
        self.messages.append(message)


@pytest.mark.asyncio
async def test_connection_manager_connect_and_broadcast() -> None:
    """Connected clients should receive broadcast messages."""
    manager = ConnectionManager()
    socket = MockWebSocket()
    await manager.connect(socket, vehicle_id=7)
    await manager.broadcast(vehicle_id=7, message="hello")

    assert socket.accepted is True
    assert socket.messages == ["hello"]


@pytest.mark.asyncio
async def test_connection_manager_disconnects_failed_clients() -> None:
    """Failed sends should remove dead connections."""
    manager = ConnectionManager()
    failing_socket = MockWebSocket(fail_send=True)
    await manager.connect(failing_socket, vehicle_id=9)
    await manager.broadcast(vehicle_id=9, message="update")

    assert failing_socket not in manager.active_connections[9]
