# AGENTS.md

## Project

**Name:** `ClamSentinel`

A desktop malware scanner. The Electron app is the only user-facing application; all backend services run as Docker Compose containers:
FastAPI, PostgreSQL 17, ClamAV (`clamd`), and an OpenTelemetry → Prometheus / Loki / Tempo / Grafana observability stack.

## Current state

Greenfield. The repository contains only `Design.md` and this file — no source code, manifests, tests, or git repo yet.
`Design.md` is the canonical spec. Read it before writing any code; it contains the full AGENTS.md target and all design decisions. `notes/` is scratch space.

## Objectives

1. Security first
2. Maintainability over cleverness
3. Strong typing (TypeScript / Python type hints)
4. Observable services
5. Container-first development
6. Minimal dependencies

When multiple implementations are possible, choose the simplest secure solution.

## Architecture

```text
Electron (native, NOT containerized)
└── React 19 + Vite + Tailwind CSS 4        frontend/  (shadcn/ui)
    └── FastAPI REST API                    backend/app/
         ├── PostgreSQL 17 + Alembic
         ├── ClamAV (clamd daemon protocol)
         └── OpenTelemetry → Prometheus, Loki, Tempo, Grafana
```

Planned layout: `electron/` (main, preload, renderer), `frontend/`, `backend/` (`app/api|core|db|models|schemas|services|telemetry|utils`, `alembic/`), `infrastructure/` (grafana, prometheus, otel, loki, tempo), `docs/`, root `docker-compose.yml` + `.env`.

## Hard rules (from Design.md)

- Backend MUST talk to ClamAV only via the clamd daemon protocol. Never `clamscan`, subprocess, or shell; stream files to clamd.
- **PostgreSQL, not SQLite.** Design.md contains an earlier SQLite design that was explicitly superseded — do not resurrect it.
- Use Alembic for every schema change; never edit schema manually. UUID primary keys; never expose raw DB IDs to the UI.
- All API routes under `/api/v1` (`/scans` CRUD, `/health`, `/ready`, `/metrics`, `/version`).
- Every HTTP request emits a trace, a JSON structured log, and metrics. Never log file contents.
- Hash every upload (SHA-256); max upload size via env var; validate MIME/extension/size; never render uploaded files.
- Business logic never lives in React components. Dark SOC-analyst theme with the exact palette in Design.md.
- Frontend state: TanStack Query (server), React Context (app), local state (UI only).

## Conventions (planned, not yet wired up)

- No dev/lint/typecheck/test commands exist yet — the repo is pre-initialization. Backend will use pytest; frontend Vitest + React Testing Library.
- Pydantic v2, SQLAlchemy 2.x, one model per file, one router per feature, functional components only, no `any`.