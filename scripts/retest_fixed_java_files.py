#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Re-test the Java files that were just fixed.
"""

import sqlite3
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple
import time
from datetime import datetime
import re

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "test_results.db"


def get_recently_fixed_files() -> List[Tuple[str, str]]:
    """Get list of Java files that were recently failing."""
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
        SELECT algorithm_path, error_message
        FROM recent_results
        WHERE rn = 1 
        AND language = 'java'
        AND status IN ('failure', 'error', 'timeout')
        ORDER BY algorithm_path
    """)
    
    failures = cursor.fetchall()
    conn.close()
    return failures


def test_java_file(java_file: Path, timeout: int = 30) -> Tuple[bool, str, str]:
    """Test a single Java file."""
    try:
        # Compile in the file's directory (not using -d to keep .class in same dir)
        compile_result = subprocess.run(
            ["javac", str(java_file)],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(java_file.parent)
        )
        
        if compile_result.returncode != 0:
            error_msg = compile_result.stderr or compile_result.stdout or ""
            return False, error_msg, compile_result.stdout or ""
        
        # Check if class file exists in the same directory
        class_file_path = java_file.parent / "Algorithm.class"
        if not class_file_path.exists():
            return False, f"Compiled class file not found: {class_file_path}", ""
        
        # No package (commented out) - use simple class name
        class_name = "Algorithm"
        classpath = str(java_file.parent)
        
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
                   duration: float, error_message: str = None, 
                   output: str = None):
    """Update test_results database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
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
            'failure',  # Previous status was failure
            1,  # State changed
        ))
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"  [WARN] Database update failed: {e}")


def main():
    """Main function."""
    print("=" * 70)
    print("RE-TESTING FIXED JAVA FILES")
    print("=" * 70)
    print()
    
    failures = get_recently_fixed_files()
    print(f"Re-testing {len(failures)} previously failing Java files")
    print()
    
    passed_count = 0
    still_failing_count = 0
    
    for idx, (algorithm_path, old_error) in enumerate(failures, 1):
        path_str = algorithm_path.replace('\\', '/')
        java_file = ROOT / path_str / "Algorithm.java"
        
        if not java_file.exists():
            print(f"[{idx}/{len(failures)}] [SKIP] File not found: {java_file}")
            still_failing_count += 1
            continue
        
        print(f"[{idx}/{len(failures)}] Testing: {algorithm_path}")
        
        start_time = time.time()
        success, error_msg, output = test_java_file(java_file)
        duration = time.time() - start_time
        
        if success:
            print(f"  [PASS] Test passed in {duration:.2f}s")
            status = 'success'
            passed_count += 1
        else:
            error_preview = error_msg[:200] if error_msg else "Unknown error"
            print(f"  [FAIL] {error_preview}...")
            status = 'failure'
            still_failing_count += 1
        
        update_database(
            str(algorithm_path),
            "java",
            status,
            duration,
            error_msg if not success else None,
            output if success else None
        )
        print()
    
    print("=" * 70)
    print(f"Summary:")
    print(f"  Total re-tested: {len(failures)}")
    print(f"  Now passing: {passed_count}")
    print(f"  Still failing: {still_failing_count}")
    print("=" * 70)


if __name__ == "__main__":
    main()

