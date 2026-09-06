"""Application exception types and handlers."""

import logging

from app.core.request_id import get_request_id
from app.core.responses import error
from fastapi import Request, status
from fastapi.responses import JSONResponse


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
    logging.getLogger(__name__).error(
        "Unhandled request error [%s]",
        get_request_id(request),
        exc_info=(type(exc), exc, exc.__traceback__),
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error(
            message="Internal server error",
            request_id=get_request_id(request),
        ),
    )
