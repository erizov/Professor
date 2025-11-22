#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clear failing Java test records and rerun tests to get fresh error information.
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


def clear_failing_java_records():
    """Delete all failing Java records from database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Count before deletion
    cursor.execute("""
        SELECT COUNT(*) FROM test_results
        WHERE language = 'java' AND status IN ('failure', 'error', 'timeout')
    """)
    count_before = cursor.fetchone()[0]
    
    # Delete failing records
    cursor.execute("""
        DELETE FROM test_results
        WHERE language = 'java' AND status IN ('failure', 'error', 'timeout')
    """)
    
    deleted = cursor.rowcount
    conn.commit()
    conn.close()
    
    print(f"Deleted {deleted} failing Java records from database")
    return deleted


def get_java_files() -> List[Path]:
    """Get all Java Algorithm.java files."""
    java_files = []
    for java_file in ROOT.glob("**/Algorithm.java"):
        # Skip sandbox files
        if "sandboxes" in str(java_file):
            continue
        java_files.append(java_file)
    return sorted(java_files)


def test_java_file(java_file: Path, timeout: int = 15) -> Tuple[bool, str, str, float]:
    """Test a single Java file: compile and run."""
    try:
        try:
            algorithm_path = str(java_file.parent.relative_to(ROOT))
        except ValueError:
            algorithm_path = str(java_file.parent)
        
        start_time = time.time()
        
        # Compile Java file
        compile_result = subprocess.run(
            ["javac", str(java_file)],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=str(ROOT)
        )
        
        if compile_result.returncode != 0:
            error_msg = compile_result.stderr or compile_result.stdout or ""
            duration = time.time() - start_time
            return False, error_msg, compile_result.stdout or "", duration
        
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
        
        duration = time.time() - start_time
        output = run_result.stdout or ""
        error_msg = run_result.stderr or ""
        success = run_result.returncode == 0
        
        return success, error_msg, output, duration
        
    except subprocess.TimeoutExpired:
        duration = time.time() - start_time
        return False, f"Test timed out after {timeout} seconds", "", duration
    except Exception as e:
        duration = time.time() - start_time if 'start_time' in locals() else 0.0
        return False, f"Error running test: {e}", "", duration


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
    
    if not error_message:
        return issues
    
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
    
    if 'public static void main' not in error_lower and 'main' in error_lower and 'could not find' in error_lower:
        issues['missing_main'] = True
    
    return issues


def update_database(algorithm_path: str, status: str, duration: float, 
                   error_message: Optional[str], output: Optional[str]):
    """Update test_results database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get previous status
        cursor.execute("""
            SELECT status FROM test_results
            WHERE algorithm_path = ? AND language = 'java'
            ORDER BY timestamp DESC
            LIMIT 1
        """, (algorithm_path,))
        
        previous_result = cursor.fetchone()
        previous_status = previous_result[0] if previous_result else None
        
        # Determine state change
        state_changed = False
        if previous_status and previous_status != status:
            state_changed = True
        
        # Insert new result
        timestamp = datetime.now().isoformat()
        cursor.execute("""
            INSERT INTO test_results 
            (algorithm_path, language, status, duration, timestamp, error_message, 
             test_output, previous_status, state_changed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            algorithm_path,
            'java',
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


def main():
    """Main function."""
    print("=" * 70)
    print("CLEAR AND RERUN FAILING JAVA TESTS")
    print("=" * 70)
    print()
    
    # Step 1: Clear failing records
    print("Step 1: Clearing failing Java records from database...")
    deleted = clear_failing_java_records()
    print(f"  ✓ Deleted {deleted} records")
    print()
    
    # Step 2: Get all Java files
    print("Step 2: Finding all Java files...")
    java_files = get_java_files()
    print(f"  ✓ Found {len(java_files)} Java files")
    print()
    
    # Step 3: Test all Java files
    print("Step 3: Testing all Java files (timeout: 15s)...")
    print()
    
    success_count = 0
    failure_count = 0
    error_summary = {
        'missing_main': 0,
        'wrong_path': 0,
        'wrong_class_name': 0,
        'package_error': 0,
        'compilation_error': 0,
        'runtime_error': 0,
        'timeout': 0
    }
    
    for idx, java_file in enumerate(java_files, 1):
        try:
            algorithm_path = str(java_file.parent.relative_to(ROOT))
        except ValueError:
            algorithm_path = str(java_file.parent)
        
        print(f"[{idx}/{len(java_files)}] Testing: {algorithm_path}")
        
        success, error_msg, output, duration = test_java_file(java_file, timeout=15)
        
        if success:
            print(f"  ✓ Test passed ({duration:.2f}s)")
            status = 'success'
            success_count += 1
        else:
            # Analyze error
            issues = analyze_error(error_msg)
            issue_list = [k for k, v in issues.items() if v]
            
            if 'timeout' in error_msg.lower():
                status = 'timeout'
                error_summary['timeout'] += 1
            elif 'compilation_error' in issue_list:
                status = 'error'
                error_summary['compilation_error'] += 1
            else:
                status = 'failure'
                error_summary['runtime_error'] += 1
            
            # Count specific issues
            for issue in issue_list:
                if issue in error_summary:
                    error_summary[issue] += 1
            
            if issue_list:
                print(f"  ✗ Issues: {', '.join(issue_list)}")
            error_preview = error_msg[:150] if error_msg else "No error message"
            print(f"  Error: {error_preview}...")
            failure_count += 1
        
        # Update database
        update_database(algorithm_path, status, duration, 
                       error_msg if not success else None, 
                       output if success else None)
        
        # Progress update every 50 files
        if idx % 50 == 0:
            print(f"  Progress: {idx}/{len(java_files)} | Success: {success_count} | Failures: {failure_count}")
        print()
    
    print("=" * 70)
    print("Summary:")
    print(f"  Total Java files: {len(java_files)}")
    print(f"  Success: {success_count}")
    print(f"  Failures: {failure_count}")
    print()
    print("Error breakdown:")
    for issue, count in error_summary.items():
        if count > 0:
            print(f"  {issue}: {count}")
    print("=" * 70)


if __name__ == "__main__":
    main()


