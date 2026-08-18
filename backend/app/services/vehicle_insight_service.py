"""Read-only vehicle diagnostic report aggregation."""

from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.core.exceptions import GlobalException
from app.prediction.predictor_factory import PredictorFactory
from app.schemas.alert import AlertReport
from app.schemas.health import HealthReport
from app.schemas.maintenance import MaintenanceReport
from app.schemas.prediction import PredictionResult
from app.services import telemetry_service
from app.services.alert_service import VehicleAlertService
from app.services.health_service import VehicleHealthService
from app.services.maintenance_service import VehicleMaintenanceService


@dataclass(frozen=True)
class VehicleInsights:
    """Calculated diagnostic reports for a vehicle's latest telemetry."""

    health: HealthReport
    alerts: AlertReport
    maintenance: MaintenanceReport
    prediction: PredictionResult


class VehicleInsightService:
    """Build related diagnostic reports without persisting derived data."""

    def __init__(self, predictor_factory: PredictorFactory | None = None) -> None:
        """Initialize report calculators and the selected predictor factory."""
        self._health_service = VehicleHealthService()
        self._alert_service = VehicleAlertService()
        self._maintenance_service = VehicleMaintenanceService()
        self._predictor_factory = predictor_factory or PredictorFactory()

    def build(self, db: Session, vehicle_id: int) -> VehicleInsights:
        """Calculate all reports from the vehicle's newest telemetry record."""
        telemetry = telemetry_service.get_latest(db, vehicle_id)
        if telemetry is None:
            raise GlobalException(
                "Telemetry data is not available for this vehicle",
                status_code=404,
            )

        health = self._health_service.calculate_health(telemetry)
        alerts = self._alert_service.generate_alerts(telemetry, health)
        maintenance = self._maintenance_service.generate_maintenance_plan(
            telemetry,
            health,
            alerts,
        )
        prediction = self._predictor_factory.create("auto").predict(
            health,
            alerts,
            maintenance,
        )

        return VehicleInsights(
            health=health,
            alerts=alerts,
            maintenance=maintenance,
            prediction=prediction,
        )
