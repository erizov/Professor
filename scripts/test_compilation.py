#!/usr/bin/env python3
"""
Test compilation of fixed Java files.
"""

import subprocess
import os
from pathlib import Path

def test_compilation(java_file):
    """Test compilation of a single Java file."""
    try:
        # Create output directory if needed
        output_dir = java_file.parent / "compiled"
        output_dir.mkdir(exist_ok=True)

        # Compile with classpath
        classpath = str(java_file.parent)
        result = subprocess.run(
            ["javac", "-cp", classpath, "-d", str(output_dir), str(java_file)],
            capture_output=True,
            text=True,
            timeout=10
        )

        success = result.returncode == 0
        if success:
            # Clean up compiled files
            import shutil
            if output_dir.exists():
                shutil.rmtree(output_dir)
            return True, ""
        else:
            return False, result.stderr.strip()

    except subprocess.TimeoutExpired:
        return False, "Compilation timed out"
    except Exception as e:
        return False, f"Compilation error: {e}"

def test_recently_fixed_files():
    """Test compilation of recently fixed files."""
    # List of files we fixed
    fixed_files = [
        "semester_01/lecture_04_searching/jump_search/Algorithm.java",
        "semester_01/lecture_04_searching/interpolation_search/Algorithm.java",
        "semester_01/lecture_05_trees/binary_tree/Algorithm.java",
        "semester_01/lecture_05_trees/binary_search_tree/Algorithm.java",
        "semester_01/lecture_06_advanced_trees/trie/Algorithm.java",
        "semester_01/lecture_06_advanced_trees/red_black_tree/Algorithm.java",
        "semester_01/lecture_06_advanced_trees/b_tree/Algorithm.java",
        "semester_01/lecture_07_heaps_priority/priority_queue/Algorithm.java",
        "semester_01/lecture_07_heaps_priority/fibonacci_heap/Algorithm.java"
    ]

    results = []
    compiled_count = 0
    failed_count = 0

    for file_path in fixed_files:
        java_file = Path(file_path)
        if java_file.exists():
            print(f"Testing: {file_path}")
            success, error = test_compilation(java_file)
            results.append((file_path, success, error))

            if success:
                compiled_count += 1
                print("  ✅ Compiles successfully"            else:
                failed_count += 1
                print(f"  ❌ Compilation failed: {error[:100]}...")
        else:
            print(f"  ⚠ File not found: {file_path}")

    print(f"\nCompilation Test Results:")
    print(f"Total files tested: {len(results)}")
    print(f"Successfully compiled: {compiled_count}")
    print(f"Compilation failures: {failed_count}")

    return results

if __name__ == "__main__":
    test_recently_fixed_files()
