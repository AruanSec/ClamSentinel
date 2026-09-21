
# DESIGN.md

This document is the canonical product design for ClamSentinel. It supersedes earlier SQLite-oriented notes and reflects the current system design that is also enforced in [AGENTS.md](AGENTS.md): PostgreSQL 17, Alembic migrations, UUID primary keys, and a backend-first architecture.

## Proposed architecture

### Web UI

ClamAV Malware Scanner Platform
React + Vite · FastAPI · PostgreSQL 17 · OpenTelemetry · Grafana

### Frontend

React 19 + Vite + Tailwind

### Backend API

FastAPI + SQLAlchemy 2.x + PostgreSQL 17
Scanning engine

ClamAV daemon (clamd)
Observability

Grafana + Prometheus + Tempo + Loki
The upload flow is:

User uploads a file from the Electron/React frontend.

FastAPI receives the file.

Backend streams it to clamd using the daemon protocol, without shelling out to clamscan.

Result is stored in PostgreSQL.

OpenTelemetry emits traces, logs, and metrics.

Grafana visualizes everything.

Complete stack
Service

Purpose

Electron

Native desktop shell

React + Vite

Web interface

Tailwind CSS

Styling

FastAPI

REST API

ClamAV (clamd)

Malware detection

PostgreSQL 17

Persistent scan metadata and results

OpenTelemetry Collector

Telemetry pipeline

Prometheus

Metrics storage

Loki

Log aggregation

Tempo

Distributed tracing

Grafana

Dashboards

Docker Compose

Service orchestration

Folder structure
malware-scanner/
│
├── docker-compose.yml
├── .env
│
├── electron/
│   ├── main/
│   ├── preload/
│   └── renderer/
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── Dockerfile
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── telemetry/
│   │   └── main.py
│   ├── alembic/
│   ├── requirements.txt
│   └── Dockerfile
│
├── infrastructure/
│   ├── grafana/
│   ├── prometheus/
│   ├── otel/
│   └── loki/
│
├── docs/
│
├── scripts/
│
└── data/
    └── uploads/

Database schema
The canonical storage layer is PostgreSQL 17, not SQLite. Schema changes are managed via Alembic; raw database identifiers are never exposed to the UI.

CREATE TABLE scans (
    id UUID PRIMARY KEY,
    filename TEXT NOT NULL,
    sha256 TEXT NOT NULL,
    filesize BIGINT,
    status TEXT NOT NULL,
    malware_name TEXT,
    scanned_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    duration_ms INTEGER
);

Example record:

Filename

Status

Malware

Duration

invoice.pdf

CLEAN

—

124 ms

payload.exe

INFECTED

Win.Trojan.Agent

88 ms

REST API
Method

Endpoint

Description

POST

/api/v1/scan

Upload & scan

GET

/api/v1/scans

List history

GET

/api/v1/scans/{id}

Scan details

DELETE

/api/v1/scans/{id}

Remove record

GET

/health

Liveness

GET

/ready

Readiness

GET

/metrics

Prometheus metrics

Health endpoint
{
  "status": "healthy",
  "database": "up",
  "clamd": "up",
  "version": "1.0.0"
}
React UI pages
Dashboard
#security #dashboard #hacker #webdesign #design #cloudsecurity #management #appdesign #uidesign #job #networksecurity #saas #saasdesign #cybersecuritydashboard #uidesign #uiux #uiuxdesigner #ui… | MD Asad | 15 comments
TeamDrive - Company File Repository
Should I run performance test as part of CI pipeline?
6
Clean Files

842
today
Threats Found

17
today
Average Scan

112 ms
Database Size

12.4 MB
Scan page
Bot Verification
File Uploader - Free React Nextjs Template
Nemesis Usage Guide - Nemesis Documentation
5
Drop Zone

Drag & drop files here

or click to browse • PDF, ZIP, EXE, DOCX…
Live scan progress

65%
invoice.pdf

2.3 MB
Scanning…

