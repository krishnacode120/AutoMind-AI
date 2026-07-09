"""Predictor factory."""

import logging

from app.prediction.base_predictor import VehiclePredictor
from app.prediction.ml_predictor import MLPredictor
from app.prediction.rule_predictor import RuleBasedPredictor

logger = logging.getLogger(__name__)


class PredictorFactory:
    """Create predictors by name."""

    def create(self, predictor_name: str) -> VehiclePredictor:
        """Create a predictor from a supported name."""
        normalized_name = predictor_name.strip().lower()

        if normalized_name == "rule":
            return RuleBasedPredictor()

        if normalized_name == "ml":
            return MLPredictor(fallback_to_rule=False)

        if normalized_name == "auto":
            logger.info("Creating auto predictor with ML fallback behavior")
            return MLPredictor(fallback_to_rule=True)

        raise ValueError(f"Unknown predictor: {predictor_name}")
