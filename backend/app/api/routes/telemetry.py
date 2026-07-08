"""Telemetry API routes."""

from typing import Any

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.telemetry import (
    LatestTelemetry,
    TelemetryCreate,
    TelemetryHistory,
    TelemetryResponse,
)
from app.services import telemetry_service
from app.utils.helpers import success_response


router = APIRouter(prefix="/telemetry", tags=["Telemetry"])


def _telemetry_payload(telemetry: Any) -> dict[str, Any]:
    """Serialize a telemetry ORM object for API responses."""
    return TelemetryResponse.model_validate(telemetry).model_dump(mode="json")


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_telemetry(
    telemetry_data: TelemetryCreate,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Create a telemetry record."""
    telemetry = telemetry_service.create_telemetry(db, telemetry_data)
    return success_response(
        message="Telemetry created successfully",
        data=_telemetry_payload(telemetry),
    )


@router.get("/latest/{vehicle_id}")
async def get_latest(
    vehicle_id: int,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Return the latest telemetry record for a vehicle."""
    telemetry = telemetry_service.get_latest(db, vehicle_id)
    payload = LatestTelemetry(
        vehicle_id=vehicle_id,
        telemetry=telemetry,
    ).model_dump(mode="json")
    return success_response(
        message="Latest telemetry retrieved successfully",
        data=payload,
    )


@router.get("/history/{vehicle_id}")
async def get_history(
    vehicle_id: int,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Return telemetry history for a vehicle."""
    records = telemetry_service.get_history(db, vehicle_id)
    payload = TelemetryHistory(
        vehicle_id=vehicle_id,
        records=records,
    ).model_dump(mode="json")
    return success_response(
        message="Telemetry history retrieved successfully",
        data=payload,
    )


@router.delete("/history/{vehicle_id}")
async def delete_history(
    vehicle_id: int,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Delete telemetry history for a vehicle."""
    deleted_count = telemetry_service.delete_history(db, vehicle_id)
    return success_response(
        message="Telemetry history deleted successfully",
        data={"deleted_count": deleted_count},
    )
