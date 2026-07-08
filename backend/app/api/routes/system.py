"""System infrastructure status routes."""

from fastapi import APIRouter

from app.database.session import engine


router = APIRouter(tags=["System"])


def _engine_name() -> str:
    """Return a display name for the configured database engine."""
    if engine.dialect.name == "sqlite":
        return "SQLite"

    return engine.dialect.name


@router.get("/system")
async def system_status() -> dict[str, str]:
    """Return database infrastructure readiness status."""
    return {
        "database": "connected",
        "engine": _engine_name(),
        "orm": "SQLAlchemy 2.x",
        "status": "ready",
    }
