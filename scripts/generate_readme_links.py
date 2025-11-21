#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate algorithm links for README.md Course Structure section.
"""

from pathlib import Path
from typing import List, Tuple, Dict
import re

ROOT = Path(__file__).resolve().parents[1]


def find_all_algorithms() -> Dict[str, List[Tuple[str, str, str]]]:
    """
    Find all algorithms organized by semester and lecture.
    Returns: {semester_num: [(lecture_name, algorithm_name, full_path), ...]}
    """
    algorithms_by_semester: Dict[str, List[Tuple[str, str, str]]] = {}
    
    for semester_dir in sorted(ROOT.glob("semester_*")):
        if not semester_dir.is_dir():
            continue
        if any(x in str(semester_dir) for x in ["__pycache__", ".git"]):
            continue
        
        semester_num = semester_dir.name.replace("semester_", "")
        algorithms_by_semester[semester_num] = []
        
        for lecture_dir in sorted(semester_dir.iterdir()):
            if not lecture_dir.is_dir():
                continue
            if "lecture_" not in lecture_dir.name:
                continue
            
            lecture_name = lecture_dir.name
            lecture_title = lecture_name.replace("lecture_", "").replace("_", " ").title()
            
            for algo_dir in sorted(lecture_dir.iterdir()):
                if not algo_dir.is_dir():
                    continue
                if algo_dir.name.startswith("lecture_"):
                    continue
                if any(x in algo_dir.name for x in ["__pycache__", ".git"]):
                    continue
                
                algorithm_name = algo_dir.name
                algorithm_title = algorithm_name.replace("_", " ").title()
                full_path = f"{semester_dir.name}/{lecture_name}/{algorithm_name}"
                
                algorithms_by_semester[semester_num].append(
                    (lecture_name, algorithm_name, full_path, algorithm_title)
                )
    
    return algorithms_by_semester


def generate_markdown_links(algorithms_by_semester: Dict[str, List[Tuple[str, str, str, str]]]) -> str:
    """Generate markdown with links to all algorithms."""
    lines = []
    
    for semester_num in sorted(algorithms_by_semester.keys(), key=int):
        algorithms = algorithms_by_semester[semester_num]
        if not algorithms:
            continue
        
        # Group by lecture
        by_lecture: Dict[str, List[Tuple[str, str, str, str]]] = {}
        for lecture_name, algo_name, full_path, algo_title in algorithms:
            if lecture_name not in by_lecture:
                by_lecture[lecture_name] = []
            by_lecture[lecture_name].append((lecture_name, algo_name, full_path, algo_title))
        
        lines.append(f"### Semester {semester_num}")
        lines.append("")
        
        for lecture_name in sorted(by_lecture.keys()):
            lecture_algorithms = by_lecture[lecture_name]
            lecture_title = lecture_name.replace("lecture_", "").replace("_", " ").title()
            
            lines.append(f"#### {lecture_title}")
            lines.append("")
            
            for _, algo_name, full_path, algo_title in lecture_algorithms:
                # Create link to algorithm README
                link = f"[{algo_title}]({full_path}/README.md)"
                lines.append(f"- {link}")
            
            lines.append("")
    
    return "\n".join(lines)


def main():
    """Main function."""
    algorithms_by_semester = find_all_algorithms()
    
    total = sum(len(algos) for algos in algorithms_by_semester.values())
    print(f"Found {total} algorithms across {len(algorithms_by_semester)} semesters")
    
    markdown = generate_markdown_links(algorithms_by_semester)
    
    # Write to file
    output_file = ROOT / "ALGORITHM_LINKS.md"
    output_file.write_text(markdown, encoding="utf-8")
    print(f"Generated links written to {output_file}")
    
    # Also print first 50 lines as preview
    print("\nPreview (first 50 lines):")
    print("\n".join(markdown.split("\n")[:50]))


if __name__ == "__main__":
    main()