History
Advanced Shadcn Table: Server-Side Sort, Filter, Paginate
Building a Lightweight Brute-force Detection System in Splunk (SIEM-lite Style) | by Khawajaaimenbasharat | Medium
Secure os downloads Secure e do Edge com a segurança de ficheiros integrada para navegadores OPSWAT- OPSWAT
6
File

Result

Time

invoice.pdf

Clean

10:42
payload.exe

Trojan

09:11
Docker Compose
This compose launches 9 containers.

services:

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend

  backend:
    build: ./backend
    env_file: .env
    volumes:
      - ./data/uploads:/uploads
    depends_on:
      - postgres
      - clamav
      - otel

  clamav:
    image: clamav/clamav:latest
    volumes:
      - clam_db:/var/lib/clamav
    ports:
      - "3310:3310"

  otel:
    image: otel/opentelemetry-collector-contrib:latest
    volumes:
      - ./otel/collector-config.yaml:/etc/otelcol/config.yaml

  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml

  loki:
    image: grafana/loki:latest

  tempo:
    image: grafana/tempo:latest

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3001:3000"
    depends_on:
      - prometheus
      - loki
      - tempo

volumes:
  clam_db:
OpenTelemetry instrumentation
The backend exports three signal types:

Signal

Destination

Traces

Tempo

Metrics

Prometheus

Logs

Loki

Example FastAPI instrumentation:

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.psycopg import PsycopgInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

FastAPIInstrumentor.instrument_app(app)
PsycopgInstrumentor().instrument()
RequestsInstrumentor().instrument()
Prometheus metrics
Your API will expose metrics such as:

# HELP malware_scans_total
# TYPE counter
malware_scans_total 152

# HELP malware_infected_total
malware_infected_total 7

# HELP scan_duration_seconds
scan_duration_seconds_bucket
Additional custom metrics:

Total scans

Clean scans

Infected scans

Average scan duration

Upload size

ClamAV availability

Grafana dashboards
I recommend four dashboards.

Executive Dashboard

Grafana Digital Signage | Display Dashboards on TV Screens
Next-Gen Security Dashboard in Grafana for Real-Time Threat Response - Foogle
Prometheus All Metrics | Grafana Labs
6
KPIs for scans, infections, latency, and system health.

API Performance

Supercharge Your Node.js Monitoring with OpenTelemetry, Prometheus, and Grafana - DEV Community
Getting Started: Monitoring a FastAPI App with Grafana and Prometheus - A Step-by-Step Guide - DEV Community
Observability with ASP.NET Core using OpenTelemetry, Prometheus and Grafana - DEV Community
5
Request rate, latency percentiles, errors, and endpoint throughput.

Threat Analytics

Malware Sandbox
Releasing an integration with the field: OpenCTI + Tanium Platform | by Samuel Hassine | Medium
Behind-the-Scenes: How to Negotiate with Ransomware Gangs
5
Malware families, infected file trends, and detection ratios.

Application Logs

Kubernetes 监控 Helm 教程 | Grafana Loki 文档 - Grafana 教程
Processing JSON log lines and displaying visualizations based on them - Dashboards - Grafana Labs Community Forums
Docker Compose Logs: A Complete Guide · Dash0
5
Searchable structured logs correlated with traces and requests.

Security considerations
The backend should never invoke clamscan via shell. Use the clamd TCP protocol instead.

Recommended protections:

SHA-256 hash every upload

Maximum upload size (e.g. 100 MB)

MIME validation

Store uploads outside the web root

Automatic deletion after configurable retention

Rate limiting

CORS restriction

Read-only storage mount for non-critical files, with PostgreSQL as the authoritative persistence layer

Technology versions
Component

Version

React

19

Vite

7

Tailwind CSS

4

FastAPI

Latest

PostgreSQL

17

ClamAV

Latest

OpenTelemetry

Latest

Grafana

12

Prometheus

Latest

Development roadmap
Phase 1 — Core MVP

