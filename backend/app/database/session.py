"""Database engine and session management."""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.config.settings import settings


def _connect_args(database_url: str) -> dict[str, bool]:
    """Return engine connection arguments for the configured database."""
    if database_url.startswith("sqlite"):
        return {"check_same_thread": False}

    return {}


engine: Engine = create_engine(
    settings.DATABASE_URL,
    connect_args=_connect_args(settings.DATABASE_URL),
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=Session,
)


def get_db() -> Generator[Session, None, None]:
    """Yield a database session for future request dependencies."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
