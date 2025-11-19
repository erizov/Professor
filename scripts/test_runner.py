#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive test runner system with timeouts and result tracking.

This script runs all algorithm tests with configurable timeouts,
separates Python and Java tests, and tracks results for reporting.
"""

import subprocess
import sys
import json
import time
import signal
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum
import sqlite3

ROOT = Path(__file__).resolve().parents[1]


class TestStatus(Enum):
    """Test execution status."""
    SUCCESS = "success"
    FAILURE = "failure"
    TIMEOUT = "timeout"
    ERROR = "error"
    SKIPPED = "skipped"
    RUNNING = "running"


@dataclass
class TestResult:
    """Test result data structure."""
    algorithm_path: str
    language: str  # "python" or "java"
    status: str
    duration: float
    timestamp: str
    error_message: Optional[str] = None
    test_output: Optional[str] = None
    previous_status: Optional[str] = None
    state_changed: bool = False


class TestRunner:
    """Test runner with timeout support and result tracking."""

    def __init__(self, config_path: Optional[Path] = None):
        """Initialize test runner with configuration."""
        self.root = ROOT
        self.config = self.load_config(config_path)
        self.db_path = self.root / "test_results.db"
        self.init_database()

    def load_config(self, config_path: Optional[Path]) -> Dict:
        """Load test configuration."""
        default_config = {
            "python": {
                "short_timeout": 30,  # seconds
                "long_timeout": 300,  # 5 minutes
            },
            "java": {
                "short_timeout": 60,  # seconds
                "long_timeout": 600,  # 10 minutes
            },
            "long_running_keywords": [
                "quantum",
                "distributed",
                "training",
                "inference",
                "optimization",
                "simulation",
                "benchmark",
                "performance",
                "mlops",
                "pipeline",
            ],
        }

        if config_path and config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                user_config = json.load(f)
                # Merge with defaults
                for key in default_config:
                    if key in user_config:
                        if isinstance(default_config[key], dict):
                            default_config[key].update(user_config[key])
                        else:
                            default_config[key] = user_config[key]
                # Also handle python_timeouts/java_timeouts format
                if "python_timeouts" in user_config:
                    default_config["python"].update(user_config["python_timeouts"])
                if "java_timeouts" in user_config:
                    default_config["java"].update(user_config["java_timeouts"])

        return default_config

    def init_database(self):
        """Initialize test results database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

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

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_algorithm_path 
            ON test_results(algorithm_path)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_timestamp 
            ON test_results(timestamp DESC)
        """)

        conn.commit()
        conn.close()

    def is_long_running(self, algorithm_path: str) -> bool:
        """Determine if algorithm is long-running based on path/keywords."""
        path_lower = algorithm_path.lower()
        for keyword in self.config["long_running_keywords"]:
            if keyword in path_lower:
                return True
        return False

    def get_timeout(self, algorithm_path: str, language: str) -> int:
        """Get timeout for algorithm based on language and running type."""
        is_long = self.is_long_running(algorithm_path)
        timeout_type = "long_timeout" if is_long else "short_timeout"
        lang_config = self.config.get(language, {})
        return lang_config.get(timeout_type, 30 if language == "python" else 60)

    def find_python_tests(self) -> List[Path]:
        """Find all Python test files."""
        test_files = []
        for test_file in self.root.rglob("test_algorithm.py"):
            # Check if it's in an algorithm directory
            if test_file.parent.name not in ["tests", "__pycache__"]:
                test_files.append(test_file)
        return sorted(test_files)

    def find_java_tests(self) -> List[Path]:
        """Find all Java algorithm files (tests are typically in the same file)."""
        java_files = []
        for java_file in self.root.rglob("Algorithm.java"):
            # Check if it's in an algorithm directory
            if java_file.parent.name not in ["tests", "__pycache__"]:
                java_files.append(java_file)
        return sorted(java_files)

    def run_python_test(
        self, test_file: Path, timeout: int
    ) -> Tuple[TestStatus, float, Optional[str], Optional[str]]:
        """Run a Python test file with timeout."""
        start_time = time.time()
        algorithm_path = str(test_file.parent.relative_to(self.root))

        try:
            # Run pytest with timeout
            # Note: pytest-timeout uses --timeout flag
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pytest",
                    str(test_file),
                    "-v",
                    "--tb=short",
                    f"--timeout={timeout}",
                ],
                capture_output=True,
                text=True,
                timeout=timeout + 10,  # Add buffer for pytest overhead
            )

            duration = time.time() - start_time

            if result.returncode == 0:
                return TestStatus.SUCCESS, duration, None, result.stdout
            else:
                error_msg = result.stderr or result.stdout
                return TestStatus.FAILURE, duration, error_msg, result.stdout

        except subprocess.TimeoutExpired:
            duration = time.time() - start_time
            return TestStatus.TIMEOUT, duration, f"Test exceeded timeout of {timeout}s", None

        except Exception as e:
            duration = time.time() - start_time
            return TestStatus.ERROR, duration, str(e), None

    def run_java_test(
        self, java_file: Path, timeout: int
    ) -> Tuple[TestStatus, float, Optional[str], Optional[str]]:
        """Run a Java algorithm file with timeout."""
        start_time = time.time()
        algorithm_path = str(java_file.parent.relative_to(self.root))

        try:
            # Compile Java file
            compile_result = subprocess.run(
                ["javac", str(java_file)],
                capture_output=True,
                text=True,
                timeout=30,
            )

            if compile_result.returncode != 0:
                duration = time.time() - start_time
                return (
                    TestStatus.ERROR,
                    duration,
                    f"Compilation failed: {compile_result.stderr}",
                    None,
                )

            # Run Java file (if it has main method)
            class_name = "Algorithm"
            class_path = str(java_file.parent)

            run_result = subprocess.run(
                ["java", "-cp", class_path, class_name],
                capture_output=True,
                text=True,
                timeout=timeout,
            )

            duration = time.time() - start_time

            # Java programs typically return 0 on success
            if run_result.returncode == 0:
                return TestStatus.SUCCESS, duration, None, run_result.stdout
            else:
                return (
                    TestStatus.FAILURE,
                    duration,
                    run_result.stderr or "Execution failed",
                    run_result.stdout,
                )

        except subprocess.TimeoutExpired:
            duration = time.time() - start_time
            return TestStatus.TIMEOUT, duration, f"Test exceeded timeout of {timeout}s", None

        except Exception as e:
            duration = time.time() - start_time
            return TestStatus.ERROR, duration, str(e), None

    def get_previous_status(self, algorithm_path: str, language: str) -> Optional[str]:
        """Get the most recent previous status for an algorithm."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT status FROM test_results
            WHERE algorithm_path = ? AND language = ?
            ORDER BY timestamp DESC
            LIMIT 1
        """,
            (algorithm_path, language),
        )

        result = cursor.fetchone()
        conn.close()

        return result[0] if result else None

    def save_result(self, result: TestResult):
        """Save test result to database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get previous status
        previous_status = self.get_previous_status(result.algorithm_path, result.language)
        result.previous_status = previous_status

        # Check if state changed
        if previous_status:
            if previous_status == TestStatus.SUCCESS.value and result.status != TestStatus.SUCCESS.value:
                result.state_changed = True
            elif previous_status != TestStatus.SUCCESS.value and result.status == TestStatus.SUCCESS.value:
                result.state_changed = True

        cursor.execute(
            """
            INSERT INTO test_results 
            (algorithm_path, language, status, duration, timestamp, error_message, 
             test_output, previous_status, state_changed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                result.algorithm_path,
                result.language,
                result.status,
                result.duration,
                result.timestamp,
                result.error_message,
                result.test_output,
                result.previous_status,
                1 if result.state_changed else 0,
            ),
        )

        conn.commit()
        conn.close()

    def run_all_tests(self, languages: List[str] = None, filter_path: Optional[str] = None):
        """Run all tests for specified languages."""
        if languages is None:
            languages = ["python", "java"]

        results = []

        if "python" in languages:
            print("Running Python tests...")
            python_tests = self.find_python_tests()
            if filter_path:
                python_tests = [t for t in python_tests if filter_path in str(t)]

            for test_file in python_tests:
                algorithm_path = str(test_file.parent.relative_to(self.root))
                timeout = self.get_timeout(algorithm_path, "python")
                is_long = self.is_long_running(algorithm_path)

                print(f"  Testing {algorithm_path} (Python, {'long' if is_long else 'short'}-running, timeout: {timeout}s)...")

                status, duration, error, output = self.run_python_test(test_file, timeout)

                result = TestResult(
                    algorithm_path=algorithm_path,
                    language="python",
                    status=status.value,
                    duration=duration,
                    timestamp=datetime.now().isoformat(),
                    error_message=error,
                    test_output=output,
                )

                self.save_result(result)
                results.append(result)

                status_symbol = "[PASS]" if status == TestStatus.SUCCESS else "[FAIL]"
                print(f"    {status_symbol} {status.value} ({duration:.2f}s)")

        if "java" in languages:
            print("\nRunning Java tests...")
            java_tests = self.find_java_tests()
            if filter_path:
                java_tests = [t for t in java_tests if filter_path in str(t)]

            for java_file in java_tests:
                algorithm_path = str(java_file.parent.relative_to(self.root))
                timeout = self.get_timeout(algorithm_path, "java")
                is_long = self.is_long_running(algorithm_path)

                print(f"  Testing {algorithm_path} (Java, {'long' if is_long else 'short'}-running, timeout: {timeout}s)...")

                status, duration, error, output = self.run_java_test(java_file, timeout)

                result = TestResult(
                    algorithm_path=algorithm_path,
                    language="java",
                    status=status.value,
                    duration=duration,
                    timestamp=datetime.now().isoformat(),
                    error_message=error,
                    test_output=output,
                )

                self.save_result(result)
                results.append(result)

                status_symbol = "[PASS]" if status == TestStatus.SUCCESS else "[FAIL]"
                print(f"    {status_symbol} {status.value} ({duration:.2f}s)")

        return results

    def get_recent_results(self, limit: int = 5) -> Dict[str, List[Dict]]:
        """Get recent test results grouped by algorithm."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get all unique algorithm paths
        cursor.execute(
            """
            SELECT DISTINCT algorithm_path, language 
            FROM test_results
            ORDER BY algorithm_path, language
        """
        )

        algorithms = cursor.fetchall()
        results_by_algorithm = {}

        for algorithm_path, language in algorithms:
            key = f"{algorithm_path}:{language}"

            cursor.execute(
                """
                SELECT algorithm_path, language, status, duration, timestamp, 
                       error_message, previous_status, state_changed
                FROM test_results
                WHERE algorithm_path = ? AND language = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """,
                (algorithm_path, language, limit),
            )

            rows = cursor.fetchall()
            results_by_algorithm[key] = [
                {
                    "algorithm_path": row[0],
                    "language": row[1],
                    "status": row[2],
                    "duration": row[3],
                    "timestamp": row[4],
                    "error_message": row[5],
                    "previous_status": row[6],
                    "state_changed": bool(row[7]),
                }
                for row in rows
            ]

        conn.close()
        return results_by_algorithm


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Run algorithm tests with timeouts")
    parser.add_argument(
        "--python", action="store_true", help="Run Python tests only"
    )
    parser.add_argument(
        "--java", action="store_true", help="Run Java tests only"
    )
    parser.add_argument(
        "--config", type=Path, help="Path to test configuration JSON file"
    )
    parser.add_argument(
        "--filter", type=str, help="Filter tests by path substring"
    )

    args = parser.parse_args()

    languages = []
    if args.python:
        languages.append("python")
    if args.java:
        languages.append("java")
    if not languages:
        languages = ["python", "java"]

    runner = TestRunner(args.config)
    results = runner.run_all_tests(languages=languages, filter_path=args.filter)

    # Print summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)

    status_counts = {}
    for result in results:
        status_counts[result.status] = status_counts.get(result.status, 0) + 1

    for status, count in sorted(status_counts.items()):
        print(f"  {status}: {count}")

    print(f"\nTotal: {len(results)} tests")
    print("=" * 70)


if __name__ == "__main__":
    main()

