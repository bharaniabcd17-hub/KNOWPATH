"""Schemas for Knowledge Genome domain."""
from __future__ import annotations

from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel


class ConceptSummary(BaseModel):
    id: UUID
    slug: str
    title: str
    description: str
    difficulty: int
    domain: str
    mastery: Optional[float] = None
    confidence: Optional[float] = None

    model_config = {"from_attributes": True}


class ConceptDetail(ConceptSummary):
    content_md: str
    prerequisites: list[str]  # slugs of prerequisites
    dependents: list[str]     # slugs of dependent concepts
    misconceptions: list[dict[str, str]]


class GraphNode(BaseModel):
    id: str  # slug
    title: str
    difficulty: int
    mastery: Optional[float] = None
    confidence: Optional[float] = None


class GraphEdge(BaseModel):
    from_slug: str
    to_slug: str
    type: str = "prerequisite"
    strength: float = 1.0


class GenomeGraph(BaseModel):
    nodes: list[GraphNode]
    edges: list[GraphEdge]
