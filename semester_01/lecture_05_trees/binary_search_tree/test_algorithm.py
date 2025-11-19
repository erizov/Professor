#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for Binary Search Tree.
"""

import unittest
import sys
from pathlib import Path

# Add parent directories to path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from tests.test_framework_setup import AlgorithmTestCase


class TestBinarysearchtree(AlgorithmTestCase):
    """Test Binary Search Tree implementation."""

    def setUp(self):
        """Set up test fixtures."""
        from semester_01.lecture_05_trees.binary_search_tree.algorithm import BinarySearchTree
        self.BST = BinarySearchTree
        # For search tests, we'll use the search method
        self.algorithm = lambda arr, target: self._search_in_bst(arr, target)
    
    def _search_in_bst(self, arr, target):
        """Helper to build BST from array and search."""
        bst = self.BST()
        for val in arr:
            bst.insert(val)
        return bst.search(target)

    def test_basic_search(self):
        """Test basic search functionality."""
        arr = [1, 3, 5, 7, 9, 11, 13]
        result = self.algorithm(arr, 7)
        self.assertTrue(result)  # Should return True if found

    def test_not_found(self):
        """Test when element is not found."""
        arr = [1, 3, 5, 7, 9]
        result = self.algorithm(arr, 10)
        self.assertFalse(result)

    def test_empty_input(self):
        """Test with empty input."""
        result = self.algorithm([], 5)
        self.assertFalse(result)

    def test_single_element(self):
        """Test with single element."""
        result = self.algorithm([42], 42)
        self.assertTrue(result)

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

    def test_first_element(self):
        """Test searching for first element."""
        arr = [1, 2, 3, 4, 5]
        result = self.algorithm(arr, 1)
        self.assertTrue(result)

    def test_last_element(self):
        """Test searching for last element."""
        arr = [1, 2, 3, 4, 5]
        result = self.algorithm(arr, 5)
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
