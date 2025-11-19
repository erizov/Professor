#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check TODO status and implementation completeness
"""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def check_todo_status():
    """Check TODO items and missing implementations."""
    todo_count = 0
    todo_implement_count = 0
    missing_impl_count = 0
    placeholder_count = 0
    multiple_main_count = 0

    for algo_file in ROOT.rglob("**/algorithm.py"):
        if "supporting_documents" in str(algo_file) or "scripts" in str(algo_file):
            continue

        try:
            content = algo_file.read_text(encoding="utf-8")

            # Count TODO items
            todos = content.count("TODO")
            if todos > 0:
                todo_count += todos
                if "TODO" in content and "Implement" in content:
                    todo_implement_count += 1

            # Check for multiple main() functions
            main_count = len(re.findall(r"^\s*def\s+main\s*\(", content, re.MULTILINE))
            if main_count > 1:
                multiple_main_count += 1

            # Check for placeholders
            if "pass" in content and "def " in content:
                func_match = re.search(
                    r"def\s+\w+\([^)]*\)[^:]*:\s*(.*?)(?=\ndef\s+|\Z)",
                    content,
                    re.DOTALL,
                )
                if func_match:
                    func_body = func_match.group(1).strip()
                    if func_body == "pass":
                        placeholder_count += 1

            # Check for return None only (but not if it's part of a larger function)
            if "return None" in content:
                # Count return statements
                return_count = len(re.findall(r"\breturn\b", content))
                if return_count == 1 and "def " in content:
                    # Check if it's the only return in a function
                    func_match = re.search(
                        r"def\s+\w+\([^)]*\)[^:]*:\s*(.*?)(?=\ndef\s+|\Z)",
                        content,
                        re.DOTALL,
                    )
                    if func_match:
                        func_body = func_match.group(1)
                        if (
                            func_body.count("return") == 1
                            and "return None" in func_body
                        ):
                            missing_impl_count += 1
        except Exception:
            continue

    return {
        "total_todos": todo_count,
        "todo_implement": todo_implement_count,
        "missing_impl": missing_impl_count,
        "placeholders": placeholder_count,
        "multiple_main": multiple_main_count,
    }


def main():
    """Report TODO status."""
    status = check_todo_status()

    print("=" * 70)
    print("TODO Status Report")
    print("=" * 70)
    print(f"\nTotal TODO items: {status['total_todos']}")
    print(f"Algorithms with TODO Implement: {status['todo_implement']}")
    print(
        f"Algorithms with missing implementation (return None only): {status['missing_impl']}"
    )
    print(f"Algorithms with placeholder (pass only): {status['placeholders']}")
    print(f"Algorithms with multiple main() functions: {status['multiple_main']}")
    print(
        f"\nTotal algorithms needing work: {status['todo_implement'] + status['missing_impl'] + status['placeholders'] + status['multiple_main']}"
    )


if __name__ == "__main__":
    main()
