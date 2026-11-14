# PROJECT-EVOLVE / KNOWPATH Checklist

> Status values: `todo` | `in-progress` | `done-verified` | `blocked`

## Phase 1 – Foundation & Vertical Slice

| # | Task | Status | Verification Proof |
|---|------|--------|---------------------|
| 1 | Repo scaffold: config files, Makefile, CI, root docs | done-verified | Verified `pyproject.toml`, `.env.example`, `Makefile`, `.github/workflows/ci.yml`, `ARCHITECTURE.md` |
| 2 | Database schema & migrations (all 21 models) | done-verified | Initialized 21 SQLAlchemy 2 async models in `backend/app/models.py`, verified via `init_db.py` |
| 3 | Auth domain: JWT login, register, 18+ age gate, session | done-verified | Tested in `tests/test_auth.py` (5 passed) and `test_e2e_journey.py` |
| 4 | User & Profile domain: preferences, weekly hours, data export, delete | done-verified | Tested in `test_e2e_journey.py` (profile fetch, goal setting, GDPR export, hard deletion) |
| 5 | Knowledge Genome: 79 concepts, 118 prerequisite edges, DAG traversal | done-verified | Verified by `content/validate.py` (cycle-free DAG) and `test_scoring.py` |
| 6 | Evidence & Assessment: question ingest, server grading, misconceptions | done-verified | 430 questions, 34 tagged misconceptions, tested in `test_scoring.py` & `test_e2e_journey.py` |
| 7 | Scoring engine: deterministic Beta-distribution, recency decay, credible interval | done-verified | 10 tests passed in `test_scoring.py` (Beta update, speed penalty, dispute factor, 80% CI) |
| 8 | Gap detection: topological prerequisite gap ranking + foundation bonus (1.25x) | done-verified | Tested in `test_scoring.py::test_gap_detection_ranking` |
| 9 | Cognitive Twin: probabilistic state, snapshots, "why this score" explainability | done-verified | Tested in `test_isolation.py::test_user_a_cannot_read_user_b_twin` & `test_e2e_journey.py` |
| 10 | Roadmap domain: goal setting, topologically ranked missing concepts | done-verified | Tested in `test_e2e_journey.py` & `backend/app/domains/roadmap/router.py` |
| 11 | Missions domain: 15-45 min micro-tasks, reading, completion evidence | done-verified | Tested in `test_e2e_journey.py` (`/api/v1/missions/today` and `/complete`) |
| 12 | Companion domain: grounded educational tutor with `[AI-Generated]` badge | done-verified | Tested in `test_agents.py` (5 passed: promise blocking, AI label, source citations) |
| 13 | Reviews domain: SM-2 spaced retention queue & interval updates | done-verified | Tested in `test_scoring.py::test_retention_sm2_pass_and_fail` |
| 14 | Disputes domain: challenge scores/questions, 0.5x weight halving | done-verified | Tested in `test_scoring.py::test_dispute_reduces_weight_by_half` & `test_e2e_journey.py` |
| 15 | Admin domain: user management, audit logs, dispute desk, token cost tracking | done-verified | Tested in `test_isolation.py::test_admin_can_access_admin_endpoints` |
| 16 | Frontend: design system, Tailwind, layout, theme, Navbar, Footer, Sidebar, Header | done-verified | Tested via `tsc --noEmit` and production `next build` (compiled successfully) |
| 17 | Frontend: Auth flows (login, register with 18+ DOB gate, explicit consent) | done-verified | Built in `src/app/(auth)/login` & `register`, compiled in Next.js bundle |
| 18 | Frontend: Dashboard Overview + Cognitive Twin visualization & "Why this score" | done-verified | Built in `src/app/(dashboard)/dashboard` & `twin`, 80% CI & evidence inspect |
| 19 | Frontend: Roadmap + Daily Missions + Knowledge Genome + Diagnostic runner | done-verified | Built in `src/app/(dashboard)/roadmap`, `missions`, `genome`, `assessment/diagnostic` |
| 20 | E2E integration test: full vertical slice lifecycle verification | done-verified | Automated async test `tests/test_e2e_journey.py` passed in 0.88s |
| 21 | Content seed: 79 concepts, 118 edges, 34 misconceptions, 430 questions | done-verified | Validated with `content/validate.py` (0 errors), seeded into `evolve_dev.db` |
