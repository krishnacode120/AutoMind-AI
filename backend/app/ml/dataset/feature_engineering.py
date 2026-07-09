"""Feature engineering utilities for ML dataset generation."""

from typing import Any

from app.models.telemetry import Telemetry
from app.schemas.alert import AlertReport
from app.schemas.health import HealthReport
from app.schemas.maintenance import MaintenanceReport
from app.schemas.prediction import PredictionResult


TELEMETRY_FEATURES: tuple[str, ...] = (
    "vehicle_state",
    "driving_mode",
    "speed",
    "rpm",
    "fuel_level",
    "engine_temperature",
    "battery_voltage",
    "oil_life",
    "coolant_level",
    "tire_pressure_fl",
    "tire_pressure_fr",
    "tire_pressure_rl",
    "tire_pressure_rr",
    "brake_wear",
    "engine_load",
    "throttle_position",
    "gear",
    "trip_distance",
    "odometer",
    "fuel_consumption",
)


class FeatureEngineer:
    """Build flat dataset rows from existing domain outputs."""

    def build_features(
        self,
        telemetry: Telemetry,
        health_report: HealthReport,
        alert_report: AlertReport,
        maintenance_report: MaintenanceReport,
        prediction: PredictionResult,
        scenario_profile: str | None = None,
        injected_faults: tuple[str, ...] = (),
    ) -> dict[str, Any]:
        """Return one flat feature row for a telemetry sample."""
        row = {
            "telemetry_id": telemetry.id,
            "timestamp": telemetry.timestamp.isoformat(),
            "created_at": (
                telemetry.created_at.isoformat()
                if telemetry.created_at
                else None
            ),
            "vehicle_id": telemetry.vehicle_id,
            "driving_profile": scenario_profile,
            "injected_faults": "|".join(injected_faults) or None,
            "fault_count": len(injected_faults),
        }

        for feature_name in TELEMETRY_FEATURES:
            row[feature_name] = getattr(telemetry, feature_name)

        row.update(
            {
                "health_score": health_report.health_score,
                "health_status": health_report.health_status,
                "alert_count": alert_report.alert_count,
                "highest_alert_severity": (
                    alert_report.highest_severity.value
                    if alert_report.highest_severity
                    else None
                ),
                "maintenance_priority": (
                    maintenance_report.overall_priority.value
                ),
                "maintenance_task_count": maintenance_report.task_count,
                "prediction_type": prediction.prediction_type,
                "prediction_confidence": prediction.confidence,
                "predicted_failure": prediction.predicted_failure,
                "estimated_remaining_km": prediction.estimated_remaining_km,
            }
        )
        return row
