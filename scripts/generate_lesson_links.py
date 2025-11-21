#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate lesson links for README.md"""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def get_all_lectures():
    """Get all lecture directories organized by semester."""
    lectures_by_semester = {}
    
    for semester_dir in sorted(ROOT.glob("semester_*")):
        if not semester_dir.is_dir():
            continue
        
        semester_num = re.search(r'semester_(\d+)', semester_dir.name)
        if not semester_num:
            continue
        
        semester_num = int(semester_num.group(1))
        lectures = []
        
        for lecture_dir in sorted(semester_dir.glob("lecture_*")):
            if not lecture_dir.is_dir():
                continue
            
            lecture_name = lecture_dir.name
            lecture_path = lecture_dir.relative_to(ROOT)
            lectures.append((lecture_name, lecture_path))
        
        if lectures:
            lectures_by_semester[semester_num] = lectures
    
    return lectures_by_semester


def format_lecture_name(lecture_name):
    """Format lecture name for display."""
    # Convert lecture_01_sorting_fundamentals to "01: Sorting Fundamentals"
    parts = lecture_name.split('_')
    if len(parts) >= 2 and parts[0] == 'lecture':
        num = parts[1]
        title = ' '.join(word.capitalize() for word in parts[2:])
        return f"{num}: {title}"
    return lecture_name.replace('_', ' ').title()


def generate_links_markdown():
    """Generate markdown with links to all lectures."""
    lectures_by_semester = get_all_lectures()
    
    markdown = "## Course Structure with Lesson Links\n\n"
    
    for semester_num in sorted(lectures_by_semester.keys()):
        lectures = lectures_by_semester[semester_num]
        markdown += f"### Semester {semester_num}\n\n"
        
        for lecture_name, lecture_path in lectures:
            formatted_name = format_lecture_name(lecture_name)
            markdown += f"- [{formatted_name}]({lecture_path.as_posix()}/)\n"
        
        markdown += "\n"
    
    return markdown


if __name__ == "__main__":
    print(generate_links_markdown())

