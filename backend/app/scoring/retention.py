"""Retention scheduler — SM-2-like spaced repetition."""
from __future__ import annotations

import datetime
from dataclasses import dataclass
from uuid import UUID


MIN_EASE: float = 1.3
INITIAL_INTERVAL_DAYS: float = 1.0
INITIAL_EASE: float = 2.5


@dataclass
class ReviewSchedule:
    user_id: UUID
    concept_id: UUID
    interval_days: float
    ease: float
    next_review_at: datetime.datetime
    review_count: int = 0


def compute_next_interval(
    previous_interval_days: float,
    ease: float,
    result: str,
) -> tuple[float, float]:
    """
    SM-2-like scheduling.
    result: "pass" or "fail"
    Returns (new_interval_days, new_ease)
    """
    if result == "pass":
        new_interval = previous_interval_days * ease
        new_ease = ease + 0.15
    else:
        new_interval = INITIAL_INTERVAL_DAYS
        new_ease = ease - 0.15

    new_ease = max(MIN_EASE, new_ease)
    return (new_interval, new_ease)


def schedule_review(
    user_id: UUID,
    concept_id: UUID,
    result: str,
    current_schedule: ReviewSchedule | None,
) -> ReviewSchedule:
    """Create or update a review schedule based on result."""
    if current_schedule is None:
        prev_interval = INITIAL_INTERVAL_DAYS
        prev_ease = INITIAL_EASE
        review_count = 0
    else:
        prev_interval = current_schedule.interval_days
        prev_ease = current_schedule.ease
        review_count = current_schedule.review_count

    new_interval, new_ease = compute_next_interval(prev_interval, prev_ease, result)
    next_review_at = datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=new_interval)

    return ReviewSchedule(
        user_id=user_id,
        concept_id=concept_id,
        interval_days=new_interval,
        ease=new_ease,
        next_review_at=next_review_at,
        review_count=review_count + 1,
    )
