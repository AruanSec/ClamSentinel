# AGENTS.md

## Project

**Name:** `ClamSentinel` — desktop malware scanner. Electron shell (planned) + React/Vite frontend, FastAPI backend, PostgreSQL 17 + ClamAV (`clamd`) containers, OpenTelemetry → Prometheus / Loki / Tempo / Grafana.

## Current state

Early scaffold (3 commits). Working: minimal FastAPI app under `backend/app/`, a Vite React dashboard shell under `frontend/` (inline styles, no Tailwind/shadcn/router yet), `docker-compose.yml` (postgres 17 + clamav + backend), `.env.example`, README. Not yet present: `electron/`, `infrastructure/`, Alembic migrations, `/api/v1` wiring, clamd client, tests, lint/typecheck/CI.

## Canonical docs

- `notes/Design.md` — the spec. Read before writing code. Contains full design decisions and the exact UI palette.
- `notes/PLAN.md` — phased roadmap (Phases 1–9, "UI/UX leads").
- `notes/Phase 1.md` — concrete frontend plan. **It deliberately overrides Design.md's pinned versions: use Vite 8, React 19.3, Tailwind 4.3 (CSS-first, no tailwind.config), react-router 7.18, recharts 3.10.** Dev machine has node 26 / npm 11.
- `notes/` is NOT scratch; it's the authoritative planning + spec area.

## Architecture

```text
Electron (native, NOT containerized)          -- Phase 2+
└── frontend/  React 19 + Vite + Tailwind 4 + shadcn/ui  (Phase 1 to build)
    └── backend/app/  FastAPI (+ pydantic-settings, SQLAlchemy 2.x, Alembic)
         ├── PostgreSQL 17 (driver: postgresql+psycopg)
         ├── ClamAV via clamd daemon protocol only
         └── OpenTelemetry → Prometheus, Loki, Tempo, Grafana
```

## Commands

```bash
docker compose up -d            # postgres:17 + clamav + backend (repo root)
cd backend && uv sync           # uv-managed; pyproject + uv.lock committed; Python 3.12
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
cd frontend && npm install && npm run dev   # Vite on :5173
npm run build                   # dist/ is gitignored
```

Backend tests: pytest/pytest-asyncio/httpx are in the `dev` dependency group but no test files exist yet. Frontend test runner: Vitest + jsdom (configured in `vite.config.ts`), no tests yet. No lint/typecheck scripts exist yet — do not claim to run them.

## Gotchas

- **Import convention is currently broken — pick one side when touching it.** Source imports are absolute `from backend.app.*` (e.g. `db/session.py`, `api/v1/scans.py`), but README/Dockerfile run `uvicorn app.main:app`. The Docker image copies only `app/` into `/app`, so the container can only resolve `app.*` (top-level), while `backend/app.main:app` only resolves from the repo root. `app.main` imports nothing internal today, which is the only reason the app starts. Wiring the router or session will `ModuleNotFoundError` with the documented run command. Standardize on either `app.*` (matches Docker, but requires renaming imports) or running from repo root as `backend.app.main:app`.
- **Router not wired**: `app/api/v1/scans.py` defines `/api/v1/*` (incl. a duplicate `/api/v1/health`) but is never included in `app.main` — `/api/v1/scans` currently 404s. Root `/health`, `/ready`, `/version` live in `main.py`.
- **Env config**: settings use `env_prefix="CLAMSENTINEL_"` and `env_file=".env"` **relative to CWD**. Backend runs from `backend/`, so the repo-root `.env`/`.env.example` is not auto-loaded — default config values are used unless env vars are set. `docker-compose.yml` passes `CLAMSENTINEL_*` vars explicitly. DB creds are dev-only `scanner/change_me`.
- **clamav readiness**: compose waits only on `service_started` for clamav; `clamav/clamav:latest` is slow on first boot (signature fetch). Don't assume clamd responds immediately.
- `requirements.txt` duplicates `pyproject.toml` deps (both committed) — keep in sync when adding dependencies.
- Backend OTel only has a ConsoleSpanExporter so far (`telemetry/otel.py`); Prometheus/Loki/Tempo/Grafana are later phases.

## Hard rules (from Design.md)

- Backend MUST talk to ClamAV only via the **clamd daemon protocol** — never `clamscan`, subprocess, or shell; stream files to clamd.
- **PostgreSQL, not SQLite** (an earlier SQLite design was explicitly superseded — do not resurrect it). Alembic for every schema change; UUID PKs; never expose raw DB IDs to the UI.
- Every HTTP request emits a trace, a JSON structured log, and metrics. Never log file contents.
- Hash every upload (SHA-256); max upload size via env var (`CLAMSENTINEL_MAX_UPLOAD_SIZE_MB`); validate MIME/extension/size; never render uploaded files.
- API routes under `/api/v1`. Business logic never lives in React components.
- Frontend state: TanStack Query (server), React Context (app), local state (UI only).
- Dark SOC theme using the exact palette in Design.md (`#0B1220` bg, `#111827` surface, `#374151` border, `#2563EB` primary, `#22C55E`/`#F59E0B`/`#EF4444` status, `#E5E7EB` text). Status never communicated by color alone (a11y rule).

## Conventions

Pydantic v2, SQLAlchemy 2.x, one model per file, one router per feature, functional components only, strict TS (no `any`), minimal dependencies, simplest secure solution.