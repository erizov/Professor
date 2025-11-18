#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate table of contents for the comprehensive textbook.
Extracts headings and algorithm information to create a navigable TOC.
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
TEXTBOOK_PATH = ROOT / "COMPREHENSIVE_COURSE_TEXTBOOK.md"


def extract_algorithm_metadata() -> Dict:
    """Extract metadata for all algorithms."""
    algorithms = {}
    
    for semester_dir in ROOT.glob("semester_*"):
        if not semester_dir.is_dir():
            continue
            
        semester_num = int(semester_dir.name.replace("semester_", ""))
        difficulty = "Undergraduate" if semester_num <= 8 else "Graduate"
        
        for lecture_dir in semester_dir.glob("lecture_*"):
            if not lecture_dir.is_dir():
                continue
                
            for algo_dir in lecture_dir.iterdir():
                if not algo_dir.is_dir():
                    continue
                    
                # Check if it's an algorithm folder
                has_code = (
                    (algo_dir / "algorithm.py").exists()
                    or (algo_dir / "Algorithm.java").exists()
                    or (algo_dir / "algorithm.sql").exists()
                )
                
                if not has_code:
                    continue
                
                algo_name = algo_dir.name
                rel_path = str(algo_dir.relative_to(ROOT))
                
                # Extract metadata
                metadata_file = algo_dir / "metadata.json"
                category = "Algorithm"
                if metadata_file.exists():
                    try:
                        metadata = json.loads(metadata_file.read_text(encoding="utf-8"))
                        category = metadata.get("category", "Algorithm")
                    except:
                        pass
                
                # Determine languages
                languages = []
                if (algo_dir / "algorithm.py").exists():
                    languages.append("Python")
                if (algo_dir / "Algorithm.java").exists():
                    languages.append("Java")
                if (algo_dir / "algorithm.sql").exists():
                    languages.append("SQL")
                
                # Create anchor from algorithm name
                anchor = re.sub(r'[^\w\s-]', '', algo_name.lower())
                anchor = re.sub(r'[-\s]+', '-', anchor)
                
                algorithms[algo_name] = {
                    "name": algo_name,
                    "display_name": algo_name.replace("_", " ").title(),
                    "semester": f"Semester {semester_num}",
                    "semester_num": semester_num,
                    "lecture": lecture_dir.name.replace("_", " ").title(),
                    "category": category,
                    "difficulty": difficulty,
                    "languages": languages,
                    "path": rel_path,
                    "anchor": anchor,
                }
    
    return algorithms


def extract_headings_from_textbook() -> List[Tuple[int, str, str]]:
    """
    Extract all headings from the textbook.
    
    Returns:
        List of (level, text, anchor) tuples
    """
    if not TEXTBOOK_PATH.exists():
        return []
    
    headings = []
    content = TEXTBOOK_PATH.read_text(encoding="utf-8")
    
    # Pattern to match markdown headings
    pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
    
    for match in pattern.finditer(content):
        level = len(match.group(1))
        text = match.group(2).strip()
        
        # Create anchor from heading text
        anchor = re.sub(r'[^\w\s-]', '', text.lower())
        anchor = re.sub(r'[-\s]+', '-', anchor)
        anchor = anchor.strip('-')
        
        headings.append((level, text, anchor))
    
    return headings


