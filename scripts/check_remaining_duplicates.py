#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
count = 0
files = []

for p in ROOT.rglob("README.md"):
    content = p.read_text(encoding="utf-8")
    if re.search(r"is\s+\w+\s+is\s+a\s+fundamental", content, re.IGNORECASE):
        count += 1
        match = re.search(r"is\s+\w+\s+is\s+a\s+fundamental", content, re.IGNORECASE)
        files.append((p, match.group() if match else ""))

print(f"Remaining duplicates: {count}")
for p, match in files[:10]:
    print(f"{p.relative_to(ROOT)}: {match}")