React upload UI, FastAPI scan endpoint, ClamAV integration, PostgreSQL persistence, Docker Compose.

Phase 2 — Observability

OpenTelemetry SDK, Collector, Prometheus metrics, Loki logs, Tempo traces, Grafana dashboards.

Phase 3 — Production Features

Authentication, RBAC, virus definition status, scheduled scans, quarantine management, REST API documentation.

This design follows cloud-native observability practices while remaining lightweight. PostgreSQL provides the durable persistence layer, and every service can be started with a single docker compose up -d.

A strong next step is to build this as a fully production-ready repository with about 25–30 files, including the complete React frontend, Tailwind components, FastAPI backend, SQLAlchemy models, OpenTelemetry collector configuration, Prometheus and Grafana provisioning, and a ready-to-run docker-compose.yml plus .env, so it starts with one command.

Updated architecture

Technology stack
Layer

Technology

Desktop UI

Electron

Frontend

React 19 + Vite

Styling

Tailwind CSS 4

Backend

FastAPI

Database

PostgreSQL 17

Scanner

ClamAV (clamd)

ORM

SQLAlchemy + Alembic

Metrics

Prometheus

Logs

Loki

Traces

Tempo

Telemetry

OpenTelemetry

Docker Compose services
Your desktop application remains outside Docker, while all infrastructure runs in containers.

services:
  backend:
    build: ./backend
    depends_on:
      postgres:
        condition: service_healthy
      clamav:
        condition: service_started

  postgres:
    image: postgres:17
    environment:
      POSTGRES_DB: malware
      POSTGRES_USER: scanner
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U scanner"]

  clamav:
    image: clamav/clamav:latest

  otel:
    image: otel/opentelemetry-collector-contrib

  prometheus:
    image: prom/prometheus

  loki:
    image: grafana/loki

  tempo:
    image: grafana/tempo

  grafana:
    image: grafana/grafana

volumes:
  postgres_data:
Database design
Instead of a single table, I'd normalize it slightly.

scans

One row per scan job

Column

Type

id

UUID
status

enum
started_at

timestamp
completed_at

timestamp
duration_ms

integer
files

File metadata and hashes

Column

Type

sha256

text (unique)
filename

text
size

bigint
mime_type

text
detections

Malware results

Column

Type

scan_id

FK
engine

ClamAV
signature

text
infected

boolean
This design lets you later add additional engines (YARA, VirusTotal metadata, etc.) without changing the schema.

API endpoints
Scanning
Method

Endpoint

POST

/api/v1/scans

GET

/api/v1/scans

GET

/api/v1/scans/{id}

DELETE

/api/v1/scans/{id}

System
Endpoint

Purpose

/health

Liveness

/ready

DB + ClamAV readiness

/metrics

Prometheus metrics

/version

Application version

A readiness response might be:

{
  "status": "ready",
  "postgres": "healthy",
  "clamav": "healthy",
  "definitions": "2026-09-20T18:22:00Z"
}
Electron workflow

Why PostgreSQL is the preferred persistence layer

PostgreSQL fits the containerized architecture well and provides stronger concurrency, indexing, JSON support, and production-grade operational behavior for a security application. Since the backend is already containerized, the additional operational cost is minimal while the reliability and scale benefits are significant.

I would also add these production features
Alembic for database migrations (never manually edit schema)

pgAdmin 4 as an optional container for database administration

Redis (optional later) for background scan queues

JWT authentication for the Electron client

UUID primary keys instead of integers

Structured JSON logging with correlation IDs for every scan

This would result in a professional desktop application where Electron is the only thing the user installs, while Docker Compose manages PostgreSQL, ClamAV, Grafana, and the observability stack in the background.

Alembic is the expected migration tool for schema evolution, ensuring safe and reviewable changes as the project grows.



Ad

Suggest a UI/UX for the electron app 

For an Electron malware scanner, I'd aim for a SOC analyst aesthetic rather than a consumer antivirus. Think Grafana + Windows Security + Linear: dark theme, minimal distractions, fast navigation, and rich status information.

