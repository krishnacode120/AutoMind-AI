"""Metric utilities for model evaluation and comparison."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


@dataclass(frozen=True)
class ModelMetrics:
    """Container for common binary classification metrics."""

    accuracy: float
    precision: float
    recall: float
    f1_score: float
    roc_auc: float
    confusion_matrix: list[list[int]]

    def to_dict(self) -> dict[str, Any]:
        """Serialize model metrics for JSON output."""
        return {
            "accuracy": self.accuracy,
            "precision": self.precision,
            "recall": self.recall,
            "f1_score": self.f1_score,
            "roc_auc": self.roc_auc,
            "confusion_matrix": self.confusion_matrix,
        }


def calculate_classification_metrics(
    y_true: list[int],
    y_pred: list[int],
    y_prob: list[float],
) -> ModelMetrics:
    """Compute all required classification metrics safely."""
    confusion = confusion_matrix(y_true, y_pred, labels=[0, 1])
    roc_auc = _safe_roc_auc(y_true, y_prob)

    return ModelMetrics(
        accuracy=float(accuracy_score(y_true, y_pred)),
        precision=float(precision_score(y_true, y_pred, zero_division=0)),
        recall=float(recall_score(y_true, y_pred, zero_division=0)),
        f1_score=float(f1_score(y_true, y_pred, zero_division=0)),
        roc_auc=roc_auc,
        confusion_matrix=confusion.astype(int).tolist(),
    )


def _safe_roc_auc(y_true: list[int], y_prob: list[float]) -> float:
    """Return ROC-AUC, defaulting to 0.0 when undefined."""
    unique_labels = set(y_true)
    if len(unique_labels) < 2:
        return 0.0

    return float(roc_auc_score(y_true, y_prob))
