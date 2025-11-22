#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run only failing Java tests, update database, and save errors to file.
"""

import sqlite3
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple, Optional
import re
import time
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "test_results.db"
ERRORS_FILE = ROOT / "java_failing_tests_errors.txt"


def get_failing_java_tests() -> List[Tuple[str, str, str, str]]:
    """Get list of failing Java tests (algorithm_path, language, status, error_message)."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get latest status for each algorithm:language pair (Java only)
    cursor.execute("""
        WITH recent_results AS (
            SELECT 
                algorithm_path,
                language,
                status,
                error_message,
                ROW_NUMBER() OVER (
                    PARTITION BY algorithm_path, language 
                    ORDER BY timestamp DESC
                ) as rn
            FROM test_results
        )
        SELECT algorithm_path, language, status, error_message
        FROM recent_results
        WHERE rn = 1 
        AND language = 'java'
        AND status IN ('failure', 'error', 'timeout')
        ORDER BY algorithm_path
    """)
    
    failures = []
    for row in cursor.fetchall():
        algorithm_path, language, status, error_message = row
        failures.append((algorithm_path, language, status, error_message or ""))
    
    conn.close()
    return failures


def test_java_file(java_file: Path, timeout: int = 30) -> Tuple[bool, str, str]:
    """
    Test a single Java file: compile and run.
    """
    if timeout < 15:
        raise ValueError(f"Timeout {timeout}s is too aggressive. Minimum recommended: 15s")

    try:
        try:
            algorithm_path = str(java_file.parent.relative_to(ROOT))
        except ValueError:
            algorithm_path = str(java_file.parent)
        
        # Compile Java file
        compile_result = subprocess.run(
            ["javac", str(java_file)],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(java_file.parent)
        )
        
        if compile_result.returncode != 0:
            error_msg = compile_result.stderr or compile_result.stdout or ""
            return False, error_msg, compile_result.stdout or ""
        
        # Run Java file
        content = java_file.read_text(encoding='utf-8')
        # Check for active package declaration (not commented out)
        package_match = re.search(r'^package\s+([^;]+);', content, re.MULTILINE)
        # Also check for commented package to handle it as non-packaged
        commented_package_match = re.search(r'^//\s*package\s+([^;]+);', content, re.MULTILINE)
        
        if package_match and not commented_package_match:
            # Active package declaration
            package_name = package_match.group(1)
            class_name = f"{package_name}.Algorithm"
            classpath = "."
            class_file_path = java_file.parent / "Algorithm.class"
            if not class_file_path.exists():
                return False, f"Compiled class file not found: {class_file_path}", ""
        else:
            # No package or commented out package - treat as non-packaged class
            class_name = "Algorithm"
            classpath = str(java_file.parent)

        # Run Java class
        run_result = subprocess.run(
            ["java", "-cp", classpath, class_name],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(ROOT)
        )
        
        output = run_result.stdout or ""
        error_msg = run_result.stderr or ""
        success = run_result.returncode == 0
        
        return success, error_msg, output
        
    except subprocess.TimeoutExpired:
        return False, f"Test timed out after {timeout} seconds", ""
    except Exception as e:
        return False, f"Error running test: {e}", ""


