"""Tests for prediction components and factory fallback flow."""

from app.prediction.predictor_factory import PredictorFactory
from app.prediction.rule_predictor import RuleBasedPredictor


def test_rule_predictor_returns_valid_prediction(
    health_report,
    alert_report,
    maintenance_report,
) -> None:
    """Rule predictor should return a valid response model."""
    result = RuleBasedPredictor().predict(
        health_report,
        alert_report,
        maintenance_report,
    )
    assert result.prediction_type == "rule"
    assert 0.0 <= result.confidence <= 1.0
    assert isinstance(result.predicted_failure, str)


def test_auto_predictor_falls_back_when_ml_artifacts_missing(
    health_report,
    alert_report,
    maintenance_report,
) -> None:
    """Auto predictor should fallback to rule mode without ML artifacts."""
    predictor = PredictorFactory().create("auto")
    result = predictor.predict(
        health_report,
        alert_report,
        maintenance_report,
    )
    assert result.prediction_type == "rule-fallback"
    assert result.recommended_action != ""
