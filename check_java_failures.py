#!/usr/bin/env python3
import sqlite3

try:
    conn = sqlite3.connect('test_results.db')
    cursor = conn.cursor()

    # Count Java-specific failures
    cursor.execute("""
        SELECT COUNT(*) FROM test_results
        WHERE status IN ('failure', 'error')
        AND algorithm_path LIKE 'semester_%'
        AND language = 'java'
    """)

    java_failures = cursor.fetchone()[0]

    # Count total Java tests
    cursor.execute("""
        SELECT COUNT(*) FROM test_results
        WHERE algorithm_path LIKE 'semester_%'
        AND language = 'java'
    """)

    total_java = cursor.fetchone()[0]

    # Get Java success rate
    cursor.execute("""
        SELECT status, COUNT(*) FROM test_results
        WHERE algorithm_path LIKE 'semester_%'
        AND language = 'java'
        GROUP BY status
    """)

    java_breakdown = cursor.fetchall()

    conn.close()

    print('=== JAVA ALGORITHM FILES STATUS ===')
    print(f'Total Java algorithm tests: {total_java}')
    print(f'Failing Java tests: {java_failures}')
    if total_java > 0:
        success_rate = ((total_java - java_failures) / total_java) * 100
        print('.1f')
    print()
    print('Java status breakdown:')
    for status, count in java_breakdown:
        print(f'  {status}: {count}')

except Exception as e:
    print(f"Error: {e}")
