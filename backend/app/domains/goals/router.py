"""Goals API router."""
from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import CurrentUser, get_current_user, get_db
from app.domains.goals.schemas import GOAL_TARGETS, GoalCreate, GoalRead
from app.models import Goal

router = APIRouter(prefix="/goals", tags=["Goals"])


@router.get("/", response_model=list[GoalRead])
async def get_my_goals(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """List goals belonging to the authenticated learner."""
    stmt = select(Goal).where(Goal.user_id == uuid.UUID(current_user.id))
    result = await db.execute(stmt)
    return result.scalars().all()


@router.post("/", response_model=GoalRead, status_code=status.HTTP_201_CREATED)
async def create_goal(
    req: GoalCreate,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Set or update target learning goal."""
    u_id = uuid.UUID(current_user.id)
    # Deactivate existing goals
    await db.execute(update(Goal).where(Goal.user_id == u_id).values(active=False))

    target_concepts = GOAL_TARGETS.get(req.goal_key, [])
    goal = Goal(
        id=uuid.uuid4(),
        user_id=u_id,
        goal_key=req.goal_key,
        target_concept_ids=target_concepts,
        active=True,
    )
    db.add(goal)
    await db.commit()
    await db.refresh(goal)
    return goal


@router.get("/active", response_model=GoalRead)
async def get_active_goal(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Retrieve active goal for authenticated learner."""
    stmt = select(Goal).where(Goal.user_id == uuid.UUID(current_user.id), Goal.active.is_(True))
    result = await db.execute(stmt)
    goal = result.scalar_one_or_none()
    if not goal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active goal found")
    return goal