Design direction
50 Best Dashboard Design Examples for 2026 | Muzli Blog
Intruex | AI-Powered Security Operations
Windows Defender. Protection history: no recent actions. - Resolved Malware Removal Logs - Malwarebytes Forums
5
The app should feel like a professional security tool, with a permanent left navigation, a command-style top bar, and content that prioritizes scan status and system health.

Application layout

Navigation
Dashboard

Quick Scan

Scan History

Quarantine

Virus Definitions

Observability

Settings

Keep the navigation fixed. Electron windows are usually wide enough that a 220–240 px sidebar works well.

1. Dashboard
Browse thousands of Topology Map images for design inspiration | Dribbble
Cyber Security Monitoring Dashboard by Delbueno™ Studio on Dribbble
The Ultimate Guide to Multi-Cluster Kubernetes: Scaling Beyond Single Cluster Limits: Part 3/3 | by Salwan Mohamed | Medium
6
The landing page should answer one question immediately:

Am I protected?

Suggested KPI cards:

Protected Files

12,482
+148 today

Threats Detected

17
3 quarantined

Average Scan

98 ms
Definitions

v27981
Up to date

Below the cards:

Recent scans table

Detection trend chart

ClamAV status indicator

2. Quick Scan page
This is the page users will visit most.

Browse thousands of Drag And Drop UI images for design inspiration | Dribbble
154+ Upload Download Components for React & Tailwind | 21st.dev
How to Run an Antivirus Scan to Detect Viruses?
6
Layout
Drop files or folders
Supports EXE, DLL, ZIP, PDF, DOCX, ISO and entire directories

Current Scan

65%

Scanning Downloads/
842 files
When scanning, animate only the progress bar—not the entire interface.

3. Scan History
Table - EmviUI by MayoralVen on Dribbble
defensia-agent | DigitalOcean Documentation
React Datagrid for Saas web apps and dashboards by Virgil Pana on Dribbble
6
Include filtering similar to Defender XDR.

Column

Notes

Status

Colored badge

Filename

Clickable

SHA-256

Copy button

Signature

Malware family

Time

Relative + exact

Duration

ms

Add:

Search

Date range picker

Status filter

Export CSV

4. Quarantine
Fortect Mac Suite: Quarantine Management - Fortect
How to use Quarantine in Avast Antivirus | Avast
Nemesis Usage Guide - Nemesis Documentation
5
Instead of deleting immediately:

Trojan.Win32.Agent

Quarantined
payload.exe

SHA-256: 8F3A…D92E

Every restore action should require confirmation.

5. Observability page
Since you're already shipping Grafana, embed the dashboards.

Prometheus vs Grafana: The Key Differences to Know | Better Stack Community
Monitoring the world 📊 · James Millner
Using Grafana Loki as a Centralized Logging Solution | The Cyberpunk.Tools Blog
7
Tabs:

Metrics
Logs
Traces
This avoids opening Grafana in a browser.

6. Settings
Organize settings into categories rather than one long page.

Settings
Scanning

Recursive scanning, max file size, exclusions
Updates

FreshClam schedule and proxy
Database

Backup and retention
Telemetry

Enable OTEL and log level
Color palette
Purpose

Color

Background

#0B1220

Surface

#111827

Border

#374151

Primary

#2563EB

Success

#22C55E

Warning

#F59E0B

Danger

#EF4444

Text

#E5E7EB

This palette aligns well with Tailwind's default colors.

Typography
Font: Inter

Sidebar: 14 px Medium

Page titles: 28 px Semibold

KPI numbers: 32–40 px Bold

Tables: 13 px Regular

Keep line heights generous to reduce visual fatigue.

Micro-interactions
These small touches make Electron feel polished:

Hover elevation on cards (2 px)

Progress bar updates smoothly at 60 fps

Success toast: “Scan completed — 842 files scanned”

