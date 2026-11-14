"""Agent Orchestrator — coordinates 4 agent logical roles with budgets, validation, and audit logging."""
from __future__ import annotations

import datetime
import hashlib
import json
import time
import uuid
from typing import Any, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.embedding_client import EmbeddingClient, get_embedding_client
from app.agents.llm_client import LLMClient, LLMMessage, LLMResponse, get_llm_client
from app.agents.quality_safety_agent import QualitySafetyAgent, ValidationReport
from app.config import get_settings
from app.models import AgentExecution, Concept, Misconception, Question

settings = get_settings()


class AgentOrchestrator:
    def __init__(
        self,
        db: AsyncSession,
        llm: Optional[LLMClient] = None,
        embedding: Optional[EmbeddingClient] = None,
    ) -> None:
        self.db = db
        self.llm = llm or get_llm_client()
        self.embedding = embedding or get_embedding_client()
        self.safety = QualitySafetyAgent()

    async def _check_budget(self, user_id: uuid.UUID) -> bool:
        """Check if user has exceeded daily LLM budget."""
        today = datetime.datetime.now(datetime.timezone.utc).date()
        stmt = select(func.sum(AgentExecution.cost_usd)).where(
            AgentExecution.workflow_id == str(user_id),
            func.date(AgentExecution.started_at) == today,
        )
        res = await self.db.execute(stmt)
        cost_today = res.scalar_one() or 0.0
        return cost_today < settings.llm_budget_usd_per_user_per_day

    async def _record_execution(
        self,
        agent: str,
        workflow_id: str,
        input_data: str,
        output_data: Optional[dict[str, Any]],
        status: str,
        error: Optional[str],
        latency_ms: int,
        tokens_in: int,
        tokens_out: int,
        cost_usd: float,
    ) -> AgentExecution:
        input_hash = hashlib.sha256(input_data.encode("utf-8")).hexdigest()[:16]
        execution = AgentExecution(
            id=uuid.uuid4(),
            agent=agent,
            workflow_id=workflow_id,
            input_hash=input_hash,
            output=output_data,
            status=status,
            error=error,
            latency_ms=latency_ms,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            cost_usd=cost_usd,
            started_at=datetime.datetime.now(datetime.timezone.utc),
            completed_at=datetime.datetime.now(datetime.timezone.utc),
        )
        self.db.add(execution)
        await self.db.commit()
        return execution

    async def explain_concept(
        self,
        user_id: uuid.UUID,
        concept_slug: str,
        question: str,
        user_misconceptions: list[str] = [],
    ) -> dict[str, Any]:
        """Teaching Agent: grounded concept explanation citing stored concept content."""
        start_time = time.perf_counter()

        # 1. Budget check
        within_budget = await self._check_budget(user_id)
        if not within_budget:
            # Fallback to rule-based explanation
            return {
                "explanation": (
                    "🤖 [Rule-Based Fallback]\n"
                    "Daily AI budget exhausted. Please refer to the Concept Detail page for direct notes."
                ),
                "sources": [concept_slug],
                "is_ai": False,
                "is_fallback": True,
            }

        # 2. Retrieve ground truth concept content
        c_stmt = select(Concept).where(Concept.slug == concept_slug)
        c_res = await self.db.execute(c_stmt)
        concept = c_res.scalar_one_or_none()
        if not concept:
            raise ValueError(f"Concept '{concept_slug}' not found")

        # 3. Retrieve valid concept slugs for safety validation
        all_c_res = await self.db.execute(select(Concept.slug))
        valid_slugs = set(all_c_res.scalars().all())

        system_prompt = (
            "You are the Teaching Agent for PROJECT-EVOLVE. "
            "You explain Python concepts strictly grounded in the provided concept documentation. "
            "Address common misconceptions if present. "
            "NEVER make guarantees about jobs or exams. "
            "Prefix your response with 🤖 [AI-Generated Explanation]."
        )

        user_content = (
            f"Concept: {concept.title} ({concept.slug})\n\n"
            f"Official Documentation:\n{concept.content_md}\n\n"
            f"Known Learner Misconceptions: {', '.join(user_misconceptions) or 'None'}\n\n"
            f"Learner Question: {question}"
        )

        messages = [LLMMessage(role="user", content=user_content)]

        # Call LLM
        response = await self.llm.complete(messages, system=system_prompt, max_tokens=800)
        latency = int((time.perf_counter() - start_time) * 1000)

        # 4. Quality & Safety Validation
        val_report = self.safety.validate_teaching_output(
            explanation=response.content,
            concept_slug=concept_slug,
            valid_concept_slugs=valid_slugs,
        )

        final_explanation = response.content
        status_str = "success"
        error_msg = None

        if not val_report.is_valid:
            # Retry once with failure reason
            retry_prompt = (
                f"{system_prompt}\n"
                f"Previous output was rejected due to: {'; '.join(val_report.reasons)}. "
                f"Please fix and adhere strictly to the rules."
            )
            response = await self.llm.complete(messages, system=retry_prompt, max_tokens=800)
            val_retry = self.safety.validate_teaching_output(
                explanation=response.content,
                concept_slug=concept_slug,
                valid_concept_slugs=valid_slugs,
            )
            if not val_retry.is_valid:
                # Safe deterministic fallback
                final_explanation = (
                    f"🤖 [AI-Generated Explanation - Safe Fallback]\n\n"
                    f"{concept.content_md[:400]}...\n\n"
                    f"Sources cited: {concept.slug}"
                )
                status_str = "failed"
                error_msg = f"Safety check failed: {'; '.join(val_retry.reasons)}"
            else:
                final_explanation = response.content

        # Record in agent_executions table
        await self._record_execution(
            agent="teaching_agent",
            workflow_id=str(user_id),
            input_data=question,
            output_data={"concept": concept_slug, "explanation": final_explanation[:200]},
            status=status_str,
            error=error_msg,
            latency_ms=latency,
            tokens_in=response.tokens_in,
            tokens_out=response.tokens_out,
            cost_usd=response.cost_usd,
        )

        return {
            "explanation": final_explanation,
            "sources": [concept_slug],
            "is_ai": True,
            "latency_ms": latency,
        }

    async def generate_draft_question(self, concept_slug: str) -> Question:
        """Assessment Agent: generates a DRAFT question requiring admin approval before publication."""
        start_time = time.perf_counter()

        c_stmt = select(Concept).where(Concept.slug == concept_slug)
        c_res = await self.db.execute(c_stmt)
        concept = c_res.scalar_one_or_none()
        if not concept:
            raise ValueError(f"Concept '{concept_slug}' not found")

        system_prompt = (
            "You are the Assessment Agent for PROJECT-EVOLVE. "
            "Generate an original multiple-choice diagnostic question in valid JSON. "
            "Output format: {\"stem\": \"...\", \"options\": {\"A\": \"...\", \"B\": \"...\", \"C\": \"...\", \"D\": \"...\"}, \"correct\": \"A\", \"explanation\": \"...\", \"difficulty\": 0.3, \"discrimination\": 0.6}"
        )

        messages = [
            LLMMessage(
                role="user",
                content=f"Create a draft question testing: {concept.title}\n{concept.description}",
            )
        ]

        response = await self.llm.complete(messages, system=system_prompt, max_tokens=600)
        latency = int((time.perf_counter() - start_time) * 1000)

        # Parse JSON
        parsed: dict[str, Any] = {}
        try:
            cleaned = response.content.replace("```json", "").replace("```", "").strip()
            # Strip prefix if mock label was added
            if "{" in cleaned:
                cleaned = cleaned[cleaned.index("{"):cleaned.rindex("}") + 1]
            parsed = json.loads(cleaned)
        except Exception:
            parsed = {
                "stem": f"Which statement correctly describes {concept.title}?",
                "options": {
                    "A": "It is an integral feature of standard Python semantics.",
                    "B": "It was deprecated in Python 3.",
                    "C": "It is only available in external libraries.",
                    "D": "It raises a syntax error in Python.",
                },
                "correct": "A",
                "explanation": f"{concept.title} is standard in Python fundamentals.",
                "difficulty": 0.3,
                "discrimination": 0.5,
            }

        # Create Draft Question in DB with status="draft" (never auto-published)
        draft_id = f"q-draft-{uuid.uuid4().hex[:8]}"
        q_obj = Question(
            id=draft_id,
            concept_slug=concept_slug,
            type="multiple_choice",
            stem=parsed.get("stem", "Question stem"),
            options=parsed.get("options", {"A": "Yes", "B": "No"}),
            correct=parsed.get("correct", "A"),
            difficulty=float(parsed.get("difficulty", 0.3)),
            discrimination=float(parsed.get("discrimination", 0.5)),
            explanation=parsed.get("explanation", "Explanation"),
            status="draft",  # Stays draft until admin approval
        )
        self.db.add(q_obj)

        await self._record_execution(
            agent="assessment_agent",
            workflow_id="admin-draft",
            input_data=concept_slug,
            output_data={"question_id": draft_id, "status": "draft"},
            status="success",
            error=None,
            latency_ms=latency,
            tokens_in=response.tokens_in,
            tokens_out=response.tokens_out,
            cost_usd=response.cost_usd,
        )

        await self.db.commit()
        await self.db.refresh(q_obj)
        return q_obj
