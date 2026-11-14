"""Schemas for Profile domain."""
from __future__ import annotations

from typing import Any, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class Preferences(BaseModel):
    explanation_style: Literal["simple", "detailed", "example-first"] = "simple"
    session_length: Literal[15, 30, 45] = 30


class ProfileRead(BaseModel):
    user_id: UUID
    display_name: str
    education_level: str
    weekly_hours: int
    preferences: Preferences

    model_config = {"from_attributes": True}


class ProfileUpdate(BaseModel):
    display_name: Optional[str] = None
    education_level: Optional[str] = None
    weekly_hours: Optional[int] = Field(None, ge=1, le=40)
    preferences: Optional[Preferences] = None
