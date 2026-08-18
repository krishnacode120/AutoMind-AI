# System Architecture

## Layers

```text
React dashboard
        |
FastAPI REST and WebSocket routes
        |
Vehicle, telemetry, and diagnostic services
        |
SQLite persistence     BON context and knowledge engine
        |
Simulator -> dataset generator -> offline ML training
```

## Backend Modules

- `app/api/`: REST and WebSocket route registration.
- `app/services/`: vehicle persistence and deterministic report calculations.
- `app/simulator/`: state machine, physics, sensors, persistence adapter, and
  runner.
- `app/prediction/`: predictor abstraction, rule predictor, and optional
  trained-model predictor.
- `app/ai/`: BON intent parsing, context aggregation, deterministic knowledge
  responses, and conversation memory.
- `app/ml/`: scenario-driven dataset generation and offline training utilities.

Derived reports are calculated from latest telemetry on demand. This prevents
stale copies and keeps the telemetry record as the source of operational state.
