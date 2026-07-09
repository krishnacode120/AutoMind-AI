"""Model evaluation helpers for AutoMind ML training."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.ml.training.metrics import ModelMetrics, calculate_classification_metrics


@dataclass(frozen=True)
class EvaluationResult:
    """Evaluated model metrics with metadata used by reports."""

    model_name: str
    metrics: ModelMetrics

    def to_dict(self) -> dict[str, Any]:
        """Serialize evaluation result for reporting."""
        return {
            "model_name": self.model_name,
            "metrics": self.metrics.to_dict(),
        }


def evaluate_model(
    model_name: str,
    y_true: list[int],
    y_pred: list[int],
    y_prob: list[float],
) -> EvaluationResult:
    """Evaluate one model against true labels."""
    return EvaluationResult(
        model_name=model_name,
        metrics=calculate_classification_metrics(
            y_true=y_true,
            y_pred=y_pred,
            y_prob=y_prob,
        ),
    )
