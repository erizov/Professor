#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update README.md files:
1. Update Educational Materials section to show only links for chosen language
2. Remove 'Name of Algorithm' placeholder
3. Remove empty '## Code Files' section
"""

import re
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

ROOT = Path(__file__).resolve().parents[1]


def update_educational_materials_section(content: str, folder_path: Path, language: str = 'en') -> str:
    """Update Educational Materials section to show only links for chosen language."""
    
    # Check which language files exist
    has_ru_school = (folder_path / "school.ru.md").exists()
    has_ru_univer = (folder_path / "univer.ru.md").exists()
    has_en_school = (folder_path / "school.en.md").exists()
    has_en_univer = (folder_path / "univer.en.md").exists()
    
    # Use provided language, or determine from available files
    if language not in ['ru', 'en']:
        if has_en_school or has_en_univer:
            language = 'en'
        elif has_ru_school or has_ru_univer:
            language = 'ru'
        else:
            language = 'en'
    
    # Pattern to match the Educational Materials section
    pattern = r'(## Educational Materials / Учебные материалы\s*\n\n)(.*?)(?=\n##|\Z)'
    
    def replace_section(match):
        # Use language-specific header
        if language == 'ru':
            header = "## Учебные материалы\n\n"
        else:
            header = "## Educational Materials\n\n"
        
        # Generate new content based on chosen language and available files
        links = []
        
        if language == 'ru':
            if has_ru_school:
                links.append("- [Школьный уровень](school.ru.md)")
            if has_ru_univer:
                links.append("- [Университетский уровень](univer.ru.md)")
        else:  # language == 'en'
            if has_en_school:
                links.append("- [School Level](school.en.md)")
            if has_en_univer:
                links.append("- [University Level](univer.en.md)")
        
        # If no links found, show message in chosen language
        if not links:
            if language == 'ru':
                new_content = "*Учебные материалы недоступны.*\n"
            else:
                new_content = "*No educational materials available.*\n"
        else:
            new_content = '\n'.join(links) + '\n'
        
        return header + new_content + '\n'
    
    # Replace the section
    content = re.sub(pattern, replace_section, content, flags=re.DOTALL)
    
    return content


def remove_name_of_algorithm(content: str) -> str:
    """Remove 'Name of Algorithm' placeholder and similar patterns."""
    # Remove lines that contain only "Name of Algorithm" (with optional whitespace)
    # Also handle variations like "Name of Algorithm  " with trailing spaces
    
    # Pattern to match standalone "Name of Algorithm" line with surrounding blank lines
    pattern = r'^\s*Name of Algorithm\s*$\n+'
    content = re.sub(pattern, '', content, flags=re.MULTILINE | re.IGNORECASE)
    
    # Also handle case where it's on a line by itself with blank lines around
    pattern2 = r'\n\s*Name of Algorithm\s*\n+'
    content = re.sub(pattern2, '\n', content, flags=re.MULTILINE | re.IGNORECASE)
    
    # Remove lines that are just algorithm name with leading spaces (like "   Data Observability")
    # This pattern matches lines that are just whitespace + algorithm name + optional whitespace
    # and are followed by blank line
    pattern3 = r'\n\s{3,}[A-Z][a-zA-Z\s]+\s*\n\n'
    # More specific: match lines with 3+ spaces followed by title case words
    pattern3 = r'\n\s{3,}([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*\n\n'
    content = re.sub(pattern3, '\n\n', content, flags=re.MULTILINE)
    
    # Clean up multiple blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    return content


def remove_empty_code_files_section(content: str) -> str:
    """Remove empty '## Code Files' section."""
    # Pattern to match Code Files section with optional content
    # Matches: ## Code Files\n\n (with optional whitespace and empty content)
    # This will match sections that are empty or have only whitespace
    
    # First, try to match section with content between Code Files and next section
    pattern = r'## Code Files\s*\n(?:\s*\n)*(?=\n##|\Z)'
    content = re.sub(pattern, '', content, flags=re.MULTILINE)
    
    # Also handle case where Code Files is followed by another section immediately
    pattern2 = r'## Code Files\s*\n\n(?=##)'
    content = re.sub(pattern2, '', content, flags=re.MULTILINE)
    
    # Clean up any remaining double blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    return content


def update_readme_file(readme_path: Path, language: str = 'en') -> bool:
    """Update a single README.md file."""
    try:
        content = readme_path.read_text(encoding='utf-8')
        original_content = content
        
        folder_path = readme_path.parent
        
        # Apply all updates
        content = remove_name_of_algorithm(content)
        content = remove_empty_code_files_section(content)
        content = update_educational_materials_section(content, folder_path, language)
        
        # Clean up multiple blank lines
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        # Only write if content changed
        if content != original_content:
            readme_path.write_text(content, encoding='utf-8')
            return True
        return False
    except Exception as e:
        print(f"  [ERROR] {e}")
        return False


def main():
    """Main function to update all README.md files."""
    import sys
    
    print("=" * 70)
    print("UPDATING README.MD FILES")
    print("=" * 70)
    print()
    print("This script will:")
    print("1. Update Educational Materials section (based on chosen language)")
    print("2. Remove 'Name of Algorithm' placeholder")
    print("3. Remove empty '## Code Files' section")
    print()
    
    # Get language from command line argument or use default
    language = 'en'
    if len(sys.argv) > 1:
        lang_arg = sys.argv[1].lower()
        if lang_arg in ['ru', 'en']:
            language = lang_arg
        else:
            print(f"Warning: Invalid language '{lang_arg}', using 'en'")
    else:
        print("Usage: python update_readme_educational_materials.py [en|ru]")
        print("Default: en")
        print()
    
    print(f"Language: {language}")
    print()
    
    # Find all README.md files
    readme_files = []
    for semester_dir in ROOT.glob("semester_*"):
        for lecture_dir in semester_dir.glob("lecture_*"):
            for algo_dir in lecture_dir.iterdir():
                if algo_dir.is_dir() and not algo_dir.name.startswith('.'):
                    readme_path = algo_dir / "README.md"
                    if readme_path.exists():
                        readme_files.append(readme_path)
    
    readme_files.sort()
    
    print(f"Found {len(readme_files)} README.md files")
    print()
    
    updated_count = 0
    error_count = 0
    
    for idx, readme_path in enumerate(readme_files, 1):
        relative_path = readme_path.relative_to(ROOT)
        print(f"[{idx}/{len(readme_files)}] {relative_path}")
        
        if update_readme_file(readme_path, language):
            print(f"  [OK] Updated")
            updated_count += 1
        else:
            print(f"  [OK] No changes needed")
        
        if idx % 100 == 0:
            print(f"\nProgress: {idx}/{len(readme_files)} processed\n")
    
    print()
    print("=" * 70)
    print(f"Summary:")
    print(f"  Total files: {len(readme_files)}")
    print(f"  Files updated: {updated_count}")
    print(f"  Errors: {error_count}")
    print("=" * 70)


if __name__ == "__main__":
    main()

