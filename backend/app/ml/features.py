"""Shared report features available during both training and inference."""

from typing import Any

from sklearn.base import BaseEstimator, TransformerMixin

NUMERIC_FEATURES = (
    "health_score",
    "alert_count",
    "maintenance_task_count",
    "estimated_remaining_km",
)
CATEGORICAL_FEATURES = (
    "health_status",
    "highest_alert_severity",
    "maintenance_priority",
)
MODEL_FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES


class RecordNormalizer(TransformerMixin, BaseEstimator):
    """Normalize CSV strings and runtime values into identical feature records."""

    def __init__(self, numeric_features, categorical_features) -> None:
        self.numeric_features = numeric_features
        self.categorical_features = categorical_features

    def fit(self, rows, y=None):
        """No learned state is needed for record normalization."""
        return self

    def transform(self, rows) -> list[dict[str, Any]]:
        """Convert numeric strings before vectorization; mark missing categories."""
        normalized = []
        for row in rows:
            result = {}
            for name in self.numeric_features:
                raw = row.get(name)
                result[name] = float("nan") if raw in (None, "") else float(raw)
            for name in self.categorical_features:
                raw = row.get(name)
                result[name] = "missing" if raw in (None, "") else str(raw)
            normalized.append(result)
        return normalized
