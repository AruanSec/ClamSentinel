# PLAN.md — ClamSentinel Implementation Plan

Implemented in phases, each independently verifiable. All decisions drawn from `Design.md` (the canonical spec). UI/UX design leads.

---

## Phase 1 — UI/UX Design System + Page Mocks (front-end only, mock data)

1. **Design tokens** — Tailwind 4 `@theme` in CSS-first config: exact palette (`#0B1220` bg, `#111827` surface, `#374151` border, `#2563EB` primary, `#22C55E`/`#F59E0B`/`#EF4444` status, `#E5E7EB` text), Inter font, type scale (sidebar 14, titles 28 semibold, KPI 32–40 bold, tables 13).
2. **shadcn/ui baseline** — button, card, badge, table, tabs, sheet/dialog, toast (Sonner), command palette, input, progress, dropdown.
3. **App shell** — 220–240px fixed sidebar (`Dashboard`, `Quick Scan`, `Scan History`, `Quarantine`, `Virus Definitions`, `Observability`, `Settings`), command-style top bar, dark theme.
4. **Shared components** — `KpiCard`, `StatusBadge` (color + icon/text, never color alone), `CopyHash`, `DropZone`, `ScanProgress` (animated at 60fps), `DataTable`, `EmptyState`, confirm dialog.
5. **Page mocks (mock data, no backend)**
   - Dashboard: 4 KPI cards, recent-scans table, detection trend chart, ClamAV status
   - Quick Scan: drag-drop zone (files/folders), live progress
   - Scan History: search, status filter, date range, CSV export, SHA-256 copy
   - Quarantine: list + restore-with-confirmation flow
   - Observability: Metrics/Logs/Traces tabs (placeholders for Grafana embed)
   - Settings: Scanning / Updates / Database / Telemetry categories
6. **Micro-interactions** — hover elevation (2px), success ("Scan completed — 842 files scanned") and threat toasts, Ctrl+K global search/command palette.
7. **A11y pass + review** — keyboard nav, focus indicators, high contrast; verify against Design.md §"Suggest a UI/UX" and its palette.

**Exit criteria:** frontend serves with all nav pages rendering; design reviewed against Design.md; lint + build pass.

## Phase 2 — Frontend Foundation + Electron Shell

Scaffold `electron/` (main, preload, renderer) and `frontend/` (React 19 + Vite + Tailwind 4 + shadcn/ui); routing; TanStack Query setup; typed service interfaces backed by a mock API module. No business logic in components.

## Phase 3 — Backend Foundation

FastAPI app with pydantic-settings env config, request middleware emitting trace + JSON log + metrics, `/health`, `/ready`, `/metrics`, `/version`, CORS, JWT auth scaffolding, `{error:{code,message}}` envelope.

## Phase 4 — Database + Scan CRUD

docker-compose `postgres:17`; SQLAlchemy 2.x models (`scans`, `files`, `detections`) with UUID PKs; Alembic init + first migration; `/api/v1/scans` CRUD.

## Phase 5 — ClamAV Integration

clamd-client streaming uploads (no clamscan/subprocess); SHA-256, MIME/extension, size-env validation; scan jobs persisted to DB.

## Phase 6 — Frontend ↔ Backend Integration

Replace mocks with TanStack Query hooks against real API; live dashboard, history, quarantine; error handling.

## Phase 7 — Observability Stack

docker-compose OTel Collector, Prometheus, Loki, Tempo, Grafana; custom metrics (scans/infected/duration); 4 Grafana dashboards; embed in Observability page.

## Phase 8 — Production Features

Quarantine storage, virus-definition status, scheduled scans, settings persistence, retention/backup, rate limiting.

## Phase 9 — Packaging + Testing + CI

Electron packaging, pytest + Vitest suites, CI pipeline.