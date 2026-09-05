"""Verify dataset generation, model fitting, serialization and live inference."""

from app.ml.dataset.dataset_generator import DatasetGenerator
from app.ml.features import MODEL_FEATURES, NUMERIC_FEATURES, CATEGORICAL_FEATURES
from app.ml.training.train import (
    load_and_split_dataset,
    train_models,
    evaluate_models,
    select_best_model,
)
from app.ml.training.model_registry import ModelRegistry
from app.prediction.ml_predictor import MLPredictor


def test_dataset_training_and_inference(
    tmp_path, health_report, alert_report, maintenance_report
):
    path = tmp_path / "dataset.csv"
    dataset = DatasetGenerator(random_seed=42).generate(1000, path)
    assert 0.2 <= dataset.statistics["failure_rate"] <= 0.4
    bundle = load_and_split_dataset(path, 0.2, 0.2, 42)
    assert set(bundle.feature_names) == set(MODEL_FEATURES)
    assert "injected_faults" not in bundle.feature_names
    models = train_models(
        bundle.x_train,
        bundle.y_train,
        list(NUMERIC_FEATURES),
        list(CATEGORICAL_FEATURES),
        42,
    )
    results = evaluate_models(models, bundle.x_validation, bundle.y_validation)
    best = select_best_model(results)
    directory = tmp_path / "models"
    predictor = MLPredictor(models_dir=directory, fallback_to_rule=True)
    assert (
        predictor.predict(
            health_report, alert_report, maintenance_report
        ).prediction_type
        == "rule-fallback"
    )
    ModelRegistry(directory).save_artifacts(
        models[best.model_name],
        best.model_name,
        bundle.feature_names,
        bundle.dataset_size,
        best.metrics.to_dict(),
        results,
    )
    report = predictor.predict(health_report, alert_report, maintenance_report)
    assert report.prediction_type == "ml"
    assert 0 <= report.confidence <= 1
    other = MLPredictor(models_dir=tmp_path / "missing", fallback_to_rule=True)
    assert (
        other.predict(health_report, alert_report, maintenance_report).prediction_type
        == "rule-fallback"
    )


def test_dataset_acceptance_10000(tmp_path):
    result = DatasetGenerator(random_seed=0).generate(10000, tmp_path / "large.csv")
    assert len(result.rows) == result.statistics["sample_count"] == 10000
    assert 0.2 <= result.statistics["failure_rate"] <= 0.4
    assert result.csv_path.stat().st_size > 0
