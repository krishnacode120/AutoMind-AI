"""Custom OpenAPI schema configuration."""

from typing import Any

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.config.settings import settings


def build_openapi_schema(app: FastAPI) -> dict[str, Any]:
    """Build the OpenAPI schema for the application."""
    if app.openapi_schema:
        return app.openapi_schema

    app.openapi_schema = get_openapi(
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION,
        routes=app.routes,
        contact={
            "name": settings.CONTACT_NAME,
            "url": settings.CONTACT_URL,
        },
        license_info={
            "name": settings.LICENSE_NAME,
            "url": settings.LICENSE_URL,
        },
    )
    return app.openapi_schema


def configure_openapi(app: FastAPI) -> None:
    """Attach the custom OpenAPI builder to the application."""
    app.openapi = lambda: build_openapi_schema(app)
