#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Python files one by one: test, commit on success (no push).
"""

import subprocess
import sys
from pathlib import Path
import threading
import time
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]

# Global state for status reporting
_status_lock = threading.Lock()
_status_state = {
    'current_file': None,
    'current_idx': 0,
    'total_files': 0,
    'passed_count': 0,
    'failed_count': 0,
    'skipped_count': 0,
    'start_time': None,
    'stop_event': threading.Event()
}


def status_reporter():
    """Background thread that reports status every 3 minutes."""
    while not _status_state['stop_event'].wait(180):  # Wait 3 minutes
        with _status_lock:
            state = _status_state.copy()
        
        if state['start_time'] is None:
            continue
        
        elapsed = time.time() - state['start_time']
        elapsed_str = f"{int(elapsed // 60)}m {int(elapsed % 60)}s"
        
        print("", flush=True)
        print("=" * 80, flush=True)
        print(f"STATUS UPDATE ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})", flush=True)
        print("=" * 80, flush=True)
        print(f"Elapsed time: {elapsed_str}", flush=True)
        print(f"Progress: {state['current_idx']}/{state['total_files']} files", flush=True)
        print(f"  ✓ Passed and committed: {state['passed_count']}", flush=True)
        print(f"  ❌ Failed: {state['failed_count']}", flush=True)
        print(f"  ⊘ Skipped: {state['skipped_count']}", flush=True)
        if state['current_file']:
            print(f"Currently processing: {state['current_file']}", flush=True)
        print("=" * 80, flush=True)
        print("", flush=True)


def get_all_python_test_files() -> list[tuple[str, Path]]:
    """Get list of all Python test files (algo_path, test_file)."""
    test_files = []
    for test_file in ROOT.rglob("test_algorithm.py"):
        # Skip files in scripts, tests, or __pycache__ directories
        if any(part in ["scripts", "tests", "__pycache__"] for part in test_file.parts):
            continue
        # Get algorithm path (parent directory relative to ROOT)
        algo_path = str(test_file.parent.relative_to(ROOT))
        test_files.append((algo_path, test_file))
    
    return sorted(test_files)


def test_single_file(test_file: Path) -> tuple[bool, str]:
    """Test a single test file and return (success, output)."""
    try:
        # Run pytest on the specific test file with timeout
        result = subprocess.run(
            [sys.executable, "-m", "pytest", str(test_file), "-v", "--tb=short", "--timeout=30"],
            capture_output=True,
            text=True,
            timeout=45,  # Overall timeout slightly longer than pytest timeout
            cwd=str(ROOT)
        )
        
        # Check if tests passed
        success = result.returncode == 0
        output = result.stdout + result.stderr
        
        return success, output
    except subprocess.TimeoutExpired:
        return False, "Test timed out after 45 seconds"
    except Exception as e:
        return False, f"Error running test: {e}"


def commit_file(test_file: Path, algo_path: str) -> bool:
    """Commit the test file on successful test (no push)."""
    try:
        # Check if file has changes
        result = subprocess.run(
            ["git", "diff", "--quiet", str(test_file)],
            cwd=str(ROOT),
            capture_output=True,
            timeout=10
        )
        
        # If no changes, check if file is untracked
        if result.returncode == 0:
            # File has no changes, check if it's untracked
            result = subprocess.run(
                ["git", "ls-files", "--error-unmatch", str(test_file)],
                cwd=str(ROOT),
                capture_output=True,
                timeout=10
            )
            if result.returncode != 0:
                # File is untracked, add it
                subprocess.run(
                    ["git", "add", str(test_file)],
                    check=True,
                    cwd=str(ROOT),
                    capture_output=True,
                    timeout=10
                )
        else:
            # File has changes, stage it
            subprocess.run(
                ["git", "add", str(test_file)],
                check=True,
                cwd=str(ROOT),
                capture_output=True,
                timeout=10
            )
        
        # Commit
        commit_msg = f"Test passed: {algo_path}"
        subprocess.run(
            ["git", "commit", "-m", commit_msg],
            check=True,
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=10
        )
        
        return True
    except subprocess.TimeoutExpired:
        print(f"  ❌ Commit timed out", flush=True)
        return False
    except subprocess.CalledProcessError as e:
        # If commit fails because nothing to commit, that's okay
        if "nothing to commit" in (e.stderr or "").lower():
            return True
        print(f"  ⚠ Commit failed: {e.stderr if hasattr(e, 'stderr') else str(e)}", flush=True)
        return False


def main():
    """Main function to test Python files one by one."""
    # Ensure output is flushed immediately
    sys.stdout.reconfigure(encoding='utf-8')
    
    start_timestamp = datetime.now()
    start_time = time.time()
    
    print("=" * 80, flush=True)
    print("TESTING PYTHON FILES ONE BY ONE", flush=True)
    print("=" * 80, flush=True)
    print(flush=True)
    
    print("=" * 80, flush=True)
    print(f"🚀 STARTED AT: {start_timestamp.strftime('%Y-%m-%d %H:%M:%S')}", flush=True)
    print("=" * 80, flush=True)
    print(flush=True)
    
    print("Loading all Python test files...", flush=True)
    test_files = get_all_python_test_files()
    print(f"Found {len(test_files)} Python test files", flush=True)
    print(flush=True)
    
    # Initialize status state
    with _status_lock:
        _status_state['total_files'] = len(test_files)
        _status_state['start_time'] = start_time
        _status_state['passed_count'] = 0
        _status_state['failed_count'] = 0
        _status_state['skipped_count'] = 0
    
    # Start status reporter thread
    print("📊 Status updates will appear every 3 minutes", flush=True)
    print("📝 Status after each file will be shown", flush=True)
    print(flush=True)
    status_thread = threading.Thread(target=status_reporter, daemon=True)
    status_thread.start()
    
    passed_count = 0
    failed_count = 0
    skipped_count = 0
    
    try:
        for idx, (algo_path, test_file) in enumerate(test_files, 1):
            # Update status
            with _status_lock:
                _status_state['current_idx'] = idx
                _status_state['current_file'] = algo_path
                _status_state['passed_count'] = passed_count
                _status_state['failed_count'] = failed_count
                _status_state['skipped_count'] = skipped_count
            
            print(f"[{idx}/{len(test_files)}] Testing: {algo_path}", flush=True)
            print(f"  Test file: {test_file.relative_to(ROOT)}", flush=True)
            
            # Test the file
            print(f"  🧪 Running tests (timeout: 45s)...", flush=True)
            success, output = test_single_file(test_file)
            
            if success:
                print(f"  ✓ Tests passed!", flush=True)
                
                # Commit on success (no push)
                print(f"  💾 Committing (no push)...", flush=True)
                if commit_file(test_file, algo_path):
                    print(f"  ✓ Committed successfully", flush=True)
                    passed_count += 1
                    with _status_lock:
                        _status_state['passed_count'] = passed_count
                else:
                    # Commit failed but test passed, still count as passed
                    print(f"  ⚠ Commit had issues, but test passed", flush=True)
                    passed_count += 1
                    with _status_lock:
                        _status_state['passed_count'] = passed_count
            else:
                print(f"  ❌ Tests failed", flush=True)
                print(f"  Test output (first 500 chars):", flush=True)
                print(f"  {output[:500]}", flush=True)
                
                failed_count += 1
                with _status_lock:
                    _status_state['failed_count'] = failed_count
            
            # Print status after each file
            elapsed = time.time() - _status_state['start_time']
            elapsed_str = f"{int(elapsed // 60)}m {int(elapsed % 60)}s"
            print("-" * 80, flush=True)
            print(f"STATUS: [{idx}/{len(test_files)}] | Passed: {passed_count} | Failed: {failed_count} | Elapsed: {elapsed_str}", flush=True)
            print("-" * 80, flush=True)
            print(flush=True)
    
    finally:
        # Stop status reporter
        _status_state['stop_event'].set()
        status_thread.join(timeout=5)
    
    end_timestamp = datetime.now()
    end_time = time.time()
    total_elapsed = end_time - start_time
    elapsed_str = f"{int(total_elapsed // 60)}m {int(total_elapsed % 60)}s"
    
    print("", flush=True)
    print("=" * 80, flush=True)
    print("SUMMARY", flush=True)
    print("=" * 80, flush=True)
    print(f"Total processed: {len(test_files)}", flush=True)
    print(f"  ✓ Passed and committed: {passed_count}", flush=True)
    print(f"  ❌ Failed: {failed_count}", flush=True)
    print(f"  ⊘ Skipped: {skipped_count}", flush=True)
    print(f"Total elapsed time: {elapsed_str}", flush=True)
    print("=" * 80, flush=True)
    print("", flush=True)
    print("=" * 80, flush=True)
    print(f"✅ FINISHED AT: {end_timestamp.strftime('%Y-%m-%d %H:%M:%S')}", flush=True)
    print(f"⏱️  DURATION: {elapsed_str}", flush=True)
    print("=" * 80, flush=True)


if __name__ == "__main__":
    main()

