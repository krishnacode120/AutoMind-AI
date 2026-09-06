"""Intent parsing module."""

import re

from app.ai.types import IntentResult

INTENT_KEYWORDS: list[tuple[str, list[str]]] = [
    ("health", ["health", "status", "condition", "how is my car", "how is my vehicle"]),
    ("alerts", ["alert", "warning", "critical", "issue", "fault", "problem"]),
    (
        "maintenance",
        ["maintenance", "service", "repair", "task", "oil", "filter", "brake"],
    ),
    (
        "prediction",
        ["predict", "prediction", "failure", "remaining", "life", "forecast"],
    ),
    (
        "telemetry",
        [
            "telemetry",
            "speed",
            "rpm",
            "temperature",
            "fuel",
            "sensor",
            "odometer",
            "battery",
            "coolant",
            "tire",
        ],
    ),
    ("vehicle", ["vehicle", "car", "model", "make", "year", "vin", "specs"]),
]


class IntentParser:
    """Parses user messages to identify the core intent."""

    def __init__(self) -> None:
        """Initialize the intent parser."""
        self.supported_intents = [
            "health",
            "alerts",
            "maintenance",
            "prediction",
            "telemetry",
            "vehicle",
            "general",
            "unknown",
        ]

    def parse(self, message: str) -> IntentResult:
        """Analyze a message and return the recognized intent."""
        msg_lower = message.lower().strip()

        matched_intent = "unknown"
        for intent, keywords in INTENT_KEYWORDS:
            if any(
                re.search(r"\b" + re.escape(kw) + r"s?\b", msg_lower) for kw in keywords
            ):
                matched_intent = intent
                break

        if matched_intent == "unknown":
            greetings = ["hello", "hi", "hey", "bon", "help", "who are you"]
            if any(
                re.search(r"\b" + re.escape(greeting) + r"\b", msg_lower)
                for greeting in greetings
            ):
                matched_intent = "general"

        confidence = 0.95 if matched_intent != "unknown" else 0.50

        return IntentResult(
            intent=matched_intent,
            confidence=confidence,
            entities={},
        )
