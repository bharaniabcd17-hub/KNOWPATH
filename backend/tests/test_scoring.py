"""Unit tests for deterministic scoring engine and explainable algorithms.

Tests:
- Evidence weighting (Section 7.1)
- Beta distribution mastery & confidence (Section 7.2)
- Credible interval calculation
- Gap detection & priority ranking (Section 7.3)
- Retention interval calculation (SM-2, Section 7.4)
- Adaptive item selection (Section 7.5)
- Fairness test: demographic attributes not in scoring inputs (Section 9)
"""
from __future__ import annotations

import uuid
from app.scoring.engine import (
    compute_credible_interval,
    compute_evidence_weight,
    recency_factor,
    reliability_factor,
    update_mastery,
    EvidenceItem,
)
from app.scoring.gap_detector import (
    Concept as ScoringConcept,
    ConceptEdge as ScoringEdge,
    MasteryState as ScoringMastery,
    detect_gaps,
)
from app.scoring.item_selector import Question as ScoringQuestion, select_next_item
from app.scoring.retention import compute_next_interval


def test_evidence_weight_base_and_sources():
    """Verify base weights: self_reported = 0.15, ai_estimated = 0.35, assessment_verified = 1.0."""
    w_self = compute_evidence_weight("self_reported", age_days=0, discrimination=1.0, time_ms=30000)
    w_ai = compute_evidence_weight("ai_estimated", age_days=0, discrimination=1.0, time_ms=30000)
    w_ver = compute_evidence_weight("assessment_verified", age_days=0, discrimination=1.0, time_ms=30000)

    assert abs(w_self - 0.15) < 1e-4
    assert abs(w_ai - 0.35) < 1e-4
    assert abs(w_ver - 1.0) < 1e-4


def test_recency_decay_half_life():
    """Verify 60-day half life decay: recency(60) == 0.5."""
    r0 = recency_factor(0)
    r60 = recency_factor(60)
    r120 = recency_factor(120)

    assert abs(r0 - 1.0) < 1e-4
    assert abs(r60 - 0.5) < 1e-4
    assert abs(r120 - 0.25) < 1e-4


def test_reliability_speed_penalty():
    """Answers under 3 seconds receive reliability reduction; floor is 0.3."""
    rel_normal = reliability_factor(discrimination=0.8, time_ms=15000)
    rel_fast = reliability_factor(discrimination=0.8, time_ms=1500)

    assert rel_normal == 0.8
    assert rel_fast == 0.4  # Halved due to fast response time
    assert reliability_factor(discrimination=0.1, time_ms=500) == 0.3  # Floor at 0.3


def test_dispute_reduces_weight_by_half():
    """Per Section 7.1: dispute_factor is 0.5 while dispute is open."""
    w_normal = compute_evidence_weight("assessment_verified", age_days=0, discrimination=1.0, time_ms=30000, disputed=False)
    w_disputed = compute_evidence_weight("assessment_verified", age_days=0, discrimination=1.0, time_ms=30000, disputed=True)

    assert abs(w_disputed - (w_normal * 0.5)) < 1e-4


def test_beta_mastery_update():
    """Verify deterministic Beta update: mastery = alpha / (alpha + beta)."""
    # Start with prior alpha=1.0, beta=1.0 (mastery = 0.5)
    item_correct = EvidenceItem(source_type="assessment_verified", value=1.0, age_days=0, discrimination=1.0, time_ms=30000)
    res = update_mastery(alpha=1.0, beta=1.0, evidence_items=[item_correct])

    # alpha becomes 1.0 + 1.0 = 2.0; beta stays 1.0; mastery = 2/3 = 0.6667
    assert abs(res.alpha - 2.0) < 1e-4
    assert abs(res.beta - 1.0) < 1e-4
    assert abs(res.mastery - (2.0 / 3.0)) < 1e-4
    assert 0.0 <= res.confidence <= 1.0


def test_credible_interval():
    """Credible interval should narrow as more evidence accumulates."""
    low1, high1 = compute_credible_interval(alpha=1.0, beta=1.0, ci=0.80)
    low2, high2 = compute_credible_interval(alpha=20.0, beta=5.0, ci=0.80)

    width1 = high1 - low1
    width2 = high2 - low2
    assert width2 < width1  # More evidence narrows the interval


