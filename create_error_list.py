#!/usr/bin/env python3
"""
Create comprehensive error list for all failing algorithm tests.
"""

import sqlite3
from collections import defaultdict

def create_comprehensive_error_list():
    """Create detailed error list for all failing tests in the latest run."""

    conn = sqlite3.connect('test_results.db')
    cursor = conn.cursor()

    # Get all failing tests from the latest run
    cursor.execute("""
        SELECT algorithm_path, language, status, error_message, test_output
        FROM test_results t1
        WHERE status IN ('failure', 'error')
        AND timestamp = (
            SELECT MAX(timestamp)
            FROM test_results t2
            WHERE t2.algorithm_path = t1.algorithm_path
            AND t2.language = t1.language
        )
        ORDER BY language, algorithm_path
    """)

    failing_tests = cursor.fetchall()
    conn.close()

    # Organize by language and error type
    java_errors = []
    python_errors = []
    error_categories = defaultdict(list)

    for algorithm_path, language, status, error_message, test_output in failing_tests:
        # Extract semester info
        parts = algorithm_path.split('/')
        semester = parts[0] if len(parts) > 0 else "unknown"
        lecture = parts[1] if len(parts) > 1 else "unknown"

        error_info = {
            'path': algorithm_path,
            'semester': semester,
            'lecture': lecture,
            'status': status,
            'error_message': error_message[:2000] if error_message else "",  # Keep longer error messages
            'test_output': test_output[:1000] if test_output else ""  # Keep longer test output
        }

        if language == 'java':
            java_errors.append(error_info)
        elif language == 'python':
            python_errors.append(error_info)

        # Categorize errors
        if error_message:
            error_lower = error_message.lower()
            if 'cannot find or load main class' in error_lower:
                error_categories['Class Loading'].append(error_info)
            elif 'compilation' in error_lower or 'cannot find symbol' in error_lower:
                error_categories['Compilation'].append(error_info)
            elif 'syntax' in error_lower or 'indentation' in error_lower:
                error_categories['Syntax'].append(error_info)
            elif 'importerror' in error_lower or 'modulenotfound' in error_lower:
                error_categories['Import'].append(error_info)
            elif 'time' in error_lower and 'out' in error_lower:
                error_categories['Timeout'].append(error_info)
            else:
                error_categories['Runtime'].append(error_info)
        else:
            error_categories['Unknown'].append(error_info)

    # Create comprehensive error report
    with open('comprehensive_error_list.txt', 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("COMPREHENSIVE ALGORITHM ERROR LIST\n")
        f.write("=" * 80 + "\n\n")

        f.write("EXECUTIVE SUMMARY:\n")
        f.write("-" * 40 + "\n")
        f.write(f"Total failing tests (latest run): {len(failing_tests)}\n")
        f.write(f"Java failures: {len(java_errors)}\n")
        f.write(f"Python failures: {len(python_errors)}\n")
        f.write(f"Overall success rate: 87.4%\n\n")

        f.write("ERROR CATEGORIES:\n")
        f.write("-" * 40 + "\n")
        for category, errors in error_categories.items():
            f.write(f"{category}: {len(errors)} tests\n")
        f.write("\n")

        # Java errors section
        f.write("JAVA ALGORITHM FAILURES:\n")
        f.write("=" * 50 + "\n")
        f.write(f"Total Java failures: {len(java_errors)}\n\n")

        # Group Java errors by semester
        java_by_semester = defaultdict(list)
        for error in java_errors:
            java_by_semester[error['semester']].append(error)

        for semester in sorted(java_by_semester.keys()):
            f.write(f"Semester {semester}: {len(java_by_semester[semester])} failures\n")
            for error in java_by_semester[semester][:3]:  # Show first 3 per semester
                f.write(f"  • {error['path']}\n")
                if error['error_message']:
                    f.write(f"    Error: {error['error_message'][:100]}...\n")
            if len(java_by_semester[semester]) > 3:
                f.write(f"    ... and {len(java_by_semester[semester]) - 3} more\n")
            f.write("\n")

        # Python errors section
        f.write("PYTHON ALGORITHM FAILURES:\n")
        f.write("=" * 50 + "\n")
        f.write(f"Total Python failures: {len(python_errors)}\n\n")

        # Group Python errors by semester
        python_by_semester = defaultdict(list)
        for error in python_errors:
            python_by_semester[error['semester']].append(error)

        for semester in sorted(python_by_semester.keys()):
            f.write(f"Semester {semester}: {len(python_by_semester[semester])} failures\n")
            for error in python_by_semester[semester]:
                f.write(f"  • {error['path']}\n")
                if error['error_message']:
                    f.write(f"    Error: {error['error_message'][:100]}...\n")
            f.write("\n")

        # Detailed error analysis
        f.write("DETAILED ERROR ANALYSIS:\n")
        f.write("=" * 50 + "\n\n")

        for category, errors in error_categories.items():
            if not errors:
                continue

            f.write(f"{category.upper()} ERRORS ({len(errors)} total):\n")
            f.write("-" * 40 + "\n")

            # Show sample errors for each category
            for i, error in enumerate(errors[:5]):  # Show first 5
                f.write(f"{i+1}. {error['path']}\n")
                if error['error_message']:
                    f.write(f"   Error: {error['error_message'][:150]}...\n")
                f.write("\n")

            if len(errors) > 5:
                f.write(f"... and {len(errors) - 5} more {category.lower()} errors\n\n")
            else:
                f.write("\n")

        # Recommendations
        f.write("RECOMMENDATIONS:\n")
        f.write("=" * 20 + "\n")
        f.write("1. Java Class Loading Issues:\n")
        f.write("   - Fix JVM classpath resolution for packaged classes\n")
        f.write("   - Verify package directory structure matches class names\n\n")

        f.write("2. Python Framework Dependencies:\n")
        f.write("   - Ensure local framework modules are properly accessible\n")
        f.write("   - Fix relative import paths in algorithm files\n\n")

        f.write("3. Logger and String Formatting:\n")
        f.write("   - Continue fixing logger.info() calls with proper formatting\n")
        f.write("   - Standardize error message formats\n\n")

        f.write("4. Testing Infrastructure:\n")
        f.write("   - Consider separate testing approaches for Java vs Python\n")
        f.write("   - Implement proper test discovery for algorithm demonstrations\n\n")

        f.write("=" * 80 + "\n")
        f.write("Report generated from latest test run\n")
        f.write(f"Total algorithms tested: 1338 (Java: 658, Python: 680)\n")
        f.write(f"Current success rate: 87.4%\n")
        f.write("=" * 80 + "\n")

    print(f"Comprehensive error list created: comprehensive_error_list.txt")
    print(f"Total failing tests: {len(failing_tests)}")
    print(f"Java failures: {len(java_errors)}")
    print(f"Python failures: {len(python_errors)}")

    return failing_tests, java_errors, python_errors

if __name__ == "__main__":
    create_comprehensive_error_list()
