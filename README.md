# AutoMind AI

A vehicle intelligence workspace for telemetry, diagnostics, maintenance, and contextual guidance from BON.

AutoMind AI 2.0 combines a React dashboard with a FastAPI backend. Register vehicles, generate sample drives, inspect sensor history, and understand what the latest readings mean. Core workflows run locally without an external AI account.

## Features

- Responsive dashboard with vehicle overview, health score, sensor metrics, and alerts.
- Vehicle creation, editing, deletion, search, and persistent selection.
- Normal driving, overheating, low fuel, and worn-brake simulation scenarios.
- Live WebSocket updates with reconnect backoff and periodic refresh.
- Interactive speed, RPM, temperature, and fuel charts.
- Paged telemetry history and CSV export of the displayed page, with every recorded field.
- Seven-system health assessments, alert severity filters, maintenance recommendations, and predictions.
- BON conversations with retry, browser persistence, and clear-history controls.
- Light and dark themes saved in the current browser.

## Run locally

Requirements: Python 3.11 or 3.12 and Node.js 22.12 or later.

```sh
python -m venv .venv
# Windows PowerShell
.venv/Scripts/Activate.ps1
# macOS / Linux
# source .venv/bin/activate

python -m pip install -r requirements-dev.txt
cd frontend
npm ci
cd ..
python scripts/dev.py
```

