"""SQLAlchemy 2.0 ORM models for PROJECT-EVOLVE Phase 1 MVP.

Implements all 21 core tables specified in Section 5 of the design prompt:
- users, profiles, goals
- concepts, concept_edges, questions, question_misconceptions, misconceptions
- attempts, responses, evidence, mastery_states, twin_snapshots
- roadmaps, roadmap_items, missions, review_schedule
- disputes, agent_executions, audit_logs, jobs
"""
from __future__ import annotations

import datetime
import uuid
from typing import Any, Optional

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

# Compatibility JSON type for PostgreSQL (JSONB) or SQLite (JSON/Text) in tests
try:
    from sqlalchemy.dialects.postgresql import JSONB as JSONType
except ImportError:
    from sqlalchemy import JSON as JSONType  # type: ignore[assignment]


# ---------------------------------------------------------------------------
# 1. Users & Accounts
# ---------------------------------------------------------------------------
class User(Base):
    """User account entity. Supports role-based access and soft delete."""
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(32), default="learner", nullable=False)  # "learner" | "admin"
    dob: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    consent_version: Mapped[str] = mapped_column(String(64), nullable=False)
    consent_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.datetime.now(datetime.timezone.utc), nullable=False
    )
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        CheckConstraint("role IN ('learner', 'admin')", name="check_user_role"),
        Index("ix_users_deleted_at", "deleted_at"),
    )

    profile: Mapped["Profile"] = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")


# ---------------------------------------------------------------------------
# 2. Profiles
# ---------------------------------------------------------------------------
class Profile(Base):
    """Learner profile and preferences."""
    __tablename__ = "profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    display_name: Mapped[str] = mapped_column(String(128), nullable=False)
    education_level: Mapped[str] = mapped_column(String(64), default="undergraduate", nullable=False)
    weekly_hours: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    preferences: Mapped[dict[str, Any]] = mapped_column(JSONType, default=dict, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="profile")


# ---------------------------------------------------------------------------
# 3. Goals
# ---------------------------------------------------------------------------
class Goal(Base):
    """Target learning goals."""
    __tablename__ = "goals"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    goal_key: Mapped[str] = mapped_column(String(64), nullable=False)  # e.g. "python_placements"
    target_concept_ids: Mapped[list[Any]] = mapped_column(JSONType, default=list, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


# ---------------------------------------------------------------------------
# 4. Concepts (Knowledge Genome)
# ---------------------------------------------------------------------------
class Concept(Base):
    """Knowledge Genome concept node."""
    __tablename__ = "concepts"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    slug: Mapped[str] = mapped_column(String(128), unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)  # 1-5
    domain: Mapped[str] = mapped_column(String(64), default="python_fundamentals", nullable=False)
    content_md: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.datetime.now(datetime.timezone.utc), nullable=False
    )

    __table_args__ = (
        CheckConstraint("difficulty >= 1 AND difficulty <= 5", name="check_concept_difficulty_range"),
    )


# ---------------------------------------------------------------------------
# 5. Concept Edges (Prerequisites)
# ---------------------------------------------------------------------------
class ConceptEdge(Base):
    """Prerequisite edge in the Knowledge Genome DAG."""
    __tablename__ = "concept_edges"

    from_concept_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("concepts.id", ondelete="CASCADE"), primary_key=True)
    to_concept_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("concepts.id", ondelete="CASCADE"), primary_key=True)
    type: Mapped[str] = mapped_column(String(32), default="prerequisite", nullable=False)
    strength: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)

    __table_args__ = (
        CheckConstraint("from_concept_id != to_concept_id", name="check_no_self_edge"),
        CheckConstraint("strength >= 0.0 AND strength <= 1.0", name="check_edge_strength_range"),
    )


# ---------------------------------------------------------------------------
# 6. Misconceptions
# ---------------------------------------------------------------------------
class Misconception(Base):
    """Catalog of known conceptual misunderstandings."""
    __tablename__ = "misconceptions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)  # e.g. "misc-001"
    concept_slug: Mapped[str] = mapped_column(ForeignKey("concepts.slug", ondelete="CASCADE"), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)


# ---------------------------------------------------------------------------
# 7. Questions
# ---------------------------------------------------------------------------
class Question(Base):
    """Assessment items."""
    __tablename__ = "questions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)  # e.g. "q-001"
    concept_slug: Mapped[str] = mapped_column(ForeignKey("concepts.slug", ondelete="CASCADE"), index=True, nullable=False)
    type: Mapped[str] = mapped_column(String(32), nullable=False)  # multiple_choice | multi_select | code_reading | predict_bug
    stem: Mapped[str] = mapped_column(Text, nullable=False)
    options: Mapped[dict[str, Any]] = mapped_column(JSONType, nullable=False)
    correct: Mapped[Any] = mapped_column(JSONType, nullable=False)
    difficulty: Mapped[float] = mapped_column(Float, nullable=False)  # 0.0 - 1.0
    discrimination: Mapped[float] = mapped_column(Float, nullable=False)  # 0.0 - 1.0
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="approved", nullable=False)  # draft | approved | retired

    __table_args__ = (
        CheckConstraint("status IN ('draft', 'approved', 'retired')", name="check_question_status"),
        CheckConstraint("difficulty >= 0.0 AND difficulty <= 1.0", name="check_question_difficulty_range"),
    )


