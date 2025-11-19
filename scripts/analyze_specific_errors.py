#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Analyze specific error types: TypeError, AssertionError, AttributeError."""

import sqlite3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "test_results.db"

def get_errors_by_type(error_type: str):
    """Get failures of a specific error type."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        WITH recent AS (
            SELECT 
                algorithm_path,
                language,
                status,
                error_message,
                test_output,
                ROW_NUMBER() OVER (
                    PARTITION BY algorithm_path, language 
                    ORDER BY timestamp DESC
                ) as rn
            FROM test_results
            WHERE language = 'python'
        )
        SELECT algorithm_path, error_message, test_output
        FROM recent
        WHERE rn = 1 AND status IN ('failure', 'error')
        ORDER BY algorithm_path
    """)
    
    failures = []
    for algo_path, error_msg, test_output in cursor.fetchall():
        text = (error_msg or "") + "\n" + (test_output or "")
        
        if error_type == "TypeError" and 'typeerror' in text.lower():
            failures.append((algo_path, error_msg, test_output))
        elif error_type == "AssertionError" and 'assertionerror' in text.lower():
            failures.append((algo_path, error_msg, test_output))
        elif error_type == "AttributeError" and 'attributeerror' in text.lower():
            failures.append((algo_path, error_msg, test_output))
    
    conn.close()
    return failures

def extract_error_detail(error_msg, test_output):
    """Extract specific error detail."""
    text = (error_msg or "") + "\n" + (test_output or "")
    
    # Find the actual error line
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if 'TypeError:' in line or 'AssertionError:' in line or 'AttributeError:' in line:
            # Get next few lines for context
            return '\n'.join(lines[max(0, i-2):min(len(lines), i+5)])
    
    return text[:500]

print("=" * 80)
print("TYPEERROR ANALYSIS")
print("=" * 80)
type_errors = get_errors_by_type("TypeError")
print(f"Total: {len(type_errors)}")
for algo_path, error_msg, test_output in type_errors[:10]:
    print(f"\n{algo_path}")
    detail = extract_error_detail(error_msg, test_output)
    print(f"  {detail[:300]}")

print("\n" + "=" * 80)
print("ASSERTIONERROR ANALYSIS")
print("=" * 80)
assertion_errors = get_errors_by_type("AssertionError")
print(f"Total: {len(assertion_errors)}")
for algo_path, error_msg, test_output in assertion_errors:
    print(f"\n{algo_path}")
    detail = extract_error_detail(error_msg, test_output)
    print(f"  {detail[:300]}")

print("\n" + "=" * 80)
print("ATTRIBUTEERROR ANALYSIS")
print("=" * 80)
attribute_errors = get_errors_by_type("AttributeError")
print(f"Total: {len(attribute_errors)}")
for algo_path, error_msg, test_output in attribute_errors:
    print(f"\n{algo_path}")
    detail = extract_error_detail(error_msg, test_output)
    print(f"  {detail[:300]}")

