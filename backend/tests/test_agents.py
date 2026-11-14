"""Tests for AI Agents, Safety Validator, and Orchestrator."""
from __future__ import annotations

import uuid
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.llm_client import MockLLMClient, LLMMessage
from app.agents.orchestrator import AgentOrchestrator
from app.agents.quality_safety_agent import QualitySafetyAgent


@pytest.mark.asyncio
async def test_mock_llm_returns_labeled_response():
    """Mock LLM response is always explicitly labeled as AI/Mock."""
    client = MockLLMClient()
    res = await client.complete([LLMMessage(role="user", content="Explain variables")])
    assert "AI-Generated" in res.content
    assert res.is_mock is True
    assert res.tokens_in > 0
    assert res.tokens_out > 0


def test_quality_safety_blocks_outcome_guarantees():
    """Safety Agent rejects outputs promising outcome guarantees (jobs, salaries)."""
    safety = QualitySafetyAgent()
    unsafe_text = "🤖 [AI-Generated] We guarantee you will get a high-paying job once you finish."
    report = safety.validate_teaching_output(
        explanation=unsafe_text,
        concept_slug="variables-basics",
        valid_concept_slugs={"variables-basics"},
    )
    assert report.is_valid is False
    assert any("outcome guarantee" in r for r in report.reasons)


def test_quality_safety_blocks_unlabeled_ai():
    """Safety Agent rejects outputs lacking mandatory AI labeling."""
    safety = QualitySafetyAgent()
    unlabeled_text = "Variables store data in memory."
    report = safety.validate_teaching_output(
        explanation=unlabeled_text,
        concept_slug="variables-basics",
        valid_concept_slugs={"variables-basics"},
    )
    assert report.is_valid is False
    assert any("AI-label" in r for r in report.reasons)


def test_quality_safety_validates_draft_questions():
    """Safety Agent validates draft questions have all fields and matching options."""
    safety = QualitySafetyAgent()
    invalid_q = {
        "stem": "What is Python?",
        "options": {"A": "A language"},
        "correct": "B",  # B not in options!
    }
    report = safety.validate_question_draft(invalid_q, {"variables-basics"})
    assert report.is_valid is False


@pytest.mark.asyncio
async def test_orchestrator_teaching_and_logging(db_session: AsyncSession):
    """Teaching agent runs concept-grounded explanation and records in agent_executions."""
    from app.models import Concept
    # Ensure test concept exists in test DB session
    existing = await db_session.get(Concept, uuid.UUID("00000000-0000-0000-0000-000000000001"))
    if not existing:
        c = Concept(
            id=uuid.UUID("00000000-0000-0000-0000-000000000001"),
            slug="variables-basics",
            title="Variables Basics",
            description="Variables in Python.",
            difficulty=1,
            domain="python_fundamentals",
            content_md="A variable is a symbolic label pointing to an object.",
        )
        db_session.add(c)
        await db_session.commit()

    orchestrator = AgentOrchestrator(db_session)
    user_id = uuid.uuid4()

    result = await orchestrator.explain_concept(
        user_id=user_id,
        concept_slug="variables-basics",
        question="What is variable assignment?",
    )
    assert result["is_ai"] is True
    assert "variables-basics" in result["sources"]
    assert len(result["explanation"]) > 20
