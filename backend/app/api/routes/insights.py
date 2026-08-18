"""Read-only vehicle diagnostic routes."""

from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.vehicle_insight_service import VehicleInsightService
from app.utils.helpers import success_response


router = APIRouter(prefix="/vehicles/{vehicle_id}", tags=["Vehicle Insights"])


def _insights(db: Session, vehicle_id: int):
    """Build current diagnostic reports for a vehicle."""
    return VehicleInsightService().build(db, vehicle_id)


@router.get("/health")
async def get_vehicle_health(
    vehicle_id: int,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Return the current health report for a vehicle."""
    insights = _insights(db, vehicle_id)
    return success_response(
        message="Vehicle health retrieved successfully",
        data=insights.health.model_dump(mode="json"),
    )


@router.get("/alerts")
async def get_vehicle_alerts(
    vehicle_id: int,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Return current deterministic alerts for a vehicle."""
    insights = _insights(db, vehicle_id)
    return success_response(
        message="Vehicle alerts retrieved successfully",
        data=insights.alerts.model_dump(mode="json"),
    )


@router.get("/maintenance")
async def get_vehicle_maintenance(
    vehicle_id: int,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Return the current maintenance plan for a vehicle."""
    insights = _insights(db, vehicle_id)
    return success_response(
        message="Vehicle maintenance retrieved successfully",
        data=insights.maintenance.model_dump(mode="json"),
    )


@router.get("/prediction")
async def get_vehicle_prediction(
    vehicle_id: int,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Return the current failure prediction for a vehicle."""
    insights = _insights(db, vehicle_id)
    return success_response(
        message="Vehicle prediction retrieved successfully",
        data=insights.prediction.model_dump(mode="json"),
    )
