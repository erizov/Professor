#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Get detailed AssertionError information."""

import sqlite3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "test_results.db"

def get_assertion_errors():
    """Get all AssertionError failures with details."""
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
        if 'assertionerror' in text.lower() or ('assert' in text.lower() and 'failed' in text.lower()):
            failures.append((algo_path, error_msg, test_output))
    
    conn.close()
    return failures

def extract_assertion_details(text):
    """Extract assertion error details."""
    lines = text.split('\n')
    details = []
    
    for i, line in enumerate(lines):
        if 'AssertionError' in line or ('assert' in line.lower() and 'failed' in line.lower()):
            # Get context
            start = max(0, i - 2)
            end = min(len(lines), i + 8)
            details.append('\n'.join(lines[start:end]))
            
            # Look for "!=" or "Lists differ"
            if '!=' in line or 'Lists differ' in line:
                match = re.search(r'(.+?)\s*!=\s*(.+)', line)
                if match:
                    details.append(f"Expected: {match.group(2)}")
                    details.append(f"Got: {match.group(1)}")
    
    return '\n'.join(details[:500])

def main():
    """Print AssertionError details."""
    failures = get_assertion_errors()
    print(f"Found {len(failures)} AssertionError failures:\n")
    
    for algo_path, error_msg, test_output in failures:
        print(f"{'='*80}")
        print(f"{algo_path}")
        print('-'*80)
        text = (error_msg or "") + "\n" + (test_output or "")
        details = extract_assertion_details(text)
        print(details[:800])
        print()

if __name__ == "__main__":
    main()

