"""Base predictor interface."""

from abc import ABC, abstractmethod

from app.schemas.alert import AlertReport
from app.schemas.health import HealthReport
from app.schemas.maintenance import MaintenanceReport
from app.schemas.prediction import PredictionResult


class VehiclePredictor(ABC):
    """Abstract interface for vehicle predictors."""

    @abstractmethod
    def predict(
        self,
        health_report: HealthReport,
        alert_report: AlertReport,
        maintenance_report: MaintenanceReport,
    ) -> PredictionResult:
        """Generate a vehicle prediction."""

    @abstractmethod
    def supports_training(self) -> bool:
        """Return whether this predictor supports training."""

    @abstractmethod
    def model_name(self) -> str:
        """Return the predictor model name."""
