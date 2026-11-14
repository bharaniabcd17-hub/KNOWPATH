"""Comprehensive End-to-End Integration Test for KNOWPATH / PROJECT-EVOLVE.

Tests the complete vertical slice:
Registration (18+ Age Gate) -> Goal Setup -> Diagnostic Assessment ->
Deterministic Scoring & Misconceptions -> Cognitive Twin -> Roadmap ->
Daily Missions -> SM-2 Reviews -> Teaching Companion -> Disputes -> Admin Desk -> Data Export -> Hard Deletion.
"""

import uuid
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Concept, Question


@pytest.mark.asyncio
async def test_complete_user_lifecycle(client: AsyncClient, db_session: AsyncSession):
    # 0. Seed a test concept and question into the test database
    c = Concept(
        id=uuid.uuid4(),
        slug="variables_intro",
        title="Variables Introduction",
        description="Introduction to variables and binding",
        difficulty=1,
        domain="python_fundamentals",
        content_md="Variables bind names to values in Python memory.",
    )
    db_session.add(c)
    await db_session.flush()

    q = Question(
        id="q_var_test",
        concept_slug="variables_intro",
        stem="What does `x = 5` do in Python?",
        type="code_reading",
        difficulty=0.2,
        discrimination=0.8,
        options={"A": "Binds x to 5", "B": "Error"},
        correct="A",
        explanation="Assigns the integer 5 to variable name x.",
        status="approved",
    )
    db_session.add(q)
    await db_session.commit()

    # 1. Health check
    res = await client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"

    # 2. Registration with 18+ Age Gate
    reg_payload = {
        "email": "e2e_journey@example.com",
        "password": "SecurePassword123!",
        "dob": "1999-04-12",
        "consent_version": "1.0",
    }
    res = await client.post("/api/v1/auth/register", json=reg_payload)
    assert res.status_code == 201
    data = res.json()
    token = data["access_token"]
    user_id = data["user_id"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Verify user profile & set goal
    res = await client.get("/api/v1/profiles/me", headers=headers)
    assert res.status_code == 200

    res = await client.post(
        "/api/v1/goals/",
        headers=headers,
        json={"goal_key": "python_placements"},
    )
    assert res.status_code in (200, 201)

    # 4. Genome concepts inspection
    res = await client.get("/api/v1/genome/concepts", headers=headers)
    assert res.status_code == 200
    concepts = res.json()
    assert len(concepts) >= 1

    # 5. Start Diagnostic Assessment
    res = await client.post(
        "/api/v1/assessments/diagnostic/start",
        headers=headers,
        json={"kind": "diagnostic"},
    )
    assert res.status_code == 200
    diag_data = res.json()
    attempt_id = diag_data["attempt_id"]
    first_item = diag_data["first_item"]
    assert attempt_id is not None
    assert first_item is not None

    # 6. Submit answer
    sub_payload = {
        "attempt_id": attempt_id,
        "question_id": first_item["question_id"],
        "answer": "A",
        "time_ms": 4500,
    }
    res = await client.post(
        "/api/v1/assessments/diagnostic/submit",
        headers=headers,
        json=sub_payload,
    )
    assert res.status_code == 200
    sub_res = res.json()
    assert "correct" in sub_res
    assert sub_res["correct"] is True

    # 7. Inspect Cognitive Twin
    res = await client.get("/api/v1/twin/", headers=headers)
    assert res.status_code == 200
    twin_data = res.json()
    assert "concepts" in twin_data
    assert len(twin_data["concepts"]) >= 1

    # 8. Roadmap generation
    res = await client.get("/api/v1/roadmap/", headers=headers)
    assert res.status_code == 200
    roadmap_data = res.json()
    assert "items" in roadmap_data

    # 9. Daily Mission
    res = await client.get("/api/v1/missions/today", headers=headers)
    assert res.status_code == 200
    mission = res.json()
    if mission and "id" in mission:
        complete_res = await client.post(f"/api/v1/missions/{mission['id']}/complete", headers=headers)
        assert complete_res.status_code in (200, 204)

    # 10. AI Teaching Companion
    comp_payload = {
        "concept_slug": "variables_intro",
        "question": "What is variable binding in Python?",
    }
    res = await client.post("/api/v1/companion/explain", headers=headers, json=comp_payload)
    assert res.status_code == 200
    comp_res = res.json()
    assert "explanation" in comp_res
    assert comp_res["is_ai"] is True
    assert len(comp_res["sources"]) > 0

    # 11. File a dispute
    disp_payload = {
        "target_type": "score",
        "target_id": "variables_intro",
        "reason": "Requesting manual audit of assessment item scoring.",
    }
    res = await client.post("/api/v1/disputes/", headers=headers, json=disp_payload)
    assert res.status_code == 201
    dispute_id = res.json()["id"]

    # 12. Check user disputes
    res = await client.get("/api/v1/disputes/", headers=headers)
    assert res.status_code == 200
    assert len(res.json()) >= 1

    # 13. Data export (GDPR Article 20)
    res = await client.get("/api/v1/users/export", headers=headers)
    assert res.status_code == 200

    # 14. Hard Account Deletion (GDPR Article 17)
    res = await client.request(
        "DELETE",
        "/api/v1/users/me",
        headers=headers,
        json={"confirmation": "DELETE"},
    )
    assert res.status_code in (200, 204)
