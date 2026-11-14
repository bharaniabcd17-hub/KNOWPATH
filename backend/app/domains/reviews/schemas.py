"""Schemas for Spaced Revision / Reviews domain."""
from __future__ import annotations

import datetime
from uuid import UUID

from pydantic import BaseModel


class ReviewItem(BaseModel):
    concept_slug: str
    concept_title: str
    difficulty: int
    due_at: datetime.datetime
    interval_days: float
    ease: float
    is_overdue: bool
    last_result: str | None = None


class ReviewSubmit(BaseModel):
    concept_slug: str
    result: str  # "pass" | "fail"
