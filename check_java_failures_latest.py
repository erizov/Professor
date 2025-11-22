#!/usr/bin/env python3
import sqlite3

try:
    conn = sqlite3.connect('test_results.db')
    cursor = conn.cursor()

    # Count Java-specific failures from latest run only (most recent timestamp per algorithm)
    cursor.execute("""
        SELECT COUNT(*) FROM (
            SELECT algorithm_path, status
            FROM test_results t1
            WHERE algorithm_path LIKE 'semester_%'
            AND language = 'java'
            AND timestamp = (
                SELECT MAX(timestamp)
                FROM test_results t2
                WHERE t2.algorithm_path = t1.algorithm_path
                AND t2.language = t1.language
            )
        ) WHERE status IN ('failure', 'error')
    """)

    java_failures = cursor.fetchone()[0]

    # Count total Java tests (latest run only)
    cursor.execute("""
        SELECT COUNT(*) FROM (
            SELECT algorithm_path, status
            FROM test_results t1
            WHERE algorithm_path LIKE 'semester_%'
            AND language = 'java'
            AND timestamp = (
                SELECT MAX(timestamp)
                FROM test_results t2
                WHERE t2.algorithm_path = t1.algorithm_path
                AND t2.language = t1.language
            )
        )
    """)

    total_java = cursor.fetchone()[0]

    # Get Java success rate breakdown (latest run only)
    cursor.execute("""
        SELECT status, COUNT(*) FROM (
            SELECT algorithm_path, status
            FROM test_results t1
            WHERE algorithm_path LIKE 'semester_%'
            AND language = 'java'
            AND timestamp = (
                SELECT MAX(timestamp)
                FROM test_results t2
                WHERE t2.algorithm_path = t1.algorithm_path
                AND t2.language = t1.language
            )
        ) GROUP BY status
    """)

    java_breakdown = cursor.fetchall()

    # Get total unique Java algorithm files
    cursor.execute("""
        SELECT COUNT(DISTINCT algorithm_path) FROM test_results
        WHERE algorithm_path LIKE 'semester_%'
        AND language = 'java'
    """)

    unique_java_files = cursor.fetchone()[0]

    conn.close()

    print('=== JAVA ALGORITHM FILES STATUS (LATEST RUN ONLY) ===')
    print(f'Unique Java algorithm files: {unique_java_files}')
    print(f'Total Java tests (latest run): {total_java}')
    print(f'Failing Java tests (latest run): {java_failures}')
    if total_java > 0:
        success_rate = ((total_java - java_failures) / total_java) * 100
        print('.1f')
    print()
    print('Java status breakdown (latest run):')
    for status, count in java_breakdown:
        print(f'  {status}: {count}')

except Exception as e:
    print(f"Error: {e}")
