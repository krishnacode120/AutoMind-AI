"""Vehicle service functions."""

from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleUpdate
from sqlalchemy import delete, select
from app.models.telemetry import Telemetry
from sqlalchemy.orm import Session


def create_vehicle(db: Session, vehicle_data: VehicleCreate) -> Vehicle:
    """Create and persist a vehicle."""
    vehicle = Vehicle(**vehicle_data.model_dump())
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    return vehicle


def get_vehicle(db: Session, vehicle_id: int) -> Vehicle | None:
    """Return a vehicle by primary key."""
    return db.get(Vehicle, vehicle_id)


def list_vehicles(
    db: Session,
    skip: int = 0,
    limit: int = 100,
) -> list[Vehicle]:
    """Return a list of vehicles."""
    statement = select(Vehicle).order_by(Vehicle.id).offset(skip).limit(limit)
    return list(db.scalars(statement).all())


def update_vehicle(
    db: Session,
    vehicle: Vehicle,
    vehicle_data: VehicleUpdate,
) -> Vehicle:
    """Update and persist a vehicle."""
    update_data = vehicle_data.model_dump(exclude_unset=True)

    for field_name, value in update_data.items():
        setattr(vehicle, field_name, value)

    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    return vehicle


def delete_vehicle(db: Session, vehicle: Vehicle) -> None:
    """Delete a vehicle."""
    db.execute(delete(Telemetry).where(Telemetry.vehicle_id == vehicle.id))
    db.delete(vehicle)
    db.commit()
