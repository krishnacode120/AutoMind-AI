"""Logging configuration for AutoMind AI."""

import logging


LOGGER_NAME = "automind"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def setup_logging() -> None:
    """Configure console logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FORMAT,
    )


def get_logger(module_name: str | None = None) -> logging.Logger:
    """Return a project logger for the given module."""
    if module_name:
        return logging.getLogger(f"{LOGGER_NAME}.{module_name}")

    return logging.getLogger(LOGGER_NAME)