# ---------------------------------------------------------------------------
# 8. Question Misconceptions
# ---------------------------------------------------------------------------
class QuestionMisconception(Base):
    """Maps incorrect options directly to diagnosed misconceptions."""
    __tablename__ = "question_misconceptions"

    question_id: Mapped[str] = mapped_column(ForeignKey("questions.id", ondelete="CASCADE"), primary_key=True)
    option_key: Mapped[str] = mapped_column(String(8), primary_key=True)
    misconception_id: Mapped[str] = mapped_column(ForeignKey("misconceptions.id", ondelete="CASCADE"), nullable=False)


# ---------------------------------------------------------------------------
# 9. Attempts
# ---------------------------------------------------------------------------
class Attempt(Base):
    """An assessment session."""
    __tablename__ = "attempts"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    kind: Mapped[str] = mapped_column(String(32), nullable=False)  # diagnostic | quiz | mission_check
    started_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.datetime.now(datetime.timezone.utc), nullable=False
    )
    completed_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        CheckConstraint("kind IN ('diagnostic', 'quiz', 'mission_check')", name="check_attempt_kind"),
    )


# ---------------------------------------------------------------------------
# 10. Responses
# ---------------------------------------------------------------------------
class Response(Base):
    """Individual question answer in an assessment."""
    __tablename__ = "responses"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    attempt_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("attempts.id", ondelete="CASCADE"), index=True, nullable=False)
    question_id: Mapped[str] = mapped_column(ForeignKey("questions.id", ondelete="CASCADE"), index=True, nullable=False)
    answer: Mapped[Any] = mapped_column(JSONType, nullable=False)
    correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    time_ms: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    selected_misconception_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("misconceptions.id", ondelete="SET NULL"), nullable=True
    )


# ---------------------------------------------------------------------------
# 11. Evidence
# ---------------------------------------------------------------------------
class Evidence(Base):
    """Granular evidence item supporting mastery estimates."""
    __tablename__ = "evidence"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    concept_slug: Mapped[str] = mapped_column(ForeignKey("concepts.slug", ondelete="CASCADE"), nullable=False)
    source_type: Mapped[str] = mapped_column(String(32), nullable=False)  # self_reported | ai_estimated | assessment_verified
    value: Mapped[float] = mapped_column(Float, nullable=False)  # 0.0 - 1.0
    weight: Mapped[float] = mapped_column(Float, nullable=False)
    observed_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.datetime.now(datetime.timezone.utc), nullable=False
    )
    ref_type: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    ref_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    disputed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    __table_args__ = (
        CheckConstraint("source_type IN ('self_reported', 'ai_estimated', 'assessment_verified')", name="check_evidence_source_type"),
        CheckConstraint("value >= 0.0 AND value <= 1.0", name="check_evidence_value_range"),
        Index("ix_evidence_user_concept", "user_id", "concept_slug"),
    )


# ---------------------------------------------------------------------------
# 12. Mastery States
# ---------------------------------------------------------------------------
class MasteryState(Base):
    """Cognitive Twin concept mastery estimate per user."""
    __tablename__ = "mastery_states"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    concept_slug: Mapped[str] = mapped_column(ForeignKey("concepts.slug", ondelete="CASCADE"), primary_key=True)
    mastery: Mapped[float] = mapped_column(Float, default=0.5, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    alpha: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    beta: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.datetime.now(datetime.timezone.utc), nullable=False
    )

    __table_args__ = (
        CheckConstraint("mastery >= 0.0 AND mastery <= 1.0", name="check_mastery_range"),
        CheckConstraint("confidence >= 0.0 AND confidence <= 1.0", name="check_confidence_range"),
        Index("ix_mastery_states_user_concept", "user_id", "concept_slug"),
    )


# ---------------------------------------------------------------------------
# 13. Twin Snapshots
# ---------------------------------------------------------------------------
class TwinSnapshot(Base):
    """Historical snapshot of Cognitive Twin state."""
    __tablename__ = "twin_snapshots"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    taken_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.datetime.now(datetime.timezone.utc), nullable=False
    )
    state: Mapped[dict[str, Any]] = mapped_column(JSONType, nullable=False)
    trigger: Mapped[str] = mapped_column(String(64), nullable=False)  # diagnostic_completed, mission_completed, daily


