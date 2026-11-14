"""Schemas for Goals domain."""
from __future__ import annotations

from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel

GoalKeyType = Literal["python_placements", "python_data", "python_basics"]

GOAL_TARGETS: dict[str, list[str]] = {
    "python_basics": [
        "variables-basics", "data-types-overview", "integers", "floats", "strings-basics",
        "booleans", "none-type", "print-function", "input-function", "arithmetic-operators",
        "comparison-operators", "logical-operators", "if-statements", "elif-else", "while-loops",
        "for-loops", "range-function", "lists-basics", "functions-basics", "return-values",
    ],
    "python_data": [
        "variables-basics", "data-types-overview", "integers", "floats", "strings-basics",
        "booleans", "string-methods", "lists-basics", "list-methods", "list-slicing",
        "list-comprehensions", "dicts-basics", "dict-methods", "dict-comprehensions",
        "nested-data", "tuples", "sets", "functions-basics", "lambda-functions",
        "higher-order-functions", "file-reading", "file-writing", "file-context-managers",
        "exceptions-basics", "try-except", "standard-library",
    ],
    "python_placements": [
        "variables-basics", "data-types-overview", "integers", "strings-basics", "booleans",
        "if-statements", "for-loops", "while-loops", "lists-basics", "list-slicing",
        "dicts-basics", "functions-basics", "recursion", "oop-concepts", "classes-basics",
        "constructors", "instance-methods", "inheritance", "method-overriding",
        "complexity-basics", "linear-search", "binary-search", "bubble-sort",
        "selection-sort", "insertion-sort", "two-pointer", "sliding-window",
    ],
}


class GoalCreate(BaseModel):
    goal_key: GoalKeyType


class GoalRead(BaseModel):
    id: UUID
    user_id: UUID
    goal_key: str
    target_concept_ids: list[str]
    active: bool

    model_config = {"from_attributes": True}
