# AGENTS.md - Persistent project rules for PROJECT-EVOLVE

## Mission
Evidence-based learner intelligence: model what a learner demonstrably knows, find gaps, recommend the next action, always explainably.

## Non-negotiable rules
- Read CHECKLIST.md at session start. Update it after every task.
- Only statuses: todo | in-progress | done-verified | blocked.
- done-verified requires executed tests or recorded manual proof.
- Never fake integrations, credentials, test results or data. Mock adapters must be labeled.
- Scores are computed deterministically (see docs/scoring.md). LLMs may paraphrase, never compute.
- Every AI output is schema-validated, labeled as AI, and traceable in agent_executions.
- Evidence source types are never upgraded implicitly: self_reported < ai_estimated < assessment_verified.
- No outcome guarantees (jobs, grades, salaries).
- No cross-user data access. All user-owned queries are scoped by user id.
- Out-of-scope items are not stubbed or shown in the UI.

## Stack
Next.js (App Router) + TypeScript strict + Tailwind; FastAPI + Pydantic v2 + SQLAlchemy 2 + Alembic; PostgreSQL + pgvector; LLMClient / EmbeddingClient interfaces with mock implementations.

## Conventions
- Backend modules by domain under backend/app/domains/<domain>/{router,service,repo,schemas}.py.
- All DB changes via Alembic migrations. No manual schema edits.
- Config via environment. .env.example is the source of truth.
- Ruff + mypy + ESLint + tsc must pass before marking a task done.
- Tests live beside domain code (backend/tests/<domain>) and in e2e/.
- Record architecture decisions in docs/decisions.md (date, decision, reason).

## Commands
make setup | make dev | make test | make lint | make migrate | make seed | make e2e

## Handoff
If stopping early, write HANDOFF.md: done, next, blockers, known bugs.
