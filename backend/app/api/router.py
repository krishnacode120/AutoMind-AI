"""API router registration."""

from fastapi import APIRouter

from app.api.routes import health, system, telemetry, vehicle, ws
from app.core.version import API_PREFIX

router = APIRouter(prefix=API_PREFIX)
router.include_router(health.router)
router.include_router(system.router)
router.include_router(telemetry.router)
router.include_router(vehicle.router)

# Include websocket without prefixing if necessary, but here we'll just add it to the main router.
# So it will be at /api/v1/ws/telemetry/{vehicle_id}
router.include_router(ws.router)

