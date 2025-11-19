#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for Merge Sort.
"""

import unittest
import sys
from pathlib import Path

# Add parent directories to path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from tests.test_framework_setup import AlgorithmTestCase


class TestMergesort(AlgorithmTestCase):
    """Test Merge Sort implementation."""

    def setUp(self):
        """Set up test fixtures."""
        from semester_01.lecture_02_efficient_sorting.merge_sort.algorithm import (
            merge_sort,
        )

        self.algorithm = merge_sort

    def test_basic_sorting(self):
        """Test basic sorting functionality."""
        result = self.algorithm([3, 1, 4, 1, 5, 9, 2, 6])
        self.assertEqual(result, [1, 1, 2, 3, 4, 5, 6, 9])

    def test_empty_input(self):
        """Test with empty input."""
        result = self.algorithm([])
        self.assertEqual(result, [])

    def test_single_element(self):
        """Test with single element."""
        result = self.algorithm([42])
        self.assertEqual(result, [42])

    def test_already_sorted(self):
        """Test with already sorted input."""
        result = self.algorithm([1, 2, 3, 4, 5])
        self.assertEqual(result, [1, 2, 3, 4, 5])

    def test_reverse_sorted(self):
        """Test with reverse sorted input."""
        result = self.algorithm([5, 4, 3, 2, 1])
        self.assertEqual(result, [1, 2, 3, 4, 5])

    def test_duplicates(self):
        """Test with duplicate elements."""
        result = self.algorithm([3, 3, 3, 1, 1, 2])
        self.assertEqual(result, [1, 1, 2, 3, 3, 3])

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

    def test_already_sorted(self):
        """Test with already sorted input."""
        arr = [1, 2, 3, 4, 5]
        result = self.algorithm(arr.copy())
        self.assertEqual(result, arr)

    def test_negative_numbers(self):
        """Test with negative numbers."""
        arr = [-5, -2, -8, -1, -9]
        result = self.algorithm(arr.copy())
        self.assertEqual(result, [-9, -8, -5, -2, -1])


if __name__ == "__main__":
    unittest.main()
