#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix visualization formatting in README files."""

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


def fix_readme_formatting(readme_path: Path):
    """Fix visualization section formatting."""
    content = readme_path.read_text(encoding="utf-8")
    original_content = content
    
    # Fix: SVG link inside ASCII code block
    # Pattern: ```\n\n### Flowchart (SVG) - SVG should be outside code block
    pattern = r"```\n\n### Flowchart \(SVG\)"
    replacement = "```\n\n### Flowchart (SVG)"
    content = re.sub(pattern, replacement, content)
    
    # Fix: Empty code block before SVG
    pattern = r"```\n\n### Flowchart \(SVG\)"
    replacement = "```\n\n### Flowchart (SVG)"
    content = re.sub(pattern, replacement, content)
    
    # Fix: SVG link inside code block (more specific pattern)
    # Find: ```\n\n### Flowchart (SVG)\n\n![...](...)\n\nBubble Sort Flowchart:
    # Replace: ```\n\n### Flowchart (SVG)\n\n![...](...)\n\n```\n\nBubble Sort Flowchart:
    pattern = r"(```\n\n### Flowchart \(SVG\)\n\n!\[.*?\]\(.*?\)\n\n)([A-Z].*? Flowchart:)"
    replacement = r"\1```\n\n\2"
    content = re.sub(pattern, replacement, content)
    
    if content != original_content:
        readme_path.write_text(content, encoding="utf-8")
        return True
    
    return False


def main():
    """Main function."""
    algorithm_folders = find_all_algorithm_folders()
    
    fixed = 0
    
    print(f"Found {len(algorithm_folders)} algorithm folders")
    print("Fixing visualization formatting...\n")
    
    for algo_dir in algorithm_folders:
        readme_path = algo_dir / "README.md"
        if fix_readme_formatting(readme_path):
            fixed += 1
            if fixed % 50 == 0:
                print(f"Fixed {fixed} README files...")
    
    print(f"\n=== Summary ===")
    print(f"Fixed README files: {fixed}")
    print(f"Total: {len(algorithm_folders)}")


if __name__ == "__main__":
    main()

