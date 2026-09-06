"""API router registration."""

from app.api.routes import bon, health, insights, system, telemetry, vehicle, ws
from app.core.version import API_PREFIX
from fastapi import APIRouter

router = APIRouter(prefix=API_PREFIX)
router.include_router(bon.router)
router.include_router(health.router)
router.include_router(insights.router)
router.include_router(system.router)
router.include_router(telemetry.router)
router.include_router(vehicle.router)

# Include websocket without prefixing if necessary.
# It will be at /api/v1/ws/telemetry/{vehicle_id}
router.include_router(ws.router)
