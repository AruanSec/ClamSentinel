# ClamSentinel

ClamSentinel is a desktop malware-scanning application built around an Electron shell, a React + Vite frontend, and a FastAPI backend powered by PostgreSQL and ClamAV.

## Overview

This project follows a security-first architecture:

- Electron desktop app for the user-facing experience
- React frontend for dashboard and scan workflows
- FastAPI backend for REST endpoints and orchestration
- PostgreSQL 17 for durable persistence
- ClamAV daemon (`clamd`) for malware detection
- OpenTelemetry + Prometheus + Loki + Tempo + Grafana for observability

## Repository layout

```text
ClamSeentinel/
├── AGENTS.md
├── README.md
├── .env.example
├── .gitignore
├── docker-compose.yml
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── __init__.py
│       ├── api/
│       ├── core/
│       ├── db/
│       ├── models/
│       ├── schemas/
│       ├── services/
│       ├── telemetry/
│       └── main.py
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── src/
├── notes/
│   ├── AGENTS.md
│   ├── Design.md
│   ├── PLAN.md
│   └── Phase 1.md
└── .github/ (optional future CI)
```

## Current status

The repository is in an early scaffold phase and is intended to evolve toward a production-grade malware scanning platform.

## Local setup

### 1) Python backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2) Frontend

```bash
cd frontend
npm install
npm run dev
```

### 3) Container services

```bash
docker compose up -d
```

## Environment

Copy `.env.example` to `.env` and adjust values as needed.

## Security notes

- Backend must communicate with ClamAV via the `clamd` daemon protocol.
- PostgreSQL is the required database layer; SQLite is intentionally not used.
- Schema changes must be handled with Alembic migrations.
- Uploaded files must be validated and hashed before scanning.

## Development workflow

- Keep business logic out of React components.
- Prefer typed Python and TypeScript.
- Use structured logs and telemetry for every request.
- Follow the design rules in `AGENTS.md` and the canonical design notes in `notes/Design.md`.

## Next milestones

- Add real database models and Alembic migrations
- Implement ClamAV scan service and upload validation
- Expose `/api/v1` routes for scan management and health checks
- Add production observability and dashboards
- Expand the Electron app shell and UI

## License

This project is currently in development and does not yet define a final license.
