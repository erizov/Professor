#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update README.md files based on user's preferred language.
This script is called when user changes language preference.
"""

import sys
import io
from pathlib import Path

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding='utf-8', errors='replace'
    )
    sys.stderr = io.TextIOWrapper(
        sys.stderr.buffer, encoding='utf-8', errors='replace'
    )

# Add parent directory to path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.update_readme_educational_materials import (
    update_readme_file,
    remove_name_of_algorithm,
    remove_empty_code_files_section,
    update_educational_materials_section
)


def update_all_readmes_for_language(language: str = 'en'):
    """Update all README.md files for specified language."""
    if language not in ['ru', 'en']:
        language = 'en'
    
    # Find all README.md files
    readme_files = []
    for semester_dir in ROOT.glob("semester_*"):
        for lecture_dir in semester_dir.glob("lecture_*"):
            for algo_dir in lecture_dir.iterdir():
                if algo_dir.is_dir() and not algo_dir.name.startswith('.'):
                    readme_path = algo_dir / "README.md"
                    if readme_path.exists():
                        readme_files.append(readme_path)
    
    updated_count = 0
    for readme_path in readme_files:
        if update_readme_file(readme_path, language):
            updated_count += 1
    
    return updated_count


if __name__ == "__main__":
    language = sys.argv[1] if len(sys.argv) > 1 else 'en'
    if language not in ['ru', 'en']:
        language = 'en'
    
    print(f"Updating all README.md files for language: {language}")
    updated = update_all_readmes_for_language(language)
    print(f"Updated {updated} files")

