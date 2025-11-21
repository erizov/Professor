#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check path format mismatch between test_results and algorithms DB."""

import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEST_DB = ROOT / "test_results.db"
ALGO_DB = ROOT / "database" / "algorithms.db"

print("=" * 80)
print("CHECKING PATH FORMAT MISMATCH")
print("=" * 80)
print()

# Get sample paths from test_results
test_conn = sqlite3.connect(TEST_DB)
test_cursor = test_conn.cursor()
test_cursor.execute("""
    SELECT DISTINCT algorithm_path 
    FROM test_results 
    WHERE language = 'java' 
    LIMIT 5
""")
test_paths = [row[0] for row in test_cursor.fetchall()]
test_conn.close()

print("Sample paths from test_results (Java):")
for path in test_paths:
    print(f"  {repr(path)}")
    print(f"    Has backslash: {'\\\\' in path}")
    print(f"    Has forward slash: {'/' in path}")
    normalized = path.replace('\\', '/')
    print(f"    Normalized: {repr(normalized)}")
    print()

# Get sample paths from algorithms DB
if ALGO_DB.exists():
    algo_conn = sqlite3.connect(ALGO_DB)
    algo_cursor = algo_conn.cursor()
    algo_cursor.execute("""
        SELECT DISTINCT folder_path 
        FROM algorithms 
        LIMIT 5
    """)
    algo_paths = [row[0] for row in algo_cursor.fetchall()]
    algo_conn.close()
    
    print("Sample paths from algorithms DB:")
    for path in algo_paths:
        print(f"  {repr(path)}")
        print(f"    Has backslash: {'\\\\' in path}")
        print(f"    Has forward slash: {'/' in path}")
        print()
    
    # Check if normalized test paths match algo paths
    print("Matching test:")
    test_normalized = {p.replace('\\', '/') for p in test_paths}
    algo_normalized = {p.replace('\\', '/') for p in algo_paths}
    
    matches = test_normalized.intersection(algo_normalized)
    print(f"  Matches: {len(matches)}/{len(test_normalized)}")
    if matches:
        print("  Sample matches:")
        for m in list(matches)[:3]:
            print(f"    {m}")
    else:
        print("  ⚠ No matches found!")
        print("  Sample test paths (normalized):")
        for p in list(test_normalized)[:3]:
            print(f"    {p}")
        print("  Sample algo paths (normalized):")
        for p in list(algo_normalized)[:3]:
            print(f"    {p}")
else:
    print("⚠ algorithms.db not found!")

