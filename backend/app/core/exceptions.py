"""Application exception types and handlers."""

from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.core.request_id import get_request_id
from app.core.responses import error


class GlobalException(Exception):
    """Base application exception for consistent error responses."""

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code


async def global_exception_handler(
    request: Request,
    exc: GlobalException,
) -> JSONResponse:
    """Convert application exceptions into JSON responses."""
    return JSONResponse(
        status_code=exc.status_code,
        content=error(
            message=exc.message,
            request_id=get_request_id(request),
        ),
    )


async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """Convert unexpected exceptions into consistent JSON responses."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error(
            message=str(exc) or "Internal server error",
            request_id=get_request_id(request),
        ),
    )
