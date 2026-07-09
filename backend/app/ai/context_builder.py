"""BON context building module."""

from collections.abc import Iterator, Mapping
from typing import Any

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.ai.conversation_memory import ConversationMemory
from app.database.session import SessionLocal
from app.prediction.predictor_factory import PredictorFactory
from app.schemas.alert import AlertReport
from app.schemas.health import HealthReport
from app.schemas.maintenance import MaintenanceReport
from app.schemas.telemetry import TelemetryResponse
from app.schemas.vehicle import VehicleResponse
from app.services import telemetry_service, vehicle_service
from app.services.alert_service import VehicleAlertService
from app.services.health_service import VehicleHealthService
from app.services.maintenance_service import VehicleMaintenanceService
from app.utils.time_utils import utc_now


class BONContext(BaseModel, Mapping[str, Any]):
    """Context collected for BON responses."""

    vehicle: dict[str, Any] | None = None
    telemetry: dict[str, Any] | None = None
    health: dict[str, Any] | None = None
    alerts: dict[str, Any] | None = None
    maintenance: dict[str, Any] | None = None
    prediction: dict[str, Any] | None = None
    conversation: list[dict[str, Any]] = Field(default_factory=list)
    timestamp: str

    def __getitem__(self, key: str) -> Any:
        """Return context value by key."""
        return self.model_dump(mode="json")[key]

    def __iter__(self) -> Iterator[str]:
        """Return an iterator over context keys."""
        return iter(self.model_dump(mode="json"))

    def __len__(self) -> int:
        """Return the number of context fields."""
        return len(self.model_dump(mode="json"))


class ContextBuilder:
    """Build application context for BON without performing AI reasoning."""

    def __init__(
        self,
        memory: ConversationMemory | None = None,
        predictor_factory: PredictorFactory | None = None,
    ) -> None:
        """Initialize context builder dependencies."""
        self._memory = memory or ConversationMemory()
        self._predictor_factory = predictor_factory or PredictorFactory()

    def build(
        self,
        vehicle_id: int,
        intent: str,
        session_id: str | None = None,
    ) -> BONContext:
        """Fetch and aggregate context for BON."""
        with SessionLocal() as db:
            vehicle = self._safe_call(self._build_vehicle, db, vehicle_id)
            telemetry = self._safe_call(self._get_latest_telemetry, db, vehicle_id)
            health = self._safe_call(self._build_health, telemetry)
            alerts = self._safe_call(self._build_alerts, telemetry, health)
            maintenance = self._safe_call(
                self._build_maintenance,
                telemetry,
                health,
                alerts,
            )
            prediction = self._safe_call(
                self._build_prediction,
                health,
                alerts,
                maintenance,
            )

        return BONContext(
            vehicle=vehicle,
            telemetry=telemetry,
            health=health,
            alerts=alerts,
            maintenance=maintenance,
            prediction=prediction,
            conversation=self._conversation_history(session_id),
            timestamp=utc_now().isoformat(),
        )

    def _build_vehicle(
        self,
        db: Session,
        vehicle_id: int,
    ) -> dict[str, Any] | None:
        """Return serialized vehicle context."""
        vehicle = vehicle_service.get_vehicle(db, vehicle_id)
        if vehicle is None:
            return None

        return VehicleResponse.model_validate(vehicle).model_dump(mode="json")

    def _get_latest_telemetry(
        self,
        db: Session,
        vehicle_id: int,
    ) -> dict[str, Any] | None:
        """Return serialized latest telemetry context."""
        telemetry = telemetry_service.get_latest(db, vehicle_id)
        if telemetry is None:
            return None

        return TelemetryResponse.model_validate(telemetry).model_dump(mode="json")

    def _build_health(
        self,
        telemetry: dict[str, Any] | None,
    ) -> dict[str, Any] | None:
        """Return serialized health context."""
        if telemetry is None:
            return None

        report = VehicleHealthService().calculate_health(_ObjectView(telemetry))
        return report.model_dump(mode="json")

    def _build_alerts(
        self,
        telemetry: dict[str, Any] | None,
        health: dict[str, Any] | None,
    ) -> dict[str, Any] | None:
        """Return serialized alert context."""
        if telemetry is None or health is None:
            return None

        health_report = HealthReport.model_validate(health)
        report = VehicleAlertService().generate_alerts(
            _ObjectView(telemetry),
            health_report,
        )
        return report.model_dump(mode="json")

    def _build_maintenance(
        self,
        telemetry: dict[str, Any] | None,
        health: dict[str, Any] | None,
        alerts: dict[str, Any] | None,
    ) -> dict[str, Any] | None:
        """Return serialized maintenance context."""
        if telemetry is None or health is None or alerts is None:
            return None

        health_report = HealthReport.model_validate(health)
        alert_report = AlertReport.model_validate(alerts)
        report = VehicleMaintenanceService().generate_maintenance_plan(
            _ObjectView(telemetry),
            health_report,
            alert_report,
        )
        return report.model_dump(mode="json")

    def _build_prediction(
        self,
        health: dict[str, Any] | None,
        alerts: dict[str, Any] | None,
        maintenance: dict[str, Any] | None,
    ) -> dict[str, Any] | None:
        """Return serialized prediction context."""
        if health is None or alerts is None or maintenance is None:
            return None

        predictor = self._predictor_factory.create("rule")
        result = predictor.predict(
            HealthReport.model_validate(health),
            AlertReport.model_validate(alerts),
            MaintenanceReport.model_validate(maintenance),
        )
        return result.model_dump(mode="json")

    def _conversation_history(
        self,
        session_id: str | None,
    ) -> list[dict[str, Any]]:
        """Return the latest conversation exchanges for a session."""
        if not session_id:
            return []

        return self._memory.get_history(session_id)[-10:]

    def _safe_call(self, func: Any, *args: Any) -> Any | None:
        """Run a context step and return None if unavailable."""
        try:
            return func(*args)
        except Exception:
            return None


class _ObjectView:
    """Expose dictionary values as attributes for service protocols."""

    def __init__(self, data: dict[str, Any]) -> None:
        """Initialize object view."""
        self._data = data

    def __getattr__(self, name: str) -> Any:
        """Return dictionary value by attribute name."""
        return self._data[name]