def test_gap_detection_ranking():
    """Concepts with low mastery (<0.6) or low confidence (<0.3) are detected as gaps and ranked by impact."""
    c1 = uuid.uuid4()
    c2 = uuid.uuid4()
    c3 = uuid.uuid4()

    edges = [
        ScoringEdge(from_id=c1, to_id=c2),  # c1 is prerequisite for c2
        ScoringEdge(from_id=c2, to_id=c3),  # c2 is prerequisite for c3
    ]

    mastery = {
        c1: ScoringMastery(concept_id=c1, mastery=0.3, confidence=0.8),  # Weak foundation gap
        c2: ScoringMastery(concept_id=c2, mastery=0.5, confidence=0.8),
        c3: ScoringMastery(concept_id=c3, mastery=0.8, confidence=0.8),
    }

    concepts = {
        c1: ScoringConcept(id=c1, slug="c1", title="Foundations", difficulty=0.2),
        c2: ScoringConcept(id=c2, slug="c2", title="Intermediate", difficulty=0.4),
        c3: ScoringConcept(id=c3, slug="c3", title="Advanced Target", difficulty=0.6),
    }

    gaps = detect_gaps(
        target_concept_ids=[c3],
        concept_edges=edges,
        mastery_states=mastery,
        all_concepts=concepts,
    )

    gap_slugs = [g.slug for g in gaps]
    assert "c1" in gap_slugs
    assert "c2" in gap_slugs
    assert "c3" not in gap_slugs  # c3 is mastered (0.8)

    # c1 blocks c2 and c3, so it receives foundation bonus and high priority
    assert gaps[0].slug == "c1"
    assert gaps[0].blocking_count >= 1


def test_retention_sm2_pass_and_fail():
    """SM-2 retention rule: pass multiplies interval by ease; fail resets interval to 1.0 day."""
    # Pass case
    interval, ease = compute_next_interval(previous_interval_days=2.0, ease=2.3, result="pass")
    assert interval == 2.0 * 2.3  # 4.6
    assert abs(ease - 2.45) < 1e-4  # ease + 0.15

    # Fail case
    interval_fail, ease_fail = compute_next_interval(previous_interval_days=10.0, ease=2.45, result="fail")
    assert interval_fail == 1.0  # Reset to 1 day
    assert abs(ease_fail - 2.30) < 1e-4  # ease - 0.15


def test_adaptive_item_selection():
    """Item selector prioritizes frontier concepts with highest uncertainty."""
    c_easy = uuid.uuid4()
    c_hard = uuid.uuid4()

    q1 = ScoringQuestion(id=uuid.uuid4(), concept_id=c_easy, difficulty=0.3, discrimination=0.6, status="approved")
    q2 = ScoringQuestion(id=uuid.uuid4(), concept_id=c_hard, difficulty=0.8, discrimination=0.6, status="approved")

    # c_easy has high uncertainty (confidence=0.0)
    mastery = {
        c_easy: ScoringMastery(concept_id=c_easy, mastery=0.5, confidence=0.0),
        c_hard: ScoringMastery(concept_id=c_hard, mastery=0.8, confidence=0.9),
    }

    selected = select_next_item(
        mastery_states=mastery,
        concept_edges=[],
        target_concepts=[c_easy, c_hard],
        available_questions=[q1, q2],
        recently_seen_question_ids=[],
    )

    assert selected is not None
    assert selected.concept_id == c_easy  # Targeted concept with highest uncertainty


def test_fairness_no_demographic_inputs():
    """Fairness verification: Ensure scoring and gap detection take only learning evidence."""
    import inspect
    from app.scoring.engine import compute_evidence_weight, update_mastery
    from app.scoring.gap_detector import detect_gaps

    weight_params = inspect.signature(compute_evidence_weight).parameters.keys()
    update_params = inspect.signature(update_mastery).parameters.keys()
    gap_params = inspect.signature(detect_gaps).parameters.keys()

    forbidden_inputs = {"gender", "race", "age", "ethnicity", "country", "location", "demographic", "income"}

    assert forbidden_inputs.isdisjoint(weight_params)
    assert forbidden_inputs.isdisjoint(update_params)
    assert forbidden_inputs.isdisjoint(gap_params)
