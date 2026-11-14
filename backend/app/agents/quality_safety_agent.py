"""Quality and Safety Agent — validates all AI outputs before returning to user or database."""
from __future__ import annotations

import re
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel


class ValidationReport(BaseModel):
    is_valid: bool
    reasons: list[str] = []


class QualitySafetyAgent:
    """Rigorous gatekeeper enforcing responsible AI rules from Section 9 & AGENTS.md."""

    FORBIDDEN_OUTCOME_PHRASES = [
        "guarantee", "guaranteed job", "guaranteed salary", "100% placement",
        "will get hired", "certified master", "pass your interview guaranteed",
    ]

    def validate_teaching_output(
        self,
        explanation: str,
        concept_slug: str,
        valid_concept_slugs: set[str],
        known_twin_data: Optional[dict[str, Any]] = None,
    ) -> ValidationReport:
        reasons: list[str] = []

        # 1. Check for AI labeling
        if "AI-Generated" not in explanation and "🤖" not in explanation:
            reasons.append("Missing mandatory AI-label prefix.")

        # 2. Check for outcome guarantees (non-negotiable rule)
        lower_text = explanation.lower()
        for phrase in self.FORBIDDEN_OUTCOME_PHRASES:
            if phrase in lower_text:
                reasons.append(f"Contains forbidden outcome guarantee: '{phrase}'.")

        # 3. Check that it cites valid concepts
        if concept_slug not in valid_concept_slugs:
            reasons.append(f"Invalid concept slug reference: '{concept_slug}'.")

        # 4. Check for unverified credential/mastery fabrications
        if "you are verified as an expert" in lower_text and not (
            known_twin_data and known_twin_data.get("is_verified_expert")
        ):
            reasons.append("Claims learner credentials not substantiated by Cognitive Twin evidence.")

        return ValidationReport(is_valid=len(reasons) == 0, reasons=reasons)

    def validate_question_draft(
        self,
        question_data: dict[str, Any],
        valid_concept_slugs: set[str],
    ) -> ValidationReport:
        reasons: list[str] = []

        # Check required fields
        for field in ["stem", "options", "correct", "explanation", "difficulty"]:
            if field not in question_data:
                reasons.append(f"Missing required question field: '{field}'.")

        # Check options
        options = question_data.get("options", {})
        correct = question_data.get("correct")
        if not isinstance(options, dict) or len(options) < 2:
            reasons.append("Options must be a dict with at least 2 choices.")
        elif correct not in options:
            reasons.append(f"Correct answer '{correct}' is not among options {list(options.keys())}.")

        # Check concept reference if present
        concept_slug = question_data.get("concept_slug")
        if concept_slug and concept_slug not in valid_concept_slugs:
            reasons.append(f"Draft question references unknown concept '{concept_slug}'.")

        return ValidationReport(is_valid=len(reasons) == 0, reasons=reasons)
