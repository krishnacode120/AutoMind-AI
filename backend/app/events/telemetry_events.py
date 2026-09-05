"""Telemetry-specific event topics."""

# Fired when a new telemetry snapshot is successfully persisted
TELEMETRY_CREATED = "telemetry.created"


def publish_telemetry(telemetry) -> None:
    """Detach the event payload from the committing SQLAlchemy session."""
    from app.events.event_bus import event_bus
    from app.schemas.telemetry import TelemetryResponse

    payload = TelemetryResponse.model_validate(telemetry).model_dump(mode="json")
    event_bus.publish(TELEMETRY_CREATED, payload)
