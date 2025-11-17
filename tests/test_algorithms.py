#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for algorithm implementations.
"""

import unittest
import sys
from pathlib import Path

# Add project root to path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tests.test_framework_setup import AlgorithmTestCase


class TestSortingAlgorithms(AlgorithmTestCase):
    """Test sorting algorithms."""
    
    def test_insertion_sort(self):
        """Test insertion sort."""
        from semester_1.lecture_01_sorting_fundamentals.insertion_sort.algorithm import insertion_sort
        
        # Test basic sorting
        arr = [64, 34, 25, 12, 22, 11, 90]
        result = insertion_sort(arr.copy())
        self.assert_sorted(result, arr)
        
        # Test empty array
        self.assertEqual(insertion_sort([]), [])
        
        # Test single element
        self.assertEqual(insertion_sort([1]), [1])
        
        # Test already sorted
        arr = [1, 2, 3, 4, 5]
        result = insertion_sort(arr.copy())
        self.assertEqual(result, arr)
    
    def test_quick_sort(self):
        """Test quick sort."""
        from semester_1.lecture_02_efficient_sorting.quick_sort.algorithm import quick_sort
        
        arr = [64, 34, 25, 12, 22, 11, 90]
        result = quick_sort(arr.copy())
        self.assert_sorted(result, arr)
    
    def test_merge_sort(self):
        """Test merge sort."""
        # Will be available after implementation
        pass
    
    def test_bubble_sort(self):
        """Test bubble sort."""
        from semester_1.lecture_01_sorting_fundamentals.bubble_sort.algorithm import bubble_sort
        
        arr = [64, 34, 25, 12, 22, 11, 90]
        result = bubble_sort(arr.copy())
        self.assert_sorted(result, arr)


class TestSearchingAlgorithms(AlgorithmTestCase):
    """Test searching algorithms."""
    
    def test_binary_search(self):
        """Test binary search."""
        from semester_1.lecture_04_searching.binary_search.algorithm import binary_search
        
        arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        
        # Test found
        result = binary_search(arr, 5)
        self.assert_search_result(result, 5, arr, found=True)
        
        # Test not found
        result = binary_search(arr, 11)
        self.assert_search_result(result, 11, arr, found=False)
    
    def test_linear_search(self):
        """Test linear search."""
        from semester_1.lecture_04_searching.linear_search.algorithm import linear_search
        
        arr = [1, 2, 3, 4, 5]
        
        # Test found
        result = linear_search(arr, 3)
        self.assert_search_result(result, 3, arr, found=True)
        
        # Test not found
        result = linear_search(arr, 6)
        self.assertEqual(result, None)


class TestGraphAlgorithms(AlgorithmTestCase):
    """Test graph algorithms."""
    
    def test_bfs(self):
        """Test BFS."""
        from semester_1.lecture_09_graph_algorithms.bfs.algorithm import bfs
        
        graph = {
            0: [1, 2],
            1: [3, 4],
            2: [5],
            3: [],
            4: [],
            5: []
        }
        
        result = bfs(graph, 0)
        self.assertIsInstance(result, list)
        self.assertIn(0, result)
    
    def test_dfs(self):
        """Test DFS."""
        # Will be available after implementation
        pass


class TestPerformance(AlgorithmTestCase):
    """Test algorithm performance."""
    
    def test_sorting_performance(self):
        """Test sorting algorithm performance."""
        import random
        from semester_1.lecture_02_efficient_sorting.quick_sort.algorithm import quick_sort
        
        # Generate large array
        arr = [random.randint(0, 1000) for _ in range(1000)]
        
        # Should complete in reasonable time
        self.assert_performance(lambda: quick_sort(arr.copy()), max_time_seconds=1.0)


if __name__ == '__main__':
    unittest.main()

