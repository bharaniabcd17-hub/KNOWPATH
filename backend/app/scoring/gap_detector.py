"""Gap detector — finds knowledge gaps from prerequisite graph traversal."""
from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


# ---------------------------------------------------------------------------
# Data types (domain-agnostic, no DB imports)
# ---------------------------------------------------------------------------
@dataclass
class ConceptEdge:
    from_id: UUID
    to_id: UUID
    edge_type: str = "prerequisite"


@dataclass
class MasteryState:
    concept_id: UUID
    mastery: float = 0.0
    confidence: float = 0.0


@dataclass
class Concept:
    id: UUID
    slug: str
    title: str
    difficulty: float = 0.5


@dataclass
class GapItem:
    concept_id: UUID
    slug: str
    title: str
    mastery: float
    confidence: float
    reason: str  # "gap" | "unknown"
    blocking_count: int
    priority: float


# ---------------------------------------------------------------------------
# Gap detection
# ---------------------------------------------------------------------------

def detect_gaps(
    target_concept_ids: list[UUID],
    concept_edges: list[ConceptEdge],
    mastery_states: dict[UUID, MasteryState],
    all_concepts: dict[UUID, Concept],
) -> list[GapItem]:
    """
    Traverse prerequisite graph from target concepts.
    A concept is a gap if mastery < 0.6 or confidence < 0.3 (labeled "unknown").
    priority = impact * (1 - mastery) * foundation_bonus
    """
    # Build adjacency: prereq -> list of dependents
    dependents: dict[UUID, set[UUID]] = {}
    prerequisites: dict[UUID, set[UUID]] = {}
    for edge in concept_edges:
        if edge.edge_type == "prerequisite":
            # edge means: from_id is prerequisite of to_id
            dependents.setdefault(edge.from_id, set()).add(edge.to_id)
            prerequisites.setdefault(edge.to_id, set()).add(edge.from_id)

    # BFS/DFS to find all concepts reachable backwards from targets
    reachable: set[UUID] = set()

    def collect_prereqs(cid: UUID) -> None:
        for prereq in prerequisites.get(cid, set()):
            if prereq not in reachable:
                reachable.add(prereq)
                collect_prereqs(prereq)

    for tid in target_concept_ids:
        reachable.add(tid)
        collect_prereqs(tid)

    # For each reachable concept, compute transitive impact (how many targets depend on it)
    def count_target_dependents(cid: UUID, visited: set[UUID] | None = None) -> int:
        if visited is None:
            visited = set()
        if cid in visited:
            return 0
        visited.add(cid)
        count = 1 if cid in target_concept_ids else 0
        for dep in dependents.get(cid, set()):
            count += count_target_dependents(dep, visited)
        return count

    max_impact = max(1, len(target_concept_ids))
    impact_map: dict[UUID, float] = {}
    for cid in reachable:
        impact_map[cid] = count_target_dependents(cid) / max_impact

    # Find gaps
    gaps: list[GapItem] = []
    for cid in reachable:
        if cid not in all_concepts:
            continue
        concept = all_concepts[cid]
        state = mastery_states.get(cid)
        mastery = state.mastery if state else 0.0
        confidence = state.confidence if state else 0.0

        if mastery < 0.6 or confidence < 0.3:
            reason = "unknown" if confidence < 0.3 else "gap"
            gaps.append(GapItem(
                concept_id=cid,
                slug=concept.slug,
                title=concept.title,
                mastery=mastery,
                confidence=confidence,
                reason=reason,
                blocking_count=0,  # filled below
                priority=0.0,  # filled below
            ))

    # Count blocking: how many other gaps does this gap block?
    gap_ids = {g.concept_id for g in gaps}
    for gap in gaps:
        blocking = sum(
            1 for dep in dependents.get(gap.concept_id, set())
            if dep in gap_ids
        )
        gap.blocking_count = blocking
        impact = impact_map.get(gap.concept_id, 0.0)
        foundation_bonus = 1.25 if blocking > 0 else 1.0
        gap.priority = impact * (1.0 - gap.mastery) * foundation_bonus

    gaps.sort(key=lambda g: g.priority, reverse=True)
    return gaps


def has_cycle(concept_edges: list[ConceptEdge]) -> bool:
    """Detect if the prerequisite graph has a cycle (DFS)."""
    adjacency: dict[UUID, list[UUID]] = {}
    for edge in concept_edges:
        adjacency.setdefault(edge.from_id, []).append(edge.to_id)

    visited: set[UUID] = set()
    rec_stack: set[UUID] = set()

    def dfs(node: UUID) -> bool:
        visited.add(node)
        rec_stack.add(node)
        for neighbor in adjacency.get(node, []):
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in rec_stack:
                return True
        rec_stack.discard(node)
        return False

    for node in list(adjacency.keys()):
        if node not in visited:
            if dfs(node):
                return True
    return False
