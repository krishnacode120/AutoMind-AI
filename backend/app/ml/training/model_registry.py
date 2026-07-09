"""Persistence helpers for trained model artifacts and reports."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import joblib

from app.ml.training.evaluate import EvaluationResult


@dataclass(frozen=True)
class SavedArtifacts:
    """Saved file locations for model outputs."""

    model_path: Path
    metadata_path: Path
    evaluation_report_path: Path


class ModelRegistry:
    """Store best model and training metadata on disk."""

    def __init__(self, base_dir: str | Path) -> None:
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def save_artifacts(
        self,
        best_model: Any,
        best_model_name: str,
        feature_names: list[str],
        dataset_size: int,
        best_metrics: dict[str, Any],
        evaluation_results: list[EvaluationResult],
    ) -> SavedArtifacts:
        """Save model binary plus metadata and evaluation report."""
        model_path = self.base_dir / "best_model.pkl"
        metadata_path = self.base_dir / "model_metadata.json"
        evaluation_report_path = self.base_dir / "evaluation_report.json"

        joblib.dump(best_model, model_path)

        metadata = {
            "model_name": best_model_name,
            "training_timestamp": datetime.now(timezone.utc).isoformat(),
            "dataset_size": dataset_size,
            "metrics": best_metrics,
            "feature_names": feature_names,
        }
        evaluation_report = {
            "models": [result.to_dict() for result in evaluation_results],
            "best_model": best_model_name,
        }

        self._write_json(metadata_path, metadata)
        self._write_json(evaluation_report_path, evaluation_report)

        return SavedArtifacts(
            model_path=model_path.resolve(),
            metadata_path=metadata_path.resolve(),
            evaluation_report_path=evaluation_report_path.resolve(),
        )

    @staticmethod
    def _write_json(path: Path, payload: dict[str, Any]) -> None:
        path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=True),
            encoding="utf-8",
        )
