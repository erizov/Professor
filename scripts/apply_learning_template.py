#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Apply the Universal Algorithm Learning Template to selected algorithm READMEs.

Each description is adapted from respected references (e.g., Wikipedia,
standard CS textbooks) and rewritten to satisfy the Rapid 5-Minute form.
"""

import argparse
import json
from pathlib import Path
from textwrap import dedent
from typing import Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "scripts" / "data" / "learning_template_entries.json"


def render_template(info: dict) -> str:
    steps = "\n".join(f"{idx + 1}. {step}" for idx, step in enumerate(info["steps"]))
    strengths = "\n".join(f"- {item}" for item in info["strengths"])
    weaknesses = "\n".join(f"- {item}" for item in info["weaknesses"])
    alternatives = ", ".join(info["alternatives"])

    template = f"""# {info['name']}

1. **Name of Algorithm**  
   {info['name']}

2. **What problem does it solve? (1 sentence)**  
   {info['problem']}

3. **Intuition (plain-language explanation)**  
   {info['intuition']}

4. **Inputs & Outputs**  
   - Input: {info['inputs']}  
   - Output: {info['outputs']}

5. **Step-by-step description (5–10 lines max)**  
{steps}

6. **Tiny example (hand-simulated)**  
   {info['example']}

7. **Time & Space Complexity**  
   - Time: {info['time_complexity']}  
   - Space: {info['space_complexity']}

8. **Strengths**  
{strengths}

9. **Weaknesses / limitations**  
{weaknesses}

10. **Compare with alternatives**  
    Alternatives: {alternatives}

11. **30-second explanation (your own words)**  
    {info['explanation']}

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
"""

    return dedent(template).strip() + "\n"


def load_entries() -> List[Dict]:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Template data file not found: {DATA_PATH}")
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    return data.get("entries", [])


def filter_entries(entries: List[Dict], targets: Optional[List[str]]) -> List[Dict]:
    if not targets:
        return entries
    normalized = {t.lower() for t in targets}
    results = []
    for entry in entries:
        path = entry.get("path", "")
        if path.lower() in normalized:
            results.append(entry)
    return results


def update_readmes(entries: List[Dict]) -> int:
    updated = 0
    for entry in entries:
        path = entry["path"]
        target = ROOT / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render_template(entry), encoding="utf-8")
        updated += 1
        print(f"[UPDATED] {path}")
    return updated


def main():
    parser = argparse.ArgumentParser(
        description="Apply the Universal Algorithm Learning Template to selected README files."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Paths (relative to repo root) to README files defined in the metadata source. Default: all entries.",
    )
    args = parser.parse_args()

    entries = load_entries()
    selected = filter_entries(entries, args.paths)
    if not selected:
        print("[INFO] No matching entries found. Nothing to update.")
        return

    updated_files = update_readmes(selected)
    print(f"\nUpdated {updated_files} README files with the universal template.")


if __name__ == "__main__":
    main()

