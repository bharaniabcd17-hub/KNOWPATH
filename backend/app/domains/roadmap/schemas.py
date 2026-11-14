"""Schemas for Roadmap and Gap detection domain."""
from __future__ import annotations

import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel


class RoadmapItemDetail(BaseModel):
    id: UUID
    position: int
    concept_slug: str
    concept_title: str
    difficulty: int
    status: str  # pending | in_progress | done
    gap_type: str  # "gap" | "unknown"
    priority: float
    because: str  # Human-readable explanation


class RoadmapRead(BaseModel):
    id: UUID
    user_id: UUID
    items: list[RoadmapItemDetail]
    created_at: datetime.datetime
    updated_at: datetime.datetime
