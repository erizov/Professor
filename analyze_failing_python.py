#!/usr/bin/env python3
"""
Analyze the specific failing Python algorithm files to identify patterns.
"""

import sqlite3
from collections import Counter

def analyze_failing_python():
    """Analyze the failing Python files to identify common patterns."""

    conn = sqlite3.connect('test_results.db')
    cursor = conn.cursor()

    # Get the failing Python files with their error messages
    cursor.execute("""
        SELECT algorithm_path, status, error_message, test_output
        FROM test_results t1
        WHERE algorithm_path LIKE 'semester_%'
        AND language = 'python'
        AND status IN ('failure', 'error')
        AND timestamp = (
            SELECT MAX(timestamp)
            FROM test_results t2
            WHERE t2.algorithm_path = t1.algorithm_path
            AND t2.language = t1.language
        )
        ORDER BY algorithm_path
    """)

    failing_tests = cursor.fetchall()
    conn.close()

    print("=== ANALYSIS OF FAILING PYTHON FILES ===\n")

    # Analyze error patterns
    error_patterns = []
    syntax_errors = []
    runtime_errors = []
    import_errors = []

    for algorithm_path, status, error_message, test_output in failing_tests:
        # Extract semester and lecture info
        parts = algorithm_path.split('/')
        semester = parts[0] if parts else "unknown"
        lecture = parts[1] if len(parts) > 1 else "unknown"

        # Categorize errors
        if error_message:
            error_lower = error_message.lower()

            # Syntax errors
            if any(keyword in error_lower for keyword in ['syntaxerror', 'indentationerror', 'syntax error']):
                syntax_errors.append((algorithm_path, error_message[:200]))
                error_patterns.append('Syntax/Indentation Error')
            # Import errors
            elif any(keyword in error_lower for keyword in ['importerror', 'modulenotfounderror', 'import error']):
                import_errors.append((algorithm_path, error_message[:200]))
                error_patterns.append('Import Error')
            # Runtime errors
            elif any(keyword in error_lower for keyword in ['runtimeerror', 'valueerror', 'typeerror', 'attributeerror']):
                runtime_errors.append((algorithm_path, error_message[:200]))
                error_patterns.append('Runtime Error')
            else:
                error_patterns.append('Other Error')

    # Print summary
    print(f"Total failing Python tests: {len(failing_tests)}")
    print(f"Syntax errors: {len(syntax_errors)}")
    print(f"Import errors: {len(import_errors)}")
    print(f"Runtime errors: {len(runtime_errors)}")
    print()

    # Error pattern analysis
    pattern_counts = Counter(error_patterns)
    print("ERROR PATTERN ANALYSIS:")
    print("-" * 40)
    for pattern, count in pattern_counts.most_common():
        percentage = (count / len(failing_tests)) * 100 if failing_tests else 0
        print(".1f")
    print()

    # Semester distribution
    semester_counts = Counter()
    for algorithm_path, _, _, _ in failing_tests:
        parts = algorithm_path.split('/')
        semester = parts[0] if parts else "unknown"
        semester_counts[semester] += 1

    print("FAILING TESTS BY SEMESTER:")
    print("-" * 40)
    for semester, count in sorted(semester_counts.items()):
        percentage = (count / len(failing_tests)) * 100 if failing_tests else 0
        print(".1f")
    print()

    # Show sample errors
    print("SAMPLE SYNTAX ERRORS:")
    print("-" * 40)
    for i, (path, error) in enumerate(syntax_errors[:3]):
        print(f"{i+1}. {path}")
        print(f"   Error: {error}...")
        print()

    print("SAMPLE IMPORT ERRORS:")
    print("-" * 40)
    for i, (path, error) in enumerate(import_errors[:3]):
        print(f"{i+1}. {path}")
        print(f"   Error: {error}...")
        print()

    print("SAMPLE RUNTIME ERRORS:")
    print("-" * 40)
    for i, (path, error) in enumerate(runtime_errors[:3]):
        print(f"{i+1}. {path}")
        print(f"   Error: {error}...")
        print()

    return failing_tests, syntax_errors, import_errors, runtime_errors

def get_failing_python_list():
    """Get just the list of failing Python file paths."""
    conn = sqlite3.connect('test_results.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT algorithm_path
        FROM test_results t1
        WHERE algorithm_path LIKE 'semester_%'
        AND language = 'python'
        AND status IN ('failure', 'error')
        AND timestamp = (
            SELECT MAX(timestamp)
            FROM test_results t2
            WHERE t2.algorithm_path = t1.algorithm_path
            AND t2.language = t1.language
        )
        ORDER BY algorithm_path
    """)

    failing_paths = [row[0] for row in cursor.fetchall()]
    conn.close()

    return failing_paths

if __name__ == "__main__":
    analyze_failing_python()
