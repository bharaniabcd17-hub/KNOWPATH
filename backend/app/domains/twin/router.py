"""Cognitive Twin API router."""
from __future__ import annotations

import datetime
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import CurrentUser, get_current_user, get_db
from app.domains.twin.schemas import (
    MasteryStateDetail,
    SnapshotItem,
    TopEvidenceItem,
    TwinPageData,
    WhyScorePanel,
)
from app.models import Concept, ConceptEdge, Evidence, MasteryState, TwinSnapshot
from app.scoring.engine import compute_credible_interval

router = APIRouter(prefix="/twin", tags=["Twin"])


@router.get("/", response_model=TwinPageData)
async def get_twin(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Get complete Cognitive Twin state for authenticated learner."""
    u_id = uuid.UUID(current_user.id)

    # 1. Fetch all concepts
    c_stmt = select(Concept).order_by(Concept.difficulty, Concept.slug)
    c_res = await db.execute(c_stmt)
    all_concepts = c_res.scalars().all()
    concept_map = {c.slug: c for c in all_concepts}
    concept_id_to_slug = {c.id: c.slug for c in all_concepts}

    # 2. Fetch prerequisite edges
    e_stmt = select(ConceptEdge)
    e_res = await db.execute(e_stmt)
    edges = e_res.scalars().all()
    prereq_map: dict[str, list[str]] = {}
    for e in edges:
        from_slug = concept_id_to_slug.get(e.from_concept_id)
        to_slug = concept_id_to_slug.get(e.to_concept_id)
        if from_slug and to_slug:
            prereq_map.setdefault(to_slug, []).append(from_slug)

    # 3. Fetch user's mastery states (STRICTLY SCOPED BY USER ID)
    m_stmt = select(MasteryState).where(MasteryState.user_id == u_id)
    m_res = await db.execute(m_stmt)
    mastery_records = {m.concept_slug: m for m in m_res.scalars().all()}

    # 4. Fetch evidence grouped by concept (STRICTLY SCOPED BY USER ID)
    ev_stmt = select(Evidence).where(Evidence.user_id == u_id).order_by(desc(Evidence.weight))
    ev_res = await db.execute(ev_stmt)
    all_evidence = ev_res.scalars().all()

    evidence_by_concept: dict[str, list[Evidence]] = {}
    for ev in all_evidence:
        evidence_by_concept.setdefault(ev.concept_slug, []).append(ev)

    # 5. Build concept details with deterministic why-panels
    details: list[MasteryStateDetail] = []
    total_mastery = 0.0
    total_conf = 0.0
    evaluated_count = 0

    for c in all_concepts:
        m = mastery_records.get(c.slug)
        ev_items = evidence_by_concept.get(c.slug, [])

        alpha = m.alpha if m else 1.0
        beta_val = m.beta if m else 1.0
        mastery = m.mastery if m else 0.5
        confidence = m.confidence if m else 0.0
        updated = m.updated_at if m else datetime.datetime.now(datetime.timezone.utc)

        if m:
            total_mastery += mastery
            total_conf += confidence
            evaluated_count += 1

        low, high = compute_credible_interval(alpha, beta_val, ci=0.80)

        # Source mix calculation
        source_mix = {"assessment_verified": 0, "ai_estimated": 0, "self_reported": 0}
        for item in ev_items:
            if item.source_type in source_mix:
                source_mix[item.source_type] += 1

        top_evidence = [
            TopEvidenceItem(
                id=item.id,
                source_type=item.source_type,
                value=item.value,
                weight=round(item.weight, 4),
                observed_at=item.observed_at,
                disputed=item.disputed,
            )
            for item in ev_items[:3]
        ]

        # Prerequisite foundation gap check (Section 7.2)
        has_foundation_gap = False
        if mastery >= 0.6 and confidence >= 0.3:
            for p_slug in prereq_map.get(c.slug, []):
                p_state = mastery_records.get(p_slug)
                if p_state and p_state.confidence >= 0.3 and p_state.mastery < 0.4:
                    has_foundation_gap = True
                    break

        formula_text = (
            f"mastery = alpha / (alpha + beta) = {alpha:.2f} / ({alpha:.2f} + {beta_val:.2f}) = {mastery:.2f}. "
            f"Confidence: {confidence:.2f} (80% credible interval [{low:.2f}, {high:.2f}])."
        )

        why_panel = WhyScorePanel(
            concept_slug=c.slug,
            mastery=round(mastery, 3),
            confidence=round(confidence, 3),
            interval_low=round(low, 3),
            interval_high=round(high, 3),
            alpha=round(alpha, 3),
            beta=round(beta_val, 3),
            formula_explanation=formula_text,
            top_evidence=top_evidence,
            source_mix=source_mix,
            possible_foundation_gap=has_foundation_gap,
        )

        details.append(
            MasteryStateDetail(
                concept_slug=c.slug,
                concept_title=c.title,
                difficulty=c.difficulty,
                mastery=round(mastery, 3),
                confidence=round(confidence, 3),
                interval_low=round(low, 3),
                interval_high=round(high, 3),
                evidence_count=len(ev_items),
                why_panel=why_panel,
                possible_foundation_gap=has_foundation_gap,
                updated_at=updated,
            )
        )

    # 6. Snapshots count
    snap_count_stmt = select(func.count(TwinSnapshot.id)).where(TwinSnapshot.user_id == u_id)
    snap_res = await db.execute(snap_count_stmt)
    snap_count = snap_res.scalar_one() or 0

    return TwinPageData(
        user_id=u_id,
        overall_mastery=round(total_mastery / max(1, evaluated_count), 3) if evaluated_count else 0.5,
        overall_confidence=round(total_conf / max(1, evaluated_count), 3) if evaluated_count else 0.0,
        concepts_evaluated=evaluated_count,
        total_concepts=len(all_concepts),
        concepts=details,
        snapshots_count=snap_count,
    )


@router.get("/snapshots", response_model=list[SnapshotItem])
async def get_snapshots(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """List historical snapshots of the learner's Cognitive Twin."""
    stmt = (
        select(TwinSnapshot)
        .where(TwinSnapshot.user_id == uuid.UUID(current_user.id))
        .order_by(desc(TwinSnapshot.taken_at))
        .limit(20)
    )
    res = await db.execute(stmt)
    snapshots = res.scalars().all()
    return [
        SnapshotItem(
            id=s.id,
            taken_at=s.taken_at,
            trigger=s.trigger,
            state=s.state,
        )
        for s in snapshots
    ]
