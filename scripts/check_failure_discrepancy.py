#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check discrepancy in failure counts."""

import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "test_results.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Method 1: Get latest status for all Python tests, then count failures
print("Method 1: Get latest status for all tests, then count failures")
cursor.execute("""
    WITH recent AS (
        SELECT 
            algorithm_path,
            language,
            status,
            ROW_NUMBER() OVER (
                PARTITION BY algorithm_path, language 
                ORDER BY timestamp DESC
            ) as rn
        FROM test_results
        WHERE language = 'python'
    )
    SELECT COUNT(*) 
    FROM recent
    WHERE rn = 1 AND status IN ('failure', 'error')
""")
count1 = cursor.fetchone()[0]
print(f"  Count: {count1}")

# Method 2: Filter failures first, then get latest (like report script)
print("\nMethod 2: Filter failures first, then get latest (report script method)")
cursor.execute("""
    WITH recent AS (
        SELECT 
            algorithm_path,
            language,
            status,
            ROW_NUMBER() OVER (
                PARTITION BY algorithm_path, language 
                ORDER BY timestamp DESC
            ) as rn
        FROM test_results
        WHERE language = 'python' AND status IN ('failure', 'error')
    )
    SELECT COUNT(*) 
    FROM recent
    WHERE rn = 1
""")
count2 = cursor.fetchone()[0]
print(f"  Count: {count2}")

# Method 3: Count all failure/error records (not just latest)
print("\nMethod 3: Count all failure/error records (not just latest)")
cursor.execute("""
    SELECT COUNT(*) 
    FROM test_results
    WHERE language = 'python' AND status IN ('failure', 'error')
""")
count3 = cursor.fetchone()[0]
print(f"  Count: {count3}")

# Find algorithms that have both success and failure records
print("\nFinding algorithms with mixed statuses...")
cursor.execute("""
    WITH recent AS (
        SELECT 
            algorithm_path,
            language,
            status,
            ROW_NUMBER() OVER (
                PARTITION BY algorithm_path, language 
                ORDER BY timestamp DESC
            ) as rn
        FROM test_results
        WHERE language = 'python'
    ),
    latest_status AS (
        SELECT algorithm_path, status
        FROM recent
        WHERE rn = 1
    ),
    has_failures AS (
        SELECT DISTINCT algorithm_path
        FROM test_results
        WHERE language = 'python' AND status IN ('failure', 'error')
    )
    SELECT ls.algorithm_path, ls.status
    FROM latest_status ls
    INNER JOIN has_failures hf ON ls.algorithm_path = hf.algorithm_path
    WHERE ls.status NOT IN ('failure', 'error')
    ORDER BY ls.algorithm_path
    LIMIT 20
""")
mixed = cursor.fetchall()
print(f"  Found {len(mixed)} algorithms with latest status != failure/error but have failure records")
if mixed:
    print("  Examples:")
    for algo_path, status in mixed[:10]:
        print(f"    {algo_path}: latest={status}")

# Find algorithms that have failure records but latest is success
print("\nFinding algorithms where latest is success but have failure records...")
cursor.execute("""
    WITH recent AS (
        SELECT 
            algorithm_path,
            language,
            status,
            ROW_NUMBER() OVER (
                PARTITION BY algorithm_path, language 
                ORDER BY timestamp DESC
            ) as rn
        FROM test_results
        WHERE language = 'python'
    ),
    latest_status AS (
        SELECT algorithm_path, status
        FROM recent
        WHERE rn = 1
    ),
    has_failures AS (
        SELECT DISTINCT algorithm_path
        FROM test_results
        WHERE language = 'python' AND status IN ('failure', 'error')
    )
    SELECT COUNT(*)
    FROM latest_status ls
    INNER JOIN has_failures hf ON ls.algorithm_path = hf.algorithm_path
    WHERE ls.status = 'success'
""")
success_with_failures = cursor.fetchone()[0]
print(f"  Count: {success_with_failures}")

# Find algorithms that have failure records but latest is timeout
cursor.execute("""
    WITH recent AS (
        SELECT 
            algorithm_path,
            language,
            status,
            ROW_NUMBER() OVER (
                PARTITION BY algorithm_path, language 
                ORDER BY timestamp DESC
            ) as rn
        FROM test_results
        WHERE language = 'python'
    ),
    latest_status AS (
        SELECT algorithm_path, status
        FROM recent
        WHERE rn = 1
    ),
    has_failures AS (
        SELECT DISTINCT algorithm_path
        FROM test_results
        WHERE language = 'python' AND status IN ('failure', 'error')
    )
    SELECT COUNT(*)
    FROM latest_status ls
    INNER JOIN has_failures hf ON ls.algorithm_path = hf.algorithm_path
    WHERE ls.status = 'timeout'
""")
timeout_with_failures = cursor.fetchone()[0]
print(f"  Algorithms with latest=timeout but have failure records: {timeout_with_failures}")

print("\n" + "=" * 80)
print("DISCREPANCY ANALYSIS")
print("=" * 80)
print(f"Method 1 (all tests, then filter): {count1}")
print(f"Method 2 (filter first, then latest): {count2}")
print(f"Difference: {count2 - count1}")
print(f"\nAlgorithms with latest=success but have failure records: {success_with_failures}")
print(f"Algorithms with latest=timeout but have failure records: {timeout_with_failures}")
print(f"\nTotal algorithms that would be counted in Method 2 but not Method 1: {success_with_failures + timeout_with_failures}")

conn.close()

