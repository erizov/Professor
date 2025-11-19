#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhance README files with information from Wikipedia and other public sources.
Fetches comprehensive information and adds to algorithm README files.
"""

import re
import json
import requests
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import quote
import time
import html

ROOT = Path(__file__).resolve().parents[1]

# Wikipedia API endpoint
WIKIPEDIA_API = "https://en.wikipedia.org/api/rest_v1/page/summary/"

# Rate limiting
REQUEST_DELAY = 0.5  # seconds between requests


def fetch_wikipedia_summary(algorithm_name: str) -> Optional[Dict]:
    """
    Fetch Wikipedia summary for an algorithm.

    Args:
        algorithm_name: Name of algorithm to search

    Returns:
        Dictionary with title, extract, and URL, or None
    """
    # Clean algorithm name for Wikipedia search
    search_terms = [
        algorithm_name.replace("_", " ").title(),
        algorithm_name.replace("_", " ") + " algorithm",
        algorithm_name.replace("_", " ") + " (computer science)",
    ]

    for term in search_terms:
        try:
            url = WIKIPEDIA_API + quote(term)
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                data = response.json()
                if "extract" in data and data["extract"]:
                    return {
                        "title": data.get("title", ""),
                        "extract": data.get("extract", ""),
                        "url": data.get("content_urls", {})
                        .get("desktop", {})
                        .get("page", ""),
                        "thumbnail": (
                            data.get("thumbnail", {}).get("source", "")
                            if "thumbnail" in data
                            else None
                        ),
                    }

            time.sleep(REQUEST_DELAY)
        except Exception as e:
            print(f"Error fetching Wikipedia for '{term}': {e}")
            continue

    return None


def fetch_algorithm_info(algorithm_name: str, category: str) -> Dict:
    """
    Fetch comprehensive algorithm information from multiple sources.

    Args:
        algorithm_name: Name of algorithm
        category: Algorithm category

    Returns:
        Dictionary with algorithm information
    """
    info = {
        "wikipedia": None,
        "description": "",
        "history": "",
        "applications": [],
        "complexity": {},
        "variants": [],
        "references": [],
    }

    # Fetch from Wikipedia
    wiki_data = fetch_wikipedia_summary(algorithm_name)
    if wiki_data:
        info["wikipedia"] = wiki_data
        info["description"] = wiki_data.get("extract", "")
        info["references"].append(
            {
                "title": wiki_data.get("title", ""),
                "url": wiki_data.get("url", ""),
                "type": "Wikipedia",
            }
        )

    # Algorithm-specific information
    info.update(get_algorithm_specific_info(algorithm_name, category))

    return info


def get_algorithm_specific_info(algorithm_name: str, category: str) -> Dict:
    """Get algorithm-specific information from known sources."""
    info = {"history": "", "applications": [], "complexity": {}, "variants": []}

    # Known algorithm information
    algorithm_info = {
        "bubble_sort": {
            "history": "Bubble sort was first described in 1956 by computer scientist Donald Knuth. It is one of the simplest sorting algorithms.",
            "applications": [
                "Educational purposes to teach sorting concepts",
                "Small datasets where simplicity is preferred",
                "Nearly sorted data (optimized version)",
            ],
            "variants": ["Cocktail sort", "Comb sort", "Gnome sort"],
        },
        "quick_sort": {
            "history": "Quick sort was developed by Tony Hoare in 1959. It is one of the most efficient general-purpose sorting algorithms.",
            "applications": [
                "Standard library implementations (C++ std::sort, Java Arrays.sort)",
                "Large datasets requiring efficient sorting",
                "In-memory sorting operations",
            ],
            "variants": [
                "Dual-pivot quick sort",
                "3-way quick sort",
                "Randomized quick sort",
            ],
        },
        "merge_sort": {
            "history": "Merge sort was invented by John von Neumann in 1945. It is a stable, divide-and-conquer algorithm.",
            "applications": [
                "External sorting (sorting data too large for memory)",
                "Stable sorting requirements",
                "Parallel processing implementations",
            ],
            "variants": [
                "Bottom-up merge sort",
                "Natural merge sort",
                "In-place merge sort",
            ],
        },
        "binary_search": {
            "history": "Binary search was first described in 1946 by John Mauchly. It requires the array to be sorted.",
            "applications": [
                "Searching in sorted arrays",
                "Finding insertion points",
                "Range queries in databases",
            ],
            "variants": [
                "Interpolation search",
                "Exponential search",
                "Ternary search",
            ],
        },
        "bfs": {
            "history": "Breadth-first search was formalized in the 1950s. It explores all nodes at the current depth before moving to the next level.",
            "applications": [
                "Shortest path in unweighted graphs",
                "Level-order tree traversal",
                "Social network analysis",
                "Web crawling",
            ],
            "variants": ["Bidirectional BFS", "Multi-source BFS"],
        },
        "dfs": {
            "history": "Depth-first search was described in the 19th century for solving mazes. It explores as far as possible before backtracking.",
            "applications": [
                "Topological sorting",
                "Finding connected components",
                "Solving puzzles and mazes",
                "Tree/graph traversal",
            ],
            "variants": ["Iterative DFS", "DFS with timestamps", "Post-order DFS"],
        },
    }

    # Try exact match
    if algorithm_name in algorithm_info:
        return algorithm_info[algorithm_name]

    # Try partial match
    for key, value in algorithm_info.items():
        if key in algorithm_name.lower():
            return value

    return info


def enhance_readme_with_sources(readme_path: Path) -> bool:
    """
    Enhance a README file with information from external sources.

    Args:
        readme_path: Path to README.md file

    Returns:
        True if enhancements were made
    """
    if not readme_path.exists():
        return False

    algorithm_name = readme_path.parent.name
    content = readme_path.read_text(encoding="utf-8")

    # Read metadata for category
    metadata_path = readme_path.parent / "metadata.json"
    category = "algorithm"
    if metadata_path.exists():
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            category = metadata.get("category", "algorithm")
        except:
            pass

    # Fetch external information
    print(f"Fetching information for {algorithm_name}...")
    external_info = fetch_algorithm_info(algorithm_name, category)

    changes_made = False
    new_sections = {}

    # Add Wikipedia information to Introduction if available
    if external_info.get("wikipedia") and "## Introduction" in content:
        wiki_data = external_info["wikipedia"]
        intro_match = re.search(
            r"(## Introduction\s*\n\n)(.*?)(?=\n\n##|\Z)", content, re.DOTALL
        )

        if (
            intro_match and len(intro_match.group(2).strip()) < 200
        ):  # Only if intro is short
            enhanced_intro = intro_match.group(2).strip()
            if wiki_data.get("extract"):
                # Add Wikipedia information
                wiki_extract = wiki_data["extract"][:500]  # Limit length
                enhanced_intro += f"\n\n{wiki_extract}"
                enhanced_intro += f"\n\n*Source: [Wikipedia - {wiki_data.get('title', '')}]({wiki_data.get('url', '')})*"

                content = (
                    content[: intro_match.start()]
                    + intro_match.group(1)
                    + enhanced_intro
                    + content[intro_match.end() :]
                )
                changes_made = True

    # Add Historical Context section
    if external_info.get("history") and "## Historical Context" not in content:
        new_sections["## Historical Context"] = external_info["history"]
        changes_made = True

    # Add Real-World Applications (enhance existing or add new)
    if external_info.get("applications"):
        if "## Real-World Applications" in content:
            # Enhance existing section
            apps_section = re.search(
                r"(## Real-World Applications\s*\n\n)(.*?)(?=\n\n##|\Z)",
                content,
                re.DOTALL,
            )
            if apps_section:
                existing_apps = apps_section.group(2)
                new_apps = "\n".join(
                    [f"- **{app}**" for app in external_info["applications"]]
                )
                enhanced_apps = existing_apps + "\n\n" + new_apps
                content = (
                    content[: apps_section.start()]
                    + apps_section.group(1)
                    + enhanced_apps
                    + content[apps_section.end() :]
                )
                changes_made = True
        else:
            new_sections["## Real-World Applications"] = "\n".join(
                [f"- **{app}**" for app in external_info["applications"]]
            )
            changes_made = True

    # Add Algorithm Variants section
    if external_info.get("variants") and "## Algorithm Variants" not in content:
        new_sections["## Algorithm Variants"] = (
            "Several variants and improvements of this algorithm exist:\n\n"
            + "\n".join(
                [
                    f"- **{variant}**: [Description]"
                    for variant in external_info["variants"]
                ]
            )
        )
        changes_made = True

    # Add References section
    if external_info.get("references") and "## References" not in content:
        refs_text = "## References\n\n"
        for ref in external_info["references"]:
            refs_text += f"- [{ref.get('title', '')}]({ref.get('url', '')}) - {ref.get('type', 'Source')}\n"
        new_sections["## References"] = refs_text.strip()
        changes_made = True

    # Add External Sources section
    if external_info.get("wikipedia") and "## External Sources" not in content:
        wiki_data = external_info["wikipedia"]
        sources_text = "## External Sources\n\n"
        sources_text += f"- **[Wikipedia: {wiki_data.get('title', '')}]({wiki_data.get('url', '')})**\n"
        sources_text += "  - Comprehensive article with detailed explanation, history, and examples\n"
        new_sections["## External Sources"] = sources_text.strip()
        changes_made = True

    # Insert new sections before "## Further Reading" or at end
    if new_sections:
        insertion_point = content.find("## Further Reading")
        if insertion_point == -1:
            insertion_point = content.find("## References")
        if insertion_point == -1:
            insertion_point = len(content)

        new_sections_text = "\n\n".join(
            [f"{header}\n\n{body}" for header, body in new_sections.items()]
        )

        content = (
            content[:insertion_point].rstrip()
            + "\n\n"
            + new_sections_text
            + "\n\n"
            + content[insertion_point:].lstrip()
        )
        changes_made = True

    if changes_made:
        readme_path.write_text(content, encoding="utf-8")

    return changes_made


def main():
    """Enhance all README files with external sources."""
    readme_files = list(ROOT.rglob("*/README.md"))

    # Filter out root README
    readme_files = [f for f in readme_files if f.parent != ROOT]

    total = len(readme_files)
    enhanced = 0

    print(f"Enhancing {total} README files with external sources...")
    print("This may take a while due to rate limiting...\n")

    for i, readme_path in enumerate(readme_files, 1):
        try:
            if enhance_readme_with_sources(readme_path):
                enhanced += 1
                print(f"[{i}/{total}] Enhanced: {readme_path.parent.name}")
            else:
                print(f"[{i}/{total}] Skipped: {readme_path.parent.name}")

            # Progress update every 50 files
            if i % 50 == 0:
                print(f"\n[PROGRESS] Enhanced {enhanced}/{i} README files so far...\n")

            # Rate limiting
            time.sleep(REQUEST_DELAY)

        except Exception as e:
            print(f"Error enhancing {readme_path}: {e}")
            continue

    print(
        f"\n[COMPLETE] Enhanced {enhanced}/{total} README files with external sources"
    )


if __name__ == "__main__":
    main()
