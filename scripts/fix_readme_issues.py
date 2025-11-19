#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix common issues in README.md files:
1. Remove duplicate sections (e.g., ## Introduction appearing twice)
2. Fix header formatting (e.g., "## TL;DR (Too Long; Didn't Read)" -> "## TL;DR")
3. Remove "See algorithm.py and Algorithm.java" mentions
4. Add specific descriptions for Key Characteristics (Time/Space Complexity, Stability)
5. Fix spacing: 1 line between header and body, 2 lines between sections
"""

import re
from pathlib import Path
from typing import Dict, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]

# Specific explanations for complexity and stability by algorithm
COMPLEXITY_EXPLANATIONS: Dict[str, Dict[str, str]] = {
    "quick_sort": {
        "time": "O(n log n) average case because it divides the array in half on average each recursion, but O(n²) worst case when pivot is always the smallest/largest element.",
        "space": "O(log n) for the recursion stack since the depth of recursion is logarithmic in the average case.",
        "stability": "Not stable because equal elements may be swapped during partitioning, changing their relative order.",
    },
    "merge_sort": {
        "time": "O(n log n) guaranteed because it always divides the array exactly in half, creating a balanced recursion tree of depth log n.",
        "space": "O(n) because it requires a temporary array of the same size as the input to merge sorted subarrays.",
        "stability": "Stable because when merging, equal elements from the left subarray are always placed before those from the right, preserving original order.",
    },
    "heap_sort": {
        "time": "O(n log n) because building the heap takes O(n) and each of the n extract-max operations takes O(log n).",
        "space": "O(1) because it sorts in-place by rearranging elements within the original array without additional data structures.",
        "stability": "Not stable because heap operations can swap elements that are far apart, potentially changing the relative order of equal elements.",
    },
    "bubble_sort": {
        "time": "O(n²) because it makes n passes through the array, and each pass compares and potentially swaps adjacent elements.",
        "space": "O(1) because it only uses a constant amount of extra space for temporary variables during swapping.",
        "stability": "Stable because it only swaps adjacent elements when they are out of order, preserving the relative order of equal elements.",
    },
    "insertion_sort": {
        "time": "O(n²) worst case because each element may need to be compared with all previous elements, but O(n) for nearly sorted arrays.",
        "space": "O(1) because it sorts in-place by shifting elements within the array without requiring additional memory.",
        "stability": "Stable because it inserts elements in their correct position without swapping equal elements, maintaining their original order.",
    },
    "selection_sort": {
        "time": "O(n²) because it must scan the remaining unsorted portion n times, each scan taking O(n) to find the minimum.",
        "space": "O(1) because it only uses a constant amount of extra space for storing indices and temporary swap variables.",
        "stability": "Not stable because selecting the minimum and swapping it to the front can move an element past equal elements, changing their order.",
    },
    "binary_search": {
        "time": "O(log n) because each comparison eliminates half of the remaining search space, requiring at most log₂(n) comparisons.",
        "space": "O(1) for iterative version because it only uses a few variables, or O(log n) for recursive version due to call stack.",
        "stability": "N/A - searching algorithms don't have stability since they don't rearrange elements.",
    },
    "linear_search": {
        "time": "O(n) because in the worst case, it must examine every element in the array until finding the target or reaching the end.",
        "space": "O(1) because it only uses a constant amount of extra space for loop variables and comparisons.",
        "stability": "N/A - searching algorithms don't have stability since they don't rearrange elements.",
    },
    "bfs": {
        "time": "O(V + E) where V is vertices and E is edges, because each vertex and edge is visited exactly once.",
        "space": "O(V) because the queue can contain at most all vertices, and visited set stores all vertices.",
        "stability": "N/A - graph traversal algorithms don't have stability since they don't sort or rearrange elements.",
    },
    "dfs": {
        "time": "O(V + E) where V is vertices and E is edges, because each vertex and edge is visited exactly once.",
        "space": "O(V) for the recursion stack in worst case (linear graph), or O(h) where h is the maximum depth for tree-like graphs.",
        "stability": "N/A - graph traversal algorithms don't have stability since they don't sort or rearrange elements.",
    },
    "dijkstra": {
        "time": "O((V + E) log V) with binary heap because each vertex is extracted once (V log V) and each edge relaxes once (E log V).",
        "space": "O(V) for the priority queue, distance array, and visited set, each storing at most V elements.",
        "stability": "N/A - shortest path algorithms don't have stability since they don't sort or rearrange elements.",
    },
    "knapsack": {
        "time": "O(nW) where n is items and W is capacity, because the DP table has n×W cells, each computed in constant time.",
        "space": "O(nW) for the DP table storing optimal values for all subproblems, or O(W) if optimized to use only previous row.",
        "stability": "N/A - optimization algorithms don't have stability since they select items rather than sorting them.",
    },
    "edit_distance": {
        "time": "O(mn) where m and n are string lengths, because the DP table has m×n cells, each computed in constant time.",
        "space": "O(mn) for the DP table, or O(min(m,n)) if optimized to use only two rows at a time.",
        "stability": "N/A - string algorithms don't have stability since they compute distances rather than sorting.",
    },
}


def get_algorithm_name_from_path(readme_path: Path) -> str:
    """Extract algorithm name from file path."""
    return readme_path.parent.name


def get_complexity_explanation(
    algorithm_name: str, complexity_type: str
) -> Optional[str]:
    """Get specific explanation for complexity or stability."""
    normalized_name = algorithm_name.lower().replace("-", "_")

    if normalized_name in COMPLEXITY_EXPLANATIONS:
        return COMPLEXITY_EXPLANATIONS[normalized_name].get(complexity_type)

    # Try partial matches
    for key, explanations in COMPLEXITY_EXPLANATIONS.items():
        if key in normalized_name or normalized_name in key:
            return explanations.get(complexity_type)

    return None


def remove_duplicate_sections(content: str) -> Tuple[str, bool]:
    """Remove duplicate sections (e.g., ## Introduction appearing twice)."""
    changed = False

    # First, fix cases where headers are concatenated (e.g., "## Introduction## Introduction")
    # Match pattern like "## Introduction## Introduction" - find repeated header text
    def fix_concatenated_header(match):
        header_text = match.group(1)
        return header_text

    # Pattern: ##+ followed by text, then same pattern repeated
    content = re.sub(
        r"(##+\s+)([^\n#]+?)(\1\2)+", r"\1\2", content, flags=re.IGNORECASE
    )

    lines = content.split("\n")
    seen_sections = set()
    new_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Check if this is a section header (## or ###)
        if re.match(r"^##+\s+", line):
            section_name = line.strip()
            # Normalize section name (remove extra spaces, make lowercase for comparison)
            normalized = re.sub(r"\s+", " ", section_name.lower())

            if normalized in seen_sections:
                # Skip this duplicate section and its content until next section
                changed = True
                i += 1
                # Skip blank line after header
                if i < len(lines) and lines[i].strip() == "":
                    i += 1
                # Skip content until next section or end
                while i < len(lines):
                    if re.match(r"^##+\s+", lines[i]):
                        break
                    i += 1
                continue
            else:
                seen_sections.add(normalized)

        new_lines.append(line)
        i += 1

    if changed:
        return "\n".join(new_lines), True
    return content, False


def fix_header_formatting(content: str) -> Tuple[str, bool]:
    """Fix header formatting issues."""
    changed = False

    # Fix "## TL;DR (Too Long; Didn't Read)" -> "## TL;DR"
    pattern1 = r"^##\s+TL;DR\s+\([^)]+\)"
    if re.search(pattern1, content, re.MULTILINE):
        content = re.sub(pattern1, "## TL;DR", content, flags=re.MULTILINE)
        changed = True

    return content, changed


def remove_see_algorithm_mentions(content: str) -> Tuple[str, bool]:
    """Remove 'See algorithm.py and Algorithm.java' mentions."""
    patterns = [
        r"See\s+algorithm\.py\s+and\s+Algorithm\.java",
        r"See\s+algorithm\.py",
        r"See\s+Algorithm\.java",
        r"see\s+algorithm\.py\s+and\s+Algorithm\.java",
        r"see\s+algorithm\.py",
        r"see\s+Algorithm\.java",
    ]

    changed = False
    for pattern in patterns:
        if re.search(pattern, content, re.IGNORECASE):
            content = re.sub(pattern, "", content, flags=re.IGNORECASE)
            changed = True

    # Clean up extra blank lines that might result
    content = re.sub(r"\n\s*\n\s*\n+", "\n\n", content)

    return content, changed


def add_complexity_explanations(content: str, algorithm_name: str) -> Tuple[str, bool]:
    """Add specific explanations for Key Characteristics."""
    changed = False

    # Pattern to match Key Characteristics section
    pattern = r"(\*\*Key\s+Characteristics:\*\*\s*\n)((?:- \*\*[^*]+\*\*: [^\n]+\n?)+)"

    def replace_characteristics(match):
        nonlocal changed
        header = match.group(1)
        characteristics = match.group(2)

        # Extract current characteristics
        time_match = re.search(r"- \*\*Time Complexity\*\*: ([^\n]+)", characteristics)
        space_match = re.search(
            r"- \*\*Space Complexity\*\*: ([^\n]+)", characteristics
        )
        stability_match = re.search(r"- \*\*Stability\*\*: ([^\n]+)", characteristics)

        new_characteristics = []

        if time_match:
            time_value = time_match.group(1).strip()
            explanation = get_complexity_explanation(algorithm_name, "time")
            if explanation:
                # Extract just the complexity notation (e.g., "O(n log n)") from explanation
                # If explanation starts with complexity, use it; otherwise append to existing
                if (
                    explanation.startswith("O(")
                    or explanation.startswith("Θ(")
                    or explanation.startswith("Ω(")
                ):
                    new_characteristics.append(f"- **Time Complexity**: {explanation}")
                elif time_value == "Varies":
                    new_characteristics.append(f"- **Time Complexity**: {explanation}")
                else:
                    new_characteristics.append(
                        f"- **Time Complexity**: {time_value}. {explanation}"
                    )
                changed = True
            else:
                new_characteristics.append(f"- **Time Complexity**: {time_value}")
        else:
            explanation = get_complexity_explanation(algorithm_name, "time")
            if explanation:
                new_characteristics.append(f"- **Time Complexity**: {explanation}")
                changed = True
            else:
                new_characteristics.append("- **Time Complexity**: Varies")

        if space_match:
            space_value = space_match.group(1).strip()
            explanation = get_complexity_explanation(algorithm_name, "space")
            if explanation:
                if (
                    explanation.startswith("O(")
                    or explanation.startswith("Θ(")
                    or explanation.startswith("Ω(")
                ):
                    new_characteristics.append(f"- **Space Complexity**: {explanation}")
                elif space_value == "Varies":
                    new_characteristics.append(f"- **Space Complexity**: {explanation}")
                else:
                    new_characteristics.append(
                        f"- **Space Complexity**: {space_value}. {explanation}"
                    )
                changed = True
            else:
                new_characteristics.append(f"- **Space Complexity**: {space_value}")
        else:
            explanation = get_complexity_explanation(algorithm_name, "space")
            if explanation:
                new_characteristics.append(f"- **Space Complexity**: {explanation}")
                changed = True
            else:
                new_characteristics.append("- **Space Complexity**: Varies")

        if stability_match:
            stability_value = stability_match.group(1).strip()
            # Remove any existing explanation from stability_value
            stability_value = re.sub(
                r"\s+Not stable.*|N/A\s+Not stable.*", "", stability_value
            ).strip()
            explanation = get_complexity_explanation(algorithm_name, "stability")
            if explanation:
                # Check if explanation is already in the value
                if (
                    explanation.lower() in stability_value.lower()
                    or stability_value.lower() in explanation.lower()
                ):
                    # Already has explanation, just use it
                    new_characteristics.append(f"- **Stability**: {explanation}")
                elif stability_value == "N/A" or stability_value == "":
                    new_characteristics.append(f"- **Stability**: {explanation}")
                else:
                    new_characteristics.append(
                        f"- **Stability**: {stability_value}. {explanation}"
                    )
                changed = True
            else:
                new_characteristics.append(
                    f"- **Stability**: {stability_value if stability_value else 'N/A'}"
                )
        else:
            explanation = get_complexity_explanation(algorithm_name, "stability")
            if explanation:
                new_characteristics.append(f"- **Stability**: {explanation}")
                changed = True
            else:
                new_characteristics.append("- **Stability**: N/A")

        return header + "\n".join(new_characteristics) + "\n"

    if re.search(pattern, content):
        content = re.sub(
            pattern, replace_characteristics, content, flags=re.MULTILINE | re.DOTALL
        )

    return content, changed


def fix_spacing(content: str) -> Tuple[str, bool]:
    """Fix spacing: 1 line between header and body, 2 lines between sections."""
    changed = False
    lines = content.split("\n")
    new_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]
        new_lines.append(line)

        # Check if this is a section header (## or ###)
        if re.match(r"^##+\s+", line):
            # Should have exactly 1 blank line after header
            i += 1
            if i < len(lines):
                if lines[i].strip() == "":
                    # Already has blank line, keep it
                    new_lines.append("")
                    i += 1
                else:
                    # No blank line, add one
                    new_lines.append("")
                    changed = True
        else:
            i += 1

    # Join and fix spacing between sections (2 blank lines)
    content = "\n".join(new_lines)

    # Ensure 2 blank lines between major sections (##)
    # But keep 1 blank line between subsections (###)
    content = re.sub(r"(##\s+[^\n]+)\n\n([^#\n])", r"\1\n\n\2", content)
    content = re.sub(r"(##\s+[^\n]+)\n([^#\n])", r"\1\n\n\2", content)

    # Normalize multiple blank lines to max 2
    content = re.sub(r"\n{4,}", "\n\n\n", content)

    # Ensure exactly 2 blank lines between ## sections
    content = re.sub(r"(##\s+[^\n]+)\n+([^#\n])", r"\1\n\n\2", content)

    return content, changed


def fix_readme(readme_path: Path) -> bool:
    """Fix all issues in a README file."""
    try:
        content = readme_path.read_text(encoding="utf-8")
        original_content = content
        algorithm_name = get_algorithm_name_from_path(readme_path)

        # Apply all fixes
        content, changed1 = remove_duplicate_sections(content)
        content, changed2 = fix_header_formatting(content)
        content, changed3 = remove_see_algorithm_mentions(content)
        content, changed4 = add_complexity_explanations(content, algorithm_name)
        content, changed5 = fix_spacing(content)

        if (
            any([changed1, changed2, changed3, changed4, changed5])
            or content != original_content
        ):
            readme_path.write_text(content, encoding="utf-8")
            return True

        return False
    except Exception as e:
        print(f"Error processing {readme_path}: {e}")
        return False


def main():
    """Main function to fix all README files."""
    updated_count = 0
    processed_count = 0

    for semester_dir in ROOT.glob("semester_*"):
        if not semester_dir.is_dir():
            continue

        for lecture_dir in semester_dir.iterdir():
            if not lecture_dir.is_dir():
                continue

            for algo_dir in lecture_dir.iterdir():
                if not algo_dir.is_dir():
                    continue

                readme_path = algo_dir / "README.md"
                if not readme_path.exists():
                    continue

                processed_count += 1

                if fix_readme(readme_path):
                    updated_count += 1
                    if updated_count % 50 == 0:
                        print(f"Fixed {updated_count} READMEs...")

    print(f"\nProcessed {processed_count} README files")
    print(f"Updated {updated_count} files with fixes")


if __name__ == "__main__":
    main()
