#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check Java records in test_results database."""

import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "test_results.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("=" * 80)
print("CHECKING JAVA RECORDS IN DATABASE")
print("=" * 80)
print()

# Check languages
cursor.execute("SELECT DISTINCT language FROM test_results")
languages = [r[0] for r in cursor.fetchall()]
print(f"Languages in DB: {languages}")
print()

# Count records by language
cursor.execute("SELECT language, COUNT(*) FROM test_results GROUP BY language")
print("Record counts by language:")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]}")
print()

# Check Java records
cursor.execute("SELECT COUNT(*) FROM test_results WHERE language = 'java'")
java_count = cursor.fetchone()[0]
print(f"Total Java records: {java_count}")
print()

if java_count > 0:
    # Sample Java records
    cursor.execute("""
        SELECT algorithm_path, language, status, timestamp 
        FROM test_results 
        WHERE language = 'java' 
        ORDER BY timestamp DESC 
        LIMIT 10
    """)
    print("Sample Java records (latest 10):")
    for row in cursor.fetchall():
        print(f"  Path: {row[0]}")
        print(f"    Language: {row[1]}")
        print(f"    Status: {row[2]}")
        print(f"    Timestamp: {row[3]}")
        print()
    
    # Check for path format issues
    cursor.execute("""
        SELECT DISTINCT algorithm_path 
        FROM test_results 
        WHERE language = 'java' 
        LIMIT 5
    """)
    print("Sample algorithm_path values:")
    for row in cursor.fetchall():
        print(f"  '{row[0]}'")
        print(f"    Contains backslash: {'\\\\' in row[0]}")
        print(f"    Contains forward slash: {'/' in row[0]}")
        print()
else:
    print("⚠ No Java records found in database!")
    print()

conn.close()

