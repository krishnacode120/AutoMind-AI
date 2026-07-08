"""Request ID middleware and helpers."""

from contextvars import ContextVar
from time import perf_counter
from uuid import uuid4

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from app.config.logging import get_logger


REQUEST_ID_HEADER = "X-Request-ID"
_request_id_context: ContextVar[str | None] = ContextVar(
    "request_id",
    default=None,
)
logger = get_logger(__name__)


def current_request_id() -> str | None:
    """Return the request ID stored for the current context."""
    return _request_id_context.get()


def get_request_id(request: Request) -> str | None:
    """Return the request ID from the request state or context."""
    request_id = getattr(request.state, "request_id", None)
    return request_id or current_request_id()


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Attach a generated request ID to every request and response."""

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        request_id = str(uuid4())
        token = _request_id_context.set(request_id)
        request.state.request_id = request_id
        started_at = perf_counter()

        try:
            response = await call_next(request)
        except Exception:
            duration_ms = (perf_counter() - started_at) * 1000
            logger.exception(
                "request_id=%s method=%s path=%s status=500 duration_ms=%.2f",
                request_id,
                request.method,
                request.url.path,
                duration_ms,
            )
            raise
        finally:
            _request_id_context.reset(token)

        response.headers[REQUEST_ID_HEADER] = request_id
        duration_ms = (perf_counter() - started_at) * 1000
        logger.info(
            "request_id=%s method=%s path=%s status=%s duration_ms=%.2f",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )
        return response
