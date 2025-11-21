#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update main README.md with links to individual algorithms."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def find_all_algorithms():
    """Find all algorithms organized by semester and lecture."""
    algorithms_by_semester = {}
    
    for semester_dir in sorted(ROOT.glob("semester_*")):
        if not semester_dir.is_dir():
            continue
        
        semester_num = re.search(r'semester_(\d+)', semester_dir.name)
        if not semester_num:
            continue
        
        semester_num = int(semester_num.group(1))
        algorithms_by_lecture = {}
        
        for lecture_dir in sorted(semester_dir.glob("lecture_*")):
            if not lecture_dir.is_dir():
                continue
            
            lecture_name = lecture_dir.name
            algorithms = []
            
            for algo_dir in sorted(lecture_dir.iterdir()):
                if algo_dir.is_dir() and (algo_dir / "README.md").exists():
                    algo_name = algo_dir.name.replace("_", " ").title()
                    algo_path = algo_dir.relative_to(ROOT)
                    algorithms.append((algo_name, algo_path))
            
            if algorithms:
                algorithms_by_lecture[lecture_name] = algorithms
        
        if algorithms_by_lecture:
            algorithms_by_semester[semester_num] = algorithms_by_lecture
    
    return algorithms_by_semester


def format_lecture_name(lecture_name: str):
    """Format lecture name for display."""
    parts = lecture_name.split('_')
    if len(parts) >= 2 and parts[0] == 'lecture':
        num = parts[1]
        title = ' '.join(word.capitalize() for word in parts[2:])
        return f"{num}: {title}"
    return lecture_name.replace('_', ' ').title()


def generate_algorithm_links_section():
    """Generate markdown section with algorithm links."""
    algorithms_by_semester = find_all_algorithms()
    
    markdown = "## 📚 Individual Algorithm Links\n\n"
    markdown += "> **Quick Navigation**: Browse individual algorithms by semester and lecture.\n\n"
    
    for semester_num in sorted(algorithms_by_semester.keys()):
        algorithms_by_lecture = algorithms_by_semester[semester_num]
        markdown += f"### Semester {semester_num}\n\n"
        
        for lecture_name in sorted(algorithms_by_lecture.keys()):
            algorithms = algorithms_by_lecture[lecture_name]
            formatted_lecture = format_lecture_name(lecture_name)
            
            markdown += f"#### {formatted_lecture}\n\n"
            
            for algo_name, algo_path in algorithms:
                markdown += f"- [{algo_name}]({algo_path.as_posix()}/README.md)\n"
            
            markdown += "\n"
    
    return markdown


def update_main_readme():
    """Update main README.md with algorithm links section."""
    readme_path = ROOT / "README.md"
    content = readme_path.read_text(encoding="utf-8")
    
    # Generate new algorithm links section
    new_section = generate_algorithm_links_section()
    
    # Check if section already exists
    if "## 📚 Individual Algorithm Links" in content:
        # Replace existing section
        pattern = r"(## 📚 Individual Algorithm Links\s*\n.*?)(?=\n## |\Z)"
        new_content = re.sub(pattern, new_section, content, flags=re.DOTALL)
    else:
        # Insert after "Course Structure with Lesson Links" section
        if "## 📚 Course Structure with Lesson Links" in content:
            pattern = r"(## 📚 Course Structure with Lesson Links.*?\n\n)"
            new_content = re.sub(pattern, r"\1" + new_section, content, flags=re.DOTALL)
        else:
            # Insert before "💡 Key Features" section
            pattern = r"(## 💡 Key Features)"
            new_content = re.sub(pattern, new_section + r"\1", content)
    
    readme_path.write_text(new_content, encoding="utf-8")
    print("✓ Updated main README.md with individual algorithm links")


if __name__ == "__main__":
    update_main_readme()

