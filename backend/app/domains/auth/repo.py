"""Data access layer for User and Auth entities."""
from __future__ import annotations

import datetime
import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Profile, User


class AuthRepo:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email, User.deleted_at.is_(None))
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        stmt = select(User).where(User.id == user_id, User.deleted_at.is_(None))
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_user(
        self,
        email: str,
        hashed_password: str,
        dob: datetime.date,
        consent_version: str,
        role: str = "learner",
    ) -> User:
        user = User(
            id=uuid.uuid4(),
            email=email,
            hashed_password=hashed_password,
            dob=dob,
            role=role,
            is_verified=True,  # Auto-verified for local dev / mock MVP
            consent_version=consent_version,
            consent_at=datetime.datetime.now(datetime.timezone.utc),
        )
        self.db.add(user)

        # Create matching profile
        profile = Profile(
            user_id=user.id,
            display_name=email.split("@")[0],
            education_level="undergraduate",
            weekly_hours=5,
            preferences={"explanation_style": "simple", "session_length": 30},
        )
        self.db.add(profile)

        await self.db.commit()
        await self.db.refresh(user)
        return user
