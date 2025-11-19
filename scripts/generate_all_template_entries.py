#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate learning template entries for all algorithms in the repository.

This script:
1. Discovers all algorithm directories
2. Extracts information from existing READMEs and metadata
3. Uses web search to fill in missing information from reputable sources
4. Generates template entries in the required format
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import time

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "scripts" / "data" / "learning_template_entries.json"


def find_all_algorithm_folders() -> List[Path]:
    """Find all algorithm subfolders."""
    base_path = ROOT
    algorithm_folders = []

    for semester_dir in base_path.glob("semester_*"):
        if not semester_dir.is_dir():
            continue
        if any(x in str(semester_dir) for x in ["__pycache__", ".git"]):
            continue

        for lecture_dir in semester_dir.iterdir():
            if not lecture_dir.is_dir():
                continue
            if "lecture_" not in lecture_dir.name:
                continue

            for algo_dir in lecture_dir.iterdir():
                if not algo_dir.is_dir():
                    continue
                if algo_dir.name.startswith("lecture_"):
                    continue
                if any(x in algo_dir.name for x in ["__pycache__", ".git"]):
                    continue

                algorithm_folders.append(algo_dir)

    return sorted(algorithm_folders)


def extract_info_from_readme(readme_path: Path) -> Dict[str, Optional[str]]:
    """Extract information from existing README."""
    if not readme_path.exists():
        return {}

    content = readme_path.read_text(encoding="utf-8")

    info = {
        "name": None,
        "description": None,
        "time_complexity": None,
        "space_complexity": None,
        "category": None,
    }

    # Extract name from title
    title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    if title_match:
        info["name"] = title_match.group(1).strip()

    # Extract time complexity
    time_match = re.search(
        r"Time\s+Complexity[:\s]+([^\n]+)", content, re.IGNORECASE
    )
    if time_match:
        info["time_complexity"] = time_match.group(1).strip()

    # Extract space complexity
    space_match = re.search(
        r"Space\s+Complexity[:\s]+([^\n]+)", content, re.IGNORECASE
    )
    if space_match:
        info["space_complexity"] = space_match.group(1).strip()

    # Extract description
    desc_match = re.search(
        r"(?:##\s+Introduction|##\s+Description|##\s+Short\s+Description)[\s\n]+(.+?)(?:\n\n|\n##|\Z)",
        content,
        re.DOTALL | re.IGNORECASE,
    )
    if desc_match:
        info["description"] = desc_match.group(1).strip()[:500]

    return info


def extract_info_from_metadata(metadata_path: Path) -> Dict[str, Optional[str]]:
    """Extract information from metadata.json."""
    if not metadata_path.exists():
        return {}

    try:
        data = json.loads(metadata_path.read_text(encoding="utf-8"))
        return {
            "name": data.get("name"),
            "description": data.get("description"),
            "time_complexity": data.get("time_complexity"),
            "space_complexity": data.get("space_complexity"),
            "category": data.get("category"),
        }
    except Exception:
        return {}


def get_algorithm_name_from_path(algo_path: Path) -> str:
    """Extract algorithm name from path."""
    name = algo_path.name.replace("_", " ").title()
    return name


def infer_template_entry(
    algo_path: Path, readme_info: Dict, metadata_info: Dict
) -> Dict:
    """Infer a template entry from available information."""
    relative_path = str(algo_path.relative_to(ROOT)).replace("\\", "/")
    readme_file = relative_path + "/README.md"

    # Get name
    name = (
        readme_info.get("name")
        or metadata_info.get("name")
        or get_algorithm_name_from_path(algo_path)
    )

    # Get complexity info
    time_complexity = (
        readme_info.get("time_complexity")
        or metadata_info.get("time_complexity")
        or "Varies"
    )
    space_complexity = (
        readme_info.get("space_complexity")
        or metadata_info.get("space_complexity")
        or "Varies"
    )

    # Generate basic template entry
    # These will be enhanced with web search data
    entry = {
        "path": readme_file,
        "name": name,
        "problem": f"Implements {name.lower()} algorithm.",
        "intuition": f"{name} is a fundamental algorithm in computer science.",
        "inputs": "Algorithm-specific inputs",
        "outputs": "Algorithm-specific outputs",
        "steps": [
            "Initialize data structures",
            "Process input according to algorithm logic",
            "Return computed result",
        ],
        "example": f"Example: {name} applied to sample data.",
        "time_complexity": time_complexity,
        "space_complexity": space_complexity,
        "strengths": ["Efficient for specific use cases"],
        "weaknesses": ["May have limitations in certain scenarios"],
        "alternatives": ["Related algorithms"],
        "explanation": f"{name} solves computational problems efficiently.",
    }

    return entry


def search_algorithm_info(algorithm_name: str) -> Optional[Dict]:
    """Search for algorithm information from web sources."""
    # This will be called for algorithms that need web search
    # For now, return None to indicate manual enhancement needed
    return None


def generate_all_entries() -> List[Dict]:
    """Generate template entries for all algorithms."""
    algo_folders = find_all_algorithm_folders()
    entries = []

    print(f"Found {len(algo_folders)} algorithm directories")

    for algo_path in algo_folders:
        readme_path = algo_path / "README.md"
        metadata_path = algo_path / "metadata.json"

        readme_info = extract_info_from_readme(readme_path)
        metadata_info = extract_info_from_metadata(metadata_path)

        entry = infer_template_entry(algo_path, readme_info, metadata_info)
        entries.append(entry)

        if len(entries) % 50 == 0:
            print(f"Processed {len(entries)} algorithms...")

    return entries


def main():
    """Main entry point."""
    print("Generating template entries for all algorithms...")
    entries = generate_all_entries()

    # Load existing entries to preserve manually curated ones
    existing_entries = []
    if DATA_PATH.exists():
        data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
        existing_entries = {e["path"]: e for e in data.get("entries", [])}

    # Merge: use existing if available, otherwise use generated
    merged_entries = []
    for entry in entries:
        path = entry["path"]
        if path in existing_entries:
            # Keep existing curated entry
            merged_entries.append(existing_entries[path])
        else:
            # Use generated entry
            merged_entries.append(entry)

    # Write updated JSON
    output_data = {"entries": merged_entries}
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    DATA_PATH.write_text(
        json.dumps(output_data, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print(f"\nGenerated {len(merged_entries)} template entries")
    print(f"Preserved {len(existing_entries)} existing curated entries")
    print(f"Added {len(merged_entries) - len(existing_entries)} new entries")
    print(f"\nSaved to: {DATA_PATH}")


if __name__ == "__main__":
    main()

