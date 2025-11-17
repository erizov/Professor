#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for Interpolation Search.
"""

import unittest
import sys
from pathlib import Path

# Add parent directories to path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from tests.test_framework_setup import AlgorithmTestCase


class TestInterpolationsearch(AlgorithmTestCase):
    """Test Interpolation Search implementation."""
    
    def setUp(self):
        """Set up test fixtures."""
        from semester_1.lecture_04_searching.interpolation_search.algorithm import interpolation_search
        self.algorithm = interpolation_search
    
    def test_basic_search(self):
        """Test basic search functionality."""
        arr = [1, 3, 5, 7, 9, 11, 13]
        result = self.algorithm(arr, 7)
        self.assertIsNotNone(result)
        self.assertIn(result, [3, arr.index(7)])  # Index or boolean
    
    def test_not_found(self):
        """Test when element is not found."""
        arr = [1, 3, 5, 7, 9]
        result = self.algorithm(arr, 10)
        self.assertIsNone(result) if result is not bool else self.assertFalse(result)
    
    def test_empty_input(self):
        """Test with empty input."""
        result = self.algorithm([], 5)
        self.assertIsNone(result) if result is not bool else self.assertFalse(result)
    
    def test_single_element(self):
        """Test with single element."""
        result = self.algorithm([42], 42)
        self.assertIsNotNone(result) if result is not bool else self.assertTrue(result)
    
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


    def test_not_found(self):
        """Test when target not found."""
        arr = [1, 2, 3, 4, 5]
        result = self.algorithm(arr, 6)
        self.assert_search_result(result, 6, arr, found=False)

    def test_first_element(self):
        """Test searching for first element."""
        arr = [1, 2, 3, 4, 5]
        result = self.algorithm(arr, 1)
        self.assert_search_result(result, 1, arr, found=True)

    def test_last_element(self):
        """Test searching for last element."""
        arr = [1, 2, 3, 4, 5]
        result = self.algorithm(arr, 5)
        self.assert_search_result(result, 5, arr, found=True)

    if __name__ == '__main__':
    unittest.main()
