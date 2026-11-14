"""Scoring engine — deterministic Beta-distribution mastery computation.

LLMs never compute scores. All formulas are from docs/scoring.md.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any
from uuid import UUID

try:
    from scipy.stats import beta as beta_dist  # type: ignore[import-untyped]
    HAVE_SCIPY = True
except ImportError:
    HAVE_SCIPY = False

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
BASE_WEIGHTS: dict[str, float] = {
    "self_reported": 0.15,
    "ai_estimated": 0.35,
    "assessment_verified": 1.0,
}
HALF_LIFE_DAYS: float = 60.0
PREREQUISITE_MASTERY_THRESHOLD: float = 0.4


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------
@dataclass
class EvidenceItem:
    source_type: str  # self_reported | ai_estimated | assessment_verified
    value: float  # 0.0 – 1.0  (correct fraction)
    age_days: float
    discrimination: float  # IRT-style, 0.0 – 1.0
    time_ms: int
    disputed: bool = False
    evidence_id: UUID | None = None


@dataclass
class MasteryResult:
    mastery: float
    confidence: float
    interval_low: float
    interval_high: float
    alpha: float
    beta: float


@dataclass
class WhyPanel:
    mastery: float
    confidence: float
    source_mix: dict[str, int]
    top_evidence: list[dict[str, Any]]
    prerequisite_gap_flags: list[str]


# ---------------------------------------------------------------------------
# Core formulas
# ---------------------------------------------------------------------------

def recency_factor(age_days: float, half_life_days: float = HALF_LIFE_DAYS) -> float:
    """Exponential decay: 1.0 today, 0.5 after half_life_days."""
    return 0.5 ** (age_days / half_life_days)


def reliability_factor(discrimination: float, time_ms: int, expected_time_ms: int = 30000) -> float:
    """Very fast answers reduce reliability. Floor is 0.3."""
    base = min(1.0, discrimination if discrimination > 0 else 0.5)
    if time_ms < 3000:  # under 3 seconds is suspiciously fast
        base = max(0.3, base * 0.5)
    return max(0.3, base)


def compute_evidence_weight(
    source_type: str,
    age_days: float,
    discrimination: float,
    time_ms: int,
    disputed: bool = False,
) -> float:
    """Compute the weight for a single evidence item."""
    base = BASE_WEIGHTS[source_type]
    recency = recency_factor(age_days)
    reliability = reliability_factor(discrimination, time_ms)
    dispute_factor = 0.5 if disputed else 1.0
    return base * recency * reliability * dispute_factor


def compute_credible_interval(alpha: float, beta_val: float | None = None, ci: float = 0.80, *, beta: float | None = None) -> tuple[float, float]:
    """Return (low, high) of the credible interval using Beta distribution or normal approximation."""
    effective_beta = beta if beta is not None else (beta_val if beta_val is not None else 1.0)
    if HAVE_SCIPY:
        tail = (1.0 - ci) / 2.0
        low = float(beta_dist.ppf(tail, alpha, effective_beta))
        high = float(beta_dist.ppf(1.0 - tail, alpha, effective_beta))
        return (low, high)
    
    # Fallback approximation for 80% CI (z ~ 1.28155)
    mean = alpha / (alpha + effective_beta)
    var = (alpha * effective_beta) / (((alpha + effective_beta) ** 2) * (alpha + effective_beta + 1))
    std = math.sqrt(var)
    z = 1.28155
    low = max(0.0, mean - z * std)
    high = min(1.0, mean + z * std)
    return (low, high)


def update_mastery(alpha: float, beta_val: float | None = None, evidence_items: list[EvidenceItem] | None = None, *, beta: float | None = None) -> MasteryResult:
    """Update Beta distribution parameters from evidence and return mastery result."""
    effective_beta = beta if beta is not None else (beta_val if beta_val is not None else 1.0)
    items = evidence_items or []
    for item in items:
        w = compute_evidence_weight(
            source_type=item.source_type,
            age_days=item.age_days,
            discrimination=item.discrimination,
            time_ms=item.time_ms,
            disputed=item.disputed,
        )
        alpha += w * item.value
        effective_beta += w * (1.0 - item.value)

    mastery = alpha / (alpha + effective_beta)

    low, high = compute_credible_interval(alpha, effective_beta)
    interval_width = high - low
    confidence = max(0.0, 1.0 - interval_width)

    return MasteryResult(
        mastery=mastery,
        confidence=confidence,
        interval_low=low,
        interval_high=high,
        alpha=alpha,
        beta=effective_beta,
    )


def prerequisite_gap_flag(
    concept_mastery: float,
    prerequisite_masteries: dict[str, float],
) -> list[str]:
    """Flag concepts where mastery is high but prerequisite is below threshold."""
    flags: list[str] = []
    if concept_mastery > 0.6:
        for prereq_slug, prereq_mastery in prerequisite_masteries.items():
            if prereq_mastery < PREREQUISITE_MASTERY_THRESHOLD:
                flags.append(f"possible_foundation_gap:{prereq_slug}")
    return flags


def get_top_evidence(evidence_items: list[EvidenceItem], top_n: int = 3) -> list[dict[str, Any]]:
    """Return the top N contributing evidence items by weight."""
    weighted = []
    for item in evidence_items:
        w = compute_evidence_weight(
            source_type=item.source_type,
            age_days=item.age_days,
            discrimination=item.discrimination,
            time_ms=item.time_ms,
            disputed=item.disputed,
        )
        weighted.append({
            "evidence_id": str(item.evidence_id) if item.evidence_id else None,
            "source_type": item.source_type,
            "value": item.value,
            "weight": w,
            "age_days": item.age_days,
            "disputed": item.disputed,
        })
    weighted.sort(key=lambda x: x["weight"], reverse=True)
    return weighted[:top_n]


def get_source_mix(evidence_items: list[EvidenceItem]) -> dict[str, int]:
    """Count evidence by source type."""
    mix: dict[str, int] = {"self_reported": 0, "ai_estimated": 0, "assessment_verified": 0}
    for item in evidence_items:
        mix[item.source_type] = mix.get(item.source_type, 0) + 1
    return mix


def compute_why_panel(
    alpha: float,
    beta_val: float,
    evidence_items: list[EvidenceItem],
    prerequisite_masteries: dict[str, float] | None = None,
) -> WhyPanel:
    """Return structured explanation data for the why panel."""
    result = update_mastery(alpha, beta_val, evidence_items)
    prereq_masteries = prerequisite_masteries or {}
    flags = prerequisite_gap_flag(result.mastery, prereq_masteries)
    return WhyPanel(
        mastery=result.mastery,
        confidence=result.confidence,
        source_mix=get_source_mix(evidence_items),
        top_evidence=get_top_evidence(evidence_items),
        prerequisite_gap_flags=flags,
    )
