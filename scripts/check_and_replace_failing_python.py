#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check 38 failing Python programs and replace with working implementations.
"""

import sqlite3
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "test_results.db"


def get_failing_python_files() -> List[Tuple[str, str]]:
    """Get list of failing Python algorithm paths."""
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
        AND language = 'python'
        AND status IN ('failure', 'error', 'timeout')
        ORDER BY algorithm_path
    """)
    
    failures = cursor.fetchall()
    conn.close()
    return failures


def test_python_file(python_file: Path) -> Tuple[bool, str]:
    """Test a Python file."""
    try:
        result = subprocess.run(
            [sys.executable, str(python_file)],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(ROOT)
        )
        return result.returncode == 0, result.stderr or result.stdout
    except Exception as e:
        return False, str(e)


def main():
    """Main function."""
    print("=" * 70)
    print("CHECKING 38 FAILING PYTHON PROGRAMS")
    print("=" * 70)
    print()
    
    failures = get_failing_python_files()
    print(f"Found {len(failures)} failing Python tests")
    print()
    
    still_failing = []
    
    for algorithm_path, error_message in failures:
        path_str = algorithm_path.replace('\\', '/')
        algorithm_file = ROOT / path_str / "algorithm.py"
        
        if not algorithm_file.exists():
            print(f"[WARN] File not found: {algorithm_file}")
            still_failing.append((algorithm_path, "File not found"))
            continue
        
        print(f"Testing: {algorithm_path}")
        success, error = test_python_file(algorithm_file)
        
        if success:
            print(f"  [PASS]")
        else:
            error_preview = error[:100] if error else "Unknown error"
            print(f"  [FAIL] {error_preview}...")
            still_failing.append((algorithm_path, error))
        print()
    
    print("=" * 70)
    print(f"Summary:")
    print(f"  Total checked: {len(failures)}")
    print(f"  Still failing: {len(still_failing)}")
    print(f"  Now passing: {len(failures) - len(still_failing)}")
    print("=" * 70)
    
    if still_failing:
        print("\nStill failing algorithms:")
        for path, error in still_failing:
            print(f"  - {path}")
    
    return still_failing


if __name__ == "__main__":
    main()

