#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run only failing Python tests, update database, and save errors to file.
"""

import sqlite3
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple, Optional
import time
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "test_results.db"
ERRORS_FILE = ROOT / "python_failing_tests_errors.txt"


def get_failing_python_tests() -> List[Tuple[str, str, str, str]]:
    """Get list of failing Python tests."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
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
        AND language = 'python'
        AND status IN ('failure', 'error', 'timeout')
        ORDER BY algorithm_path
    """)
    
    failures = []
    for row in cursor.fetchall():
        algorithm_path, language, status, error_message = row
        failures.append((algorithm_path, language, status, error_message or ""))
    
    conn.close()
    return failures


def test_python_file(python_file: Path, timeout: int = 30) -> Tuple[bool, str, str]:
    """Test a single Python file."""
    try:
        result = subprocess.run(
            [sys.executable, str(python_file)],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(ROOT)
        )

        success = result.returncode == 0
        output = result.stdout or ""
        error_msg = result.stderr or ""

        if not success:
            error_msg = f"{error_msg}\n{output}" if error_msg else output

        return success, error_msg, output

    except subprocess.TimeoutExpired:
        return False, f"Test timed out after {timeout} seconds", ""
    except Exception as e:
        return False, f"Error running test: {e}", ""


def update_database(algorithm_path: str, language: str, status: str, 
                   duration: float, error_message: Optional[str], 
                   output: Optional[str]):
    """Update test_results database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT status FROM test_results
            WHERE algorithm_path = ? AND language = ?
            ORDER BY timestamp DESC
            LIMIT 1
        """, (algorithm_path, language))
        
        previous_result = cursor.fetchone()
        previous_status = previous_result[0] if previous_result else None
        
        state_changed = False
        if previous_status and previous_status != status:
            state_changed = True
        
        timestamp = datetime.now().isoformat()
        cursor.execute("""
            INSERT INTO test_results 
            (algorithm_path, language, status, duration, timestamp, error_message, 
             test_output, previous_status, state_changed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            algorithm_path,
            language,
            status,
            duration,
            timestamp,
            error_message,
            output,
            previous_status,
            1 if state_changed else 0,
        ))
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"  [WARN] Database update failed: {e}")


def main():
    """Main function."""
    print("=" * 70)
    print("RUNNING FAILING PYTHON TESTS")
    print("=" * 70)
    print()

    failures = get_failing_python_tests()
    print(f"Found {len(failures)} failing Python tests")
    print()

    passed_count = 0
    still_failing_count = 0
    errors = []

    for idx, (algorithm_path, language, current_status, current_error) in enumerate(failures, 1):
        print(f"[{idx}/{len(failures)}] Testing: {algorithm_path}")
        
        path_str = algorithm_path.replace('\\', '/')
        python_file = ROOT / path_str / "algorithm.py"
        
        if not python_file.exists():
            print(f"  [SKIP] File not found: {python_file}")
            still_failing_count += 1
            continue
        
        start_time = time.time()
        success, error_msg, output = test_python_file(python_file)
        duration = time.time() - start_time
        
        if success:
            print(f"  [PASS] Test passed!")
            status = 'success'
            passed_count += 1
        else:
            error_preview = error_msg[:200] if error_msg else "No error message"
            print(f"  [FAIL] {error_preview}...")
            status = 'failure'
            still_failing_count += 1
            errors.append(f"{algorithm_path}:\n{error_msg}\n{'='*70}\n")
        
        update_database(algorithm_path, language, status, duration, 
                       error_msg if not success else None, 
                       output if success else None)
        print()
    
    # Save errors to file
    if errors:
        ERRORS_FILE.write_text('\n'.join(errors), encoding='utf-8')
        print(f"Errors saved to: {ERRORS_FILE}")
    
    print("=" * 70)
    print(f"Summary:")
    print(f"  Total tested: {len(failures)}")
    print(f"  Now passing: {passed_count}")
    print(f"  Still failing: {still_failing_count}")
    print("=" * 70)


if __name__ == "__main__":
    main()

