# Software Requirements Specification

## Functional Requirements

1. Operators can create, view, edit, and remove vehicles.
2. The system stores validated telemetry for an existing vehicle.
3. The system derives health, alerts, maintenance recommendations, and a
   prediction from the latest telemetry without persisting duplicate reports.
4. BON answers supported vehicle questions using current vehicle context and
   recent session history.
5. The dashboard displays vehicle, telemetry, health, alert, maintenance,
   prediction, and BON data.
6. The simulator and dataset generator remain usable independently of FastAPI.

## Non-Functional Requirements

- Python modules use type hints and are independently testable.
- The application uses SQLite locally and SQLAlchemy-compatible database access.
- API responses use a common success/error envelope where applicable.
- The frontend must build with TypeScript strict checking.
- The application supports local development through Uvicorn and Vite.

## Constraints

- Diagnostic rules are deterministic.
- ML training is offline; a missing model falls back to the rule predictor in
  automatic mode.
- The project does not collect external vehicle telemetry or user identity data.
