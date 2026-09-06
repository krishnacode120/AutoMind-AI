# AutoMind backend

FastAPI, SQLAlchemy, Pydantic, deterministic simulation, and optional ML prediction.

Install `requirements-dev.txt` from the repository root for development, or
`requirements.txt` for runtime only. Then:

```sh
cd backend
python -m uvicorn app.main:app --reload
python -m pytest -q
python -m ruff check app tests
```

SQLite defaults to `automind.db` in the backend working directory.
Configuration uses environment variables and an optional `.env`.
Tables are created on startup; existing records are retained. API documentation
is at `/docs`; routes use `/api/v1`. Integration tests use an isolated database.

See the [root README](../README.md) for API routes, scenarios, training, and Docker.
