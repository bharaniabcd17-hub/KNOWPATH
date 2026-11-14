"""Profiles API router."""
from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import CurrentUser, get_current_user, get_db
from app.domains.profiles.schemas import ProfileRead, ProfileUpdate
from app.models import Profile

router = APIRouter(prefix="/profiles", tags=["Profiles"])


@router.get("/me", response_model=ProfileRead)
async def get_my_profile(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Retrieve profile for the authenticated learner."""
    stmt = select(Profile).where(Profile.user_id == uuid.UUID(current_user.id))
    result = await db.execute(stmt)
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return profile


@router.patch("/me", response_model=ProfileRead)
async def update_my_profile(
    req: ProfileUpdate,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Update profile and preferences for the authenticated learner."""
    stmt = select(Profile).where(Profile.user_id == uuid.UUID(current_user.id))
    result = await db.execute(stmt)
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

    if req.display_name is not None:
        profile.display_name = req.display_name
    if req.education_level is not None:
        profile.education_level = req.education_level
    if req.weekly_hours is not None:
        profile.weekly_hours = req.weekly_hours
    if req.preferences is not None:
        profile.preferences = req.preferences.model_dump()

    await db.commit()
    await db.refresh(profile)
    return profile
