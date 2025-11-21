#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Remove numbered lists and fix code file links in README files."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def find_all_readme_files():
    """Find all README.md files in algorithm directories."""
    readme_files = []
    
    for semester_dir in sorted(ROOT.glob("semester_*")):
        if not semester_dir.is_dir():
            continue
        
        for lecture_dir in sorted(semester_dir.glob("lecture_*")):
            if not lecture_dir.is_dir():
                continue
            
            for algo_dir in sorted(lecture_dir.iterdir()):
                if algo_dir.is_dir():
                    readme_path = algo_dir / "README.md"
                    if readme_path.exists():
                        readme_files.append(readme_path)
    
    return readme_files


def remove_numbered_lists(content: str) -> str:
    """Remove numbered list items from content."""
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        stripped = line.strip()
        # Pattern to match numbered lists like "1. **Text**" or "1. Text" at start of line
        # Also handle lines with just numbers like "1. Initialize"
        if re.match(r'^\d+\.\s+', stripped):
            # Remove the number and dot, keep the rest
            cleaned = re.sub(r'^\d+\.\s+', '', line)
            # If it has ** at start and end, remove one level of bold
            cleaned = re.sub(r'\*\*([^*]+)\*\*', r'\1', cleaned)
            new_lines.append(cleaned)
        else:
            new_lines.append(line)
    
    return '\n'.join(new_lines)


def fix_code_file_links(content: str, readme_path: Path) -> str:
    """Fix code file links to use /code/ route for web interface."""
    algo_dir = readme_path.parent
    relative_path = algo_dir.relative_to(ROOT)
    
    # Pattern to match markdown links like [Python Implementation](path/to/file.py)
    link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    
    def replace_link(match):
        link_text = match.group(1)
        link_path = match.group(2)
        
        # Check if it's a code file link
        if link_path.endswith(('.py', '.java')):
            # Extract just the filename
            filename = Path(link_path).name
            
            # Check if file exists in the algorithm directory
            file_path = algo_dir / filename
            if file_path.exists():
                # Use /code/ route for web interface
                code_path = f"/code/{relative_path.as_posix()}/{filename}"
                return f"[{link_text}]({code_path})"
            else:
                # File doesn't exist, return original
                return match.group(0)
        else:
            # Not a code file, return original
            return match.group(0)
    
    # Replace all links
    new_content = re.sub(link_pattern, replace_link, content)
    
    return new_content


def process_readme(readme_path: Path) -> bool:
    """Process a single README file."""
    try:
        content = readme_path.read_text(encoding='utf-8')
        original_content = content
        
        # Remove numbered lists
        content = remove_numbered_lists(content)
        
        # Fix code file links
        content = fix_code_file_links(content, readme_path)
        
        if content != original_content:
            readme_path.write_text(content, encoding='utf-8')
            return True
        return False
    except Exception as e:
        print(f"Error processing {readme_path}: {e}")
        return False


def main():
    """Main function."""
    readme_files = find_all_readme_files()
    
    print(f"Found {len(readme_files)} README files")
    print("Processing files...\n")
    
    updated = 0
    errors = 0
    
    for readme_path in readme_files:
        try:
            if process_readme(readme_path):
                updated += 1
                rel_path = readme_path.relative_to(ROOT)
                print(f"[OK] Updated: {rel_path}")
        except Exception as e:
            errors += 1
            rel_path = readme_path.relative_to(ROOT)
            print(f"[ERROR] {rel_path}: {e}")
    
    print(f"\n=== Summary ===")
    print(f"Updated: {updated}")
    print(f"Errors: {errors}")
    print(f"Total: {len(readme_files)}")


if __name__ == "__main__":
    main()