Threat toast uses amber/red with an action button

Command palette (Ctrl+K) for quick navigation

Global search for scan history

Suggested branding
ClamSentinel is a strong working name.

A simple logo would be a shield containing a stylized clam shell, using blue for trust and green for successful protection.

Window layout

I recommend building the UI with shadcn/ui components on top of Tailwind CSS. They work exceptionally well in Electron, provide accessible primitives (dialogs, tables, toasts, command palette), and give the application a polished native-desktop feel while remaining fully customizable.


Generate AGENTS.md file so I can guild my agent during execution 

# AGENTS.md

## Project

**Name:** ClamSentinel

A desktop malware scanner built with Electron, React, Vite, Tailwind CSS, FastAPI, PostgreSQL, ClamAV, OpenTelemetry, Grafana, Prometheus, Loki, and Tempo.

The Electron application is the only user-facing application. All backend services run as Docker Compose containers.

---

# Primary Objectives

The agent must prioritize the following:

1. Security first
2. Maintainability over cleverness
3. Strong typing
4. Observable services
5. Container-first development
6. Minimal dependencies

When multiple implementations are possible, choose the simplest secure solution.

---

# Architecture

```text
Electron
│
├── React + Vite + Tailwind
│
└── FastAPI REST API
     │
     ├── PostgreSQL
     ├── ClamAV (clamd)
     └── OpenTelemetry
            │
            ├── Prometheus
            ├── Loki
            ├── Tempo
            └── Grafana
```

---

# Repository Structure

```text
clamsentinel/

  AGENTS.md
  docker-compose.yml
  .env.example

  electron/
    main/
    preload/
    renderer/

  frontend/
    src/
      components/
      pages/
      hooks/
      lib/
      types/
      services/

  backend/
    app/
      api/
      core/
      db/
      models/
      schemas/
      services/
      telemetry/
      utils/
    alembic/

  infrastructure/
    grafana/
    prometheus/
    otel/
    loki/
    tempo/

  docs/
```

Never place business logic inside React components.

---

# Technology Requirements

| Layer     | Technology      |
| --------- | --------------- |
| Desktop   | Electron        |
| UI        | React 19        |
| Build     | Vite            |
| Styling   | Tailwind CSS v4 |
| Backend   | FastAPI         |
| ORM       | SQLAlchemy 2.x  |
| Migration | Alembic         |
| Database  | PostgreSQL 17   |
| Scanner   | ClamAV (clamd)  |
| Metrics   | Prometheus      |
| Logs      | Loki            |
| Traces    | Tempo           |
| Telemetry | OpenTelemetry   |

Do not replace these technologies unless explicitly instructed.

---

# Coding Standards

## General

- Use TypeScript everywhere in the frontend.
- Use Python 3.13 type hints everywhere.
- Avoid `any`.
- Avoid global mutable state.
- Prefer composition over inheritance.

## Python

- Use Pydantic v2.
- Use SQLAlchemy ORM.
- One model per file.
- One router per feature.
- Use dependency injection.

Example layout:

```text
api/
    scan.py
    health.py
    metrics.py
```

## React

Use functional components only.

```tsx
export function ScanCard() {
  return (...)
}
```

Never use class components.

---

# UI/UX Guidelines

Theme: Dark by default.

Colors:

| Purpose    | Value   |
| ---------- | ------- |
| Background | #0B1220 |
| Surface    | #111827 |
| Border     | #374151 |
| Primary    | #2563EB |
| Success    | #22C55E |
| Warning    | #F59E0B |
| Danger     | #EF4444 |

Design language:

- Minimal
- Professional
- SOC dashboard aesthetic
- Rounded corners (12–16 px)
- Subtle shadows only
- No excessive animations

---

# Backend Rules

## API Prefix

```
/api/v1
```

Endpoints:

| Method | Endpoint    |
| ------ | ----------- |
| POST   | /scans      |
| GET    | /scans      |
| GET    | /scans/{id} |
| DELETE | /scans/{id} |
| GET    | /health     |
| GET    | /ready      |
| GET    | /metrics    |

