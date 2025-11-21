#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update individual algorithm README.md files with links to code files."""

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


def get_code_file_links(algo_dir: Path):
    """Get links to code files in the algorithm directory."""
    links = []
    relative_path = algo_dir.relative_to(ROOT)
    
    # Check for Python file
    if (algo_dir / "algorithm.py").exists():
        links.append(f"- [Python Implementation]({relative_path.as_posix()}/algorithm.py)")
    
    # Check for Java file
    if (algo_dir / "Algorithm.java").exists():
        links.append(f"- [Java Implementation]({relative_path.as_posix()}/Algorithm.java)")
    
    # Check for test file
    if (algo_dir / "test_algorithm.py").exists():
        links.append(f"- [Python Tests]({relative_path.as_posix()}/test_algorithm.py)")
    
    # Check for Java test file
    java_test = list(algo_dir.glob("*Test.java"))
    if java_test:
        for test_file in java_test:
            test_name = test_file.name
            links.append(f"- [Java Tests]({relative_path.as_posix()}/{test_name})")
    
    return links


def update_readme_with_links(readme_path: Path, code_links: list):
    """Update README.md with code file links."""
    if not code_links:
        return False
    
    content = readme_path.read_text(encoding="utf-8")
    
    # Check if links section already exists
    if "## Code Files" in content or "## Implementation Files" in content:
        # Update existing section
        pattern = r"(## (Code Files|Implementation Files)\s*\n)(.*?)(?=\n## |\Z)"
        replacement = f"## Code Files\n\n" + "\n".join(code_links) + "\n\n"
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    else:
        # Add new section after the title
        lines = content.split("\n")
        insert_pos = 1
        
        # Find insertion point: after the first heading (title)
        for i, line in enumerate(lines[1:], 1):
            if line.strip().startswith("#"):
                # Found another heading, insert before it
                insert_pos = i
                break
            if i > 5:  # Don't go too far
                insert_pos = i
                break
        
        # Insert the code files section
        new_section = "\n## Code Files\n\n" + "\n".join(code_links) + "\n\n"
        lines.insert(insert_pos, new_section)
        new_content = "\n".join(lines)
    
    if new_content != content:
        readme_path.write_text(new_content, encoding="utf-8")
        return True
    
    return False


def main():
    """Main function."""
    algorithm_folders = find_all_algorithm_folders()
    
    updated = 0
    skipped = 0
    
    print(f"Found {len(algorithm_folders)} algorithm folders")
    print("Updating README.md files with code file links...\n")
    
    for algo_dir in algorithm_folders:
        readme_path = algo_dir / "README.md"
        code_links = get_code_file_links(algo_dir)
        
        if code_links:
            if update_readme_with_links(readme_path, code_links):
                updated += 1
                print(f"[OK] Updated: {algo_dir.relative_to(ROOT)}")
            else:
                skipped += 1
        else:
            skipped += 1
    
    print(f"\n=== Summary ===")
    print(f"Updated: {updated}")
    print(f"Skipped (no changes or no code files): {skipped}")
    print(f"Total: {len(algorithm_folders)}")


if __name__ == "__main__":
    main()

