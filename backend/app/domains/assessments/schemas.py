"""Schemas for Assessments domain."""
from __future__ import annotations

from typing import Any, Literal, Optional
from uuid import UUID

from pydantic import BaseModel


class AttemptStart(BaseModel):
    kind: Literal["diagnostic", "quiz", "mission_check"] = "diagnostic"
    target_concept_slug: Optional[str] = None  # For targeted quizzes


class AssessmentItem(BaseModel):
    attempt_id: UUID
    item_number: int
    total_items: int  # e.g. 15-20 for diagnostic
    question_id: str
    concept_slug: str
    concept_title: str
    type: str  # multiple_choice | multi_select | code_reading | predict_bug
    stem: str
    options: dict[str, str]  # Note: correct answer is NEVER exposed in the question payload


class SubmitAnswerRequest(BaseModel):
    attempt_id: UUID
    question_id: str
    answer: Any  # Option key e.g. "A" or list of keys
    time_ms: int = 15000


class SubmitAnswerResponse(BaseModel):
    attempt_id: UUID
    question_id: str
    correct: bool
    explanation: str
    misconception_flagged: Optional[dict[str, str]] = None  # If distractor had a misconception
    is_completed: bool
    next_item: Optional[AssessmentItem] = None
    mastery_updated: Optional[dict[str, Any]] = None


class AttemptResult(BaseModel):
    attempt_id: UUID
    kind: str
    total_answered: int
    correct_count: int
    accuracy: float
    completed: bool
    summary_by_concept: list[dict[str, Any]]
