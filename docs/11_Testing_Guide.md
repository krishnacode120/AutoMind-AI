# Testing Guide

## Test Stack

- `pytest` for unit tests
- `pytest-asyncio` for async tests
- Service, schema, predictor, BON, and websocket focused coverage

## Run Tests

```bash
cd backend
pytest -q
```

## Test Modules

- `tests/test_vehicle.py`
- `tests/test_telemetry.py`
- `tests/test_health.py`
- `tests/test_alerts.py`
- `tests/test_maintenance.py`
- `tests/test_prediction.py`
- `tests/test_bon.py`
- `tests/test_websocket.py`
- `tests/test_workflows.py`: isolated database, API CRUD, simulated drive,
  diagnostics, BON context/session history, validation and telemetry events
- `tests/test_ml_pipeline.py`: 10,000-sample dataset acceptance, training,
  serialization, inference, artifact reload and fallback isolation

## Browser Workflows

Start the backend on port 8000 and Vite on 5173. From `frontend`, run
`npx playwright install chromium` once, then `npm run test:e2e`.
To use installed Edge on Windows, set `$env:PLAYWRIGHT_CHANNEL="msedge"`.
The test verifies CRUD, WebSocket events, all pages, BON conversation isolation,
reload and clearing, and mobile overflow. It cleans up its own vehicle records
and captures screenshots in `.runtime/`.

## CI Expectations

- All tests must pass in GitHub Actions (`backend.yml`).
- Lint checks are enforced in `quality.yml`.
- Frontend build validation runs in `frontend.yml`.
