#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for Edit Distance.
"""

import unittest
import sys
from pathlib import Path

# Add parent directories to path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from tests.test_framework_setup import AlgorithmTestCase


class TestEditdistance(AlgorithmTestCase):
    """Test Edit Distance implementation."""

    def setUp(self):
        """Set up test fixtures."""
        from semester_01.lecture_11_dynamic_programming.edit_distance.algorithm import (
            edit_distance,
        )

        self.algorithm = edit_distance

    def test_basic_functionality(self):
        """Test basic algorithm functionality."""
        # TODO: Implement specific test based on algorithm
        pass

    def test_empty_input(self):
        """Test with empty input."""
        # TODO: Test edge case
        pass

    def test_single_element(self):
        """Test with single element."""
        # TODO: Test edge case
        pass

    def test_empty_input(self):
        """Test with empty input."""
        # TODO: Test edge case
        pass

    def test_single_element(self):
        """Test with single element."""
        # TODO: Test edge case
        pass

    def test_already_sorted(self):
        """Test with already sorted input."""
        # TODO: Test edge case
        pass

    def test_reverse_sorted(self):
        """Test with reverse sorted input."""
        # TODO: Test edge case
        pass

    def test_duplicates(self):
        """Test with duplicate elements."""
        # TODO: Test edge case
        pass

    def test_performance(self):
        """Test algorithm performance."""
        # TODO: Add performance test
        # self.assert_performance(lambda: self.algorithm([...]), max_time_seconds=1.0)
        pass

    def test_small_input(self):
        """Test with small input."""
        result = self.algorithm(1)
        self.assertEqual(result, 1)

    def test_zero_input(self):
        """Test with zero input."""
        result = self.algorithm(0)
        self.assertEqual(result, 0)

    def test_large_input(self):
        """Test with large input."""
        result = self.algorithm(100)
        self.assertIsNotNone(result)
        self.assertGreater(result, 0)

    def test_memoization(self):
        """Test that DP uses memoization."""
        import time

        s1 = "kitten" * 5
        s2 = "sitting" * 5
        
        start = time.time()
        result1 = self.algorithm(s1, s2)
        time1 = time.time() - start

        start = time.time()
        result2 = self.algorithm(s1, s2)
        time2 = time.time() - start

        self.assertEqual(result1, result2)
        # Second call should be faster (memoized)
        self.assertLessEqual(time2, time1)


if __name__ == "__main__":
    unittest.main()
