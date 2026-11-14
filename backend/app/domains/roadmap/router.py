"""Roadmap API router."""
from __future__ import annotations

import datetime
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.deps import CurrentUser, get_current_user, get_db
from app.domains.roadmap.schemas import RoadmapItemDetail, RoadmapRead
from app.models import Concept, ConceptEdge, Goal, MasteryState, Roadmap, RoadmapItem
from app.scoring.gap_detector import (
    Concept as ScoringConcept,
    ConceptEdge as ScoringEdge,
    MasteryState as ScoringMastery,
    detect_gaps,
)

router = APIRouter(prefix="/roadmap", tags=["Roadmap"])


@router.get("/", response_model=RoadmapRead)
async def get_roadmap(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Retrieve learner's active roadmap, or auto-generate if missing."""
    u_id = uuid.UUID(current_user.id)
    stmt = (
        select(Roadmap)
        .where(Roadmap.user_id == u_id)
        .options(selectinload(Roadmap.items))
    )
    res = await db.execute(stmt)
    roadmap = res.scalar_one_or_none()

    if not roadmap or not roadmap.items:
        roadmap = await generate_user_roadmap(u_id, db)

    # Concept metadata lookup
    c_stmt = select(Concept)
    c_res = await db.execute(c_stmt)
    concept_map = {c.slug: c for c in c_res.scalars().all()}

    items_detail: list[RoadmapItemDetail] = []
    for item in sorted(roadmap.items, key=lambda x: x.position):
        c = concept_map.get(item.concept_slug)
        reason_dict = item.reason if isinstance(item.reason, dict) else {}
        items_detail.append(
            RoadmapItemDetail(
                id=item.id,
                position=item.position,
                concept_slug=item.concept_slug,
                concept_title=c.title if c else item.concept_slug,
                difficulty=c.difficulty if c else 1,
                status=item.status,
                gap_type=reason_dict.get("gap_type", "gap"),
                priority=reason_dict.get("priority", 1.0),
                because=reason_dict.get("because", f"Recommended foundation for your target goal."),
            )
        )

    return RoadmapRead(
        id=roadmap.id,
        user_id=roadmap.user_id,
        items=items_detail,
        created_at=roadmap.created_at,
        updated_at=roadmap.updated_at,
    )


@router.post("/generate", response_model=RoadmapRead)
async def regenerate_roadmap(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Force re-generate roadmap from real evidence and detected gaps."""
    u_id = uuid.UUID(current_user.id)
    roadmap = await generate_user_roadmap(u_id, db)
    return await get_roadmap(current_user, db)


async def generate_user_roadmap(user_id: uuid.UUID, db: AsyncSession) -> Roadmap:
    """Core deterministic algorithm: compute gaps and build roadmap."""
    # 1. Fetch user's active goal
    goal_stmt = select(Goal).where(Goal.user_id == user_id, Goal.active.is_(True))
    goal_res = await db.execute(goal_stmt)
    goal = goal_res.scalar_one_or_none()

    target_slugs: list[str] = []
    if goal and goal.target_concept_ids:
        target_slugs = [str(x) for x in goal.target_concept_ids]
    else:
        target_slugs = [
            "variables-basics", "integers", "floats", "strings-basics", "booleans",
            "if-statements", "for-loops", "while-loops", "lists-basics", "functions-basics",
        ]

    # 2. Fetch all concepts and edges
    c_stmt = select(Concept)
    c_res = await db.execute(c_stmt)
    all_concepts = c_res.scalars().all()
    concept_map = {c.slug: c for c in all_concepts}
    id_to_slug = {c.id: c.slug for c in all_concepts}

    slug_to_uuid = {slug: uuid.UUID(int=abs(hash(slug)) % (2**127)) for slug in concept_map}
    uuid_to_slug = {u: slug for slug, u in slug_to_uuid.items()}

    e_stmt = select(ConceptEdge)
    e_res = await db.execute(e_stmt)
    edges = e_res.scalars().all()

    scoring_edges = [
        ScoringEdge(
            from_id=slug_to_uuid[id_to_slug[e.from_concept_id]],
            to_id=slug_to_uuid[id_to_slug[e.to_concept_id]],
        )
        for e in edges
        if e.from_concept_id in id_to_slug and e.to_concept_id in id_to_slug
    ]

    # 3. Fetch user mastery states
    m_stmt = select(MasteryState).where(MasteryState.user_id == user_id)
    m_res = await db.execute(m_stmt)
    user_mastery = {m.concept_slug: m for m in m_res.scalars().all()}

    scoring_mastery: dict[uuid.UUID, ScoringMastery] = {}
    for slug, u in slug_to_uuid.items():
        m = user_mastery.get(slug)
        scoring_mastery[u] = ScoringMastery(
            concept_id=u,
            mastery=m.mastery if m else 0.5,
            confidence=m.confidence if m else 0.0,
        )

    scoring_concepts: dict[uuid.UUID, ScoringConcept] = {
        u: ScoringConcept(id=u, slug=slug, title=concept_map[slug].title, difficulty=concept_map[slug].difficulty / 5.0)
        for slug, u in slug_to_uuid.items()
    }

    target_uuids = [slug_to_uuid[s] for s in target_slugs if s in slug_to_uuid]

    # 4. Run gap detection
    gaps = detect_gaps(
        target_concept_ids=target_uuids,
        concept_edges=scoring_edges,
        mastery_states=scoring_mastery,
        all_concepts=scoring_concepts,
    )

    # 5. Fetch or create Roadmap entity
    r_stmt = select(Roadmap).where(Roadmap.user_id == user_id).options(selectinload(Roadmap.items))
    r_res = await db.execute(r_stmt)
    roadmap = r_res.scalar_one_or_none()

    if not roadmap:
        roadmap = Roadmap(id=uuid.uuid4(), user_id=user_id)
        db.add(roadmap)
        await db.flush()
    else:
        # Clear existing items
        for old_item in roadmap.items:
            await db.delete(old_item)
        roadmap.items.clear()
        await db.flush()

    # 6. Add roadmap items from ranked gaps
    for idx, gap in enumerate(gaps[:12]):  # Top 12 actionable steps
        c_slug = gap.slug
        reason_payload = {
            "gap_type": gap.reason,
            "priority": round(gap.priority, 3),
            "blocking_count": gap.blocking_count,
            "because": (
                f"Missing foundation (mastery {gap.mastery:.2f}). Blocks {gap.blocking_count} dependent concepts in your target goal."
                if gap.reason == "gap"
                else f"Confidence too low ({gap.confidence:.2f}). Verification needed before proceeding."
            ),
        }
        item = RoadmapItem(
            id=uuid.uuid4(),
            roadmap_id=roadmap.id,
            concept_slug=c_slug,
            position=idx + 1,
            reason=reason_payload,
            status="pending" if idx > 0 else "in_progress",
        )
        db.add(item)
        roadmap.items.append(item)

    roadmap.updated_at = datetime.datetime.now(datetime.timezone.utc)
    await db.commit()
    stmt = select(Roadmap).where(Roadmap.id == roadmap.id).options(selectinload(Roadmap.items))
    res = await db.execute(stmt)
    return res.scalar_one()
