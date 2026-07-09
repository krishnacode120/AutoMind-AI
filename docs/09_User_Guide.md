# User Guide

## Prerequisites

- Python 3.11+ (recommended 3.12)
- Node.js 20+
- npm 10+

## Start Backend

```bash
cd backend
uvicorn app.main:app --reload
```

## Start Frontend

```bash
cd frontend
npm run dev
```

## Core Workflows

- Create a vehicle from the dashboard or API.
- Stream/add telemetry through simulator/API routes.
- Monitor health, alerts, and maintenance pages.
- Use BON chat for context-aware assistant responses.
- Review prediction output in prediction views.

## BON Chat

Required chat inputs:

- `vehicle_id`
- `message`
- `session_id`

BON uses current context and recent conversation history to answer vehicle queries.

## Troubleshooting

- If API calls fail, verify backend is running on port `8000`.
- If dashboard cannot fetch data, verify frontend `.env` API URL.
- If ML mode fails, use predictor `auto` mode to fallback to rule-based prediction.
