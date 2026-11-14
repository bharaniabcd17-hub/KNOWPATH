"""Missions API router."""
from __future__ import annotations

import datetime
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.deps import CurrentUser, get_current_user, get_db
from app.domains.missions.schemas import MissionItem, MissionRead
from app.domains.roadmap.router import generate_user_roadmap
from app.models import (
    Concept,
    Evidence,
    MasteryState,
    Mission,
    Question,
    ReviewSchedule,
    Roadmap,
    RoadmapItem,
)
from app.scoring.engine import compute_credible_interval, compute_evidence_weight
from app.scoring.retention import schedule_review

router = APIRouter(prefix="/missions", tags=["Missions"])


@router.get("/today", response_model=MissionRead)
async def get_today_mission(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Retrieve or generate today's targeted learning mission."""
    u_id = uuid.UUID(current_user.id)
    today = datetime.date.today()

    stmt = select(Mission).where(Mission.user_id == u_id, Mission.date == today)
    res = await db.execute(stmt)
    mission = res.scalar_one_or_none()

    if not mission:
        mission = await _generate_mission_for_date(u_id, today, db)

    items_data = mission.items if isinstance(mission.items, list) else []
    focus_slug = items_data[0]["concept_slug"] if items_data else "variables-basics"
    focus_title = items_data[0]["concept_title"] if items_data else "Variables Basics"

    # Extract 'because' from items or fallback
    because_text = "Targeted action based on your knowledge profile gaps."
    if items_data and "because" in items_data[0].get("content", {}):
        because_text = items_data[0]["content"]["because"]

    return MissionRead(
        id=mission.id,
        user_id=mission.user_id,
        date=mission.date,
        focus_concept_slug=focus_slug,
        focus_concept_title=focus_title,
        items=[MissionItem(**item) for item in items_data],
        status=mission.status,
        completed_at=mission.completed_at,
        because=because_text,
    )


@router.post("/{mission_id}/complete", response_model=dict)
async def complete_mission(
    mission_id: uuid.UUID,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Mark daily mission complete, award verified evidence, update mastery, and schedule SM-2 review."""
    u_id = uuid.UUID(current_user.id)
    stmt = select(Mission).where(Mission.id == mission_id, Mission.user_id == u_id)
    res = await db.execute(stmt)
    mission = res.scalar_one_or_none()
    if not mission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mission not found")

    if mission.status == "completed":
        return {"status": "already_completed"}

    mission.status = "completed"
    mission.completed_at = datetime.datetime.now(datetime.timezone.utc)

    # Concept focus
    items_data = mission.items if isinstance(mission.items, list) else []
    focus_slug = items_data[0]["concept_slug"] if items_data else "variables-basics"

    # 1. Add assessment_verified Evidence for completing mission check
    weight = compute_evidence_weight(
        source_type="assessment_verified",
        age_days=0.0,
        discrimination=0.8,
        time_ms=25000,
    )
    ev = Evidence(
        id=uuid.uuid4(),
        user_id=u_id,
        concept_slug=focus_slug,
        source_type="assessment_verified",
        value=1.0,
        weight=weight,
        ref_type="mission",
        ref_id=str(mission_id),
        disputed=False,
    )
    db.add(ev)

    # 2. Update MasteryState
    ms_stmt = select(MasteryState).where(MasteryState.user_id == u_id, MasteryState.concept_slug == focus_slug)
    ms_res = await db.execute(ms_stmt)
    m_state = ms_res.scalar_one_or_none()
    if not m_state:
        m_state = MasteryState(
            user_id=u_id,
            concept_slug=focus_slug,
            alpha=1.0,
            beta=1.0,
            mastery=0.5,
            confidence=0.0,
            updated_at=datetime.datetime.now(datetime.timezone.utc),
        )
        db.add(m_state)

    m_state.alpha += weight * 1.0
    m_state.mastery = m_state.alpha / (m_state.alpha + m_state.beta)
    low, high = compute_credible_interval(m_state.alpha, m_state.beta, ci=0.80)
    m_state.confidence = max(0.0, min(1.0, 1.0 - (high - low)))
    m_state.updated_at = datetime.datetime.now(datetime.timezone.utc)

    # 3. Schedule SM-2 Retention Review (Section 7.4)
    rev_stmt = select(ReviewSchedule).where(ReviewSchedule.user_id == u_id, ReviewSchedule.concept_slug == focus_slug)
    rev_res = await db.execute(rev_stmt)
    rev_schedule = rev_res.scalar_one_or_none()

    new_schedule = schedule_review(
        user_id=u_id,
        concept_id=uuid.UUID(int=abs(hash(focus_slug)) % (2**127)),
        result="pass",
        current_schedule=None,  # Or map from existing
    )

    if not rev_schedule:
        rev_schedule = ReviewSchedule(
            user_id=u_id,
            concept_slug=focus_slug,
            due_at=new_schedule.next_review_at,
            interval_days=new_schedule.interval_days,
            ease=new_schedule.ease,
            last_result="pass",
        )
        db.add(rev_schedule)
    else:
        rev_schedule.interval_days = new_schedule.interval_days
        rev_schedule.ease = new_schedule.ease
        rev_schedule.due_at = new_schedule.next_review_at
        rev_schedule.last_result = "pass"

    # 4. Advance roadmap item status
    rm_stmt = select(Roadmap).where(Roadmap.user_id == u_id).options(selectinload(Roadmap.items))
    rm_res = await db.execute(rm_stmt)
    rm = rm_res.scalar_one_or_none()
    if rm:
        for it in rm.items:
            if it.concept_slug == focus_slug:
                it.status = "done"
            elif it.status == "pending":
                it.status = "in_progress"
                break

    await db.commit()
    return {
        "status": "completed",
        "concept_slug": focus_slug,
        "new_mastery": round(m_state.mastery, 3),
        "next_review_due": rev_schedule.due_at.isoformat(),
    }


async def _generate_mission_for_date(user_id: uuid.UUID, target_date: datetime.date, db: AsyncSession) -> Mission:
    """Construct one explanation + practice items + check based on highest priority gap."""
    # Find active roadmap item
    rm_stmt = select(Roadmap).where(Roadmap.user_id == user_id).options(selectinload(Roadmap.items))
    rm_res = await db.execute(rm_stmt)
    roadmap = rm_res.scalar_one_or_none()
    if not roadmap or not roadmap.items:
        roadmap = await generate_user_roadmap(user_id, db)

    # Pick first non-done roadmap item
    target_item = None
    for item in sorted(roadmap.items, key=lambda x: x.position):
        if item.status != "done":
            target_item = item
            break

    target_slug = target_item.concept_slug if target_item else "variables-basics"

    c_stmt = select(Concept).where(Concept.slug == target_slug)
    c_res = await db.execute(c_stmt)
    concept = c_res.scalar_one_or_none()
    concept_title = concept.title if concept else target_slug
    content_md = concept.content_md if concept else "Review concept materials."

    # Fetch 2 practice questions for this concept
    q_stmt = select(Question).where(Question.concept_slug == target_slug, Question.status == "approved").limit(3)
    q_res = await db.execute(q_stmt)
    questions = q_res.scalars().all()

    items_list: list[dict[str, Any]] = [
        {
            "id": f"exp-{target_slug}",
            "type": "explanation",
            "concept_slug": target_slug,
            "concept_title": concept_title,
            "content": {
                "markdown": content_md,
                "because": target_item.reason.get("because", "Targeted gap in your learning journey.") if target_item else "Foundational topic.",
            },
        }
    ]

    for idx, q in enumerate(questions[:2]):
        items_list.append(
            {
                "id": f"prac-{q.id}",
                "type": "practice",
                "concept_slug": target_slug,
                "concept_title": concept_title,
                "content": {
                    "question_id": q.id,
                    "stem": q.stem,
                    "options": q.options,
                },
            }
        )

    if len(questions) > 2:
        check_q = questions[2]
        items_list.append(
            {
                "id": f"chk-{check_q.id}",
                "type": "check",
                "concept_slug": target_slug,
                "concept_title": concept_title,
                "content": {
                    "question_id": check_q.id,
                    "stem": check_q.stem,
                    "options": check_q.options,
                },
            }
        )

    mission = Mission(
        id=uuid.uuid4(),
        user_id=user_id,
        date=target_date,
        items=items_list,
        status="pending",
    )
    db.add(mission)
    await db.commit()
    await db.refresh(mission)
    return mission
