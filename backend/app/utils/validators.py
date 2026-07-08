"""Reusable validation helpers."""


def is_non_empty_string(value: str | None) -> bool:
    """Return whether a value is a non-empty string."""
    return isinstance(value, str) and bool(value.strip())


def is_positive_int(value: int | None) -> bool:
    """Return whether a value is a positive integer."""
    return isinstance(value, int) and value > 0
