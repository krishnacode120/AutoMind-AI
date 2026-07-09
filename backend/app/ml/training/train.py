"""Train and evaluate classification models for failure prediction."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from app.ml.training.evaluate import EvaluationResult, evaluate_model
from app.ml.training.model_registry import ModelRegistry

TARGET_COLUMN = "failure"
DEFAULT_TEST_SIZE = 0.2
DEFAULT_VALIDATION_SIZE = 0.2
DEFAULT_RANDOM_STATE = 42


@dataclass(frozen=True)
class DatasetBundle:
    """Prepared dataset split and schema metadata."""

    x_train: list[dict[str, Any]]
    x_validation: list[dict[str, Any]]
    x_test: list[dict[str, Any]]
    y_train: list[int]
    y_validation: list[int]
    y_test: list[int]
    feature_names: list[str]
    dataset_size: int


def main() -> None:
    """CLI entrypoint for model training pipeline."""
    args = parse_args()
    dataset_path = Path(args.dataset).resolve()
    models_dir = Path(args.models_dir).resolve()

    bundle = load_and_split_dataset(
        dataset_path=dataset_path,
        test_size=args.test_size,
        validation_size=args.validation_size,
        random_state=args.random_state,
    )

    trained_models = train_models(
        x_train=bundle.x_train,
        y_train=bundle.y_train,
        numeric_features=_numeric_feature_names(bundle.x_train),
        categorical_features=_categorical_feature_names(bundle.x_train),
        random_state=args.random_state,
    )

    evaluation_results = evaluate_models(
        trained_models=trained_models,
        x_test=bundle.x_test,
        y_test=bundle.y_test,
    )
    print_comparison_table(evaluation_results)

    best_result = select_best_model(evaluation_results)
    best_model = trained_models[best_result.model_name]

    registry = ModelRegistry(models_dir)
    artifacts = registry.save_artifacts(
        best_model=best_model,
        best_model_name=best_result.model_name,
        feature_names=bundle.feature_names,
        dataset_size=bundle.dataset_size,
        best_metrics=best_result.metrics.to_dict(),
        evaluation_results=evaluation_results,
    )

    print(f"Best model: {best_result.model_name}")
    print(f"Saved model: {artifacts.model_path}")
    print(f"Saved metadata: {artifacts.metadata_path}")
    print(f"Saved report: {artifacts.evaluation_report_path}")


def parse_args() -> argparse.Namespace:
    """Parse training CLI arguments."""
    parser = argparse.ArgumentParser(description="AutoMind ML training pipeline")
    parser.add_argument(
        "--dataset",
        type=str,
        required=True,
        help="Path to generated training CSV dataset.",
    )
    parser.add_argument(
        "--models-dir",
        type=str,
        default=str(Path(__file__).resolve().parents[1] / "models"),
        help="Directory to save model artifacts.",
    )
    parser.add_argument(
        "--test-size",
        type=float,
        default=DEFAULT_TEST_SIZE,
        help="Fraction reserved for test split.",
    )
    parser.add_argument(
        "--validation-size",
        type=float,
        default=DEFAULT_VALIDATION_SIZE,
        help="Fraction of remaining train split for validation.",
    )
    parser.add_argument(
        "--random-state",
        type=int,
        default=DEFAULT_RANDOM_STATE,
        help="Random seed for reproducibility.",
    )
    return parser.parse_args()


def load_and_split_dataset(
    dataset_path: Path,
    test_size: float,
    validation_size: float,
    random_state: int,
) -> DatasetBundle:
    """Load CSV, handle target extraction, and split data."""
    rows = _read_csv_rows(dataset_path)
    if not rows:
        raise ValueError(f"Dataset is empty: {dataset_path}")
    if TARGET_COLUMN not in rows[0]:
        raise ValueError(f"Required target column '{TARGET_COLUMN}' missing")

    feature_names = [name for name in rows[0].keys() if name != TARGET_COLUMN]
    x_data = [{name: row.get(name) for name in feature_names} for row in rows]
    y_data = [int(float(row[TARGET_COLUMN])) for row in rows]

    x_train_full, x_test, y_train_full, y_test = train_test_split(
        x_data,
        y_data,
        test_size=test_size,
        random_state=random_state,
        stratify=y_data if len(set(y_data)) > 1 else None,
    )

    x_train, x_validation, y_train, y_validation = train_test_split(
        x_train_full,
        y_train_full,
        test_size=validation_size,
        random_state=random_state,
        stratify=y_train_full if len(set(y_train_full)) > 1 else None,
    )

    return DatasetBundle(
        x_train=x_train,
        x_validation=x_validation,
        x_test=x_test,
        y_train=y_train,
        y_validation=y_validation,
        y_test=y_test,
        feature_names=feature_names,
        dataset_size=len(rows),
    )


def train_models(
    x_train: list[dict[str, Any]],
    y_train: list[int],
    numeric_features: list[str],
    categorical_features: list[str],
    random_state: int,
) -> dict[str, Pipeline]:
    """Train all required classifier families and return fitted pipelines."""
    preprocess = build_preprocessor(
        numeric_features=numeric_features,
        categorical_features=categorical_features,
    )

    model_factories: dict[str, Any] = {
        "Logistic Regression": LogisticRegression(
            max_iter=1000,
            random_state=random_state,
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=300,
            random_state=random_state,
        ),
        "Gradient Boosting Classifier": GradientBoostingClassifier(
            random_state=random_state,
        ),
    }

    trained_models: dict[str, Pipeline] = {}
    for model_name, estimator in model_factories.items():
        pipeline = Pipeline(
            steps=[
                ("preprocessor", preprocess),
                ("classifier", estimator),
            ]
        )
        pipeline.fit(x_train, y_train)
        trained_models[model_name] = pipeline

    return trained_models


def build_preprocessor(
    numeric_features: list[str],
    categorical_features: list[str],
) -> ColumnTransformer:
    """Build reusable preprocessing for mixed feature types."""
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
        ]
    )
    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ],
    )


def evaluate_models(
    trained_models: dict[str, Pipeline],
    x_test: list[dict[str, Any]],
    y_test: list[int],
) -> list[EvaluationResult]:
    """Evaluate all trained models on the holdout test set."""
    results: list[EvaluationResult] = []

    for model_name, model in trained_models.items():
        y_pred = model.predict(x_test).tolist()
        y_prob = model.predict_proba(x_test)[:, 1].tolist()
        results.append(
            evaluate_model(
                model_name=model_name,
                y_true=y_test,
                y_pred=y_pred,
                y_prob=y_prob,
            )
        )

    return results


def select_best_model(results: list[EvaluationResult]) -> EvaluationResult:
    """Choose best model using F1 as primary and ROC-AUC as tiebreaker."""
    if not results:
        raise ValueError("No model evaluation results to compare")

    return max(
        results,
        key=lambda item: (item.metrics.f1_score, item.metrics.roc_auc),
    )


def print_comparison_table(results: list[EvaluationResult]) -> None:
    """Print a compact metrics table for all models."""
    headers = (
        "Model",
        "Accuracy",
        "Precision",
        "Recall",
        "F1",
        "ROC-AUC",
    )
    print(
        f"{headers[0]:<30} {headers[1]:>9} {headers[2]:>9} "
        f"{headers[3]:>9} {headers[4]:>9} {headers[5]:>9}"
    )
    print("-" * 84)
    for result in results:
        metrics = result.metrics
        print(
            f"{result.model_name:<30} {metrics.accuracy:>9.4f} "
            f"{metrics.precision:>9.4f} {metrics.recall:>9.4f} "
            f"{metrics.f1_score:>9.4f} {metrics.roc_auc:>9.4f}"
        )


def _read_csv_rows(dataset_path: Path) -> list[dict[str, str]]:
    """Read CSV rows as dictionaries."""
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset CSV not found: {dataset_path}")

    with dataset_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return [dict(row) for row in reader]


def _numeric_feature_names(data: list[dict[str, Any]]) -> list[str]:
    """Infer numeric feature names from sampled data."""
    if not data:
        return []

    numeric_features: list[str] = []
    sample = data[0]
    for key in sample.keys():
        if _is_numeric_column(key, data):
            numeric_features.append(key)
    return numeric_features


def _categorical_feature_names(data: list[dict[str, Any]]) -> list[str]:
    """Infer categorical feature names from sampled data."""
    numeric_features = set(_numeric_feature_names(data))
    return [name for name in data[0].keys() if name not in numeric_features]


def _is_numeric_column(column_name: str, data: list[dict[str, Any]]) -> bool:
    """Determine whether column values are consistently numeric."""
    for row in data:
        raw_value = row.get(column_name)
        if raw_value in (None, ""):
            continue
        try:
            float(str(raw_value))
        except ValueError:
            return False
    return True


if __name__ == "__main__":
    main()
