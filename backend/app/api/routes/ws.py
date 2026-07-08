"""WebSocket routes."""

import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.websocket.connection_manager import manager
from app.events.event_bus import event_bus
from app.events.telemetry_events import TELEMETRY_CREATED
from app.schemas.telemetry import TelemetryResponse

router = APIRouter(tags=["WebSocket"])

async def handle_telemetry_created(telemetry) -> None:
    """Callback triggered by event bus when new telemetry is created."""
    # Convert SQLAlchemy model to Pydantic schema -> JSON
    payload = TelemetryResponse.model_validate(telemetry).model_dump(mode="json")
    
    # Create the standard response envelope we expect on the frontend
    message = json.dumps({
        "type": "telemetry_update",
        "data": payload
    })
    
    # Broadcast to only clients subscribed to this vehicle
    await manager.broadcast(telemetry.vehicle_id, message)

# Subscribe to the event bus immediately
event_bus.subscribe(TELEMETRY_CREATED, handle_telemetry_created)

@router.websocket("/ws/telemetry/{vehicle_id}")
async def websocket_endpoint(websocket: WebSocket, vehicle_id: int):
    """Handle incoming WebSocket connections for real-time telemetry."""
    await manager.connect(websocket, vehicle_id)
    try:
        while True:
            # We don't expect any messages from the client right now
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, vehicle_id)
