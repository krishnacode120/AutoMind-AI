"""General reusable helper functions."""

from typing import Any

from app.utils.time_utils import utc_now_iso


def timestamp() -> str:
    """Return the current UTC timestamp."""
    return utc_now_iso()


def success_response(
    message: str = "Success",
    data: Any | None = None,
) -> dict[str, Any]:
    """Return a consistent success response payload."""
    response: dict[str, Any] = {
        "success": True,
        "message": message,
        "timestamp": timestamp(),
    }

    if data is not None:
        response["data"] = data

    return response


def error_response(
    message: str = "Error",
    details: Any | None = None,
    request_id: str | None = None,
) -> dict[str, Any]:
    """Return a consistent error response payload."""
    response: dict[str, Any] = {
        "success": False,
        "message": message,
        "request_id": request_id,
        "timestamp": timestamp(),
    }

    if details is not None:
        response["details"] = details

    return response
