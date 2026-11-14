"""Knowledge Genome API router."""
from __future__ import annotations

import uuid
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import CurrentUser, get_current_user, get_db, oauth2_scheme
from app.domains.auth.service import decode_access_token
from app.domains.genome.schemas import (
    ConceptDetail,
    ConceptSummary,
    GenomeGraph,
    GraphEdge,
    GraphNode,
)
from app.models import Concept, ConceptEdge, MasteryState, Misconception

router = APIRouter(prefix="/genome", tags=["Genome"])


async def get_optional_user_id(token: Annotated[Optional[str], Depends(oauth2_scheme)] = None) -> Optional[uuid.UUID]:
    if not token:
        return None
    payload = decode_access_token(token)
    if payload and "sub" in payload:
        try:
            return uuid.UUID(payload["sub"])
        except ValueError:
            return None
    return None


@router.get("/concepts", response_model=list[ConceptSummary])
async def list_concepts(
    db: Annotated[AsyncSession, Depends(get_db)],
    user_id: Annotated[Optional[uuid.UUID], Depends(get_optional_user_id)],
    difficulty: Optional[int] = Query(None, ge=1, le=5),
):
    """List all Knowledge Genome concepts with optional user mastery overlay."""
    stmt = select(Concept).order_by(Concept.difficulty, Concept.slug)
    if difficulty:
        stmt = stmt.where(Concept.difficulty == difficulty)
    res = await db.execute(stmt)
    concepts = res.scalars().all()

    # If authenticated, fetch user mastery estimates
    mastery_map: dict[str, MasteryState] = {}
    if user_id:
        m_stmt = select(MasteryState).where(MasteryState.user_id == user_id)
        m_res = await db.execute(m_stmt)
        for m in m_res.scalars().all():
            mastery_map[m.concept_slug] = m

    summaries: list[ConceptSummary] = []
    for c in concepts:
        m_state = mastery_map.get(c.slug)
        summaries.append(
            ConceptSummary(
                id=c.id,
                slug=c.slug,
                title=c.title,
                description=c.description,
                difficulty=c.difficulty,
                domain=c.domain,
                mastery=round(m_state.mastery, 3) if m_state else None,
                confidence=round(m_state.confidence, 3) if m_state else None,
            )
        )
    return summaries


@router.get("/concepts/{slug}", response_model=ConceptDetail)
async def get_concept_detail(
    slug: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    user_id: Annotated[Optional[uuid.UUID], Depends(get_optional_user_id)],
):
    """Get full concept detail including prerequisites, dependents, and content."""
    stmt = select(Concept).where(Concept.slug == slug)
    res = await db.execute(stmt)
    concept = res.scalar_one_or_none()
    if not concept:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Concept '{slug}' not found")

    # Prerequisites (edges where to_concept_id == concept.id)
    prereq_stmt = (
        select(Concept.slug)
        .join(ConceptEdge, ConceptEdge.from_concept_id == Concept.id)
        .where(ConceptEdge.to_concept_id == concept.id)
    )
    prereq_res = await db.execute(prereq_stmt)
    prereqs = list(prereq_res.scalars().all())

    # Dependents (edges where from_concept_id == concept.id)
    dep_stmt = (
        select(Concept.slug)
        .join(ConceptEdge, ConceptEdge.to_concept_id == Concept.id)
        .where(ConceptEdge.from_concept_id == concept.id)
    )
    dep_res = await db.execute(dep_stmt)
    dependents = list(dep_res.scalars().all())

    # Misconceptions for this concept
    misc_stmt = select(Misconception).where(Misconception.concept_slug == slug)
    misc_res = await db.execute(misc_stmt)
    misconceptions = [
        {"id": m.id, "title": m.title, "explanation": m.explanation}
        for m in misc_res.scalars().all()
    ]

    # Mastery
    m_state = None
    if user_id:
        m_stmt = select(MasteryState).where(MasteryState.user_id == user_id, MasteryState.concept_slug == slug)
        m_res = await db.execute(m_stmt)
        m_state = m_res.scalar_one_or_none()

    return ConceptDetail(
        id=concept.id,
        slug=concept.slug,
        title=concept.title,
        description=concept.description,
        difficulty=concept.difficulty,
        domain=concept.domain,
        content_md=concept.content_md,
        prerequisites=prereqs,
        dependents=dependents,
        misconceptions=misconceptions,
        mastery=round(m_state.mastery, 3) if m_state else None,
        confidence=round(m_state.confidence, 3) if m_state else None,
    )


@router.get("/graph", response_model=GenomeGraph)
async def get_genome_graph(
    db: Annotated[AsyncSession, Depends(get_db)],
    user_id: Annotated[Optional[uuid.UUID], Depends(get_optional_user_id)],
):
    """Retrieve full Knowledge Genome graph structure for interactive rendering."""
    # Fetch all concepts
    c_stmt = select(Concept).order_by(Concept.difficulty, Concept.slug)
    c_res = await db.execute(c_stmt)
    concepts = c_res.scalars().all()
    concept_id_to_slug = {c.id: c.slug for c in concepts}

    # Fetch mastery map if user authenticated
    mastery_map: dict[str, MasteryState] = {}
    if user_id:
        m_stmt = select(MasteryState).where(MasteryState.user_id == user_id)
        m_res = await db.execute(m_stmt)
        for m in m_res.scalars().all():
            mastery_map[m.concept_slug] = m

    nodes: list[GraphNode] = []
    for c in concepts:
        m = mastery_map.get(c.slug)
        nodes.append(
            GraphNode(
                id=c.slug,
                title=c.title,
                difficulty=c.difficulty,
                mastery=round(m.mastery, 3) if m else None,
                confidence=round(m.confidence, 3) if m else None,
            )
        )

    # Fetch all edges
    e_stmt = select(ConceptEdge)
    e_res = await db.execute(e_stmt)
    edges_raw = e_res.scalars().all()

    edges: list[GraphEdge] = []
    for e in edges_raw:
        from_slug = concept_id_to_slug.get(e.from_concept_id)
        to_slug = concept_id_to_slug.get(e.to_concept_id)
        if from_slug and to_slug:
            edges.append(
                GraphEdge(
                    from_slug=from_slug,
                    to_slug=to_slug,
                    type=e.type,
                    strength=e.strength,
                )
            )

    return GenomeGraph(nodes=nodes, edges=edges)
