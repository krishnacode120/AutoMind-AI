"""Database initialization utilities."""

from app.database.base import Base
from app.database.session import engine
from app.models import telemetry  # noqa: F401
from app.models import vehicle  # noqa: F401


def init_db() -> None:
    """Initialize database metadata for registered models."""
    Base.metadata.create_all(bind=engine)
