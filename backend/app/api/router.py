"""API router registration."""

from fastapi import APIRouter

from app.api.routes import health, system, telemetry, vehicle
from app.core.version import API_PREFIX


router = APIRouter(prefix=API_PREFIX)
router.include_router(health.router)
router.include_router(system.router)
router.include_router(telemetry.router)
router.include_router(vehicle.router)
