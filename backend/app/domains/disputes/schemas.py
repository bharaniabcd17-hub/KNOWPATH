"""Schemas for Disputes domain."""
from __future__ import annotations

import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class DisputeCreate(BaseModel):
    target_type: Literal["question", "score"]
    target_id: str  # question id or concept slug / evidence id
    reason: str = Field(min_length=5, max_length=1000)


class DisputeRead(BaseModel):
    id: UUID
    user_id: UUID
    target_type: str
    target_id: str
    reason: str
    status: str  # open | resolved | dismissed
    resolved_at: datetime.datetime | None = None

    model_config = {"from_attributes": True}
