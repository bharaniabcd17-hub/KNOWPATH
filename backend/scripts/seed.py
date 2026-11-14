"""Seed database with validated concepts, questions, misconceptions, and prerequisite edges."""
from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select
from app.database import AsyncSessionFactory, engine, Base
from app.models import (
    Concept,
    ConceptEdge,
    Misconception,
    Question,
    QuestionMisconception,
)

# Reuse the parser functions from content/validate.py
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "content"))
from validate import parse_concepts, parse_misconceptions, parse_questions


async def seed_data():
    print("=" * 60)
    print("PROJECT-EVOLVE Database Seeding")
    print("=" * 60)

    # Ensure tables exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    content_dir = Path(__file__).parent.parent.parent / "content" / "python"

    concepts = parse_concepts((content_dir / "concepts.yaml").read_text(encoding="utf-8"))
    misconceptions = parse_misconceptions((content_dir / "misconceptions.yaml").read_text(encoding="utf-8"))
    questions = parse_questions((content_dir / "questions.yaml").read_text(encoding="utf-8"))

    async with AsyncSessionFactory() as session:
        # 1. Upsert Concepts
        print(f"Seeding {len(concepts)} concepts...")
        slug_to_concept: dict[str, Concept] = {}
        for slug, c_data in concepts.items():
            existing = await session.scalar(select(Concept).where(Concept.slug == slug))
            if not existing:
                c_obj = Concept(
                    slug=slug,
                    title=c_data.get("title", slug),
                    description=c_data.get("description", ""),
                    difficulty=int(c_data.get("difficulty", 1)),
                    domain=c_data.get("domain", "python_fundamentals"),
                    content_md=c_data.get("content_md", ""),
                )
                session.add(c_obj)
                slug_to_concept[slug] = c_obj
            else:
                slug_to_concept[slug] = existing

        await session.flush()

        # Re-fetch all concepts to get their UUIDs
        c_res = await session.execute(select(Concept))
        for c in c_res.scalars().all():
            slug_to_concept[c.slug] = c

        # 2. Upsert Concept Edges (Prerequisites)
        print("Seeding prerequisite edges...")
        edge_count = 0
        for slug, c_data in concepts.items():
            to_concept = slug_to_concept.get(slug)
            if not to_concept:
                continue
            for p_slug in c_data.get("prerequisites", []):
                from_concept = slug_to_concept.get(p_slug)
                if from_concept:
                    edge_exists = await session.scalar(
                        select(ConceptEdge).where(
                            ConceptEdge.from_concept_id == from_concept.id,
                            ConceptEdge.to_concept_id == to_concept.id,
                        )
                    )
                    if not edge_exists:
                        edge = ConceptEdge(
                            from_concept_id=from_concept.id,
                            to_concept_id=to_concept.id,
                            type="prerequisite",
                            strength=1.0,
                        )
                        session.add(edge)
                        edge_count += 1

        await session.flush()

        # 3. Upsert Misconceptions
        print(f"Seeding {len(misconceptions)} misconceptions...")
        misc_count = 0
        for m_id, m_data in misconceptions.items():
            existing_m = await session.scalar(select(Misconception).where(Misconception.id == m_id))
            if not existing_m:
                m_obj = Misconception(
                    id=m_id,
                    concept_slug=m_data.get("concept_slug", "variables-basics"),
                    title=m_data.get("title", m_id),
                    explanation=m_data.get("explanation", ""),
                )
                session.add(m_obj)
                misc_count += 1

        await session.flush()

        # 4. Upsert Questions & Option Misconceptions
        print(f"Seeding {len(questions)} questions...")
        q_count = 0
        qm_count = 0
        for q in questions:
            q_id = q["id"]
            existing_q = await session.scalar(select(Question).where(Question.id == q_id))
            if not existing_q:
                q_obj = Question(
                    id=q_id,
                    concept_slug=q.get("concept_slug", "variables-basics"),
                    type=q.get("type", "multiple_choice"),
                    stem=q.get("stem", ""),
                    options=q.get("options", {}),
                    correct=q.get("correct", "A"),
                    difficulty=float(q.get("difficulty", 0.3)),
                    discrimination=float(q.get("discrimination", 0.5)),
                    explanation=q.get("explanation", ""),
                    status="approved",
                )
                session.add(q_obj)
                q_count += 1

                # Option misconception links
                for opt_key, misc_id in q.get("misconception_tags", {}).items():
                    if misc_id in misconceptions:
                        qm = QuestionMisconception(
                            question_id=q_id,
                            option_key=opt_key,
                            misconception_id=misc_id,
                        )
                        session.add(qm)
                        qm_count += 1

        await session.commit()
        print("-" * 60)
        print("SEEDING COMPLETE:")
        print(f"  - Concepts seeded: {len(slug_to_concept)}")
        print(f"  - Prerequisite edges created: {edge_count}")
        print(f"  - Misconceptions seeded: {misc_count}")
        print(f"  - Questions seeded: {q_count}")
        print(f"  - Question misconception links: {qm_count}")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(seed_data())
