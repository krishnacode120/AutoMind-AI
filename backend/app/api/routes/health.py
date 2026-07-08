"""Health and service status routes."""

from fastapi import APIRouter

from app.config.settings import settings
from app.core.version import AI_NAME, API_VERSION, PROJECT_NAME, PROJECT_VERSION
from app.utils.time_utils import utc_now_iso


router = APIRouter(tags=["Health"])


@router.get("/")
async def root() -> dict[str, str]:
    """Return basic project status."""
    return {
        "project": PROJECT_NAME,
        "assistant": AI_NAME,
        "status": "running",
        "version": PROJECT_VERSION,
        "api_version": API_VERSION,
        "environment": settings.ENVIRONMENT,
        "server_time": utc_now_iso(),
    }


@router.get("/health")
async def health_check() -> dict[str, str]:
    """Return service health status."""
    return {"status": "healthy"}
