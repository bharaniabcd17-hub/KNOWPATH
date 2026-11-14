# KNOWPATH / PROJECT-EVOLVE — Verification & Test Report

**Execution Date:** November 2026  
**Test Suite:** `pytest tests/ -v`  
**Test Engine:** pytest 8.3.4 + pytest-asyncio 0.25.0 + httpx 0.28.1  
**Results:** **24 passed in 6.90s (100% pass rate)**

---

## 1. Test Execution Summary

| Domain / Suite | Test Count | Status | Description |
|----------------|------------|--------|-------------|
| `test_scoring.py` | 10 | **PASSED** | Deterministic formulas: weights, decay, beta update, credible intervals, SM-2, item selector |
| `test_auth.py` | 5 | **PASSED** | Registration, 18+ age gate, 409 conflict, JWT login, protected route rejection |
| `test_isolation.py` | 4 | **PASSED** | Multi-tenant isolation between User A & B, RBAC 403 checks, cross-attempt protection |
| `test_agents.py` | 5 | **PASSED** | Mock LLM labeling, promise filter, schema validation, teaching orchestrator & audit logging |
| **Total** | **24** | **100% PASS** | **Zero failures, zero warnings** |

---

## 2. Detailed Test Log Evidence

```
tests/test_scoring.py::test_source_type_weights PASSED                   [  4%]
tests/test_scoring.py::test_recency_decay PASSED                         [  8%]
tests/test_scoring.py::test_speed_penalty PASSED                         [ 12%]
tests/test_scoring.py::test_dispute_halving PASSED                       [ 16%]
tests/test_scoring.py::test_beta_distribution_update PASSED              [ 20%]
tests/test_scoring.py::test_credible_interval PASSED                     [ 25%]
tests/test_scoring.py::test_gap_ranking_with_foundation_bonus PASSED     [ 29%]
tests/test_scoring.py::test_sm2_retention_calculation PASSED             [ 33%]
tests/test_scoring.py::test_adaptive_item_selector PASSED                 [ 37%]
tests/test_scoring.py::test_subpopulation_fairness PASSED                 [ 41%]
tests/test_auth.py::test_register_success PASSED                         [ 45%]
tests/test_auth.py::test_register_underage_rejected PASSED               [ 50%]
tests/test_auth.py::test_register_duplicate_email PASSED                 [ 54%]
tests/test_auth.py::test_login_success_and_failure PASSED                [ 58%]
tests/test_auth.py::test_protected_route_requires_auth PASSED           [ 62%]
tests/test_isolation.py::test_user_twin_data_isolation PASSED           [ 66%]
tests/test_isolation.py::test_learner_cannot_access_admin PASSED        [ 70%]
tests/test_isolation.py::test_admin_can_access_admin PASSED              [ 75%]
tests/test_isolation.py::test_user_cannot_submit_to_others_attempt PASSED [ 79%]
tests/test_agents.py::test_mock_llm_deterministic_output PASSED          [ 83%]
tests/test_agents.py::test_quality_safety_agent_blocks_guarantees PASSED [ 87%]
tests/test_agents.py::test_quality_safety_agent_enforces_ai_label PASSED [ 91%]
tests/test_agents.py::test_quality_safety_agent_validates_draft_question PASSED [ 95%]
tests/test_agents.py::test_orchestrator_teaching_and_logging PASSED     [100%]

============================== 24 passed in 6.90s ==============================
```

---

## 3. Curriculum Content Verification

Executed `python content/validate.py`:
- **Concepts:** 79 concepts validated.
- **Prerequisite Edges:** 118 edges checked for cycle-free DAG topology (topological sort succeeded).
- **Misconceptions:** 34 misconception trap definitions verified.
- **Questions:** 430 assessment items validated across option keys, correct answers, and tagged distractors.
