# Roadmap

## Current Capability

- Vehicle and telemetry APIs with SQLite persistence
- Deterministic health, alerts, maintenance, and prediction reports
- Simulator, scenario generation, fault injection, CSV export, and ML training
- BON contextual chat and telemetry WebSocket support
- React operational dashboard and CI workflows

## Next Priorities

1. Add authenticated multi-user access and authorization boundaries.
2. Add database migrations and production PostgreSQL deployment profiles.
3. Add integration tests for API, WebSocket, and dashboard workflows.
4. Add model-version governance, dataset provenance, and ML inference review.
5. Add opt-in external notification channels.

## Design Principle

Future work should extend the existing layers rather than move deterministic
rules into routes, components, or persistence models.