Open [the workspace](http://127.0.0.1:5173) or [API documentation](http://127.0.0.1:8000/docs).
Ctrl+C stops both services. Alternate ports:

```sh
python scripts/dev.py --backend-port 8100 --frontend-port 5180
```

The launcher configures the frontend proxy automatically. The backend uses
`backend/automind.db` by default when started by the launcher. Existing records
are preserved; nothing seeds or resets the database automatically.

To run services separately, execute `python -m uvicorn app.main:app --reload`
from `backend/` and `npm run dev` from `frontend/`.

Environment files are optional. Copy each `.env.example` when overriding defaults.
A relative `VITE_API_BASE_URL=/api/v1` uses the frontend origin for HTTP and
WebSocket traffic. Set the process variable `VITE_PROXY_TARGET` for another
backend port. A remote API requires `VITE_API_BASE_URL`, optionally
`VITE_WS_BASE_URL`, and backend `CORS_ORIGINS` / `TRUSTED_HOSTS` JSON arrays.
Restart services after changing configuration.

## First drive

1. Open **Vehicles**, click **Add vehicle**, and save its details.
2. Open **Dashboard**, choose a scenario, and click **Simulate drive**.
3. Explore **Telemetry**, **Health**, **Alerts**, **Maintenance**, and **Predictions**.
4. Ask **BON** "How is my car?" or "What maintenance is needed?"

The interface generates 60, 120, or 300 readings per run. Each scenario is
independent and starts its simulated sensors afresh; the odometer accumulates
distance across runs. Samples use generation timestamps, so a batch is not a
wall-clock replay of a real trip. Synthetic readings are stored as ordinary
telemetry and influence the latest assessment. Deleting a vehicle also removes
its telemetry history.

## Verification

```sh
python -m ruff check backend/app backend/tests scripts
cd backend
python -m pytest -q
cd ../frontend
npm run build
npx playwright install chromium
npm run test:e2e
```

The browser runner starts isolated API and Vite services on available local ports,
uses its own SQLite database under `.runtime/`, and stops its own processes.
It checks vehicle CRUD, scenarios, streams, charts, CSV export, pagination,
theme persistence, all pages on mobile, and BON persistence, isolation, and clearing.

On Windows, `$env:PLAYWRIGHT_CHANNEL="msedge"` uses installed Edge. To test
existing servers, run `npm run test:e2e:running` with `FRONTEND_URL` and
`API_URL` as needed. Screenshots, test databases, and logs belong in the ignored
`.runtime/` directory. GitHub Actions runs backend checks, a clean frontend
build, and isolated browser tests.

## Docker

```sh
docker compose up --build
```

Open [the container workspace](http://localhost:8080). The compiled frontend is
served by nginx, which proxies API and WebSocket requests to FastAPI. The
backend runs as a non-root user; SQLite persists in the `automind-data` named
volume. Environment files are not required. This setup binds to localhost and
does not add user authentication or public access controls.

## Architecture

```text
frontend/       React + TypeScript + Vite
  src/pages/    Dashboard, vehicles, telemetry, reports, BON, settings
  src/hooks/    Cached reads, shared diagnostics, live telemetry
  src/services/ HTTP and WebSocket clients
backend/app/
  api/          Versioned REST and WebSocket routes
  services/     Vehicle workflows and diagnostic aggregation
  simulator/    State machine, physics, sensors, persistence
  ai/           BON intent parsing, context, memory, response formatting
  prediction/   Rule and optional ML predictors
  ml/           Synthetic dataset generation, training, evaluation
  database/     SQLAlchemy sessions and SQLite storage
scripts/        Cross-platform development launcher
```

Diagnostic pages share a single `/vehicles/{id}/insights` query. The backend
calculates all reports from the same latest reading. Stream bursts update the
telemetry cache immediately and batch report refreshes. REST polling remains
available during reconnects. This rebuild requires no database schema migration.

## API

Base: `/api/v1`. Most REST routes return a `data` envelope; BON chat returns
its typed response directly. See `/docs` for request schemas.

| Method           | Route                        | Purpose                                 |
| ---------------- | ---------------------------- | --------------------------------------- |
| GET              | `/health`                    | Service liveness                        |
| GET, POST        | `/vehicles`                  | List or create vehicles                 |
| GET, PUT, DELETE | `/vehicles/{id}`             | Read, edit, or delete                   |
| POST             | `/vehicles/{id}/simulation`  | Generate 1-300 readings with a scenario |
| GET              | `/vehicles/{id}/insights`    | Combined diagnostic snapshot            |
| GET              | `/vehicles/{id}/health`      | Health report                           |
| GET              | `/vehicles/{id}/alerts`      | Active alerts                           |
| GET              | `/vehicles/{id}/maintenance` | Maintenance recommendations             |
| GET              | `/vehicles/{id}/prediction`  | Prediction report                       |
| POST             | `/telemetry`                 | Ingest validated sensor data            |
| GET              | `/telemetry/latest/{id}`     | Latest reading, or null when empty      |
| GET, DELETE      | `/telemetry/history/{id}`    | Page or clear history                   |
| POST             | `/bon/chat`                  | Vehicle-aware guidance                  |
| GET, DELETE      | `/bon/sessions/{session_id}` | Read or clear conversation              |

Lists and history accept `skip >= 0` and `limit=1..1000` (default 100).
History sorts newest first, breaking timestamp ties by record ID. Input normalizes
timezone offsets to UTC; telemetry responses include a UTC offset. The
WebSocket endpoint is `/api/v1/ws/telemetry/{vehicle_id}`, with messages shaped
as `{"type":"telemetry_update","data":{...}}`.

## BON and prediction behavior

BON is a rule-based contextual assistant. Browser conversations are isolated
per vehicle and retain the latest 200 messages. Server memory is process-local,
capped at 1,000 sessions and 100 messages per session, expires after one hour
without a new message, and resets on restart. The server exposes no user
authentication; use it as a local or trusted workspace, and add identity and
authorization before offering shared access.

Health and alerts use rules. ML predictions are optional and fall back to the
rule predictor when compatible artifacts are absent. Training labels come
from synthetic, rule-defined scenarios. Model confidence and distance estimates
are not validated real-world failure probabilities.

## Dataset and model tools

From `backend/`:

```sh
python -m app.ml.dataset --size 10000 --seed 0 --output ../datasets/telemetry.csv
python -m app.ml.training.train --dataset ../datasets/telemetry.csv
```

Generation writes a CSV and statistics report without changing the application
database. Training saves artifacts under `backend/app/ml/models/`. The
pipeline excludes record IDs, timestamps, injected-fault metadata, and prediction
outputs from inference features. Validation selects the model; a separate test
split evaluates it. Retrain older artifacts before loading them.

Licensed under the [MIT License](LICENSE).
