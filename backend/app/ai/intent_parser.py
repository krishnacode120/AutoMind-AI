"""Intent parsing module."""

from app.ai.types import IntentResult


class IntentParser:
    """Parses user messages to identify the core intent."""

    def __init__(self) -> None:
        """Initialize the intent parser."""
        self.supported_intents = {
            "health",
            "alerts",
            "maintenance",
            "prediction",
            "telemetry",
            "vehicle",
            "general",
            "unknown",
        }

    def parse(self, message: str) -> IntentResult:
        """Analyze a message and return the recognized intent."""
        msg_lower = message.lower()
        
        # Deterministic placeholder logic for current milestone
        matched_intent = "unknown"
        for intent in self.supported_intents:
            if intent != "unknown" and intent != "general" and intent in msg_lower:
                matched_intent = intent
                break
        
        if matched_intent == "unknown":
            if "hello" in msg_lower or "hi" in msg_lower:
                matched_intent = "general"

        return IntentResult(
            intent=matched_intent,
            confidence=0.85,
            entities={}
        )
