"""Response formatter module."""

from typing import Any

from app.ai.types import BONResponse
from app.utils.time_utils import utc_now_iso


class ResponseFormatter:
    """Formats engine outputs into the standardized BONResponse structure."""

    def format(self, answer: str, intent: str, confidence: float, context: dict[str, Any]) -> BONResponse:
        """Wrap answer and metadata into a formal BONResponse."""
        return BONResponse(
            answer=answer,
            intent=intent,
            confidence=confidence,
            context_used=context,
            timestamp=utc_now_iso()
        )
