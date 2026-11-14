"""Admin API router."""
from __future__ import annotations

import datetime
import uuid
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import desc, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import CurrentUser, get_current_admin, get_db
from app.domains.admin.schemas import (
    AdminCostItem,
    AdminExecutionItem,
    AdminUserItem,
)
from app.domains.disputes.schemas import DisputeRead
from app.models import AgentExecution, Dispute, Evidence, MasteryState, Question, User
from app.scoring.engine import compute_credible_interval

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/users", response_model=list[AdminUserItem])
async def list_users(
    admin: Annotated[CurrentUser, Depends(get_current_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """List users for admin view (never exposes document content or private preferences)."""
    stmt = select(User).order_by(desc(User.created_at)).offset(offset).limit(limit)
    res = await db.execute(stmt)
    users = res.scalars().all()
    return [
        AdminUserItem(
            id=u.id,
            email=u.email,
            role=u.role,
            is_verified=u.is_verified,
            created_at=u.created_at,
            deleted_at=u.deleted_at,
        )
        for u in users
    ]


@router.get("/disputes", response_model=list[DisputeRead])
async def list_all_disputes(
    admin: Annotated[CurrentUser, Depends(get_current_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
    status_filter: Optional[str] = Query(None),
):
    """List all learner disputes for admin resolution."""
    stmt = select(Dispute).order_by(desc(Dispute.id))
    if status_filter:
        stmt = stmt.where(Dispute.status == status_filter)
    res = await db.execute(stmt)
    return res.scalars().all()


@router.patch("/disputes/{dispute_id}/resolve")
async def resolve_dispute(
    dispute_id: uuid.UUID,
    resolution: str,  # "resolved" | "dismissed"
    admin: Annotated[CurrentUser, Depends(get_current_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Admin resolves or dismisses a dispute, recalculating mastery states accordingly."""
    stmt = select(Dispute).where(Dispute.id == dispute_id)
    res = await db.execute(stmt)
    dispute = res.scalar_one_or_none()
    if not dispute:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dispute not found")

    dispute.status = resolution
    dispute.resolved_by = uuid.UUID(admin.id)
    dispute.resolved_at = datetime.datetime.now(datetime.timezone.utc)

    # If resolved, reset disputed factor on evidence or recalculate
    if resolution == "resolved" and dispute.target_type == "score":
        ev_stmt = select(Evidence).where(Evidence.user_id == dispute.user_id, Evidence.concept_slug == dispute.target_id)
        ev_res = await db.execute(ev_stmt)
        ev_items = ev_res.scalars().all()
        for ev in ev_items:
            ev.disputed = False
            ev.weight = ev.weight * 2.0  # Restore full weight

        ms_stmt = select(MasteryState).where(MasteryState.user_id == dispute.user_id, MasteryState.concept_slug == dispute.target_id)
        ms_res = await db.execute(ms_stmt)
        m_state = ms_res.scalar_one_or_none()
        if m_state:
            alpha = 1.0
            beta_val = 1.0
            for ev in ev_items:
                alpha += ev.weight * ev.value
                beta_val += ev.weight * (1.0 - ev.value)
            m_state.alpha = alpha
            m_state.beta = beta_val
            m_state.mastery = alpha / (alpha + beta_val)
            low, high = compute_credible_interval(alpha, beta_val, ci=0.80)
            m_state.confidence = max(0.0, min(1.0, 1.0 - (high - low)))
            m_state.updated_at = datetime.datetime.now(datetime.timezone.utc)

    await db.commit()
    return {"status": "dispute_updated", "resolution": resolution}


@router.get("/agent-executions", response_model=list[AdminExecutionItem])
async def list_agent_executions(
    admin: Annotated[CurrentUser, Depends(get_current_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
    agent: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=100),
):
    """View agent execution logs with latency, tokens, cost, and error states."""
    stmt = select(AgentExecution).order_by(desc(AgentExecution.started_at)).limit(limit)
    if agent:
        stmt = stmt.where(AgentExecution.agent == agent)
    res = await db.execute(stmt)
    return res.scalars().all()


@router.get("/costs", response_model=list[AdminCostItem])
async def get_cost_summary(
    admin: Annotated[CurrentUser, Depends(get_current_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """View LLM cost per day summary."""
    stmt = (
        select(
            func.date(AgentExecution.started_at).label("exec_date"),
            func.sum(AgentExecution.cost_usd).label("total_cost"),
            func.sum(AgentExecution.tokens_in + AgentExecution.tokens_out).label("total_tokens"),
            func.count(AgentExecution.id).label("total_execs"),
        )
        .group_by(func.date(AgentExecution.started_at))
        .order_by(desc("exec_date"))
        .limit(30)
    )
    res = await db.execute(stmt)
    records = res.all()
    return [
        AdminCostItem(
            date=str(r.exec_date),
            cost_usd=round(r.total_cost or 0.0, 4),
            total_tokens=int(r.total_tokens or 0),
            executions_count=int(r.total_execs or 0),
        )
        for r in records
    ]


@router.get("/questions/draft")
async def list_draft_questions(
    admin: Annotated[CurrentUser, Depends(get_current_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """List AI-generated draft questions pending human review."""
    stmt = select(Question).where(Question.status == "draft")
    res = await db.execute(stmt)
    return res.scalars().all()


@router.patch("/questions/{question_id}/approve")
async def approve_draft_question(
    question_id: str,
    admin: Annotated[CurrentUser, Depends(get_current_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Human approval checkpoint: approve draft question into active question pool."""
    stmt = select(Question).where(Question.id == question_id)
    res = await db.execute(stmt)
    q = res.scalar_one_or_none()
    if not q:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    q.status = "approved"
    await db.commit()
    return {"status": "approved", "question_id": question_id}
