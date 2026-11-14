"""Pydantic schemas for authentication and account management."""
from __future__ import annotations

import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator


class RegisterRequest(BaseModel):
    email: str
    password: str = Field(min_length=8)
    dob: datetime.date
    consent_version: str = "v1.0"

    @field_validator("dob")
    @classmethod
    def validate_age_gate(cls, v: datetime.date) -> datetime.date:
        """Enforce strict age gate: users under 18 cannot register in Phase 1."""
        today = datetime.date.today()
        age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))
        if age < 18:
            raise ValueError("Registration is restricted to learners aged 18 and older.")
        return v


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: UUID
    email: str
    role: str


class EmailVerifyRequest(BaseModel):
    token: str


class PasswordResetRequest(BaseModel):
    email: str


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(min_length=8)


class UserRead(BaseModel):
    id: UUID
    email: str
    role: str
    dob: datetime.date
    is_verified: bool
    created_at: datetime.datetime
    deleted_at: Optional[datetime.datetime] = None

    model_config = {"from_attributes": True}
