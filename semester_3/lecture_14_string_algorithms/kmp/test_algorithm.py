#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for Kmp.
"""

import unittest
import sys
from pathlib import Path

# Add parent directories to path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from tests.test_framework_setup import AlgorithmTestCase


class TestKmp(AlgorithmTestCase):
    """Test Kmp implementation."""
    
    def setUp(self):
        """Set up test fixtures."""
        from semester_3.lecture_14_string_algorithms.kmp.algorithm import compute_lps
        self.algorithm = compute_lps
    
    def test_basic_functionality(self):
        """Test basic algorithm functionality."""
        # TODO: Add specific test cases based on algorithm
        # Example for sorting:
        # result = self.algorithm([3, 1, 4, 1, 5])
        # self.assert_sorted(result)
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


    def test_pattern_not_found(self):
        """Test when pattern not found."""
        text = "ABCDEFG"
        pattern = "XYZ"
        result = self.algorithm(text, pattern)
        self.assertIsNone(result) or self.assertEqual(result, -1)

    if __name__ == '__main__':
    unittest.main()
