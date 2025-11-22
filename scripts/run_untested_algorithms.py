#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run Java and Python algorithms that haven't been tested before.
"""

import sqlite3
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple, Set
import time
from datetime import datetime
import re

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "test_results.db"


def get_tested_algorithms() -> Set[Tuple[str, str]]:
    """Get set of (algorithm_path, language) that have been tested."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT DISTINCT algorithm_path, language
        FROM test_results
    """)
    
    tested = {(row[0], row[1].lower()) for row in cursor.fetchall()}
    conn.close()
    return tested


def find_algorithm_files() -> List[Tuple[Path, str]]:
    """Find all algorithm files (Java and Python)."""
    algorithms = []
    
    # Find Java files
    for java_file in ROOT.rglob("**/Algorithm.java"):
        # Skip sandbox files
        if "sandbox" in str(java_file).lower():
            continue
        algorithm_path = java_file.parent.relative_to(ROOT)
        algorithms.append((java_file, "java", str(algorithm_path)))
    
    # Find Python files
    for python_file in ROOT.rglob("**/algorithm.py"):
        # Skip sandbox files and __pycache__
        if "sandbox" in str(python_file).lower() or "__pycache__" in str(python_file):
            continue
        algorithm_path = python_file.parent.relative_to(ROOT)
        algorithms.append((python_file, "python", str(algorithm_path)))
    
    return algorithms


def test_java_file(java_file: Path, timeout: int = 30) -> Tuple[bool, str, str]:
    """Test a single Java file."""
    try:
        # Compile Java file
        compile_result = subprocess.run(
            ["javac", "-d", ".", str(java_file)],
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
        commented_package_match = re.search(r'^//\s*package\s+([^;]+);', content, re.MULTILINE)
        
        if package_match and not commented_package_match:
            package_name = package_match.group(1)
            class_name = f"{package_name}.Algorithm"
            classpath = "."
            class_file_path = java_file.parent / "Algorithm.class"
            if not class_file_path.exists():
                return False, f"Compiled class file not found: {class_file_path}", ""
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
            None,  # No previous status for new tests
            0,  # No state change for new tests
        ))
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"  [WARN] Database update failed: {e}")


def main():
    """Main function."""
    print("=" * 70)
    print("RUNNING UNTESTED ALGORITHMS")
    print("=" * 70)
    print()
    
    # Get tested algorithms
    print("Loading tested algorithms...")
    tested = get_tested_algorithms()
    print(f"Found {len(tested)} tested algorithm:language combinations")
    print()
    
    # Find all algorithm files
    print("Finding algorithm files...")
    all_files = find_algorithm_files()
    print(f"Found {len(all_files)} algorithm files")
    print()
    
    # Filter untested algorithms
    untested = []
    for file_path, language, algorithm_path in all_files:
        # Normalize path for comparison
        normalized_path = str(algorithm_path).replace('\\', '/')
        key = (normalized_path, language.lower())
        
        # Also try with original path format
        if key not in tested and (algorithm_path, language.lower()) not in tested:
            untested.append((file_path, language, algorithm_path))
    
    print(f"Found {len(untested)} untested algorithms")
    print()
    
    if not untested:
        print("All algorithms have been tested!")
        return
    
    # Run tests
    passed_count = 0
    failed_count = 0
    
    for idx, (file_path, language, algorithm_path) in enumerate(untested, 1):
        print(f"[{idx}/{len(untested)}] Testing: {algorithm_path} ({language})")
        
        start_time = time.time()
        
        if language.lower() == "java":
            success, error_msg, output = test_java_file(file_path)
        else:
            success, error_msg, output = test_python_file(file_path)
        
        duration = time.time() - start_time
        
        if success:
            print(f"  [PASS] Test passed in {duration:.2f}s")
            status = 'success'
            passed_count += 1
        else:
            error_preview = error_msg[:200] if error_msg else "Unknown error"
            print(f"  [FAIL] {error_preview}...")
            status = 'failure'
            failed_count += 1
        
        # Update database
        update_database(
            str(algorithm_path),
            language,
            status,
            duration,
            error_msg if not success else None,
            output if success else None
        )
        print()
    
    print("=" * 70)
    print(f"Summary:")
    print(f"  Total tested: {len(untested)}")
    print(f"  Passed: {passed_count}")
    print(f"  Failed: {failed_count}")
    print("=" * 70)


if __name__ == "__main__":
    main()

