#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add SVG links to README files that have visualizations but missing SVG section."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def find_all_algorithm_folders():
    """Find all algorithm folders."""
    algorithm_folders = []
    
    for semester_dir in sorted(ROOT.glob("semester_*")):
        if not semester_dir.is_dir():
            continue
        
        for lecture_dir in sorted(semester_dir.glob("lecture_*")):
            if not lecture_dir.is_dir():
                continue
            
            for algo_dir in sorted(lecture_dir.iterdir()):
                if algo_dir.is_dir() and (algo_dir / "README.md").exists():
                    algorithm_folders.append(algo_dir)
    
    return algorithm_folders


def add_svg_link(readme_path: Path, algo_dir: Path):
    """Add SVG link to README if missing."""
    content = readme_path.read_text(encoding="utf-8")
    original_content = content
    
    # Check if SVG section already exists
    if "### Flowchart (SVG)" in content:
        return False
    
    # Check if SVG file exists
    vis_dir = algo_dir / "visualizations"
    svg_path = vis_dir / "flowchart.svg"
    if not svg_path.exists():
        return False
    
    # Check if visualization section exists
    if "## Algorithm Visualization" not in content:
        return False
    
    # Get algorithm name for alt text
    algorithm_name = algo_dir.name.replace("_", " ").title()
    
    # Create SVG section
    relative_svg = svg_path.relative_to(ROOT)
    svg_section = f"""
### Flowchart (SVG)

![{algorithm_name} Flowchart]({relative_svg.as_posix()})

"""
    
    # Insert after ASCII flowchart code block ends
    # Pattern: ```\n\n### Step-by-Step Execution
    pattern = r"(```\n\n)(### Step-by-Step Execution)"
    replacement = r"\1" + svg_section + r"\2"
    new_content = re.sub(pattern, replacement, content)
    
    if new_content != original_content:
        readme_path.write_text(new_content, encoding="utf-8")
        return True
    
    return False


def main():
    """Main function."""
    algorithm_folders = find_all_algorithm_folders()
    
    added = 0
    
    print(f"Found {len(algorithm_folders)} algorithm folders")
    print("Adding SVG links to README files...\n")
    
    for algo_dir in algorithm_folders:
        readme_path = algo_dir / "README.md"
        if add_svg_link(readme_path, algo_dir):
            added += 1
            if added % 50 == 0:
                print(f"Added SVG links to {added} README files...")
    
    print(f"\n=== Summary ===")
    print(f"Added SVG links: {added}")
    print(f"Total: {len(algorithm_folders)}")


if __name__ == "__main__":
    main()

