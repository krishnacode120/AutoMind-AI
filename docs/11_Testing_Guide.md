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

## CI Expectations

- All tests must pass in GitHub Actions (`backend.yml`).
- Lint checks are enforced in `quality.yml`.
- Frontend build validation runs in `frontend.yml`.
