"""Users API router: profile read, data export (JSON), and hard deletion."""
from __future__ import annotations

import datetime
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import CurrentUser, get_current_user, get_db
from app.models import (
    AuditLog,
    Dispute,
    Evidence,
    Goal,
    Job,
    MasteryState,
    Mission,
    Profile,
    Response,
    ReviewSchedule,
    Roadmap,
    TwinSnapshot,
    User,
)

router = APIRouter(prefix="/users", tags=["Users"])


class DeleteAccountRequest(BaseModel):
    confirmation: str  # Must match "DELETE"


@router.get("/export")
async def export_my_data(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Data export: download complete personal learner data in compliance with privacy regulations."""
    u_id = uuid.UUID(current_user.id)

    # 1. Fetch user & profile
    user = await db.scalar(select(User).where(User.id == u_id))
    profile = await db.scalar(select(Profile).where(Profile.user_id == u_id))
    goals = (await db.execute(select(Goal).where(Goal.user_id == u_id))).scalars().all()
    evidence = (await db.execute(select(Evidence).where(Evidence.user_id == u_id))).scalars().all()
    mastery = (await db.execute(select(MasteryState).where(MasteryState.user_id == u_id))).scalars().all()
    snapshots = (await db.execute(select(TwinSnapshot).where(TwinSnapshot.user_id == u_id))).scalars().all()
    reviews = (await db.execute(select(ReviewSchedule).where(ReviewSchedule.user_id == u_id))).scalars().all()
    disputes = (await db.execute(select(Dispute).where(Dispute.user_id == u_id))).scalars().all()

    export_payload = {
        "export_metadata": {
            "platform": "PROJECT-EVOLVE",
            "exported_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "user_id": str(u_id),
        },
        "account": {
            "email": user.email if user else "",
            "dob": str(user.dob) if user else "",
            "consent_version": user.consent_version if user else "",
            "consent_at": user.consent_at.isoformat() if user and user.consent_at else "",
            "created_at": user.created_at.isoformat() if user else "",
        },
        "profile": {
            "display_name": profile.display_name if profile else "",
            "education_level": profile.education_level if profile else "",
            "weekly_hours": profile.weekly_hours if profile else 5,
            "preferences": profile.preferences if profile else {},
        },
        "goals": [{"goal_key": g.goal_key, "active": g.active} for g in goals],
        "evidence_records": [
            {
                "concept_slug": e.concept_slug,
                "source_type": e.source_type,
                "value": e.value,
                "weight": e.weight,
                "observed_at": e.observed_at.isoformat(),
                "disputed": e.disputed,
            }
            for e in evidence
        ],
        "mastery_states": [
            {
                "concept_slug": m.concept_slug,
                "mastery": m.mastery,
                "confidence": m.confidence,
                "alpha": m.alpha,
                "beta": m.beta,
                "updated_at": m.updated_at.isoformat(),
            }
            for m in mastery
        ],
        "snapshots": [
            {"taken_at": s.taken_at.isoformat(), "trigger": s.trigger, "state": s.state}
            for s in snapshots
        ],
        "review_schedule": [
            {"concept_slug": r.concept_slug, "due_at": r.due_at.isoformat(), "interval_days": r.interval_days}
            for r in reviews
        ],
        "disputes": [
            {"target_type": d.target_type, "target_id": d.target_id, "reason": d.reason, "status": d.status}
            for d in disputes
        ],
    }

    # Record in audit log
    audit = AuditLog(
        id=uuid.uuid4(),
        actor_id=u_id,
        action="export_data",
        target=str(u_id),
        metadata_={"record_count": len(evidence) + len(mastery)},
        created_at=datetime.datetime.now(datetime.timezone.utc),
    )
    db.add(audit)
    await db.commit()

    return JSONResponse(
        content=export_payload,
        headers={"Content-Disposition": f"attachment; filename=evolve_data_{u_id}.json"},
    )


@router.delete("/me", status_code=status.HTTP_200_OK)
async def delete_my_account(
    req: DeleteAccountRequest,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Account deletion: soft delete immediately, queue hard-delete job with confirmation."""
    if req.confirmation.strip().upper() != "DELETE":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You must provide the exact confirmation string 'DELETE' to proceed.",
        )

    u_id = uuid.UUID(current_user.id)
    user = await db.scalar(select(User).where(User.id == u_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    now = datetime.datetime.now(datetime.timezone.utc)
    user.deleted_at = now

    # Queue background hard-delete job
    job = Job(
        id=uuid.uuid4(),
        type="hard_delete_user",
        payload={"user_id": str(u_id)},
        status="pending",
        run_at=now + datetime.timedelta(days=30),  # 30-day grace period
        created_at=now,
    )
    db.add(job)

    # Audit log
    audit = AuditLog(
        id=uuid.uuid4(),
        actor_id=u_id,
        action="account_deletion_requested",
        target=str(u_id),
        metadata_={"job_id": str(job.id)},
        created_at=now,
    )
    db.add(audit)

    await db.commit()
    return {
        "status": "account_marked_for_deletion",
        "message": "Your account has been deactivated and scheduled for permanent deletion.",
    }
