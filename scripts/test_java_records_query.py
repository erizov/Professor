#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test query for Java records in test_results."""

import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "test_results.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("=" * 80)
print("TESTING JAVA RECORDS QUERY")
print("=" * 80)
print()

# Test the exact query from test_reports.py
query = """
    WITH recent_results AS (
        SELECT 
            algorithm_path,
            language,
            status,
            duration,
            timestamp,
            error_message,
            previous_status,
            state_changed,
            ROW_NUMBER() OVER (
                PARTITION BY algorithm_path, language 
                ORDER BY timestamp DESC
            ) as rn
        FROM test_results
        WHERE 1=1
    )
    SELECT 
        algorithm_path,
        language,
        status,
        duration,
        timestamp,
        error_message,
        previous_status,
        state_changed
    FROM recent_results
    WHERE rn = 1
    ORDER BY timestamp DESC
    LIMIT 10
"""

print("Query without language filter:")
try:
    cursor.execute(query)
    rows = cursor.fetchall()
    print(f"Total rows: {len(rows)}")
    print()
    
    java_count = 0
    python_count = 0
    
    for row in rows:
        lang = row[1]
        if lang.lower() == 'java':
            java_count += 1
            print(f"Java: {row[0]} | {row[2]} | {row[4]}")
        elif lang.lower() == 'python':
            python_count += 1
    
    print()
    print(f"Java records in result: {java_count}")
    print(f"Python records in result: {python_count}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

print()
print("-" * 80)
print()

# Test with language filter
query_with_filter = """
    WITH recent_results AS (
        SELECT 
            algorithm_path,
            language,
            status,
            duration,
            timestamp,
            error_message,
            previous_status,
            state_changed,
            ROW_NUMBER() OVER (
                PARTITION BY algorithm_path, language 
                ORDER BY timestamp DESC
            ) as rn
        FROM test_results
        WHERE 1=1
        AND LOWER(language) = LOWER(?)
    )
    SELECT 
        algorithm_path,
        language,
        status,
        duration,
        timestamp,
        error_message,
        previous_status,
        state_changed
    FROM recent_results
    WHERE rn = 1
    ORDER BY timestamp DESC
    LIMIT 10
"""

print("Query with language filter (java):")
try:
    cursor.execute(query_with_filter, ('java',))
    rows = cursor.fetchall()
    print(f"Total rows: {len(rows)}")
    print()
    
    for i, row in enumerate(rows[:5], 1):
        print(f"{i}. Path: {row[0]}")
        print(f"   Language: {row[1]}")
        print(f"   Status: {row[2]}")
        print(f"   Timestamp: {row[4]}")
        print()
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

print()
print("-" * 80)
print()

# Check raw data
print("Raw data check:")
cursor.execute("SELECT COUNT(*) FROM test_results WHERE LOWER(language) = LOWER('java')")
java_total = cursor.fetchone()[0]
print(f"Total Java records in DB: {java_total}")

cursor.execute("SELECT COUNT(*) FROM test_results WHERE LOWER(language) = LOWER('python')")
python_total = cursor.fetchone()[0]
print(f"Total Python records in DB: {python_total}")

# Check for case sensitivity issues
cursor.execute("SELECT DISTINCT language FROM test_results")
languages = [r[0] for r in cursor.fetchall()]
print(f"Distinct languages in DB: {languages}")

conn.close()

