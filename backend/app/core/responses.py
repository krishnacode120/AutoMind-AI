"""Reusable response helpers."""

from typing import Any

from app.utils.helpers import error_response, success_response


def success(message: str = "Success", data: Any | None = None) -> dict[str, Any]:
    """Return a consistent success response."""
    return success_response(message=message, data=data)


def error(
    message: str = "Error",
    details: Any | None = None,
    request_id: str | None = None,
) -> dict[str, Any]:
    """Return a consistent error response."""
    return error_response(message=message, details=details, request_id=request_id)
