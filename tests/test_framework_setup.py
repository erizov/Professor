#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test framework setup and configuration.
Provides base test classes and utilities for algorithm testing.
"""

import sys
from pathlib import Path
import unittest
from typing import List, Any, Callable

# Add framework to path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "framework"))

try:
    from performance_timer import PerformanceTimer
except ImportError:
    PerformanceTimer = None


class AlgorithmTestCase(unittest.TestCase):
    """Base test case for algorithm implementations."""

    def assert_sorted(self, result: List[Any], original: List[Any] = None):
        """Assert that result is sorted."""
        if len(result) <= 1:
            return

        for i in range(len(result) - 1):
            self.assertLessEqual(
                result[i],
                result[i + 1],
                f"Array not sorted: {result[i]} > {result[i + 1]}",
            )

        if original:
            self.assertEqual(
                len(result), len(original), "Result length doesn't match original"
            )
            self.assertEqual(
                sorted(original), result, "Result doesn't match expected sorted array"
            )

    def assert_search_result(
        self, result: int, target: Any, array: List[Any], found: bool = True
    ):
        """Assert search result is correct."""
        if found:
            self.assertGreaterEqual(result, 0, "Index should be non-negative")
            self.assertLess(result, len(array), "Index out of bounds")
            self.assertEqual(
                array[result],
                target,
                f"Found element {array[result]} != target {target}",
            )
        else:
            self.assertEqual(result, -1, "Should return -1 when not found")

    def assert_performance(self, func: Callable, max_time_seconds: float = 1.0):
        """Assert function completes within time limit."""
        import time

        start = time.perf_counter()
        func()
        duration = time.perf_counter() - start
        self.assertLess(
            duration,
            max_time_seconds,
            f"Function took {duration:.3f}s, expected < {max_time_seconds}s",
        )


def create_test_suite(
    algorithm_name: str, test_cases: List[dict]
) -> unittest.TestSuite:
    """Create test suite from test cases."""
    suite = unittest.TestSuite()

    class DynamicTest(AlgorithmTestCase):
        pass

    for i, test_case in enumerate(test_cases):
        test_name = f"test_{test_case.get('name', f'case_{i}')}"

        def make_test(case):
            def test(self):
                func = case["function"]
                input_data = case["input"]
                expected = case.get("expected")

                if expected is not None:
                    result = func(input_data)
                    self.assertEqual(result, expected)
                else:
                    # Just verify it runs without error
                    result = func(input_data)
                    self.assertIsNotNone(result)

            return test

        setattr(DynamicTest, test_name, make_test(test_case))

    suite.addTest(unittest.makeSuite(DynamicTest))
    return suite


if __name__ == "__main__":
    unittest.main()
