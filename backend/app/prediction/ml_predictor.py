"""Future machine-learning predictor placeholder."""

from app.prediction.base_predictor import VehiclePredictor
from app.schemas.alert import AlertReport
from app.schemas.health import HealthReport
from app.schemas.maintenance import MaintenanceReport
from app.schemas.prediction import PredictionResult


class MLPredictor(VehiclePredictor):
    """Placeholder for future machine-learning predictors."""

    def predict(
        self,
        health_report: HealthReport,
        alert_report: AlertReport,
        maintenance_report: MaintenanceReport,
    ) -> PredictionResult:
        """Raise until machine-learning prediction is implemented."""
        raise NotImplementedError("ML prediction is not implemented yet")

    def supports_training(self) -> bool:
        """Return whether this predictor supports training."""
        return True

    def model_name(self) -> str:
        """Return the predictor model name."""
        return "ml-placeholder"
