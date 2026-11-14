"""Schemas for Cognitive Twin domain."""
from __future__ import annotations

import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel


class TopEvidenceItem(BaseModel):
    id: UUID
    source_type: str  # self_reported | ai_estimated | assessment_verified
    value: float
    weight: float
    observed_at: datetime.datetime
    disputed: bool = False


class WhyScorePanel(BaseModel):
    concept_slug: str
    mastery: float
    confidence: float
    interval_low: float
    interval_high: float
    alpha: float
    beta: float
    formula_explanation: str
    top_evidence: list[TopEvidenceItem]
    source_mix: dict[str, int]
    possible_foundation_gap: bool = False


class MasteryStateDetail(BaseModel):
    concept_slug: str
    concept_title: str
    difficulty: int
    mastery: float
    confidence: float
    interval_low: float
    interval_high: float
    evidence_count: int
    why_panel: WhyScorePanel
    possible_foundation_gap: bool = False
    updated_at: datetime.datetime


class TwinPageData(BaseModel):
    user_id: UUID
    overall_mastery: float
    overall_confidence: float
    concepts_evaluated: int
    total_concepts: int
    concepts: list[MasteryStateDetail]
    snapshots_count: int


class SnapshotItem(BaseModel):
    id: UUID
    taken_at: datetime.datetime
    trigger: str
    state: dict[str, Any]
