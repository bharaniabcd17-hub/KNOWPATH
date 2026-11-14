# PROJECT-EVOLVE

> **Evidence-based learner intelligence platform** — model what a learner demonstrably knows, find gaps, recommend the next action, always explainably.

---

## Overview

PROJECT-EVOLVE is a full-stack adaptive learning platform that builds a **Learner Twin** — a living, evidence-grounded model of a learner's knowledge state. The system ingests evidence from multiple sources (self-reports, AI assessments, graded exercises), applies a deterministic scoring engine, detects knowledge gaps against a Skill Genome graph, and surfaces personalised missions and roadmaps.

**Key principles:**
- Evidence is never fabricated. All scores are computed deterministically; LLMs may only paraphrase results.
- Evidence trust levels: `self_reported` < `ai_estimated` < `assessment_verified` — never upgraded implicitly.
- Every AI output is schema-validated, labeled, and traceable via `agent_executions`.
- No outcome guarantees (jobs, grades, salaries).
- All user data is scoped by `user_id`; no cross-user access.

> ⚠️ **Content seed v0 — requires subject-expert review before public launch.**

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 15 (App Router) · TypeScript strict · Tailwind CSS · Radix UI |
| Backend | FastAPI · Pydantic v2 · SQLAlchemy 2 (async) · Alembic |
| Database | PostgreSQL 16 + pgvector |
| AI | Anthropic Claude via `LLMClient` interface (mock default) |
| Auth | JWT (python-jose) + Supabase Auth |
| Infra | Docker Compose (local dev) · GitHub Actions CI |

---

## Project Structure

```
hackathon/
├── backend/           # FastAPI application
│   ├── app/
│   │   ├── domains/   # Feature domains (auth, users, genome, …)
│   │   ├── agents/    # LLM agent runners
│   │   ├── scoring/   # Deterministic scoring engine
│   │   └── jobs/      # Background jobs
│   ├── alembic/       # DB migrations
│   ├── tests/         # Pytest suites
│   └── scripts/       # Seed & utility scripts
├── frontend/          # Next.js application
│   └── src/
│       ├── app/       # App Router pages & layouts
│       ├── components/
│       └── styles/
├── content/           # YAML knowledge-base seeds
├── docs/              # Architecture, scoring, security, API docs
├── e2e/               # Playwright end-to-end tests
├── .github/workflows/ # CI
├── docker-compose.yml
├── Makefile
└── .env.example
```

---

## Quick Start

### Prerequisites
- Python 3.12+
- Node.js 20+ and pnpm 9+
- Docker (for PostgreSQL) or a local PostgreSQL 16 instance with pgvector

### Setup

```bash
# 1. Clone and enter repo
git clone <repo-url> && cd hackathon

# 2. Copy env template and fill in values
cp .env.example .env

# 3. Start database
docker compose up -d

# 4. Install all dependencies, run migrations
make setup

# 5. Start dev servers (backend :8000, frontend :3000)
make dev
```

### Common Commands

| Command | Description |
|---------|-------------|
| `make setup` | Install deps + run DB migrations |
| `make dev` | Start backend + frontend dev servers |
| `make test` | Run pytest + jest |
| `make lint` | Ruff + mypy + ESLint |
| `make migrate` | Apply Alembic migrations |
| `make seed` | Seed database with content v0 |
| `make e2e` | Run Playwright E2E tests |
| `make format` | Auto-format all code |

---

## Documentation

| Doc | Description |
|-----|-------------|
| [docs/architecture.md](docs/architecture.md) | System design, component diagram, data flow |
| [docs/scoring.md](docs/scoring.md) | Scoring engine formulas (Section 7) |
| [docs/security.md](docs/security.md) | Auth, secrets, rate limiting, data isolation |
| [docs/api.md](docs/api.md) | REST API overview and conventions |
| [docs/decisions.md](docs/decisions.md) | Architecture Decision Records |

---

## Contributing

- All DB changes via Alembic migrations — no manual schema edits.
- `ruff + mypy + ESLint + tsc` must pass before marking any task `done-verified`.
- Record significant decisions in `docs/decisions.md`.
- See [AGENTS.md](AGENTS.md) for full project rules.
- Track progress in [CHECKLIST.md](CHECKLIST.md).
