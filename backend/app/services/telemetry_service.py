"""Telemetry service functions."""

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.core.exceptions import GlobalException
from app.models.telemetry import Telemetry
from app.models.vehicle import Vehicle
from app.schemas.telemetry import TelemetryCreate
from app.utils.time_utils import utc_now


def _ensure_vehicle_exists(db: Session, vehicle_id: int) -> None:
    """Raise a 404 error if the vehicle does not exist."""
    if db.get(Vehicle, vehicle_id) is None:
        raise GlobalException("Vehicle not found", 404)


def create_telemetry(
    db: Session,
    telemetry_data: TelemetryCreate,
) -> Telemetry:
    """Create and persist a telemetry record."""
    _ensure_vehicle_exists(db, telemetry_data.vehicle_id)
    data = telemetry_data.model_dump()

    if data["timestamp"] is None:
        data["timestamp"] = utc_now()

    telemetry = Telemetry(**data)
    db.add(telemetry)
    db.commit()
    db.refresh(telemetry)
    return telemetry


def get_latest(db: Session, vehicle_id: int) -> Telemetry | None:
    """Return the latest telemetry record for a vehicle."""
    _ensure_vehicle_exists(db, vehicle_id)
    statement = (
        select(Telemetry)
        .where(Telemetry.vehicle_id == vehicle_id)
        .order_by(Telemetry.timestamp.desc(), Telemetry.id.desc())
        .limit(1)
    )
    return db.scalars(statement).first()


def get_history(
    db: Session,
    vehicle_id: int,
    skip: int = 0,
    limit: int = 100,
) -> list[Telemetry]:
    """Return telemetry history for a vehicle."""
    _ensure_vehicle_exists(db, vehicle_id)
    statement = (
        select(Telemetry)
        .where(Telemetry.vehicle_id == vehicle_id)
        .order_by(Telemetry.timestamp.desc(), Telemetry.id.desc())
        .offset(skip)
        .limit(limit)
    )
    return list(db.scalars(statement).all())


def delete_history(db: Session, vehicle_id: int) -> int:
    """Delete telemetry history for a vehicle and return deleted count."""
    _ensure_vehicle_exists(db, vehicle_id)
    statement = delete(Telemetry).where(Telemetry.vehicle_id == vehicle_id)
    result = db.execute(statement)
    db.commit()
    return int(result.rowcount or 0)
