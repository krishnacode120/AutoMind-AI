"""Application lifespan handlers."""
import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config.logging import get_logger
from app.database.database import init_db
from app.events.event_bus import event_bus


logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Handle application startup and shutdown events."""
    logger.info("Starting AutoMind AI...")
    
    # Give the event bus a reference to the main thread's asyncio loop
    event_bus.loop = asyncio.get_running_loop()
    
    init_db()
    yield
    logger.info("Stopping AutoMind AI...")

