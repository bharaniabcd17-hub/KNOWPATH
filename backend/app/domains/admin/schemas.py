"""Schemas for Admin domain."""
from __future__ import annotations

import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel


class AdminUserItem(BaseModel):
    id: UUID
    email: str
    role: str
    is_verified: bool
    created_at: datetime.datetime
    deleted_at: Optional[datetime.datetime] = None


class AdminCostItem(BaseModel):
    date: str
    cost_usd: float
    total_tokens: int
    executions_count: int


class AdminExecutionItem(BaseModel):
    id: UUID
    agent: str
    workflow_id: str
    status: str
    latency_ms: Optional[int]
    cost_usd: Optional[float]
    tokens_in: Optional[int]
    tokens_out: Optional[int]
    started_at: datetime.datetime