def update_database(algorithm_path: str, language: str, status: str, 
                   duration: float, error_message: Optional[str], 
                   output: Optional[str]):
    """Update test results in database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Ensure table exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                algorithm_path TEXT NOT NULL,
                language TEXT NOT NULL,
                status TEXT NOT NULL,
                duration REAL,
                timestamp TEXT NOT NULL,
                error_message TEXT,
                test_output TEXT,
                previous_status TEXT,
                state_changed INTEGER DEFAULT 0,
                UNIQUE(algorithm_path, language, timestamp)
            )
        """)
        
        # Get previous status
        cursor.execute("""
            SELECT status FROM test_results
            WHERE algorithm_path = ? AND language = ?
            ORDER BY timestamp DESC
            LIMIT 1
        """, (algorithm_path, language))
        
        prev_row = cursor.fetchone()
        previous_status = prev_row[0] if prev_row else None
        state_changed = 1 if previous_status and previous_status != status else 0
        
        # Insert new result
        cursor.execute("""
            INSERT INTO test_results 
            (algorithm_path, language, status, duration, timestamp, 
             error_message, test_output, previous_status, state_changed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            algorithm_path, language, status, duration,
            datetime.now().isoformat(), error_message, output,
            previous_status, state_changed
        ))
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"  ⚠ Database update failed: {e}")


def main():
    """Main function to run failing Java tests."""
    print("=" * 70)
    print("RUNNING FAILING JAVA TESTS")
    print("=" * 70)
    print()
    
    failures = get_failing_java_tests()
    print(f"Found {len(failures)} failing Java tests")
    print()
    
    if len(failures) == 0:
        print("No failing Java tests found in database.")
        return
    
    # Open errors file for writing
    errors_content = []
    errors_content.append("=" * 70)
    errors_content.append(f"JAVA FAILING TESTS ERRORS - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    errors_content.append("=" * 70)
    errors_content.append("")
    
    java_count = 0
    fixed_count = 0
    still_failing_count = 0
    
    for idx, (algorithm_path, language, current_status, current_error) in enumerate(failures, 1):
        print(f"[{idx}/{len(failures)}] Testing: {algorithm_path} ({language})")
        
        java_file = ROOT / algorithm_path / "Algorithm.java"
        if not java_file.exists():
            print(f"  ✗ File not found: {java_file}")
            still_failing_count += 1
            errors_content.append(f"\n[{idx}/{len(failures)}] {algorithm_path}")
            errors_content.append(f"  ERROR: File not found: {java_file}")
            continue
        
        start_time = time.time()
        success, error_msg, output = test_java_file(java_file)
        duration = time.time() - start_time
        java_count += 1
        
        if not success:
            error_preview = error_msg[:500] if error_msg else "No error message"
            print(f"  [FAIL] {error_preview}...")
            status = 'failure'
            still_failing_count += 1
            
            # Add to errors file
            errors_content.append(f"\n[{idx}/{len(failures)}] {algorithm_path}")
            errors_content.append(f"  Status: {status}")
            errors_content.append(f"  Duration: {duration:.2f}s")
            errors_content.append(f"  Error Message:")
            errors_content.append(f"  {error_msg if error_msg else 'No error message'}")
            errors_content.append(f"  {'-' * 68}")
        else:
            print(f"  [PASS] Test passed!")
            status = 'success'
            if current_status in ('failure', 'error', 'timeout'):
                fixed_count += 1
        
        # Update database
        update_database(algorithm_path, language, status, duration, 
                       error_msg if not success else None, 
                       output if success else None)
        
        # Print summary every 10 tests
        if idx % 10 == 0:
            print(f"  Progress: {idx}/{len(failures)} | Fixed: {fixed_count} | Still failing: {still_failing_count}")
        print()
    
    # Write errors to file
    errors_content.append("\n" + "=" * 70)
    errors_content.append("Summary:")
    errors_content.append(f"  Total tests: {len(failures)}")
    errors_content.append(f"  Fixed: {fixed_count}")
    errors_content.append(f"  Still failing: {still_failing_count}")
    errors_content.append("=" * 70)
    
    ERRORS_FILE.write_text('\n'.join(errors_content), encoding='utf-8')
    print(f"Errors saved to: {ERRORS_FILE}")
    
    print("=" * 70)
    print(f"Summary:")
    print(f"  Java tests: {java_count}")
    print(f"  Fixed: {fixed_count}")
    print(f"  Still failing: {still_failing_count}")
    print(f"  Errors saved to: {ERRORS_FILE}")
    print("=" * 70)


if __name__ == "__main__":
    main()
