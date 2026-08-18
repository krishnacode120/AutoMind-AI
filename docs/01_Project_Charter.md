# Project Charter

## Purpose

AutoMind AI is an open-source vehicle monitoring platform for simulated vehicle
data. It turns telemetry into deterministic health, alert, maintenance, and
prediction reports, and presents those results through a FastAPI API and React
dashboard.

## Objectives

- Provide a modular, locally runnable vehicle-monitoring reference project.
- Keep simulation, diagnostics, prediction, persistence, API, and UI concerns
  separated.
- Support rule-based operation without a trained ML artifact.
- Make future model training and assistant improvements additive.

## Scope

The current release supports vehicles, telemetry storage, simulation helpers,
derived diagnostics, BON contextual chat, WebSocket telemetry delivery, dataset
generation, offline ML training, and a web dashboard. Authentication, external
vehicle integrations, and production notifications are out of scope.

## Success Measures

- Backend tests and static checks pass in CI.
- Frontend produces a production build.
- Core workflows can be exercised locally with SQLite and Docker Compose.
