#!/usr/bin/env python3
"""
Fix the final remaining semester_01 Algorithm.java files missing package declarations.
"""

import os
from pathlib import Path

def fix_remaining_packages():
    """Fix package declarations for the final remaining semester_01 files."""

    # List of files that still need packages (from our earlier check)
    remaining_files = [
        "semester_01/lecture_11_dynamic_programming/fibonacci/Algorithm.java",
        "semester_01/lecture_11_dynamic_programming/knapsack/Algorithm.java",
        "semester_01/lecture_11_dynamic_programming/longest_common_subsequence/Algorithm.java",
        "semester_01/lecture_09_graph_algorithms/dfs/Algorithm.java",
        "semester_01/lecture_09_graph_algorithms/dijkstra/Algorithm.java",
        "semester_01/lecture_09_graph_algorithms/floyd_warshall/Algorithm.java",
        "semester_01/lecture_08_hash_tables/hash_table/Algorithm.java",
        "semester_01/lecture_05_trees/avl_tree/Algorithm.java"
    ]

    fixed_count = 0

    for file_path in remaining_files:
        java_file = Path(file_path)
        if not java_file.exists():
            print(f"File not found: {file_path}")
            continue

        try:
            content = java_file.read_text(encoding='utf-8')

            # Skip if already has package
            if 'package semester_01.' in content:
                continue

            # Generate package name from path
            path_parts = str(java_file.relative_to(Path('.'))).split(os.sep)[:-1]  # Exclude filename
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

    print(f"\nFixed package declarations in {fixed_count} final files")

if __name__ == "__main__":
    fix_remaining_packages()
