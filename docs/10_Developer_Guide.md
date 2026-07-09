# Developer Guide

## Local Setup

1. Install Python dependencies:
   `pip install -r requirements.txt`
2. Install frontend dependencies:
   `cd frontend && npm ci`
3. Copy env files:
   - `backend/.env.example` -> `backend/.env`
   - `frontend/.env.example` -> `frontend/.env`

## Development Commands

- Backend: `cd backend && uvicorn app.main:app --reload`
- Frontend: `cd frontend && npm run dev`
- Tests: `cd backend && pytest`
- Lint: `ruff check backend/app backend/tests`

## Code Organization

- `app/services/`: domain calculations and business services
- `app/api/routes/`: REST and WebSocket handlers
- `app/prediction/`: predictor abstraction and implementations
- `app/ai/`: BON assistant orchestration
- `app/simulator/`: simulation engines and state transitions
- `app/ml/`: dataset, training, and model runtime integration

## Contribution Workflow

1. Branch from `main`.
2. Keep commits scoped to one logical area.
3. Add or update tests with behavior changes.
4. Ensure CI checks pass before PR.
