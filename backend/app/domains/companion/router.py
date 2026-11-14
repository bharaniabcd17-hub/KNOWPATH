"""Teaching Companion API router."""
from __future__ import annotations

import uuid
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.orchestrator import AgentOrchestrator
from app.deps import CurrentUser, get_current_user, get_db
from app.models import Concept, Misconception, Response

router = APIRouter(prefix="/companion", tags=["Teaching Companion"])


class ExplainRequest(BaseModel):
    concept_slug: str
    question: str = Field(min_length=3, max_length=500)


class ExplainResponse(BaseModel):
    explanation: str
    sources: list[str]
    is_ai: bool
    latency_ms: Optional[int] = None


@router.post("/explain", response_model=ExplainResponse)
async def explain_concept(
    req: ExplainRequest,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Ask the Teaching Companion to explain a concept grounded in stored concept notes and learner misconceptions."""
    u_id = uuid.UUID(current_user.id)

    # Find any misconceptions this user selected for this concept
    misc_stmt = (
        select(Misconception.title)
        .join(Response, Response.selected_misconception_id == Misconception.id)
        .where(Misconception.concept_slug == req.concept_slug)
    )
    misc_res = await db.execute(misc_stmt)
    user_misconceptions = list(misc_res.scalars().all())

    orchestrator = AgentOrchestrator(db)
    try:
        result = await orchestrator.explain_concept(
            user_id=u_id,
            concept_slug=req.concept_slug,
            question=req.question,
            user_misconceptions=user_misconceptions,
        )
        return ExplainResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
