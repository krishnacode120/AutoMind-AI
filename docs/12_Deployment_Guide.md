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

- Replace default `SECRET_KEY`.
- Use managed database for non-local deployment.
- Add reverse proxy and TLS termination.
- Configure centralized logging and monitoring.
