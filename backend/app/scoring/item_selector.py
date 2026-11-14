"""Item selector — chooses the next assessment question using frontier algorithm."""
from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from app.scoring.gap_detector import ConceptEdge, MasteryState


@dataclass
class Question:
    id: UUID
    concept_id: UUID
    difficulty: float  # 0.0 – 1.0
    discrimination: float
    status: str  # approved | draft | retired


def select_next_item(
    mastery_states: dict[UUID, MasteryState],
    concept_edges: list[ConceptEdge],
    target_concepts: list[UUID],
    available_questions: list[Question],
    recently_seen_question_ids: list[UUID],
    max_difficulty_delta: float = 0.3,
) -> Question | None:
    """
    1. Find frontier: concepts whose prerequisites are mastered (>0.6) or unknown
    2. Among frontier, pick concept with highest uncertainty (lowest confidence)
    3. Pick question for that concept with difficulty closest to current mastery
    4. Avoid recently seen questions
    5. Balance coverage across target concepts
    """
    # Build prerequisite map: concept_id -> set of prerequisite IDs
    prereq_map: dict[UUID, set[UUID]] = {}
    for edge in concept_edges:
        if edge.edge_type == "prerequisite":
            prereq_map.setdefault(edge.to_id, set()).add(edge.from_id)

    # Find frontier concepts (all prerequisites mastered or unknown)
    frontier: list[UUID] = []
    for cid in target_concepts:
        prereqs = prereq_map.get(cid, set())
        all_ok = True
        for prereq_id in prereqs:
            prereq_state = mastery_states.get(prereq_id)
            if prereq_state is not None and prereq_state.mastery < 0.6:
                all_ok = False
                break
        if all_ok:
            frontier.append(cid)

    if not frontier:
        # Fallback: include all target concepts
        frontier = list(target_concepts)

    if not frontier:
        return available_questions[0] if available_questions else None

    # Pick concept with highest uncertainty (lowest confidence)
    def concept_uncertainty(cid: UUID) -> float:
        state = mastery_states.get(cid)
        if state is None:
            return 1.0  # unknown = maximum uncertainty
        return 1.0 - state.confidence

    frontier.sort(key=concept_uncertainty, reverse=True)
    chosen_concept = frontier[0]

    # Get current mastery for chosen concept
    chosen_state = mastery_states.get(chosen_concept)
    current_mastery = chosen_state.mastery if chosen_state else 0.5

    # Filter available questions: correct concept, approved, not recently seen
    recently_seen_set = set(recently_seen_question_ids)
    candidates = [
        q for q in available_questions
        if q.concept_id == chosen_concept
        and q.status == "approved"
        and q.id not in recently_seen_set
    ]

    if not candidates:
        # Fallback: any approved, unseen question for frontier concepts
        candidates = [
            q for q in available_questions
            if q.concept_id in frontier
            and q.status == "approved"
            and q.id not in recently_seen_set
        ]

    if not candidates:
        return None

    # Pick question with difficulty closest to current mastery, within delta
    within_delta = [
        q for q in candidates
        if abs(q.difficulty - current_mastery) <= max_difficulty_delta
    ]
    pool = within_delta if within_delta else candidates

    pool.sort(key=lambda q: abs(q.difficulty - current_mastery))
    return pool[0]
