"""Integration tests for Auth, Age Gate, and Sessions."""
from __future__ import annotations

import datetime
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_success(client: AsyncClient):
    """Adult learner (age >= 18) registers successfully and receives JWT."""
    payload = {
        "email": "learner_adult@test.com",
        "password": "Password123!",
        "dob": "2000-01-15",
        "consent_version": "v1.0",
    }
    res = await client.post("/api/v1/auth/register", json=payload)
    assert res.status_code == 201
    data = res.json()
    assert "access_token" in data
    assert data["email"] == "learner_adult@test.com"
    assert data["role"] == "learner"


@pytest.mark.asyncio
async def test_register_age_gate_under_18(client: AsyncClient):
    """Underage user (age < 18) is rejected at registration (Phase 1 age gate)."""
    # Calculate a birthdate for someone who is 16 years old
    today = datetime.date.today()
    underage_dob = f"{today.year - 16}-06-01"

    payload = {
        "email": "minor_user@test.com",
        "password": "Password123!",
        "dob": underage_dob,
        "consent_version": "v1.0",
    }
    res = await client.post("/api/v1/auth/register", json=payload)
    assert res.status_code == 422 or res.status_code == 400


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    """Duplicate email registration is rejected with 409 Conflict."""
    payload = {
        "email": "duplicate_check@test.com",
        "password": "Password123!",
        "dob": "1995-05-20",
        "consent_version": "v1.0",
    }
    res1 = await client.post("/api/v1/auth/register", json=payload)
    assert res1.status_code == 201

    res2 = await client.post("/api/v1/auth/register", json=payload)
    assert res2.status_code == 409


@pytest.mark.asyncio
async def test_login_success_and_failure(client: AsyncClient):
    """Login with correct credentials succeeds; wrong password returns 401."""
    # Register first
    await client.post(
        "/api/v1/auth/register",
        json={"email": "login_test@test.com", "password": "SecretPassword1", "dob": "1998-03-12"},
    )

    # Wrong password
    res_wrong = await client.post(
        "/api/v1/auth/login",
        json={"email": "login_test@test.com", "password": "WrongPassword"},
    )
    assert res_wrong.status_code == 401

    # Correct password
    res_correct = await client.post(
        "/api/v1/auth/login",
        json={"email": "login_test@test.com", "password": "SecretPassword1"},
    )
    assert res_correct.status_code == 200
    assert "access_token" in res_correct.json()


@pytest.mark.asyncio
async def test_protected_routes_require_token(client: AsyncClient):
    """Protected endpoints reject requests without a Bearer token."""
    res = await client.get("/api/v1/auth/me")
    assert res.status_code == 401
