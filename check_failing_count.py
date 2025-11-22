#!/usr/bin/env python3
import sqlite3

try:
    conn = sqlite3.connect('test_results.db')
    cursor = conn.cursor()

    # Count failing tests
    cursor.execute("""
        SELECT COUNT(*) FROM test_results
        WHERE status IN ('failure', 'error', 'timeout')
    """)

    failing_count = cursor.fetchone()[0]

    # Get total tests
    cursor.execute("SELECT COUNT(*) FROM test_results")
    total_count = cursor.fetchone()[0]

    # Get breakdown by status
    cursor.execute("""
        SELECT status, COUNT(*) FROM test_results
        GROUP BY status
        ORDER BY COUNT(*) DESC
    """)

    status_breakdown = cursor.fetchall()

    conn.close()

    print("=== TEST RESULTS SUMMARY ===")
    print(f"Total tests in database: {total_count}")
    print(f"Still failing count: {failing_count}")
    print()
    print("Status breakdown:")
    for status, count in status_breakdown:
        print(f"  {status}: {count}")

except Exception as e:
    print(f"Error querying database: {e}")
