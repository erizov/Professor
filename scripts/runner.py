#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Algorithm Runner - Execute algorithms from any semester/lecture.

This script provides a unified interface to run Python and Java
algorithm implementations across all semesters.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Optional, Dict, Any


def load_metadata(algorithm_path: Path) -> Optional[Dict[str, Any]]:
    """
    Load algorithm metadata from JSON file.

    Args:
        algorithm_path: Path to algorithm directory

    Returns:
        Dictionary with metadata or None if not found
    """
    metadata_file = algorithm_path / "metadata.json"
    if metadata_file.exists():
        with open(metadata_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def run_python(algorithm_path: Path) -> int:
    """
    Execute Python implementation.

    Args:
        algorithm_path: Path to algorithm directory

    Returns:
        Exit code
    """
    python_file = algorithm_path / "algorithm.py"
    if not python_file.exists():
        print(f"Error: {python_file} not found", file=sys.stderr)
        return 1

    try:
        result = subprocess.run(
            [sys.executable, str(python_file)], cwd=algorithm_path, check=False
        )
        return result.returncode
    except Exception as e:
        print(f"Error running Python: {e}", file=sys.stderr)
        return 1


def run_java(algorithm_path: Path) -> int:
    """
    Execute Java implementation.

    Args:
        algorithm_path: Path to algorithm directory

    Returns:
        Exit code
    """
    java_file = algorithm_path / "Algorithm.java"
    if not java_file.exists():
        print(f"Error: {java_file} not found", file=sys.stderr)
        return 1

    try:
        # Compile
        compile_result = subprocess.run(
            ["javac", str(java_file)],
            cwd=algorithm_path,
            capture_output=True,
            text=True,
        )
        if compile_result.returncode != 0:
            print("Compilation error:", compile_result.stderr)
            return 1

        # Run
        run_result = subprocess.run(
            ["java", "Algorithm"], cwd=algorithm_path, check=False
        )
        return run_result.returncode

    except Exception as e:
        print(f"Error running Java: {e}", file=sys.stderr)
        return 1


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Run algorithm implementations")
    parser.add_argument(
        "--semester", type=int, required=True, help="Semester number (1-4)"
    )
    parser.add_argument(
        "--lecture", required=True, help="Lecture number (e.g., '01', '02')"
    )
    parser.add_argument(
        "--algorithm", required=True, help="Algorithm name (e.g., 'bubble_sort')"
    )
    parser.add_argument(
        "--lang",
        choices=["python", "java"],
        default="python",
        help="Programming language (default: python)",
    )

    args = parser.parse_args()

    # Build path
    algorithm_path = Path(
        f"semester_{args.semester}/" f"lecture_{args.lecture}/" f"{args.algorithm}"
    )

    if not algorithm_path.exists():
        print(f"Error: Algorithm path {algorithm_path} not found", file=sys.stderr)
        return 1

    # Load and display metadata
    metadata = load_metadata(algorithm_path)
    if metadata:
        print("=" * 70)
        print(f"Algorithm: {metadata.get('name', 'Unknown')}")
        print(f"Category: {metadata.get('category', 'Unknown')}")
        print(f"Complexity: {metadata.get('complexity', {})}")
        print("=" * 70)
        print()

    # Run algorithm
    if args.lang == "python":
        return run_python(algorithm_path)
    else:
        return run_java(algorithm_path)


if __name__ == "__main__":
    sys.exit(main())
