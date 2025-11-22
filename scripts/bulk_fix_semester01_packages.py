#!/usr/bin/env python3
"""
Bulk fix package declarations for all remaining semester_01 Algorithm.java files.
"""

import os
import re
from pathlib import Path

def bulk_fix_packages():
    """Fix package declarations for all remaining semester_01 files."""
    semester01_path = Path("semester_01")
    fixed_count = 0

    # List of files we already fixed
    already_fixed = {
        'lecture_01_sorting_fundamentals/bubble_sort/Algorithm.java',
        'lecture_01_sorting_fundamentals/insertion_sort/Algorithm.java',
        'lecture_01_sorting_fundamentals/selection_sort/Algorithm.java',
        'lecture_02_efficient_sorting/quick_sort/Algorithm.java',
        'lecture_02_efficient_sorting/merge_sort/Algorithm.java',
        'lecture_02_efficient_sorting/heap_sort/Algorithm.java',
        'lecture_03_specialized_sorting/radix_sort/Algorithm.java',
        'lecture_03_specialized_sorting/counting_sort/Algorithm.java',
        'lecture_03_specialized_sorting/bucket_sort/Algorithm.java',
        'lecture_04_searching/binary_search/Algorithm.java',
        'lecture_04_searching/linear_search/Algorithm.java',
        'lecture_04_searching/jump_search/Algorithm.java',
        'lecture_04_searching/interpolation_search/Algorithm.java',
        'lecture_05_trees/binary_tree/Algorithm.java',
        'lecture_05_trees/binary_search_tree/Algorithm.java',
        'lecture_06_advanced_trees/trie/Algorithm.java',
        'lecture_06_advanced_trees/red_black_tree/Algorithm.java'
    }

    for java_file in semester01_path.rglob("Algorithm.java"):
        relative_path = str(java_file.relative_to(semester01_path))
        if relative_path in already_fixed:
            continue

        try:
            content = java_file.read_text(encoding='utf-8')

            # Skip if already has package
            if re.search(r'^\s*package\s+semester_01\.', content, re.MULTILINE):
                continue

            # Generate package name from path
            path_parts = str(java_file.relative_to(semester01_path.parent)).split(os.sep)[:-1]  # Exclude filename
            package_name = '.'.join(path_parts)

            # Add package declaration at top
            lines = content.split('\n')

            # Find first non-comment, non-empty line
            insert_idx = 0
            for i, line in enumerate(lines):
                stripped = line.strip()
                if stripped and not stripped.startswith('//') and not stripped.startswith('/*') and not stripped.startswith('*'):
                    insert_idx = i
                    break

            lines.insert(insert_idx, f'package {package_name};')
            if insert_idx > 0 or lines[insert_idx + 1].strip():
                lines.insert(insert_idx + 1, '')

            content = '\n'.join(lines)
            java_file.write_text(content, encoding='utf-8')
            print(f"Fixed package in: {java_file}")
            fixed_count += 1

        except Exception as e:
            print(f"Error processing {java_file}: {e}")

    print(f"\nBulk fixed package declarations in {fixed_count} additional files")
    return fixed_count

if __name__ == "__main__":
    bulk_fix_packages()
