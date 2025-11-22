#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rerun failing tests to populate history column and identify why they are failing.
"""

import sqlite3
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple, Optional
import re
import time

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "test_results.db"


def get_failing_tests() -> List[Tuple[str, str]]:
    """Get list of failing tests (algorithm_path, language)."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get latest status for each algorithm:language pair
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
        AND status IN ('failure', 'error', 'timeout')
        ORDER BY algorithm_path, language
    """)
    
    failures = []
    for row in cursor.fetchall():
        algorithm_path, language, status, error_message = row
        failures.append((algorithm_path, language, status, error_message))
    
    conn.close()
    return failures


def test_java_file(java_file: Path, timeout: int = 30) -> Tuple[bool, str, str]:
    """Test a single Java file: compile and run."""
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
            timeout=30,
            cwd=str(ROOT)
        )
        
        if compile_result.returncode != 0:
            error_msg = compile_result.stderr or compile_result.stdout or ""
            return False, error_msg, compile_result.stdout or ""
        
        # Run Java file
        content = java_file.read_text(encoding='utf-8')
        package_match = re.search(r'^package\s+([^;]+);', content, re.MULTILINE)
        if package_match:
            package_name = package_match.group(1)
            class_name = f"{package_name}.Algorithm"
            classpath = "."
        else:
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


def test_python_file(python_file: Path, timeout: int = 30) -> Tuple[bool, str, str]:
    """Test a single Python file."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", str(python_file), "-v"],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(ROOT)
        )
        
        success = result.returncode == 0
        output = result.stdout or ""
        error_msg = result.stderr or ""
        
        if not success:
            # Combine stdout and stderr for better error info
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
        
        # Get previous status
        cursor.execute("""
            SELECT status FROM test_results
            WHERE algorithm_path = ? AND language = ?
            ORDER BY timestamp DESC
            LIMIT 1
        """, (algorithm_path, language))
        
        previous_result = cursor.fetchone()
        previous_status = previous_result[0] if previous_result else None
        
        # Determine state change
        state_changed = False
        if previous_status and previous_status != status:
            state_changed = True
        
        # Insert new result
        from datetime import datetime
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
        print(f"  ⚠ Database update failed: {e}")


def analyze_error(error_message: str) -> dict:
    """Analyze error message to identify common issues."""
    issues = {
        'missing_main': False,
        'wrong_path': False,
        'wrong_class_name': False,
        'package_error': False,
        'compilation_error': False,
        'runtime_error': False
    }
    
    error_lower = error_message.lower()
    
    if 'could not find or load main class' in error_lower:
        issues['missing_main'] = True
        issues['wrong_path'] = True
        issues['wrong_class_name'] = True
    
    if 'cannot find symbol' in error_lower:
        issues['compilation_error'] = True
    
    if 'package' in error_lower and ('does not exist' in error_lower or 'error' in error_lower):
        issues['package_error'] = True
    
    if 'is public, should be declared in a file named' in error_message:
        issues['wrong_class_name'] = True
    
    if 'error: could not find or load main class' in error_lower:
        issues['missing_main'] = True
        issues['wrong_path'] = True
    
    if 'public static void main' not in error_lower and 'main' in error_lower:
        issues['missing_main'] = True
    
    return issues


def main():
    """Main function to rerun failing tests."""
    print("=" * 70)
    print("RERUNNING FAILING TESTS")
    print("=" * 70)
    print()
    
    failures = get_failing_tests()
    print(f"Found {len(failures)} failing tests")
    print()
    
    java_count = 0
    python_count = 0
    fixed_count = 0
    still_failing_count = 0
    
    for algorithm_path, language, current_status, current_error in failures:
        print(f"[{java_count + python_count + 1}/{len(failures)}] Testing: {algorithm_path} ({language})")
        
        # Determine file path
        if language.lower() == 'java':
            java_file = ROOT / algorithm_path / "Algorithm.java"
            if not java_file.exists():
                print(f"  ✗ File not found: {java_file}")
                still_failing_count += 1
                continue
            
            start_time = time.time()
            success, error_msg, output = test_java_file(java_file, timeout=30)
            duration = time.time() - start_time
            java_count += 1
            
        elif language.lower() == 'python':
            python_file = ROOT / algorithm_path / "test_algorithm.py"
            if not python_file.exists():
                print(f"  ✗ File not found: {python_file}")
                still_failing_count += 1
                continue
            
            start_time = time.time()
            success, error_msg, output = test_python_file(python_file, timeout=30)
            duration = time.time() - start_time
            python_count += 1
        else:
            print(f"  ⚠ Unknown language: {language}")
            continue
        
        # Analyze error
        if not success:
            issues = analyze_error(error_msg)
            issue_list = [k for k, v in issues.items() if v]
            if issue_list:
                print(f"  Issues detected: {', '.join(issue_list)}")
            print(f"  Error: {error_msg[:200]}...")
            status = 'failure'
            still_failing_count += 1
        else:
            print(f"  ✓ Test passed!")
            status = 'success'
            if current_status in ('failure', 'error', 'timeout'):
                fixed_count += 1
        
        # Update database
        update_database(algorithm_path, language, status, duration, 
                       error_msg if not success else None, 
                       output if success else None)
        print()
    
    print("=" * 70)
    print(f"Summary:")
    print(f"  Java tests: {java_count}")
    print(f"  Python tests: {python_count}")
    print(f"  Fixed: {fixed_count}")
    print(f"  Still failing: {still_failing_count}")
    print("=" * 70)


if __name__ == "__main__":
    main()

