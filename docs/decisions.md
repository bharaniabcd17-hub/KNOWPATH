# Architecture Decision Records (ADRs)

This document records the architectural and design decisions made for PROJECT-EVOLVE.

---

## ADR-001: Next.js (App Router) + FastAPI Architecture
- **Date**: 2026-11-14
- **Status**: Accepted
- **Context**: PROJECT-EVOLVE requires a high-performance, reactive UI with modern server-side rendering and static asset capabilities, paired with a deterministic, scientifically sound Python backend for Bayesian scoring, adaptive item selection, and AI integrations.
- **Decision**: Use Next.js 15 (App Router, TypeScript strict, Tailwind CSS, Radix UI) for the frontend, and FastAPI (Pydantic v2, SQLAlchemy 2 async, Alembic) for the backend.
- **Reason**: Python provides native access to scientific libraries (`scipy`, `numpy`) required for Beta distribution updates, while FastAPI offers async I/O, OpenAPI auto-documentation, and strict type safety with Pydantic v2. Next.js App Router provides optimal UX and component isolation.

---

## ADR-002: Deterministic Scoring Engine over LLM Computations
- **Date**: 2026-11-14
- **Status**: Accepted
- **Context**: Non-negotiable mission rule: scores must be verifiable, deterministic, and free from LLM hallucination or stochastic drift.
- **Decision**: All mastery scores, confidence bounds, spacing intervals, and gap detection metrics are computed strictly using deterministic algorithms (Beta conjugate priors, SM-2 modified spaced repetition, and directed acyclic graph traversal). LLMs are strictly restricted to paraphrasing explanations and generating draft questions.
- **Reason**: Guarantees zero hallucinations in student evaluation, explainability for disputes, and reproducibility across platform runs.

---

## ADR-003: Three-Tier Evidence Hierarchy
- **Date**: 2026-11-14
- **Status**: Accepted
- **Context**: Learners submit claims through various channels with differing degrees of reliability.
- **Decision**: Maintain a strict evidence source hierarchy:
  1. `self_reported` (weight: 0.15)
  2. `ai_estimated` (weight: 0.45)
  3. `assessment_verified` (weight: 1.00)
  Evidence sources can never be upgraded implicitly.
- **Reason**: Protects against over-confidence and self-report bias; ensures mastery calculations place highest trust in verified assessment results.

---

## ADR-004: PostgreSQL with pgvector for Relational and Semantic Storage
- **Date**: 2026-11-14
- **Status**: Accepted
- **Context**: The platform needs relational consistency for users, attempts, evidence, and scores, alongside vector similarity search for semantic question retrieval and companion memory.
- **Decision**: Single primary database running PostgreSQL 16 with the `pgvector` extension.
- **Reason**: Eliminates the operational overhead of dual-database architecture while providing native relational integrity, transactional ACID guarantees, and indexed cosine vector search.

---

## ADR-005: Tenant and User Isolation
- **Date**: 2026-11-14
- **Status**: Accepted
- **Context**: Compliance and student privacy requirement: learners must never access each other's evidence, scores, twin snapshots, or roadmaps.
- **Decision**: Enforce row-level query scoping by `user_id` at the repository/service layer on every user-owned query.
- **Reason**: Prevents horizontal privilege escalation and data leakage.
