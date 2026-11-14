"""Disputes API router."""
from __future__ import annotations

import datetime
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import CurrentUser, get_current_user, get_db
from app.domains.disputes.schemas import DisputeCreate, DisputeRead
from app.models import Dispute, Evidence, MasteryState
from app.scoring.engine import compute_credible_interval

router = APIRouter(prefix="/disputes", tags=["Disputes"])


@router.post("/", response_model=DisputeRead, status_code=status.HTTP_201_CREATED)
async def create_dispute(
    req: DisputeCreate,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """File a human correction dispute on a question or a concept mastery score.

    Per Section 7.1: A disputed item's weight is immediately reduced by dispute_factor (0.5).
    """
    u_id = uuid.UUID(current_user.id)
    dispute = Dispute(
        id=uuid.uuid4(),
        user_id=u_id,
        target_type=req.target_type,
        target_id=req.target_id,
        reason=req.reason,
        status="open",
    )
    db.add(dispute)

    # If disputing a score for a concept, mark matching evidence as disputed and halve effective weight
    if req.target_type == "score":
        # Target id is concept_slug
        ev_stmt = select(Evidence).where(Evidence.user_id == u_id, Evidence.concept_slug == req.target_id)
        ev_res = await db.execute(ev_stmt)
        ev_items = ev_res.scalars().all()
        for ev in ev_items:
            if not ev.disputed:
                ev.disputed = True
                ev.weight *= 0.5  # Halve weight immediately

        # Recalculate MasteryState from updated evidence
        ms_stmt = select(MasteryState).where(MasteryState.user_id == u_id, MasteryState.concept_slug == req.target_id)
        ms_res = await db.execute(ms_stmt)
        m_state = ms_res.scalar_one_or_none()
        if m_state:
            # Recompute from scratch using prior alpha=1, beta=1
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
    await db.refresh(dispute)
    return dispute


@router.get("/", response_model=list[DisputeRead])
async def list_my_disputes(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """List disputes filed by authenticated user."""
    stmt = select(Dispute).where(Dispute.user_id == uuid.UUID(current_user.id)).order_by(Dispute.id)
    res = await db.execute(stmt)
    return res.scalars().all()