Use REST conventions consistently.

---

# Database Rules

Use UUID primary keys.

Example:

```python
id: UUID
```

Never expose internal database IDs to the UI.

Tables:

- scans
- files
- detections
- users (future)

Use Alembic for every schema change.

Never modify production schema manually.

---

# ClamAV Rules

The backend MUST communicate with `clamd`.

Do NOT execute:

- clamscan
- shell commands
- subprocess scanning

Use the daemon protocol only.

Files should be streamed whenever possible.

Maximum upload size must be configurable via environment variable.

---

# Observability Requirements

Every HTTP request must produce:

- Trace
- Structured log
- Metrics

Required telemetry attributes:

| Attribute   | Example     |
| ----------- | ----------- |
| request.id  | UUID        |
| scan.id     | UUID        |
| filename    | invoice.pdf |
| sha256      | hash        |
| duration_ms | 127         |
| result      | CLEAN       |

Logs must be JSON.

Never log file contents.

---

# Docker Rules

Development starts with:

```bash
docker compose up -d
```

The compose stack must include:

- backend
- postgres
- clamav
- otel
- prometheus
- loki
- tempo
- grafana

Electron is NOT containerized.

---

# Environment Variables

Use `.env`.

Example:

```env
POSTGRES_DB=clamsentinel
POSTGRES_USER=scanner
POSTGRES_PASSWORD=change_me

DATABASE_URL=postgresql+psycopg://scanner:change_me@postgres:5432/clamsentinel

CLAMAV_HOST=clamav
CLAMAV_PORT=3310

OTEL_EXPORTER_OTLP_ENDPOINT=http://otel:4318

MAX_UPLOAD_MB=100
```

Never hardcode secrets.

---

# Security Principles

Always validate:

- MIME type
- Extension
- File size

Always compute SHA-256.

Never trust client input.

Never render uploaded files.

Use parameterized SQL only.

Sanitize all filenames.

---

# Frontend State

Preferred:

- TanStack Query for server state
- React Context for application state
- Local component state for UI only

Do not duplicate API data in multiple stores.

---

# Error Handling

Backend returns:

```json
{
  "error": {
    "code": "SCAN_FAILED",
    "message": "Unable to scan file."
  }
}
```

Never expose stack traces to users.

Frontend displays friendly messages.

---

# Testing Expectations

Backend:

- pytest
- API tests
- Service tests

Frontend:

- Vitest
- React Testing Library

Critical paths requiring tests:

- File upload
- Scan result parsing
- Database writes
- Health endpoints

---

# Performance Targets

| Operation         | Target  |
| ----------------- | ------- |
| Health endpoint   | <50 ms  |
| Scan API overhead | <20 ms  |
| Dashboard load    | <1 s    |
| History query     | <200 ms |

---

# Accessibility

Must support:

- Keyboard navigation
- Screen readers
- High contrast
- Focus indicators

Avoid color as the only status indicator.

---

# Git Workflow

Main branches:

```text
main
develop
feature/*
```

Commit format:

```text
feat:
fix:
refactor:
docs:
test:
chore:
```

Example:

```text
feat: add quarantine API
```

---

# Documentation Rule

Any new feature must update:

- OpenAPI documentation
- README (if user-facing)
- AGENTS.md if architectural rules change

---

# Agent Execution Checklist

Before completing any task, verify:

- [ ] Type-safe implementation
- [ ] No hardcoded secrets
- [ ] Docker Compose still works
- [ ] OpenTelemetry instrumentation preserved
- [ ] API documented
- [ ] Database migration created (if needed)
- [ ] UI follows design system
- [ ] Errors handled gracefully
- [ ] Logs are structured JSON
- [ ] Code is production-ready

The default assumption is that this project targets production quality rather than prototype code.
For the Electron app UI/UX, here’s one CI/CD platform option for builds.



Ad

