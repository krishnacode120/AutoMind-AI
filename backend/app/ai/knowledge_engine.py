"""Knowledge engine module."""

from collections.abc import Mapping
from typing import Any


ContextLike = Mapping[str, Any]


class KnowledgeEngine:
    """Generates deterministic vehicle-assistant answers from context."""

    def answer(self, intent: str, context: ContextLike) -> str:
        """Return a structured deterministic answer for an intent."""
        handlers = {
            "health": self._health_answer,
            "telemetry": self._telemetry_answer,
            "alerts": self._alerts_answer,
            "maintenance": self._maintenance_answer,
            "prediction": self._prediction_answer,
            "vehicle": self._vehicle_answer,
            "general": self._general_answer,
            "unknown": self._unknown_answer,
        }
        handler = handlers.get(intent, self._unknown_answer)
        return handler(context)

    def _health_answer(self, context: ContextLike) -> str:
        """Return a health-focused answer."""
        health = self._section(context, "health")
        alerts = self._section(context, "alerts")
        if health is None:
            return self._unavailable("health information")

        recommendation = self._first_item(
            health.get("recommendations"),
            "Continue regular monitoring.",
        )
        alert_count = self._value(alerts, "alert_count", "unavailable")
        return (
            "Vehicle health summary: "
            f"health score is {health.get('health_score')} and status is "
            f"{health.get('health_status')}. "
            f"Active alert count: {alert_count}. "
            f"Recommendation: {recommendation}"
        )

    def _telemetry_answer(self, context: ContextLike) -> str:
        """Return a telemetry-focused answer."""
        telemetry = self._section(context, "telemetry")
        if telemetry is None:
            return self._unavailable("latest telemetry")

        return (
            "Latest telemetry summary: "
            f"speed {telemetry.get('speed')} km/h, "
            f"RPM {telemetry.get('rpm')}, "
            f"gear {telemetry.get('gear')}, "
            f"fuel {telemetry.get('fuel_level')}%, "
            f"engine temperature {telemetry.get('engine_temperature')}C."
        )

    def _alerts_answer(self, context: ContextLike) -> str:
        """Return an alerts-focused answer."""
        alerts = self._section(context, "alerts")
        if alerts is None:
            return self._unavailable("alert information")

        top_alerts = alerts.get("alerts", [])[:3]
        alert_titles = [
            alert.get("title", "Untitled alert")
            for alert in top_alerts
        ]
        summary = "; ".join(alert_titles) if alert_titles else "No active alerts."
        return (
            "Alert summary: "
            f"highest severity is {alerts.get('highest_severity') or 'None'}, "
            f"alert count is {alerts.get('alert_count')}. "
            f"Top alerts: {summary}"
        )

    def _maintenance_answer(self, context: ContextLike) -> str:
        """Return a maintenance-focused answer."""
        maintenance = self._section(context, "maintenance")
        if maintenance is None:
            return self._unavailable("maintenance information")

        tasks = maintenance.get("tasks", [])
        top_task = tasks[0] if tasks else None
        top_task_summary = (
            f"{top_task.get('title')} - {top_task.get('recommended_action')}"
            if top_task
            else "No maintenance task is currently required."
        )
        return (
            "Maintenance summary: "
            f"overall priority is {maintenance.get('overall_priority')}, "
            f"task count is {maintenance.get('task_count')}. "
            f"Top task: {top_task_summary}"
        )

    def _prediction_answer(self, context: ContextLike) -> str:
        """Return a prediction-focused answer."""
        prediction = self._section(context, "prediction")
        if prediction is None:
            return self._unavailable("prediction information")

        confidence = prediction.get("confidence")
        confidence_text = (
            f"{round(confidence * 100)}%"
            if isinstance(confidence, int | float)
            else "unavailable"
        )
        return (
            "Prediction summary: "
            f"predicted failure is {prediction.get('predicted_failure')}, "
            f"confidence is {confidence_text}. "
            f"Recommended action: {prediction.get('recommended_action')}."
        )

    def _vehicle_answer(self, context: ContextLike) -> str:
        """Return a vehicle-focused answer."""
        vehicle = self._section(context, "vehicle")
        if vehicle is None:
            return self._unavailable("vehicle information")

        return (
            "Vehicle summary: "
            f"{vehicle.get('manufacturer')} {vehicle.get('model')} "
            f"({vehicle.get('year')}). "
            f"Fuel type: {vehicle.get('fuel_type')}. "
            f"Transmission: {vehicle.get('transmission')}."
        )

    def _general_answer(self, context: ContextLike) -> str:
        """Return an overall vehicle-assistant answer."""
        health = self._section(context, "health")
        alerts = self._section(context, "alerts")
        maintenance = self._section(context, "maintenance")
        prediction = self._section(context, "prediction")

        unavailable = self._missing_sections(
            {
                "health": health,
                "alerts": alerts,
                "maintenance": maintenance,
                "prediction": prediction,
            }
        )
        if unavailable:
            return (
                "AutoMind AI overview is partially unavailable. "
                f"Missing: {', '.join(unavailable)}."
            )

        return (
            "AutoMind AI overview: "
            f"health is {health.get('health_status')} "
            f"with score {health.get('health_score')}. "
            f"There are {alerts.get('alert_count')} active alerts. "
            f"Maintenance priority is {maintenance.get('overall_priority')}. "
            f"Prediction: {prediction.get('predicted_failure')}. "
            f"Recommended action: {prediction.get('recommended_action')}."
        )

    def _unknown_answer(self, context: ContextLike) -> str:
        """Return a fallback answer."""
        vehicle = self._section(context, "vehicle")
        if vehicle is None:
            return (
                "I can help with vehicle health, telemetry, alerts, "
                "maintenance, and predictions once vehicle information is available."
            )

        return (
            "I can help with this vehicle's health, telemetry, alerts, "
            "maintenance, and predictions. Please ask about one of those areas."
        )

    def _section(
        self,
        context: ContextLike,
        key: str,
    ) -> dict[str, Any] | None:
        """Return a dictionary context section when available."""
        value = context.get(key)
        if isinstance(value, dict):
            return value

        return None

    def _value(
        self,
        section: dict[str, Any] | None,
        key: str,
        default: Any,
    ) -> Any:
        """Return a section value or default."""
        if section is None:
            return default

        return section.get(key, default)

    def _first_item(self, values: Any, default: str) -> str:
        """Return the first item from a list-like value."""
        if isinstance(values, list) and values:
            return str(values[0])

        return default

    def _unavailable(self, label: str) -> str:
        """Return a clear unavailable-information response."""
        return f"I cannot summarize {label} because it is currently unavailable."

    def _missing_sections(
        self,
        sections: dict[str, dict[str, Any] | None],
    ) -> list[str]:
        """Return names for unavailable sections."""
        return [name for name, value in sections.items() if value is None]
