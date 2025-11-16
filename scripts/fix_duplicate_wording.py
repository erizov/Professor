#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix duplicate wording in README.md files.

Fixes patterns like:
- "Log Aggregation is log aggregation is a fundamental algorithm."
- "Svm is svm is a fundamental algorithm."
- "Single Responsibility is single responsibility is a fundamental algorithm."

To:
- "Log Aggregation is a fundamental algorithm."
- "Svm is a fundamental algorithm."
- "Single Responsibility is a fundamental algorithm."

Usage:
    python scripts/fix_duplicate_wording.py
"""

import re
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parents[1]


def extract_title_from_readme(content: str) -> str:
    """Extract the title from README content (first # heading)."""
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return ""


def fix_duplicate_wording(content: str, title: str) -> Tuple[str, bool]:
    """
    Fix duplicate wording patterns in README content.
    
    Returns:
        Tuple of (fixed_content, was_changed)
    """
    if not title:
        return content, False
    
    changed = False
    new_content = content
    
    # Generate all possible lowercase variations of the title
    title_lower = title.lower()
    words = title.split()
    title_lower_words = ' '.join(word.lower() for word in words)
    
    # Also try partial matches (e.g., "Single Responsibility" from "Single Responsibility Principle")
    title_variations = [title, title_lower, title_lower_words]
    if len(words) > 1:
        # Try first N-1 words (e.g., "Single Responsibility" from "Single Responsibility Principle")
        for i in range(1, len(words)):
            partial = ' '.join(words[:i])
            title_variations.append(partial)
            title_variations.append(partial.lower())
    
    # Pattern 1: "{Title} is {title_lowercase} is a fundamental algorithm."
    # Match: "Log Aggregation is log aggregation is a fundamental algorithm."
    for title_var in title_variations:
        if not title_var:
            continue
        title_var_lower = title_var.lower()
        
        pattern_str = rf'({re.escape(title_var)}\s+is\s+){re.escape(title_var_lower)}(\s+is\s+a\s+fundamental\s+algorithm\.)'
        pattern = re.compile(pattern_str, re.IGNORECASE)
        if pattern.search(new_content):
            def replace(match):
                nonlocal changed
                changed = True
                return f"{match.group(1)}a fundamental algorithm."
            new_content = pattern.sub(replace, new_content)
            break
    
    # Pattern 2: More general - "{Title} is {title_lowercase} is"
    # This catches variations like "X is x is" in any context
    if not changed:
        for title_var in title_variations:
            if not title_var:
                continue
            title_var_lower = title_var.lower()
            
            pattern_str = rf'({re.escape(title_var)}\s+is\s+){re.escape(title_var_lower)}(\s+is\s+)'
            pattern = re.compile(pattern_str, re.IGNORECASE)
            if pattern.search(new_content):
                def replace(match):
                    nonlocal changed
                    changed = True
                    return f"{match.group(1)}"
                new_content = pattern.sub(replace, new_content)
                break
    
    return new_content, changed


def process_readme(readme_path: Path) -> bool:
    """Process a single README file and fix duplicate wording."""
    try:
        content = readme_path.read_text(encoding="utf-8")
        title = extract_title_from_readme(content)
        
        if not title:
            return False
        
        fixed_content, was_changed = fix_duplicate_wording(content, title)
        
        if was_changed:
            readme_path.write_text(fixed_content, encoding="utf-8")
            return True
        
        return False
    except Exception as e:
        print(f"Error processing {readme_path}: {e}")
        return False


def main():
    """Main function to process all README files."""
    updated_count = 0
    processed_count = 0
    
    # Find all README.md files in algorithm directories
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
                if process_readme(readme_path):
                    updated_count += 1
                    print(f"Fixed: {readme_path.relative_to(ROOT)}")
    
    print(f"\nProcessed {processed_count} README files")
    print(f"Fixed {updated_count} files with duplicate wording")


if __name__ == "__main__":
    main()

