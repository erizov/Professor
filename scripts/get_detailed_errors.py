#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Get detailed error information for specific failures."""

import sqlite3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "test_results.db"

def get_detailed_error(algo_path: str):
    """Get detailed error for a specific algorithm."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        WITH recent AS (
            SELECT 
                algorithm_path,
                error_message,
                test_output,
                ROW_NUMBER() OVER (
                    PARTITION BY algorithm_path, language 
                    ORDER BY timestamp DESC
                ) as rn
            FROM test_results
            WHERE language = 'python' AND status IN ('failure', 'error')
        )
        SELECT error_message, test_output
        FROM recent
        WHERE rn = 1 AND algorithm_path = ?
    """, (algo_path,))
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return row[0], row[1]
    return None, None

# Get AssertionError failures
assertion_failures = [
    "semester_01\\lecture_03_specialized_sorting\\radix_sort",
    "semester_01\\lecture_04_searching\\interpolation_search",
    "semester_01\\lecture_04_searching\\jump_search",
]

print("=" * 80)
print("ASSERTION ERROR DETAILS")
print("=" * 80)

for algo_path in assertion_failures:
    error_msg, test_output = get_detailed_error(algo_path)
    print(f"\n{algo_path}")
    print("-" * 80)
    
    # Extract assertion error details
    text = (error_msg or "") + "\n" + (test_output or "")
    
    # Find assertion error
    if 'AssertionError' in text or 'assert' in text.lower():
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if 'AssertionError' in line or ('assert' in line.lower() and 'failed' in line.lower()):
                # Get context
                start = max(0, i - 3)
                end = min(len(lines), i + 10)
                print('\n'.join(lines[start:end]))
                break
    
    # Also look for "Lists differ" or "!=" patterns
    if 'Lists differ' in text or '!=' in text:
        match = re.search(r'Lists differ: (.+?) != (.+?)', text)
        if match:
            print(f"Expected: {match.group(2)}")
            print(f"Got: {match.group(1)}")
        match = re.search(r'(.+?) != (.+?) : (.+)', text)
        if match:
            print(f"Expected: {match.group(2)}")
            print(f"Got: {match.group(1)}")
            print(f"Message: {match.group(3)}")

# Get TypeError failures - focus on a few examples
type_error_examples = [
    "semester_01\\lecture_07_heaps_priority\\fibonacci_heap",
    "semester_01\\lecture_09_graph_algorithms\\bellman_ford",
    "semester_05\\lecture_27_hyperparameter_optimization\\random_search",
]

print("\n" + "=" * 80)
print("TYPE ERROR DETAILS (Examples)")
print("=" * 80)

for algo_path in type_error_examples:
    error_msg, test_output = get_detailed_error(algo_path)
    print(f"\n{algo_path}")
    print("-" * 80)
    
    text = (error_msg or "") + "\n" + (test_output or "")
    
    # Find TypeError
    if 'TypeError' in text:
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if 'TypeError' in line:
                # Get context
                start = max(0, i - 2)
                end = min(len(lines), i + 8)
                print('\n'.join(lines[start:end]))
                break

