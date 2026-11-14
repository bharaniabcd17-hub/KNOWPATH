"""Authentication API router."""
from __future__ import annotations

import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import get_db, get_current_user, CurrentUser
from app.domains.auth.repo import AuthRepo
from app.domains.auth.schemas import (
    LoginRequest,
    PasswordResetConfirm,
    PasswordResetRequest,
    RegisterRequest,
    TokenResponse,
    UserRead,
)
from app.domains.auth.service import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(req: RegisterRequest, db: Annotated[AsyncSession, Depends(get_db)]):
    """Register a new learner account with age gate and explicit consent."""
    repo = AuthRepo(db)
    existing = await repo.get_by_email(req.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )

    # Hash password and create user
    hashed = hash_password(req.password)
    user = await repo.create_user(
        email=req.email,
        hashed_password=hashed,
        dob=req.dob,
        consent_version=req.consent_version,
    )

    token = create_access_token(user.id, user.email, user.role)
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user_id=user.id,
        email=user.email,
        role=user.role,
    )


@router.post("/login", response_model=TokenResponse)
async def login(req: LoginRequest, db: Annotated[AsyncSession, Depends(get_db)]):
    """Authenticate with email and password, returning a JWT token."""
    repo = AuthRepo(db)
    user = await repo.get_by_email(req.email)
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(user.id, user.email, user.role)
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user_id=user.id,
        email=user.email,
        role=user.role,
    )


@router.post("/logout")
async def logout():
    """Client-side token disposal."""
    return {"status": "logged_out"}


@router.get("/me", response_model=UserRead)
async def get_me(current_user: Annotated[CurrentUser, Depends(get_current_user)], db: Annotated[AsyncSession, Depends(get_db)]):
    """Get current authenticated user profile."""
    repo = AuthRepo(db)
    import uuid
    user = await repo.get_by_id(uuid.UUID(current_user.id))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.post("/password-reset-request")
async def password_reset_request(req: PasswordResetRequest):
    """Simulate password reset request."""
    return {"status": "ok", "message": f"[Mock Email] Password reset link sent to {req.email}"}
