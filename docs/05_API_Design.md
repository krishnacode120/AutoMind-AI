# API Design

The REST API is served below `/api/v1`. Most resource routes return the shared
envelope `{ success, message, timestamp, data }`.

## Core Routes

| Area | Routes |
| --- | --- |
| Service | `GET /`, `GET /health`, `GET /system` |
| Vehicles | `POST/GET /vehicles`, `GET/PUT/DELETE /vehicles/{id}` |
| Telemetry | `POST /telemetry`, `GET /telemetry/latest/{id}`, `GET/DELETE /telemetry/history/{id}` |
| Vehicle insights | `GET /vehicles/{id}/health`, `/alerts`, `/maintenance`, `/prediction` |
| BON | `POST /bon/chat`, `GET/DELETE /bon/sessions/{session_id}`, `GET /bon/health` |
| WebSocket | `ws /ws/telemetry/{vehicle_id}` |

## Error Handling

Known application errors use a consistent error envelope. Invalid resource IDs
return `404`; derived report routes return `404` when the vehicle has no
telemetry; malformed requests are handled by FastAPI validation.
