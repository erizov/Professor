#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Command-line interface for Java algorithm execution framework.

Usage:
    python scripts/java_runner.py --list
    python scripts/java_runner.py --semester semester_01 --lecture lecture_01 --algorithm bubble_sort
    python scripts/java_runner.py --path "semester_01/lecture_01_sorting_fundamentals/bubble_sort/Algorithm.java"
"""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from framework.java_executor import get_executor


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Execute Java algorithms from command line'
    )
    
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all available algorithms'
    )
    
    parser.add_argument(
        '--semester',
        type=str,
        help='Semester (e.g., semester_01)'
    )
    
    parser.add_argument(
        '--lecture',
        type=str,
        help='Lecture (e.g., lecture_01_sorting_fundamentals)'
    )
    
    parser.add_argument(
        '--algorithm',
        type=str,
        help='Algorithm name (e.g., bubble_sort)'
    )
    
    parser.add_argument(
        '--path',
        type=str,
        help='Full path to Algorithm.java file'
    )
    
    parser.add_argument(
        '--timeout',
        type=int,
        default=60,
        help='Execution timeout in seconds (default: 60)'
    )
    
    args = parser.parse_args()
    
    executor = get_executor()
    
    if args.list:
        # List all algorithms
        algorithms = executor.list_algorithms()
        print(f"\nFound {len(algorithms)} algorithms:\n")
        print(f"{'Semester':<20} {'Lecture':<40} {'Algorithm':<30} {'Path'}")
        print("=" * 120)
        for algo in algorithms:
            print(f"{algo['semester']:<20} {algo['lecture']:<40} {algo['algorithm']:<30} {algo['path']}")
        return 0
    
    # Find algorithm
    algo_info = executor.find_algorithm(
        path=args.path,
        semester=args.semester,
        lecture=args.lecture,
        algorithm=args.algorithm
    )
    
    if not algo_info:
        print("Error: Algorithm not found")
        print("\nUse --list to see all available algorithms")
        return 1
    
    print(f"Executing: {algo_info.name}")
    print(f"Path: {algo_info.full_path}")
    if algo_info.package:
        print(f"Package: {algo_info.package}")
    print(f"Class: {algo_info.class_name}")
    print("-" * 80)
    
    # Execute
    success, stdout, stderr, execution_time = executor.execute_algorithm(
        algo_info,
        timeout=args.timeout
    )
    
    if success:
        print("\n✓ Execution successful!")
        if stdout:
            print("\nOutput:")
            print(stdout)
        if stderr:
            print("\nWarnings/Errors:")
            print(stderr)
    else:
        print("\n✗ Execution failed!")
        if stderr:
            print("\nError:")
            print(stderr)
        if stdout:
            print("\nOutput:")
            print(stdout)
    
    print(f"\nExecution time: {execution_time:.3f}s")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())

