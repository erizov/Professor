#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for Chaining.
"""

import unittest
import sys
from pathlib import Path

# Add parent directories to path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from tests.test_framework_setup import AlgorithmTestCase


class TestChaining(AlgorithmTestCase):
    """Test Chaining implementation."""

    def setUp(self):
        """Set up test fixtures."""
        from semester_01.lecture_08_hash_tables.chaining.algorithm import HashTableChaining
        self.HashTable = HashTableChaining

    def test_basic_functionality(self):
        """Test basic algorithm functionality."""
        ht = self.HashTable()
        ht.insert(1, "one")
        ht.insert(2, "two")
        self.assertEqual(ht.get(1), "one")
        self.assertEqual(ht.get(2), "two")

    def test_empty_input(self):
        """Test with empty input."""
        ht = self.HashTable()
        self.assertIsNone(ht.get(1))

    def test_single_element(self):
        """Test with single element."""
        ht = self.HashTable()
        ht.insert(5, "five")
        self.assertEqual(ht.get(5), "five")

    def test_already_sorted(self):
        """Test with already sorted input."""
        ht = self.HashTable()
        for i in range(5):
            ht.insert(i, f"value_{i}")
        for i in range(5):
            self.assertEqual(ht.get(i), f"value_{i}")

    def test_reverse_sorted(self):
        """Test with reverse sorted input."""
        ht = self.HashTable()
        for i in range(4, -1, -1):
            ht.insert(i, f"value_{i}")
        for i in range(5):
            self.assertEqual(ht.get(i), f"value_{i}")

    def test_duplicates(self):
        """Test with duplicate elements."""
        ht = self.HashTable()
        ht.insert(1, "first")
        ht.insert(1, "second")
        self.assertEqual(ht.get(1), "second")  # Should update value

    def test_performance(self):
        """Test algorithm performance."""
        ht = self.HashTable()
        def insert_and_get():
            for i in range(100):
                ht.insert(i, i)
                ht.get(i)
        self.assert_performance(insert_and_get, max_time_seconds=1.0)


if __name__ == "__main__":
    unittest.main()
