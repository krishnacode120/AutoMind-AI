# AutoMind AI Backend

## Purpose

The backend will provide the server-side foundation for AutoMind AI. It is planned to use Python and FastAPI for future application logic, configuration, persistence, assistant integration, simulation support, and service modules.

This backend currently contains structure and configuration scaffolding only.

## Folder Structure

- `app/api/` - Future API route modules
- `app/ai/` - Future BON assistant integration modules
- `app/config/` - Application settings, logging, and constants
- `app/core/` - Future core backend utilities and application wiring
- `app/database/` - Future SQLite database configuration and access
- `app/ml/` - Future backend machine learning integration modules
- `app/models/` - Future database models
- `app/schemas/` - Future request and response schemas
- `app/services/` - Future service-layer modules
- `app/simulator/` - Future vehicle simulation modules
- `app/static/` - Future static backend assets
- `app/templates/` - Future backend templates
- `app/utils/` - Future general-purpose backend helpers

## Install Dependencies

From the repository root, install Python dependencies later with:

```bash
pip install -r requirements.txt
```

## Run Later

A FastAPI application entry point has not been created yet. Once the backend application is implemented, it can be run with an appropriate ASGI command such as:

```bash
uvicorn app.main:app --reload
```
