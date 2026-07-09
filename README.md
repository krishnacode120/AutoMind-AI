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

Use the telemetry and vehicle API routes to create vehicles and emit telemetry snapshots through backend endpoints; simulator modules are integrated in backend services and runner components.

## Running ML Training

```bash
cd backend
python -m app.ml.training.train --dataset "PATH_TO_DATASET.csv"
```

Generated artifacts are saved in `backend/app/ml/models/`.

## Running the Dashboard

Run backend and frontend together, then open the frontend URL to access dashboard pages for vehicles, telemetry, health, maintenance, prediction, and BON.

## BON Chat Usage

- Endpoint: `POST /api/v1/bon/chat`
- Input: vehicle ID, message, session ID
- Output: answer, intent, confidence, context used, timestamp

## REST API Overview

- `GET /api/v1/` and `GET /api/v1/health`
- `POST/GET/PUT/DELETE /api/v1/vehicles`
- `POST /api/v1/telemetry`
- `GET/DELETE /api/v1/telemetry/history/{vehicle_id}`
- `GET /api/v1/telemetry/latest/{vehicle_id}`
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

## Screenshots

Screenshots will be added in a future release.

## Demo Video

Demo video link will be added in a future release.

## Roadmap

- Add production deployment templates (Kubernetes and managed DB options)
- Expand test coverage with API integration scenarios
- Add benchmark suite for simulation and prediction throughput
- Add richer BON evaluation and prompt tuning workflows

## License

This project is licensed under MIT. See [LICENSE](LICENSE).
