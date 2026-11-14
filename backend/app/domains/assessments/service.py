"""Assessment service: adaptive item selection, server-side grading, and mastery updates."""
from __future__ import annotations

import datetime
import uuid
from typing import Any, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.assessments.schemas import AssessmentItem, SubmitAnswerResponse
from app.models import (
    Attempt,
    Concept,
    ConceptEdge,
    Evidence,
    Goal,
    MasteryState,
    Misconception,
    Question,
    QuestionMisconception,
    Response,
    TwinSnapshot,
)
from app.scoring.engine import (
    compute_credible_interval,
    compute_evidence_weight,
    update_mastery,
    EvidenceItem as ScoringEvidenceItem,
)
from app.scoring.gap_detector import ConceptEdge as ScoringEdge, MasteryState as ScoringMastery
from app.scoring.item_selector import Question as ScoringQuestion, select_next_item

DIAGNOSTIC_MAX_ITEMS = 15


class AssessmentService:
    def __init__(self, db: AsyncSession, user_id: uuid.UUID) -> None:
        self.db = db
        self.user_id = user_id

    async def start_attempt(self, kind: str = "diagnostic") -> Attempt:
        """Initialize a new assessment attempt."""
        attempt = Attempt(
            id=uuid.uuid4(),
            user_id=self.user_id,
            kind=kind,
            started_at=datetime.datetime.now(datetime.timezone.utc),
        )
        self.db.add(attempt)
        await self.db.commit()
        await self.db.refresh(attempt)
        return attempt

    async def get_next_question(self, attempt_id: uuid.UUID) -> Optional[AssessmentItem]:
        """Select next adaptive question based on frontier and uncertainty."""
        # 1. Count answered questions for this attempt
        answered_stmt = select(Response.question_id).where(Response.attempt_id == attempt_id)
        answered_res = await self.db.execute(answered_stmt)
        seen_qids = set(answered_res.scalars().all())

        item_number = len(seen_qids) + 1
        if item_number > DIAGNOSTIC_MAX_ITEMS:
            return None  # Finished

        # 2. Get user's target concepts from active goal, or fall back to foundational concepts
        goal_stmt = select(Goal).where(Goal.user_id == self.user_id, Goal.active.is_(True))
        goal_res = await self.db.execute(goal_stmt)
        active_goal = goal_res.scalar_one_or_none()

        target_slugs: list[str] = []
        if active_goal and active_goal.target_concept_ids:
            target_slugs = [str(x) for x in active_goal.target_concept_ids]
        else:
            # Default diagnostic target concepts
            target_slugs = [
                "variables-basics", "data-types-overview", "integers", "floats", "strings-basics",
                "booleans", "arithmetic-operators", "comparison-operators", "if-statements",
                "for-loops", "while-loops", "lists-basics", "functions-basics", "try-except",
            ]

        # 3. Load concepts, edges, and current mastery states
        c_stmt = select(Concept)
        c_res = await self.db.execute(c_stmt)
        all_concepts = {c.slug: c for c in c_res.scalars().all()}

        m_stmt = select(MasteryState).where(MasteryState.user_id == self.user_id)
        m_res = await self.db.execute(m_stmt)
        mastery_map: dict[str, MasteryState] = {m.concept_slug: m for m in m_res.scalars().all()}

        e_stmt = select(ConceptEdge)
        e_res = await self.db.execute(e_stmt)
        edges = e_res.scalars().all()
        id_to_slug = {c.id: c.slug for c in all_concepts.values()}

        scoring_edges = [
            ScoringEdge(
                from_id=uuid.UUID(int=abs(hash(id_to_slug[e.from_concept_id])) % (2**127)),
                to_id=uuid.UUID(int=abs(hash(id_to_slug[e.to_concept_id])) % (2**127)),
            )
            for e in edges
            if e.from_concept_id in id_to_slug and e.to_concept_id in id_to_slug
        ]

        # Helper mapping for item selector
        slug_to_uuid = {slug: uuid.UUID(int=abs(hash(slug)) % (2**127)) for slug in all_concepts}
        uuid_to_slug = {u: slug for slug, u in slug_to_uuid.items()}

        scoring_mastery: dict[uuid.UUID, ScoringMastery] = {}
        for slug, u in slug_to_uuid.items():
            m = mastery_map.get(slug)
            scoring_mastery[u] = ScoringMastery(
                concept_id=u,
                mastery=m.mastery if m else 0.5,
                confidence=m.confidence if m else 0.0,
            )

        target_uuids = [slug_to_uuid[slug] for slug in target_slugs if slug in slug_to_uuid]

        # 4. Fetch available questions
        q_stmt = select(Question).where(Question.status == "approved")
        q_res = await self.db.execute(q_stmt)
        all_questions = q_res.scalars().all()

        scoring_questions: list[ScoringQuestion] = []
        q_by_uuid: dict[uuid.UUID, Question] = {}
        for q in all_questions:
            c_uuid = slug_to_uuid.get(q.concept_slug)
            if c_uuid:
                q_uuid = uuid.UUID(int=abs(hash(q.id)) % (2**127))
                q_by_uuid[q_uuid] = q
                scoring_questions.append(
                    ScoringQuestion(
                        id=q_uuid,
                        concept_id=c_uuid,
                        difficulty=q.difficulty,
                        discrimination=q.discrimination,
                        status=q.status,
                    )
                )

        seen_uuids = [uuid.UUID(int=abs(hash(qid)) % (2**127)) for qid in seen_qids]

        # 5. Run adaptive selection algorithm
        chosen = select_next_item(
            mastery_states=scoring_mastery,
            concept_edges=scoring_edges,
            target_concepts=target_uuids,
            available_questions=scoring_questions,
            recently_seen_question_ids=seen_uuids,
        )

        if not chosen or chosen.id not in q_by_uuid:
            # Fallback to any unseen question
            unseen = [q for q in all_questions if q.id not in seen_qids]
            if not unseen:
                return None
            selected_q = unseen[0]
        else:
            selected_q = q_by_uuid[chosen.id]

        concept = all_concepts.get(selected_q.concept_slug)
        title = concept.title if concept else selected_q.concept_slug

        return AssessmentItem(
            attempt_id=attempt_id,
            item_number=item_number,
            total_items=DIAGNOSTIC_MAX_ITEMS,
            question_id=selected_q.id,
            concept_slug=selected_q.concept_slug,
            concept_title=title,
            type=selected_q.type,
            stem=selected_q.stem,
            options=selected_q.options if isinstance(selected_q.options, dict) else {},
        )

    async def submit_response(
        self, attempt_id: uuid.UUID, question_id: str, answer: Any, time_ms: int
    ) -> SubmitAnswerResponse:
        """Server-side evaluate answer, record response & evidence, and update mastery state."""
        # 1. Fetch question
        q_stmt = select(Question).where(Question.id == question_id)
        q_res = await self.db.execute(q_stmt)
        question = q_res.scalar_one_or_none()
        if not question:
            raise ValueError(f"Question '{question_id}' not found")

        # 2. Grade server-side
        is_correct = False
        if isinstance(question.correct, list):
            is_correct = sorted(question.correct) == sorted(answer if isinstance(answer, list) else [answer])
        else:
            is_correct = str(question.correct).strip() == str(answer).strip()

        # 3. Detect misconception
        misconception_flag: Optional[dict[str, str]] = None
        selected_misc_id: Optional[str] = None

        if not is_correct and isinstance(answer, str):
            qm_stmt = select(QuestionMisconception).where(
                QuestionMisconception.question_id == question_id,
                QuestionMisconception.option_key == answer,
            )
            qm_res = await self.db.execute(qm_stmt)
            qm = qm_res.scalar_one_or_none()
            if qm:
                selected_misc_id = qm.misconception_id
                m_stmt = select(Misconception).where(Misconception.id == selected_misc_id)
                m_res = await self.db.execute(m_stmt)
                m_obj = m_res.scalar_one_or_none()
                if m_obj:
                    misconception_flag = {
                        "id": m_obj.id,
                        "title": m_obj.title,
                        "explanation": m_obj.explanation,
                    }

        # 4. Save Response
        response = Response(
            id=uuid.uuid4(),
            attempt_id=attempt_id,
            question_id=question_id,
            answer=answer,
            correct=is_correct,
            time_ms=time_ms,
            selected_misconception_id=selected_misc_id,
        )
        self.db.add(response)

        # 5. Create Evidence Item
        val = 1.0 if is_correct else 0.0
        weight = compute_evidence_weight(
            source_type="assessment_verified",
            age_days=0.0,
            discrimination=question.discrimination,
            time_ms=time_ms,
            disputed=False,
        )
        evidence = Evidence(
            id=uuid.uuid4(),
            user_id=self.user_id,
            concept_slug=question.concept_slug,
            source_type="assessment_verified",
            value=val,
            weight=weight,
            ref_type="response",
            ref_id=str(response.id),
            disputed=False,
        )
        self.db.add(evidence)
        await self.db.flush()

        # 6. Update MasteryState using Beta distribution update
        ms_stmt = select(MasteryState).where(
            MasteryState.user_id == self.user_id,
            MasteryState.concept_slug == question.concept_slug,
        )
        ms_res = await self.db.execute(ms_stmt)
        mastery_state = ms_res.scalar_one_or_none()

        if not mastery_state:
            mastery_state = MasteryState(
                user_id=self.user_id,
                concept_slug=question.concept_slug,
                alpha=1.0,
                beta=1.0,
                mastery=0.5,
                confidence=0.0,
                updated_at=datetime.datetime.now(datetime.timezone.utc),
            )
            self.db.add(mastery_state)

        # Apply update
        new_alpha = mastery_state.alpha + (weight * val)
        new_beta = mastery_state.beta + (weight * (1.0 - val))
        mastery_state.alpha = new_alpha
        mastery_state.beta = new_beta
        mastery_state.mastery = new_alpha / (new_alpha + new_beta)

        low, high = compute_credible_interval(new_alpha, new_beta, ci=0.80)
        mastery_state.confidence = max(0.0, min(1.0, 1.0 - (high - low)))
        mastery_state.updated_at = datetime.datetime.now(datetime.timezone.utc)

        # 7. Check if attempt complete
        ans_count_stmt = select(func.count(Response.id)).where(Response.attempt_id == attempt_id)
        ans_res = await self.db.execute(ans_count_stmt)
        count = ans_res.scalar_one() or 0

        is_completed = count >= DIAGNOSTIC_MAX_ITEMS
        if is_completed:
            att_stmt = select(Attempt).where(Attempt.id == attempt_id)
            att_res = await self.db.execute(att_stmt)
            attempt_obj = att_res.scalar_one_or_none()
            if attempt_obj and not attempt_obj.completed_at:
                attempt_obj.completed_at = datetime.datetime.now(datetime.timezone.utc)
                # Create snapshot
                await self._take_twin_snapshot("diagnostic_completed")

        await self.db.commit()

        # 8. Check for next item
        next_item = None
        if not is_completed:
            next_item = await self.get_next_question(attempt_id)
            if not next_item:
                is_completed = True

        return SubmitAnswerResponse(
            attempt_id=attempt_id,
            question_id=question_id,
            correct=is_correct,
            explanation=question.explanation,
            misconception_flagged=misconception_flag,
            is_completed=is_completed,
            next_item=next_item,
            mastery_updated={
                "concept_slug": question.concept_slug,
                "mastery": round(mastery_state.mastery, 3),
                "confidence": round(mastery_state.confidence, 3),
            },
        )

    async def _take_twin_snapshot(self, trigger: str) -> None:
        """Capture complete Cognitive Twin state snapshot."""
        ms_stmt = select(MasteryState).where(MasteryState.user_id == self.user_id)
        ms_res = await self.db.execute(ms_stmt)
        states = ms_res.scalars().all()
        snapshot_data = {
            m.concept_slug: {
                "mastery": round(m.mastery, 3),
                "confidence": round(m.confidence, 3),
                "alpha": round(m.alpha, 3),
                "beta": round(m.beta, 3),
            }
            for m in states
        }
        snap = TwinSnapshot(
            id=uuid.uuid4(),
            user_id=self.user_id,
            state=snapshot_data,
            trigger=trigger,
            taken_at=datetime.datetime.now(datetime.timezone.utc),
        )
        self.db.add(snap)
