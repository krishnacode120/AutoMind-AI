"""Reusable project and API version metadata."""

from app.config.settings import settings


API_VERSION = settings.API_VERSION
API_PREFIX = f"{settings.API_PREFIX}/{API_VERSION}"
PROJECT_VERSION = settings.APP_VERSION
PROJECT_NAME = settings.APP_NAME
AI_NAME = settings.AI_NAME
