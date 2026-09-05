# AutoMind AI

```text
AutoMind AI — Intelligent Vehicle Monitoring, Prediction, and Assistant Platform
```

AutoMind AI is an end-to-end vehicle intelligence platform that combines telemetry simulation, deterministic diagnostics, machine-learning prediction, and conversational assistance.

## BON AI Overview

BON is the in-app assistant for vehicle context. BON parses intent, builds context from vehicle telemetry and system services, and returns guided responses for operators.

## Features

- FastAPI backend with modular service architecture
- Real-time vehicle telemetry simulation and persistence
- Health scoring, alert generation, and maintenance planning
- Rule-based and ML-powered prediction framework
- BON assistant endpoint for contextual chat
- React + Vite dashboard for live vehicle monitoring
- WebSocket telemetry streaming

## System Architecture

- **Simulator Layer**: Generates vehicle state and telemetry snapshots.
- **Service Layer**: Computes health, alerts, and maintenance outputs.
- **Prediction Layer**: Supports rule and ML predictors with factory selection.
- **AI Layer**: BON orchestrates intent parsing, context building, and response formatting.
- **API Layer**: REST and WebSocket interfaces for frontend and integrations.
- **Frontend Layer**: Dashboard and BON chat experiences.

## Folder Structure

```text
AutoMind-AI/
├── backend/
│   ├── app/
│   │   ├── ai/
│   │   ├── api/
│   │   ├── core/
│   │   ├── database/
│   │   ├── ml/
│   │   ├── models/
│   │   ├── prediction/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── simulator/
│   │   └── websocket/
│   ├── tests/
│   └── Dockerfile
├── frontend/
│   ├── src/
│   └── Dockerfile
├── docs/
├── .github/workflows/
├── docker-compose.yml
└── requirements.txt
```

## Technology Stack

- **Backend**: Python, FastAPI, SQLAlchemy, Pydantic
- **ML**: scikit-learn, joblib
- **Frontend**: React, TypeScript, Vite
- **Database**: SQLite
- **Tooling**: pytest, Ruff, GitHub Actions, Docker Compose

## Installation Guide

1. Clone the repository.
2. Create environment files:
   - `cp backend/.env.example backend/.env`
   - `cp frontend/.env.example frontend/.env`
3. Install dependencies:
   - `pip install -r requirements.txt`
   - `cd frontend && npm ci`

## Backend Setup

```bash
cd backend
uvicorn app.main:app --reload
```

Backend default URL: [http://localhost:8000](http://localhost:8000)

## Frontend Setup

```bash
cd frontend
npm run dev
```

Frontend default URL: [http://localhost:5173](http://localhost:5173)

## Running the Simulator

Create a vehicle on the Vehicles page, select it in the top bar, and click
**Simulate drive** on Dashboard or Telemetry. Each click records 60 readings
through the existing physics and sensor engines. This is an explicit sample
drive, not an automatically running simulator. The dashboard receives updates
over WebSocket and also refreshes periodically.

The equivalent API call is `POST /api/v1/vehicles/{id}/simulation?samples=60`
(1-300 samples per request). Deleting a vehicle also deletes its telemetry.

## Generating Datasets

```bash
cd backend
python -m app.ml.dataset --size 10000 --seed 0 --output ../datasets/telemetry.csv
```

The CSV and adjacent `.statistics.json` report contain generated data only;
this command does not change the application database.

## Running ML Training

```bash
cd backend
python -m app.ml.training.train --dataset "PATH_TO_DATASET.csv"
```

Generated artifacts are saved in `backend/app/ml/models/`.

Training uses report fields available at inference time and excludes record IDs,
timestamps, injected-fault metadata, and prediction outputs. Validation data
selects the model; a separate test set measures the selected model. These are
synthetic, rule-defined risk labels, not evidence of real-world failure prediction.
Retrain older artifacts with the current pipeline before using ML inference.

## Running the Dashboard

Run backend and frontend together, then open the frontend URL to access dashboard pages for vehicles, telemetry, health, maintenance, prediction, and BON.

## BON Chat Usage

- Endpoint: `POST /api/v1/bon/chat`
- Input: vehicle ID, message, session ID
- Output: answer, intent, confidence, context used, timestamp

BON works on its dedicated page and on Dashboard. Browser conversations are
isolated per vehicle and survive refreshes. Clear conversation removes the
server history too. Server-side history is in memory and resets on restart.

## Verification

```bash
cd backend
python -m pytest -q
ruff check app tests
cd ../frontend
npm run build
npx playwright install chromium
npm run test:e2e
```

The browser test expects the backend and frontend to be running on ports 8000
and 5173. Set `API_URL` and `FRONTEND_URL` to test alternate ports. On Windows,
`$env:PLAYWRIGHT_CHANNEL="msedge"` uses installed Edge instead of downloading
Chromium. Test-created vehicles are removed after verification. Screenshots
and local server logs belong in the ignored `.runtime/` directory.

Configure frontend connections through `VITE_API_BASE_URL` and optionally
`VITE_WS_BASE_URL`, as shown in `frontend/.env.example`. Restart Vite after
changing environment variables. The backend's `CORS_ORIGINS` must include the
chosen frontend origin when using a non-default port.

## REST API Overview

- `GET /api/v1/` and `GET /api/v1/health`
- `POST/GET/PUT/DELETE /api/v1/vehicles`
- `POST /api/v1/telemetry`
- `GET/DELETE /api/v1/telemetry/history/{vehicle_id}`
- `GET /api/v1/telemetry/latest/{vehicle_id}`
- `GET /api/v1/vehicles/{id}/health`
- `GET /api/v1/vehicles/{id}/alerts`
- `GET /api/v1/vehicles/{id}/maintenance`
- `GET /api/v1/vehicles/{id}/prediction`
- `POST /api/v1/bon/chat`

## WebSocket Overview

- URL: `ws://localhost:8000/api/v1/ws/telemetry/{vehicle_id}`
- Event: `telemetry_update`
- Payload: serialized telemetry record in a standard message envelope

## Machine Learning Pipeline

1. Generate CSV datasets from simulator outputs.
2. Train Logistic Regression, Random Forest, and Gradient Boosting models.
3. Evaluate and compare metrics.
4. Persist the best model and metadata.
5. Use `MLPredictor` or factory `auto` mode at runtime.

## Roadmap

- Add production deployment templates (Kubernetes and managed DB options)
- Expand test coverage with API integration scenarios
- Add benchmark suite for simulation and prediction throughput
- Add richer BON evaluation and prompt tuning workflows

## License

This project is licensed under MIT. See [LICENSE](LICENSE).
