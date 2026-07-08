"""FastAPI application factory."""

from fastapi import FastAPI

from app.api.router import router
from app.config.logging import setup_logging
from app.config.settings import settings
from app.core.custom_openapi import configure_openapi
from app.core.exceptions import (
    GlobalException,
    global_exception_handler,
    unhandled_exception_handler,
)
from app.core.lifespan import lifespan
from app.core.middleware import configure_middleware


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    setup_logging()

    application = FastAPI(
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION,
        docs_url=settings.DOCS_URL,
        redoc_url=settings.REDOC_URL,
        openapi_url=settings.OPENAPI_URL,
        lifespan=lifespan,
    )

    configure_middleware(application)
    application.include_router(router)
    application.add_exception_handler(GlobalException, global_exception_handler)
    application.add_exception_handler(Exception, unhandled_exception_handler)
    configure_openapi(application)

    return application


app = create_app()