def generate_toc_markdown(headings: List[Tuple[int, str, str]], algorithms: Dict) -> str:
    """Generate table of contents in Markdown format."""
    toc_lines = ["# Table of Contents\n"]
    
    # Add quick navigation
    toc_lines.append("## Quick Navigation\n")
    toc_lines.append("- [Course Overview](#course-overview)")
    toc_lines.append("- [Algorithms by Semester](#algorithms-by-semester)")
    toc_lines.append("- [Algorithms by Category](#algorithms-by-category)")
    toc_lines.append("- [Algorithms by Language](#algorithms-by-language)")
    toc_lines.append("- [Algorithms by Difficulty](#algorithms-by-difficulty)")
    toc_lines.append("- [Full Algorithm List](#full-algorithm-list)")
    toc_lines.append("")
    
    # Group algorithms
    by_semester = defaultdict(list)
    by_category = defaultdict(list)
    by_language = defaultdict(list)
    by_difficulty = defaultdict(list)
    
    for algo in algorithms.values():
        by_semester[algo["semester"]].append(algo)
        by_category[algo["category"]].append(algo)
        for lang in algo["languages"]:
            by_language[lang].append(algo)
        by_difficulty[algo["difficulty"]].append(algo)
    
    # Algorithms by Semester
    toc_lines.append("## Algorithms by Semester\n")
    for semester in sorted(by_semester.keys(), key=lambda x: int(x.split()[-1])):
        toc_lines.append(f"### {semester}\n")
        for algo in sorted(by_semester[semester], key=lambda x: x["name"]):
            toc_lines.append(f"- [{algo['display_name']}](#{algo['anchor']})")
        toc_lines.append("")
    
    # Algorithms by Category
    toc_lines.append("## Algorithms by Category\n")
    for category in sorted(by_category.keys()):
        toc_lines.append(f"### {category}\n")
        for algo in sorted(by_category[category], key=lambda x: x["name"]):
            toc_lines.append(f"- [{algo['display_name']}](#{algo['anchor']})")
        toc_lines.append("")
    
    # Algorithms by Language
    toc_lines.append("## Algorithms by Language\n")
    for lang in sorted(by_language.keys()):
        toc_lines.append(f"### {lang}\n")
        for algo in sorted(by_language[lang], key=lambda x: x["name"]):
            toc_lines.append(f"- [{algo['display_name']}](#{algo['anchor']})")
        toc_lines.append("")
    
    # Algorithms by Difficulty
    toc_lines.append("## Algorithms by Difficulty\n")
    for difficulty in ["Undergraduate", "Graduate"]:
        if difficulty in by_difficulty:
            toc_lines.append(f"### {difficulty}\n")
            for algo in sorted(by_difficulty[difficulty], key=lambda x: x["name"]):
                toc_lines.append(f"- [{algo['display_name']}](#{algo['anchor']})")
            toc_lines.append("")
    
    # Full Algorithm List
    toc_lines.append("## Full Algorithm List\n")
    toc_lines.append("| Algorithm | Semester | Category | Languages | Difficulty |")
    toc_lines.append("|-----------|----------|----------|-----------|------------|")
    
    for algo in sorted(algorithms.values(), key=lambda x: (x["semester_num"], x["name"])):
        languages_str = ", ".join(algo["languages"])
        toc_lines.append(
            f"| [{algo['display_name']}](#{algo['anchor']}) | "
            f"{algo['semester']} | {algo['category']} | {languages_str} | {algo['difficulty']} |"
        )
    
    toc_lines.append("")
    
    # Main headings from textbook
    toc_lines.append("## Textbook Sections\n")
    current_level = 0
    for level, text, anchor in headings:
        # Skip very top-level headings
        if level <= 2 and text.lower() in ["algorithms and design patterns course", "course overview"]:
            continue
        
        # Adjust indentation
        indent = "  " * (level - 1)
        toc_lines.append(f"{indent}- [{text}](#{anchor})")
    
    return "\n".join(toc_lines)


def insert_toc_into_textbook(toc_content: str) -> bool:
    """Insert TOC into textbook after the front matter."""
    if not TEXTBOOK_PATH.exists():
        return False
    
    content = TEXTBOOK_PATH.read_text(encoding="utf-8")
    
    # Find insertion point (after front matter, before first major heading)
    # Look for "## Complete 16-Semester Comprehensive Textbook" or similar
    pattern = r'(## Complete 16-Semester Comprehensive Textbook\n)'
    match = re.search(pattern, content)
    
    if match:
        insert_pos = match.end()
        # Check if TOC already exists
        if "<!-- TABLE_OF_CONTENTS -->" in content:
            # Replace existing TOC
            toc_start = content.find("<!-- TABLE_OF_CONTENTS -->")
            toc_end = content.find("<!-- END_TABLE_OF_CONTENTS -->")
            if toc_end != -1:
                toc_end += len("<!-- END_TABLE_OF_CONTENTS -->")
                content = (
                    content[:toc_start]
                    + "<!-- TABLE_OF_CONTENTS -->\n\n"
                    + toc_content
                    + "\n\n<!-- END_TABLE_OF_CONTENTS -->\n"
                    + content[toc_end:]
                )
            else:
                # Malformed, insert after marker
                content = (
                    content[:toc_start]
                    + "<!-- TABLE_OF_CONTENTS -->\n\n"
                    + toc_content
                    + "\n\n<!-- END_TABLE_OF_CONTENTS -->\n\n"
                    + content[toc_start + len("<!-- TABLE_OF_CONTENTS -->"):]
                )
        else:
            # Insert new TOC
            content = (
                content[:insert_pos]
                + "\n\n<!-- TABLE_OF_CONTENTS -->\n\n"
                + toc_content
                + "\n\n<!-- END_TABLE_OF_CONTENTS -->\n\n"
                + content[insert_pos:]
            )
    else:
        # Fallback: insert at beginning
        if "<!-- TABLE_OF_CONTENTS -->" not in content:
            content = (
                "<!-- TABLE_OF_CONTENTS -->\n\n"
                + toc_content
                + "\n\n<!-- END_TABLE_OF_CONTENTS -->\n\n"
                + content
            )
    
    TEXTBOOK_PATH.write_text(content, encoding="utf-8")
    return True


def main():
    """Generate and insert table of contents."""
    print("Extracting algorithm metadata...")
    algorithms = extract_algorithm_metadata()
    print(f"Found {len(algorithms)} algorithms")
    
    print("Extracting headings from textbook...")
    headings = extract_headings_from_textbook()
    print(f"Found {len(headings)} headings")
    
    print("Generating table of contents...")
    toc_content = generate_toc_markdown(headings, algorithms)
    
    print("Inserting TOC into textbook...")
    if insert_toc_into_textbook(toc_content):
        print("[SUCCESS] Table of contents generated and inserted!")
    else:
        print("[ERROR] Failed to insert TOC")
    
    # Save TOC separately
    toc_path = ROOT / "TABLE_OF_CONTENTS.md"
    toc_path.write_text(toc_content, encoding="utf-8")
    print(f"[INFO] TOC also saved to: {toc_path}")


if __name__ == "__main__":
    main()

