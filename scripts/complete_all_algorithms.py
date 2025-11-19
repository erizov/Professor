#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete All Algorithms: Implementation and Framework Examples
Process all algorithms systematically, commit every 50 completions
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

# Import functions from previous phase scripts
sys.path.insert(0, str(ROOT / "scripts"))
from phase5_implement_algorithm_logic import (
    determine_category,
    generate_implementation,
    replace_todo_implementation,
)
from phase8_comprehensive_framework_examples import (
    get_framework_examples,
    add_framework_examples_to_readme,
)


def find_algorithms_needing_work() -> (
    Tuple[List[Tuple[Path, str, str]], List[Tuple[Path, str, str]]]
):
    """Find algorithms needing implementations and framework examples."""
    need_implementation = []
    need_framework_examples = []

    for algo_file in ROOT.rglob("**/algorithm.py"):
        if "supporting_documents" in str(algo_file) or "scripts" in str(algo_file):
            continue

        try:
            content = algo_file.read_text(encoding="utf-8")
            algorithm_name = algo_file.parent.name
            lecture_path = algo_file.parent.parent
            lecture_name = lecture_path.name if lecture_path else ""

            # Check if needs implementation
            if "TODO" in content and "Implement" in content:
                category = determine_category(algorithm_name, lecture_name, content)
                need_implementation.append((algo_file, algorithm_name, category))

            # Check if needs framework examples
            readme_path = algo_file.parent / "README.md"
            if readme_path.exists():
                readme_content = readme_path.read_text(encoding="utf-8")

                # Check if has Examples section but might need more
                has_examples = (
                    "## Examples of Implementation" in readme_content
                    or "## Examples of Deployment" in readme_content
                    or "## Examples" in readme_content
                )

                if has_examples:
                    # Check framework count
                    framework_count = sum(
                        1
                        for fw in [
                            "Kubernetes",
                            "Docker",
                            "Terraform",
                            "Prometheus",
                            "Istio",
                            "Kafka",
                            "Redis",
                            "PostgreSQL",
                            "PyTorch",
                            "Hugging Face",
                            "LangChain",
                            "OpenTelemetry",
                            "AWS",
                            "Spring Framework",
                            ".NET Framework",
                            "Java",
                        ]
                        if fw in readme_content
                    )

                    if framework_count < 2:
                        need_framework_examples.append(
                            (readme_path, algorithm_name, lecture_name)
                        )
        except Exception:
            continue

    return need_implementation, need_framework_examples


def commit_changes(message: str) -> bool:
    """Commit changes to git."""
    try:
        subprocess.run(["git", "add", "-A"], cwd=ROOT, check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", message], cwd=ROOT, check=True, capture_output=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Git commit failed: {e}")
        return False


def main():
    """Complete all algorithms systematically."""
    print("=" * 70)
    print("Complete All Algorithms: Implementation and Framework Examples")
    print("=" * 70)

    # Find algorithms needing work
    print("\nScanning for algorithms needing work...")
    need_impl, need_frameworks = find_algorithms_needing_work()

    print(f"\nFound:")
    print(f"  - Algorithms needing implementation: {len(need_impl)}")
    print(f"  - Algorithms needing framework examples: {len(need_frameworks)}")
    print(f"  - Total: {len(need_impl) + len(need_frameworks)}")

    total_completed = 0
    impl_completed = 0
    framework_completed = 0

    # Process implementations
    print(f"\n{'='*70}")
    print("Phase 1: Implementing Algorithms")
    print(f"{'='*70}")

    for i, (algo_file, algo_name, category) in enumerate(need_impl, 1):
        if replace_todo_implementation(algo_file, algo_name, category):
            impl_completed += 1
            total_completed += 1

            if total_completed % 50 == 0:
                print(f"\n[PROGRESS] Completed {total_completed} algorithms...")
                commit_changes(
                    f"Complete algorithms: {total_completed} algorithms implemented and enhanced"
                )
                print(f"[COMMITTED] Changes committed at {total_completed} completions")

    if impl_completed > 0 and total_completed % 50 != 0:
        commit_changes(f"Complete algorithms: {impl_completed} implementations added")
        print(f"[COMMITTED] Final implementation commit: {impl_completed} files")

    print(f"\n[COMPLETE] Implementations: {impl_completed} files")

    # Process framework examples
    print(f"\n{'='*70}")
    print("Phase 2: Adding Framework Examples")
    print(f"{'='*70}")

    for i, (readme_path, algo_name, lecture_name) in enumerate(need_frameworks, 1):
        if add_framework_examples_to_readme(readme_path, algo_name, lecture_name):
            framework_completed += 1
            total_completed += 1

            if total_completed % 50 == 0:
                print(f"\n[PROGRESS] Completed {total_completed} algorithms...")
                commit_changes(
                    f"Complete algorithms: {total_completed} algorithms implemented and enhanced"
                )
                print(f"[COMMITTED] Changes committed at {total_completed} completions")

    if framework_completed > 0 and total_completed % 50 != 0:
        commit_changes(
            f"Complete algorithms: {framework_completed} framework examples added"
        )
        print(
            f"[COMMITTED] Final framework examples commit: {framework_completed} files"
        )

    print(f"\n[COMPLETE] Framework Examples: {framework_completed} files")

    # Final summary
    print(f"\n{'='*70}")
    print("FINAL SUMMARY")
    print(f"{'='*70}")
    print(f"Total algorithms completed: {total_completed}")
    print(f"  - Implementations: {impl_completed}")
    print(f"  - Framework examples: {framework_completed}")

    # Update comprehensive textbook
    print(f"\n{'='*70}")
    print("Updating Comprehensive Textbook...")
    print(f"{'='*70}")
    try:
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "generate_comprehensive_pdf.py")],
            cwd=ROOT,
            check=True,
        )
        print("[COMPLETE] Comprehensive textbook updated")
    except Exception as e:
        print(f"[ERROR] Failed to update textbook: {e}")

    # Final commit
    if total_completed > 0:
        commit_changes(
            f"Complete all algorithms: Final commit - {total_completed} total completions ({impl_completed} implementations, {framework_completed} framework examples)"
        )
        print(f"\n[COMMITTED] Final commit with all changes")

    print(f"\n{'='*70}")
    print("ALL ALGORITHMS COMPLETION FINISHED")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
