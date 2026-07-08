import asyncio
import logging
from typing import Any, Callable

logger = logging.getLogger(__name__)

class EventBus:
    """Lightweight Event Bus for pub/sub decoupled architecture."""
    
    def __init__(self) -> None:
        self.subscribers: dict[str, list[Callable[[Any], Any]]] = {}
        self.loop: asyncio.AbstractEventLoop | None = None

    def subscribe(self, topic: str, callback: Callable[[Any], Any]) -> None:
        """Subscribe a callback to a topic."""
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(callback)

    def publish(self, topic: str, data: Any) -> None:
        """Publish data to all topic subscribers."""
        if topic not in self.subscribers:
            return

        for cb in self.subscribers[topic]:
            try:
                if asyncio.iscoroutinefunction(cb):
                    if self.loop is not None and self.loop.is_running():
                        asyncio.run_coroutine_threadsafe(cb(data), self.loop)
                    else:
                        logger.warning("EventBus: Cannot run async callback because loop is not set or running.")
                else:
                    cb(data)
            except Exception as e:
                logger.error(f"EventBus: Error executing callback for topic {topic}: {e}")

event_bus = EventBus()
