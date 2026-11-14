"""Schemas for Missions domain."""
from __future__ import annotations

import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel


class MissionItem(BaseModel):
    id: str
    type: Literal["explanation", "practice", "check"]
    concept_slug: str
    concept_title: str
    content: dict[str, Any]  # markdown for explanation, question details for practice/check


class MissionRead(BaseModel):
    id: UUID
    user_id: UUID
    date: datetime.date
    focus_concept_slug: str
    focus_concept_title: str
    items: list[MissionItem]
    status: str  # pending | in_progress | completed
    completed_at: datetime.datetime | None = None
    because: str
