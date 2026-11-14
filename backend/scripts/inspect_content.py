import os
import re

content_dir = r"e:\hackathon\content\python"

concepts = set()
for fname in ["questions_part1.yaml", "questions_part2.yaml"]:
    path = os.path.join(content_dir, fname)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    c = re.findall(r"concept_slug:\s*[\"']?([^\"'\s\n]+)[\"']?", content)
    concepts.update(c)

print(f"Unique concepts referenced in questions: {len(concepts)}")
for c in sorted(concepts):
    print(f"- {c}")

