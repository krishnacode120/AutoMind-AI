# ML Architecture

## Overview

AutoMind AI uses an offline training pipeline and runtime inference integration:

- Dataset generation from simulator-based telemetry contexts
- Structured feature engineering and binary failure labeling
- Multi-model training and evaluation
- Best-model artifact selection and runtime loading

## Training Components

- `app/ml/dataset/`: dataset generation, feature engineering, labels, CSV export
- `app/ml/training/train.py`: split, preprocess, train, compare, persist
- `app/ml/training/evaluate.py`: model evaluation wrappers
- `app/ml/training/metrics.py`: metric computation helpers
- `app/ml/training/model_registry.py`: artifact persistence

## Model Artifacts

Saved under `backend/app/ml/models/`:

- `best_model.pkl`
- `model_metadata.json`
- `evaluation_report.json`

## Runtime Inference

- `PredictorFactory.create("ml")` uses ML-only behavior.
- `PredictorFactory.create("auto")` attempts ML and falls back to rule-based prediction if artifacts are unavailable.
- Feature ordering is derived from metadata (`feature_names`), ensuring consistency with training.

The current model input is limited to the shared report features in
`app/ml/features.py`. CSV strings and runtime values use the same normalization
and vectorization pipeline. Each candidate owns its preprocessing instance.
Candidates are selected on validation F1/ROC-AUC and the selected candidate is
evaluated on the untouched test split. Artifact caching uses location and file
revision so newly trained models can be loaded without a restart.

Dataset metadata (IDs, timestamps, profile/fault annotations) and prediction
outputs are excluded from training. Synthetic failure labels encode existing
service rules; this pipeline is a classification demonstration and does not
establish real-world predictive accuracy.

## Metrics

Evaluation tracks:

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC
- Confusion Matrix
