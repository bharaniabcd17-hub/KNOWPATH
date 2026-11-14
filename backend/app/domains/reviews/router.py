"""Reviews API router."""
from __future__ import annotations

import datetime
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import CurrentUser, get_current_user, get_db
from app.domains.reviews.schemas import ReviewItem, ReviewSubmit
from app.models import Concept, Evidence, MasteryState, ReviewSchedule
from app.scoring.engine import compute_credible_interval, compute_evidence_weight
from app.scoring.retention import compute_next_interval

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.get("/due", response_model=list[ReviewItem])
async def get_due_reviews(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """List concepts due or overdue for spaced revision."""
    u_id = uuid.UUID(current_user.id)
    now = datetime.datetime.now(datetime.timezone.utc)

    stmt = (
        select(ReviewSchedule, Concept)
        .join(Concept, Concept.slug == ReviewSchedule.concept_slug)
        .where(ReviewSchedule.user_id == u_id)
        .order_by(ReviewSchedule.due_at)
    )
    res = await db.execute(stmt)
    records = res.all()

    due_items: list[ReviewItem] = []
    for sched, concept in records:
        # Include if due now or in the near future
        due_items.append(
            ReviewItem(
                concept_slug=sched.concept_slug,
                concept_title=concept.title,
                difficulty=concept.difficulty,
                due_at=sched.due_at,
                interval_days=sched.interval_days,
                ease=round(sched.ease, 2),
                is_overdue=sched.due_at <= now,
                last_result=sched.last_result,
            )
        )
    return due_items


@router.post("/complete", response_model=dict)
async def complete_review(
    req: ReviewSubmit,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Record completion of a spaced review item and apply SM-2 update."""
    u_id = uuid.UUID(current_user.id)
    if req.result not in ("pass", "fail"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Result must be 'pass' or 'fail'")

    stmt = select(ReviewSchedule).where(ReviewSchedule.user_id == u_id, ReviewSchedule.concept_slug == req.concept_slug)
    res = await db.execute(stmt)
    sched = res.scalar_one_or_none()

    prev_interval = sched.interval_days if sched else 1.0
    prev_ease = sched.ease if sched else 2.3

    new_interval, new_ease = compute_next_interval(prev_interval, prev_ease, req.result)
    next_due = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=new_interval)

    if not sched:
        sched = ReviewSchedule(
            user_id=u_id,
            concept_slug=req.concept_slug,
            due_at=next_due,
            interval_days=new_interval,
            ease=new_ease,
            last_result=req.result,
        )
        db.add(sched)
    else:
        sched.due_at = next_due
        sched.interval_days = new_interval
        sched.ease = new_ease
        sched.last_result = req.result

    # If pass, record assessment_verified evidence
    val = 1.0 if req.result == "pass" else 0.2
    w = compute_evidence_weight("assessment_verified", age_days=0.0, discrimination=0.7, time_ms=20000)
    ev = Evidence(
        id=uuid.uuid4(),
        user_id=u_id,
        concept_slug=req.concept_slug,
        source_type="assessment_verified",
        value=val,
        weight=w,
        ref_type="review",
        ref_id=str(sched.user_id),
        disputed=False,
    )
    db.add(ev)

    # Update MasteryState
    ms_stmt = select(MasteryState).where(MasteryState.user_id == u_id, MasteryState.concept_slug == req.concept_slug)
    ms_res = await db.execute(ms_stmt)
    m_state = ms_res.scalar_one_or_none()
    if m_state:
        m_state.alpha += w * val
        m_state.beta += w * (1.0 - val)
        m_state.mastery = m_state.alpha / (m_state.alpha + m_state.beta)
        low, high = compute_credible_interval(m_state.alpha, m_state.beta, ci=0.80)
        m_state.confidence = max(0.0, min(1.0, 1.0 - (high - low)))
        m_state.updated_at = datetime.datetime.now(datetime.timezone.utc)

    await db.commit()
    return {
        "status": "recorded",
        "result": req.result,
        "next_interval_days": round(new_interval, 1),
        "ease": round(new_ease, 2),
        "next_due_at": next_due.isoformat(),
    }