# ---------------------------------------------------------------------------
# 14. Roadmaps & Roadmap Items
# ---------------------------------------------------------------------------
class Roadmap(Base):
    """Personalized learning path generated from gaps."""
    __tablename__ = "roadmaps"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, index=True, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.datetime.now(datetime.timezone.utc), nullable=False
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.datetime.now(datetime.timezone.utc), nullable=False
    )

    items: Mapped[list["RoadmapItem"]] = relationship("RoadmapItem", back_populates="roadmap", cascade="all, delete-orphan", order_by="RoadmapItem.position")


class RoadmapItem(Base):
    """Ordered step in the learning path."""
    __tablename__ = "roadmap_items"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    roadmap_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("roadmaps.id", ondelete="CASCADE"), index=True, nullable=False)
    concept_slug: Mapped[str] = mapped_column(ForeignKey("concepts.slug", ondelete="CASCADE"), nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    reason: Mapped[dict[str, Any]] = mapped_column(JSONType, nullable=False)  # gap, evidence, because explanation
    status: Mapped[str] = mapped_column(String(32), default="pending", nullable=False)  # pending | in_progress | done

    roadmap: Mapped["Roadmap"] = relationship("Roadmap", back_populates="items")


# ---------------------------------------------------------------------------
# 15. Missions
# ---------------------------------------------------------------------------
class Mission(Base):
    """Daily mission matching user's time budget."""
    __tablename__ = "missions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    items: Mapped[list[Any]] = mapped_column(JSONType, nullable=False)  # explanation + practice items + check
    status: Mapped[str] = mapped_column(String(32), default="pending", nullable=False)  # pending | in_progress | completed
    completed_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        CheckConstraint("status IN ('pending', 'in_progress', 'completed')", name="check_mission_status"),
        Index("ix_missions_user_date", "user_id", "date"),
    )


# ---------------------------------------------------------------------------
# 16. Review Schedule (Retention)
# ---------------------------------------------------------------------------
class ReviewSchedule(Base):
    """SM-2 like spaced revision schedule."""
    __tablename__ = "review_schedule"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    concept_slug: Mapped[str] = mapped_column(ForeignKey("concepts.slug", ondelete="CASCADE"), primary_key=True)
    due_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    interval_days: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    ease: Mapped[float] = mapped_column(Float, default=2.3, nullable=False)
    last_result: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)  # pass | fail

    __table_args__ = (
        CheckConstraint("ease >= 1.3", name="check_ease_floor"),
        Index("ix_review_schedule_due", "user_id", "due_at"),
    )


# ---------------------------------------------------------------------------
# 17. Disputes
# ---------------------------------------------------------------------------
class Dispute(Base):
    """Human correction / score dispute record."""
    __tablename__ = "disputes"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    target_type: Mapped[str] = mapped_column(String(32), nullable=False)  # question | score
    target_id: Mapped[str] = mapped_column(String(64), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="open", nullable=False)  # open | resolved | dismissed
    resolved_by: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    resolved_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        CheckConstraint("status IN ('open', 'resolved', 'dismissed')", name="check_dispute_status"),
    )


# ---------------------------------------------------------------------------
# 18. Agent Executions
# ---------------------------------------------------------------------------
class AgentExecution(Base):
    """Audit and cost trail for every AI agent invocation."""
    __tablename__ = "agent_executions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    agent: Mapped[str] = mapped_column(String(64), nullable=False)
    workflow_id: Mapped[str] = mapped_column(String(64), nullable=False)
    input_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    output: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONType, nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="pending", nullable=False)  # pending | running | success | failed
    error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    latency_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    tokens_in: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    tokens_out: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    cost_usd: Mapped[Optional[float]] = mapped_column(Float, default=0.0, nullable=True)
    started_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.datetime.now(datetime.timezone.utc), nullable=False
    )
    completed_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


# ---------------------------------------------------------------------------
# 19. Audit Logs
# ---------------------------------------------------------------------------
class AuditLog(Base):
    """Security and compliance audit log."""
    __tablename__ = "audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    actor_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    action: Mapped[str] = mapped_column(String(64), nullable=False)  # register, login, export_data, delete_account, dispute_resolved
    target: Mapped[str] = mapped_column(String(128), nullable=False)
    metadata_: Mapped[dict[str, Any]] = mapped_column("metadata", JSONType, default=dict, nullable=False)
    ip_hash: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.datetime.now(datetime.timezone.utc), nullable=False
    )


# ---------------------------------------------------------------------------
# 20. Jobs
# ---------------------------------------------------------------------------
class Job(Base):
    """Database-backed async queue for background tasks."""
    __tablename__ = "jobs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    type: Mapped[str] = mapped_column(String(64), nullable=False)  # hard_delete_user | recalculate_mastery | snapshot_twin | generate_roadmap
    payload: Mapped[dict[str, Any]] = mapped_column(JSONType, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="pending", nullable=False)  # pending | running | done | failed
    attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    run_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.datetime.now(datetime.timezone.utc), nullable=False
    )
    last_error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.datetime.now(datetime.timezone.utc), nullable=False
    )

    __table_args__ = (
        Index("ix_jobs_status_run_at", "status", "run_at"),
    )
