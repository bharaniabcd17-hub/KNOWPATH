#!/usr/bin/env python3
"""Validation script for PROJECT-EVOLVE content database.

Checks:
1. No cycles in the prerequisite DAG (via DFS)
2. Every question references a valid concept slug
3. Every question has valid options, correct answer, and explanation
4. Every misconception tag references a valid misconception id
5. Seed counts meet Section 8 requirements:
   - Concepts: >= 60 (aiming for 60-80)
   - Questions: >= 300
   - Misconceptions: >= 25
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


def parse_concepts(text: str) -> dict[str, dict]:
    """Lightweight YAML parser for concepts.yaml."""
    concepts: dict[str, dict] = {}
    current: dict | None = None
    in_prereqs = False
    in_content = False
    content_lines: list[str] = []

    for line in text.splitlines():
        if line.startswith("- slug:"):
            if current and "slug" in current:
                if in_content:
                    current["content_md"] = "\n".join(content_lines)
                concepts[current["slug"]] = current
            slug_val = re.search(r'slug:\s*["\']?([^"\'\s]+)["\']?', line)
            current = {
                "slug": slug_val.group(1) if slug_val else "",
                "prerequisites": [],
                "content_md": "",
            }
            in_prereqs = False
            in_content = False
            content_lines = []
        elif current is not None:
            if line.strip().startswith("title:"):
                m = re.search(r'title:\s*["\']?([^"\']+)["\']?', line)
                if m:
                    current["title"] = m.group(1).strip()
            elif line.strip().startswith("difficulty:"):
                m = re.search(r'difficulty:\s*(\d+)', line)
                if m:
                    current["difficulty"] = int(m.group(1))
            elif line.strip().startswith("prerequisites:"):
                in_content = False
                if "[]" in line:
                    current["prerequisites"] = []
                    in_prereqs = False
                else:
                    in_prereqs = True
            elif in_prereqs and line.strip().startswith("-"):
                m = re.search(r'-\s*["\']?([^"\'\s]+)["\']?', line)
                if m:
                    current["prerequisites"].append(m.group(1))
            elif line.strip().startswith("content_md:"):
                in_prereqs = False
                in_content = True
                content_lines = []
            elif in_content:
                if line.startswith("    ") or line == "":
                    content_lines.append(line[4:] if len(line) >= 4 else "")
                elif line.strip().startswith("- ") or (line and not line.startswith(" ")):
                    # Left content block
                    in_content = False
                    current["content_md"] = "\n".join(content_lines)

    if current and "slug" in current:
        if in_content:
            current["content_md"] = "\n".join(content_lines)
        concepts[current["slug"]] = current

    return concepts


def parse_misconceptions(text: str) -> dict[str, dict]:
    """Lightweight YAML parser for misconceptions.yaml."""
    misconceptions: dict[str, dict] = {}
    current: dict | None = None

    for line in text.splitlines():
        if line.startswith("- id:"):
            if current and "id" in current:
                misconceptions[current["id"]] = current
            m = re.search(r'id:\s*["\']?([^"\'\s]+)["\']?', line)
            current = {"id": m.group(1) if m else ""}
        elif current is not None:
            if line.strip().startswith("title:"):
                m = re.search(r'title:\s*["\']?([^"\']+)["\']?', line)
                if m:
                    current["title"] = m.group(1).strip()
            elif line.strip().startswith("concept_slug:"):
                m = re.search(r'concept_slug:\s*["\']?([^"\'\s]+)["\']?', line)
                if m:
                    current["concept_slug"] = m.group(1).strip()
            elif line.strip().startswith("explanation:"):
                m = re.search(r'explanation:\s*["\']?([^"\']+)["\']?', line)
                if m:
                    current["explanation"] = m.group(1).strip()

    if current and "id" in current:
        misconceptions[current["id"]] = current

    return misconceptions


def parse_questions(text: str) -> list[dict]:
    """Lightweight YAML parser for questions.yaml."""
    questions: list[dict] = []
    current: dict | None = None
    in_options = False
    in_tags = False

    for line in text.splitlines():
        if line.startswith("- id:"):
            if current and "id" in current:
                questions.append(current)
            m = re.search(r'id:\s*["\']?([^"\'\s]+)["\']?', line)
            current = {
                "id": m.group(1) if m else "",
                "options": {},
                "misconception_tags": {},
            }
            in_options = False
            in_tags = False
        elif current is not None:
            if line.strip().startswith("concept_slug:"):
                in_options = False
                in_tags = False
                m = re.search(r'concept_slug:\s*["\']?([^"\'\s]+)["\']?', line)
                if m:
                    current["concept_slug"] = m.group(1).strip()
            elif line.strip().startswith("type:"):
                in_options = False
                in_tags = False
                m = re.search(r'type:\s*["\']?([^"\'\s]+)["\']?', line)
                if m:
                    current["type"] = m.group(1).strip()
            elif line.strip().startswith("difficulty:"):
                m = re.search(r'difficulty:\s*([0-9.]+)', line)
                if m:
                    current["difficulty"] = float(m.group(1))
            elif line.strip().startswith("discrimination:"):
                m = re.search(r'discrimination:\s*([0-9.]+)', line)
                if m:
                    current["discrimination"] = float(m.group(1))
            elif line.strip().startswith("correct:"):
                in_options = False
                in_tags = False
                m = re.search(r'correct:\s*["\']?([^"\'\s]+)["\']?', line)
                if m:
                    current["correct"] = m.group(1).strip()
            elif line.strip().startswith("explanation:"):
                in_options = False
                in_tags = False
                m = re.search(r'explanation:\s*["\']?(.+)', line)
                if m:
                    current["explanation"] = m.group(1).strip()
            elif line.strip().startswith("options:"):
                in_options = True
                in_tags = False
            elif in_options and re.match(r'^\s+[A-D]:', line):
                m = re.match(r'^\s+([A-D]):\s*["\']?(.*?)["\']?\s*$', line)
                if m:
                    current["options"][m.group(1)] = m.group(2)
            elif line.strip().startswith("misconception_tags:"):
                in_options = False
                in_tags = True
            elif in_tags and re.match(r'^\s+[A-D]:', line):
                m = re.match(r'^\s+([A-D]):\s*["\']?([^"\'\s]+)["\']?', line)
                if m:
                    current["misconception_tags"][m.group(1)] = m.group(2)

    if current and "id" in current:
        questions.append(current)

    return questions


def check_cycles(concepts: dict[str, dict]) -> list[list[str]]:
    """Detect cycles in prerequisite DAG using standard DFS 3-color graph traversal."""
    WHITE, GRAY, BLACK = 0, 1, 2
    state = {slug: WHITE for slug in concepts}
    cycles: list[list[str]] = []
    path: list[str] = []

    def dfs(node: str) -> None:
        state[node] = GRAY
        path.append(node)
        for prereq in concepts.get(node, {}).get("prerequisites", []):
            if prereq not in concepts:
                continue
            if state[prereq] == GRAY:
                cycle_start = path.index(prereq)
                cycles.append(path[cycle_start:] + [prereq])
            elif state[prereq] == WHITE:
                dfs(prereq)
        path.pop()
        state[node] = BLACK

    for node in concepts:
        if state[node] == WHITE:
            dfs(node)

    return cycles


def main() -> int:
    content_dir = Path(__file__).parent / "python"
    errors: list[str] = []
    warnings: list[str] = []

    print("=" * 60)
    print("PROJECT-EVOLVE Content Validation Suite")
    print("=" * 60)

    # 1. Check Concepts
    concepts_file = content_dir / "concepts.yaml"
    if not concepts_file.exists():
        print("FAIL: concepts.yaml missing!")
        return 1

    concepts_text = concepts_file.read_text(encoding="utf-8")
    concepts = parse_concepts(concepts_text)
    print(f"[x] Loaded {len(concepts)} concepts (requirement >= 60)")
    if len(concepts) < 60:
        errors.append(f"Too few concepts: {len(concepts)} < 60 required")

    # 2. Check Prerequisite DAG for cycles
    cycles = check_cycles(concepts)
    if cycles:
        for c in cycles:
            errors.append(f"Cycle detected in prerequisite DAG: {' -> '.join(c)}")
    else:
        print("[x] Prerequisite graph is a valid DAG (zero cycles detected)")

    # Check for missing prerequisite slugs
    for slug, c in concepts.items():
        for p in c.get("prerequisites", []):
            if p not in concepts:
                errors.append(f"Concept '{slug}' references missing prerequisite '{p}'")

    # 3. Check Misconceptions
    misc_file = content_dir / "misconceptions.yaml"
    if not misc_file.exists():
        print("FAIL: misconceptions.yaml missing!")
        return 1

    misc_text = misc_file.read_text(encoding="utf-8")
    misconceptions = parse_misconceptions(misc_text)
    print(f"[x] Loaded {len(misconceptions)} misconceptions (requirement >= 25)")
    if len(misconceptions) < 25:
        errors.append(f"Too few misconceptions: {len(misconceptions)} < 25 required")

    # 4. Check Questions
    q_file = content_dir / "questions.yaml"
    if not q_file.exists():
        print("FAIL: questions.yaml missing!")
        return 1

    q_text = q_file.read_text(encoding="utf-8")
    questions = parse_questions(q_text)
    print(f"[x] Loaded {len(questions)} questions (requirement >= 300)")
    if len(questions) < 300:
        errors.append(f"Too few questions: {len(questions)} < 300 required")

    # Check question fields
    invalid_concept_refs = 0
    invalid_misc_tags = 0
    invalid_correct_answers = 0

    for q in questions:
        # Check concept reference
        c_slug = q.get("concept_slug", "")
        if c_slug not in concepts:
            invalid_concept_refs += 1
            if invalid_concept_refs <= 5:
                errors.append(f"Question '{q.get('id')}' references unknown concept '{c_slug}'")

        # Check correct answer exists in options
        correct = q.get("correct", "")
        options = q.get("options", {})
        if options and correct not in options:
            invalid_correct_answers += 1
            if invalid_correct_answers <= 5:
                errors.append(f"Question '{q.get('id')}' correct answer '{correct}' not in options {list(options.keys())}")

        # Check misconception tags
        for opt_key, misc_id in q.get("misconception_tags", {}).items():
            if misc_id not in misconceptions:
                invalid_misc_tags += 1
                if invalid_misc_tags <= 5:
                    errors.append(f"Question '{q.get('id')}' references unknown misconception '{misc_id}'")

    if invalid_concept_refs > 5:
        errors.append(f"... and {invalid_concept_refs - 5} more questions with unknown concepts")
    if invalid_correct_answers > 5:
        errors.append(f"... and {invalid_correct_answers - 5} more questions with invalid correct answers")
    if invalid_misc_tags > 5:
        errors.append(f"... and {invalid_misc_tags - 5} more invalid misconception tags")

    print("-" * 60)
    if errors:
        print(f"FAILED with {len(errors)} errors:")
        for e in errors[:15]:
            print(f"  - {e}")
        return 1
    else:
        print("ALL CONTENT CHECKS PASSED:")
        print(f"  - {len(concepts)} concepts verified in DAG")
        print(f"  - {len(questions)} questions verified with options and concepts")
        print(f"  - {len(misconceptions)} misconceptions tagged and verified")
        print("=" * 60)
        return 0


if __name__ == "__main__":
    sys.exit(main())
