#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Get detailed error information from test database."""

import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "test_results.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Get one example error
cursor.execute("""
    SELECT algorithm_path, error_message, test_output
    FROM test_results
    WHERE algorithm_path = 'semester_01\\lecture_06_advanced_trees\\avl_tree'
    AND language = 'python'
    ORDER BY timestamp DESC
    LIMIT 1
""")

row = cursor.fetchone()
if row:
    algo_path, error_msg, test_output = row
    print(f"Algorithm: {algo_path}")
    print("\nError Message:")
    print(error_msg[:1000] if error_msg else "None")
    print("\nTest Output:")
    print(test_output[:2000] if test_output else "None")
else:
    print("No results found")

conn.close()

