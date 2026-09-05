# Deployment Guide

## Docker Compose

The repository includes:

- `backend/Dockerfile`
- `frontend/Dockerfile`
- `docker-compose.yml`

## Environment Files

Create:

- `backend/.env` from `backend/.env.example`
- `frontend/.env` from `frontend/.env.example`

## Start Stack

```bash
docker compose up --build
```

## Exposed Services

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:5173`

## Production Notes

Compose stores SQLite in the `automind-data` named volume at `/data/automind.db`.
It does not bind-mount a possibly missing host database file. Existing local
`backend/automind.db` data is not automatically copied to that volume.
The supplied Compose stack is intended for local development.

- Replace default `SECRET_KEY`.
- Use managed database for non-local deployment.
- Add reverse proxy and TLS termination.
- Configure centralized logging and monitoring.
