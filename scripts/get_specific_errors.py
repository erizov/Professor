#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Get specific error types for focused fixing."""

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
        
        # Check for specific error type
        if error_type == "AttributeError":
            if 'attributeerror' in text.lower() or 'attribute error' in text.lower() or "'" in text and "has no attribute" in text.lower():
                failures.append((algo_path, error_msg, test_output))
        elif error_type == "AssertionError":
            if 'assertionerror' in text.lower() or 'assertion error' in text.lower() or 'assert' in text.lower() and 'failed' in text.lower():
                failures.append((algo_path, error_msg, test_output))
        elif error_type == "TypeError":
            if 'typeerror' in text.lower() or 'type error' in text.lower():
                failures.append((algo_path, error_msg, test_output))
        elif error_type == "Unknown":
            # Check if it doesn't match common patterns
            text_lower = text.lower()
            if not any(x in text_lower for x in ['import', 'typeerror', 'attributeerror', 'assertionerror', 'syntaxerror', 'nameerror']):
                failures.append((algo_path, error_msg, test_output))
    
    conn.close()
    return failures

def extract_error_detail(error_msg, test_output):
    """Extract the actual error detail."""
    text = (error_msg or "") + "\n" + (test_output or "")
    
    # Try to find the error line
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if 'Error:' in line or 'FAILED' in line or 'ERROR' in line:
            # Get next few lines for context
            return '\n'.join(lines[max(0, i-2):min(len(lines), i+5)])
    
    # Fallback: return first 500 chars
    return text[:500]

def main():
    """Print specific error types."""
    error_types = ["AttributeError", "AssertionError", "TypeError", "Unknown"]
    
    for error_type in error_types:
        failures = get_errors_by_type(error_type)
        print(f"\n{'='*80}")
        print(f"{error_type}: {len(failures)} failures")
        print('='*80)
        
        for algo_path, error_msg, test_output in failures:
            print(f"\n{algo_path}")
            detail = extract_error_detail(error_msg, test_output)
            print(f"  {detail[:300]}...")

if __name__ == "__main__":
    main()

