"""Assessments API router."""
from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import CurrentUser, get_current_user, get_db
from app.domains.assessments.schemas import (
    AssessmentItem,
    AttemptResult,
    AttemptStart,
    SubmitAnswerRequest,
    SubmitAnswerResponse,
)
from app.domains.assessments.service import AssessmentService
from app.models import Attempt, Response

router = APIRouter(prefix="/assessments", tags=["Assessments"])


@router.post("/diagnostic/start")
async def start_diagnostic(
    req: AttemptStart,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Start an adaptive assessment session and return first question."""
    service = AssessmentService(db, uuid.UUID(current_user.id))
    attempt = await service.start_attempt(kind=req.kind)
    first_item = await service.get_next_question(attempt.id)
    return {
        "attempt_id": attempt.id,
        "kind": attempt.kind,
        "first_item": first_item,
    }


@router.get("/diagnostic/{attempt_id}/next", response_model=AssessmentItem)
async def get_next_item(
    attempt_id: uuid.UUID,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Fetch next adaptive question in the attempt."""
    # Ensure attempt belongs to user
    stmt = select(Attempt).where(Attempt.id == attempt_id, Attempt.user_id == uuid.UUID(current_user.id))
    res = await db.execute(stmt)
    attempt = res.scalar_one_or_none()
    if not attempt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment attempt not found")

    service = AssessmentService(db, uuid.UUID(current_user.id))
    item = await service.get_next_question(attempt_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Attempt completed")
    return item


@router.post("/diagnostic/submit", response_model=SubmitAnswerResponse)
async def submit_answer(
    req: SubmitAnswerRequest,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Submit an answer to an assessment question, get score feedback and next question."""
    stmt = select(Attempt).where(Attempt.id == req.attempt_id, Attempt.user_id == uuid.UUID(current_user.id))
    res = await db.execute(stmt)
    attempt = res.scalar_one_or_none()
    if not attempt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment attempt not found")

    service = AssessmentService(db, uuid.UUID(current_user.id))
    try:
        return await service.submit_response(
            attempt_id=req.attempt_id,
            question_id=req.question_id,
            answer=req.answer,
            time_ms=req.time_ms,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
