"""Vehicle API routes."""

from typing import Any

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.exceptions import GlobalException
from app.database.session import get_db
from app.schemas.vehicle import VehicleCreate, VehicleResponse, VehicleUpdate
from app.services import vehicle_service
from app.utils.helpers import success_response


router = APIRouter(prefix="/vehicles", tags=["Vehicles"])


def _vehicle_payload(vehicle: Any) -> dict[str, Any]:
    """Serialize a vehicle ORM object for API responses."""
    return VehicleResponse.model_validate(vehicle).model_dump(mode="json")


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_vehicle(
    vehicle_data: VehicleCreate,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Create a vehicle."""
    vehicle = vehicle_service.create_vehicle(db, vehicle_data)
    return success_response(
        message="Vehicle created successfully",
        data=_vehicle_payload(vehicle),
    )


@router.get("")
async def list_vehicles(
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """List vehicles."""
    vehicles = vehicle_service.list_vehicles(db)
    return success_response(
        message="Vehicles retrieved successfully",
        data=[_vehicle_payload(vehicle) for vehicle in vehicles],
    )


@router.get("/{vehicle_id}")
async def get_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Return a vehicle by ID."""
    vehicle = vehicle_service.get_vehicle(db, vehicle_id)
    if vehicle is None:
        raise GlobalException("Vehicle not found", status.HTTP_404_NOT_FOUND)

    return success_response(
        message="Vehicle retrieved successfully",
        data=_vehicle_payload(vehicle),
    )


@router.put("/{vehicle_id}")
async def update_vehicle(
    vehicle_id: int,
    vehicle_data: VehicleUpdate,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Update a vehicle by ID."""
    vehicle = vehicle_service.get_vehicle(db, vehicle_id)
    if vehicle is None:
        raise GlobalException("Vehicle not found", status.HTTP_404_NOT_FOUND)

    updated_vehicle = vehicle_service.update_vehicle(db, vehicle, vehicle_data)
    return success_response(
        message="Vehicle updated successfully",
        data=_vehicle_payload(updated_vehicle),
    )


@router.delete("/{vehicle_id}")
async def delete_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Delete a vehicle by ID."""
    vehicle = vehicle_service.get_vehicle(db, vehicle_id)
    if vehicle is None:
        raise GlobalException("Vehicle not found", status.HTTP_404_NOT_FOUND)

    vehicle_service.delete_vehicle(db, vehicle)
    return success_response(message="Vehicle deleted successfully")
