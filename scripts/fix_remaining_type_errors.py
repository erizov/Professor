#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix remaining TypeError failures."""

import sqlite3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "test_results.db"

def get_type_error_failures():
    """Get all TypeError failures."""
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
        if 'typeerror' in text.lower() or 'type error' in text.lower():
            failures.append((algo_path, error_msg, test_output))
    
    conn.close()
    return failures

def main():
    """Print all TypeError failures."""
    failures = get_type_error_failures()
    print(f"Found {len(failures)} TypeError failures:\n")
    
    for algo_path, error_msg, test_output in failures:
        print(f"{algo_path}")
        text = (error_msg or "") + "\n" + (test_output or "")
        # Extract TypeError message
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if 'TypeError' in line:
                print(f"  {line}")
                # Show next few lines for context
                for j in range(i+1, min(i+3, len(lines))):
                    if lines[j].strip():
                        print(f"  {lines[j]}")
                break
        print()

if __name__ == "__main__":
    main()

