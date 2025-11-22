#!/usr/bin/env python3
"""
Run all Java algorithm tests and verify path matching.
"""

import subprocess
import sys
import time
import re
from pathlib import Path
from typing import Tuple

ROOT = Path(__file__).parent.parent.parent

def test_java_file(java_file: Path, timeout: int = 30) -> Tuple[bool, str, str]:
    """Test a single Java file."""
    try:
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

def main():
    """Main function to run all Java tests."""
    print("=" * 70)
    print("RUNNING ALL JAVA TESTS")
    print("=" * 70)
    print()
    
    # Find all Java files
    java_files = list(ROOT.rglob("**/Algorithm.java"))
    
    # Filter out sandbox files
    java_files = [f for f in java_files if "sandbox" not in str(f)]
    
    print(f"Found {len(java_files)} Java files to test")
    print()
    
    success_count = 0
    failure_count = 0
    path_mismatch_count = 0
    
    for idx, java_file in enumerate(java_files, 1):
        algorithm_path = str(java_file.parent.relative_to(ROOT))
        print(f"[{idx}/{len(java_files)}] Testing: {algorithm_path}")
        
        success, error_msg, output = test_java_file(java_file)
        
        if success:
            print(f"  [PASS] Test passed")
            success_count += 1
        else:
            error_preview = error_msg[:200] if error_msg else "No error message"
            print(f"  [FAIL] {error_preview}...")
            failure_count += 1
            
            # Check if error is related to path/package mismatch
            if "Could not find or load main class" in error_msg or "NoClassDefFoundError" in error_msg:
                path_mismatch_count += 1
                print(f"  [PATH MISMATCH] Classpath issue detected")
        
        # Print summary every 50 tests
        if idx % 50 == 0:
            print(f"  Progress: {idx}/{len(java_files)} | Passed: {success_count} | Failed: {failure_count}")
        print()
    
    print("=" * 70)
    print("Summary:")
    print(f"  Total tests: {len(java_files)}")
    print(f"  Passed: {success_count}")
    print(f"  Failed: {failure_count}")
    print(f"  Path/Classpath issues: {path_mismatch_count}")
    print("=" * 70)

if __name__ == "__main__":
    main()
