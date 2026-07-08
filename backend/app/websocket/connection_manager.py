"""WebSocket connection manager for handling client connections."""

from collections import defaultdict
import logging

from fastapi import WebSocket

logger = logging.getLogger(__name__)

class ConnectionManager:
    """Manage WebSocket connections grouped by vehicle ID."""

    def __init__(self) -> None:
        # Map vehicle_id -> list of active WebSocket connections
        self.active_connections: dict[int, list[WebSocket]] = defaultdict(list)

    async def connect(self, websocket: WebSocket, vehicle_id: int) -> None:
        """Accept the connection and add it to the active list."""
        await websocket.accept()
        self.active_connections[vehicle_id].append(websocket)
        logger.info(f"WebSocket connected for vehicle {vehicle_id}. Total: {len(self.active_connections[vehicle_id])}")

    def disconnect(self, websocket: WebSocket, vehicle_id: int) -> None:
        """Remove the connection from the active list."""
        if vehicle_id in self.active_connections:
            if websocket in self.active_connections[vehicle_id]:
                self.active_connections[vehicle_id].remove(websocket)
                logger.info(f"WebSocket disconnected for vehicle {vehicle_id}.")

    async def broadcast(self, vehicle_id: int, message: str) -> None:
        """Broadcast a message to all connected clients for a given vehicle."""
        if vehicle_id not in self.active_connections:
            return

        connections = self.active_connections[vehicle_id].copy()
        for connection in connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.warning(f"Failed to send message to client for vehicle {vehicle_id}: {e}")
                self.disconnect(connection, vehicle_id)

manager = ConnectionManager()
