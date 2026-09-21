# Phase 1 — UI/UX Design System + Page Mocks

Implementation plan. Front-end only, mock data, runs in a browser via Vite dev server (Electron shell arrives in Phase 2).

**Decisions locked:** npm (only PM installed; node 26 / npm 11) · recharts for the trend chart · shadcn/ui via the official CLI.

**Versions verified against npm:** React 19.3, Vite 8 (Design.md pinned Vite 7 — not using the pinned version), Tailwind 4.3, react-router 7.18, recharts 3.10.

## Step 1 — Scaffold `frontend/` (Vite + React 19 + TS)

- `npm create vite@latest frontend -- --template react-ts` at repo root (Phase 2's Electron will consume this tree).
- Install: `tailwindcss@4 @tailwindcss/vite`, `react-router-dom`, `lucide-react`, `sonner`, `cmdk`, `clsx`, `tailwind-merge`, `class-variance-authority`, `recharts`, `@fontsource/inter`.
- Vite config: `@tailwindcss/vite` plugin (Tailwind 4 is CSS-first — **no** `tailwind.config.js`/PostCSS), path alias `@` → `./src`. Mirror alias in `tsconfig.json` + strict TS (no `any`).
- Add `dev` / `build` / `lint` / `typecheck` scripts (ESLint flat config + `tsc --noEmit`).

## Step 2 — Design tokens (`src/index.css`)

- `@import "tailwindcss"; @custom-variant dark;` — app is always dark (Electron-native), no light mode.
- `@theme` mapping the exact Design.md palette to CSS vars: `--background #0B1220`, `--surface #111827`, `--border #374151`, `--primary #2563EB`, `--success #22C55E`, `--warning #F59E0B`, `--danger #EF4444`, `--foreground #E5E7EB`.
- Type scale: sidebar 14px medium, page titles 28px semibold, KPI numbers 32–40px bold, tables 13px regular. Inter via `@fontsource/inter`.

## Step 3 — shadcn/ui baseline

- `npx shadcn@latest init` (Tailwind 4, dark variant, neutral base, `@/` alias) → `components.json` + `lib/utils.ts`.
- `npx shadcn@latest add` button card badge table tabs sheet dialog alert-dialog input dropdown-menu progress tooltip separator command sonner.
- Re-map the generated CSS vars so every component inherits the Design.md palette.

## Step 4 — App shell + routing

- `src/main.tsx`, `App.tsx` with `BrowserRouter`; routes: `/` dashboard, `/scan`, `/history`, `/quarantine`, `/definitions`, `/observability`, `/settings`, catch-all → `/`.
- `Layout.tsx`: fixed 240px sidebar (`Sidebar.tsx` — 7 nav items, lucide icons, active state), command-style `TopBar.tsx` (page title, global search, Ctrl+K badge). Content on surface bg.

## Step 5 — Shared components (`src/components/`)

- `KpiCard` — icon, label, value, delta ("+148 today"), data-driven tone.
- `StatusBadge` — label + icon + tone; **never color alone** (a11y rule).
- `CopyHash` — monospace truncated hash + copy button + tooltip.
- `DropZone` — drag-over states, click-to-browse, format hints.
- `ScanProgress` — only the bar animates (60fps), not the layout.
- `DataTable` — generic table wrapper: sort, paginate, empty state.
- `EmptyState`, `ConfirmDialog` (AlertDialog), `Toaster` (Sonner).

## Step 6 — Typed domain + mock data (`src/domain.ts`, `src/services/mock*`)

- Types mirror Design.md API shapes: `Scan`, `FileRecord`, `Detection`, `ClamStatus`, `QuarantineEntry`, `VirusDefinitions`.
- Mock module: generated scan histories (statuses CLEAN/INFECTED/ERROR/SCANNING), 14-day trend, KPI values.
- Pages consume mocks **only through a thin typed `services/` layer** so Phase 6 only swaps the implementation (TanStack Query) — no page code changes.

## Step 7 — Page mocks (`src/pages/`)

- **Dashboard**: 4 KPI cards (Protected 12,482 +148 · Threats 17 / 3 quarantined · Avg 98 ms · Definitions v27981 up-to-date), recent scans (top 8), detection-trend chart (recharts), ClamAV status indicator.
- **Quick Scan**: DropZone (EXE/DLL/ZIP/PDF/DOCX/ISO + folders), current-scan card with ScanProgress (65%), per-file list; success + threat toasts ("Scan completed — 842 files scanned"; threat toast amber/red with "View" action).
- **Scan History**: DataTable columns — Status, Filename (clickable), SHA-256 (CopyHash), Signature, Time (relative + exact), Duration; toolbar search, status filter, date range, **Export CSV** (client-side); pagination.
- **Quarantine**: table (signature, filename, SHA-256, date) with restore/delete behind ConfirmDialog.
- **Virus Definitions**: version, last-updated, freshness (warning tone if stale), "Check Now" (mock).
- **Observability**: Metrics/Logs/Traces tabs — Grafana embed placeholder panels (iframe wiring is Phase 7), sample log/trace tables so tabs function now.
- **Settings**: Scanning / Updates / Database / Telemetry groups with toggle/select/input controls.

## Step 8 — Micro-interactions

- Hover elevation on cards (2px lift/shadow), command palette via Ctrl+K (cmdk), global search across scan history.

## Step 9 — A11y + quality gates

- Keyboard nav, visible focus indicators, aria-labels on icon buttons, WCAG-AA contrast checks on the token palette, non-color status indication everywhere.
- Verify the mock against Design.md §"Suggest a UI/UX" checklist (layout, typography, palette, micro-interactions).

## Exit criteria

1. `npm run dev` → all 7 routes render, nav works, toasts + palette fire.
2. `npm run lint` + `npm run typecheck` + `npm run build` all pass.
3. Design diff vs. Design.md agrees on palette/typography/layout.

## Out of scope

Electron shell (P2), real API / TanStack Query (P2/P6), tests / CI (P9), live Grafana embed (P7).