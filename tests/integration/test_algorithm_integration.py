#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integration tests for algorithms.
Tests algorithms working together and with external systems.
"""

import unittest
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tests.test_framework_setup import AlgorithmTestCase


class TestSortingIntegration(AlgorithmTestCase):
    """Integration tests for sorting algorithms."""

    def test_sorting_pipeline(self):
        """Test sorting algorithms in a pipeline."""
        from semester_01.lecture_02_efficient_sorting.quick_sort.algorithm import (
            quick_sort,
        )
        from semester_01.lecture_02_efficient_sorting.merge_sort.algorithm import (
            merge_sort,
        )

        data = [64, 34, 25, 12, 22, 11, 90]

        # Test quick sort
        result1 = quick_sort(data.copy())
        self.assert_sorted(result1, data)

        # Test merge sort
        result2 = merge_sort(data.copy())
        self.assert_sorted(result2, data)

        # Both should produce same result
        self.assertEqual(result1, result2)

    def test_sorting_with_searching(self):
        """Test sorting followed by searching."""
        from semester_01.lecture_02_efficient_sorting.quick_sort.algorithm import (
            quick_sort,
        )
        from semester_01.lecture_04_searching.binary_search.algorithm import (
            binary_search,
        )

        data = [64, 34, 25, 12, 22, 11, 90]
        sorted_data = quick_sort(data.copy())

        # Binary search requires sorted array
        result = binary_search(sorted_data, 25)
        self.assertIsNotNone(result)
        self.assertIn(result, range(len(sorted_data)))


class TestGraphIntegration(AlgorithmTestCase):
    """Integration tests for graph algorithms."""

    def test_bfs_dfs_integration(self):
        """Test BFS and DFS working together."""
        from semester_01.lecture_09_graph_algorithms.bfs.algorithm import (
            Graph as BFSGraph,
        )
        from semester_01.lecture_09_graph_algorithms.dfs.algorithm import (
            Graph as DFSGraph,
        )

        edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5)]

        # BFS
        bfs_graph = BFSGraph()
        for u, v in edges:
            bfs_graph.add_edge(u, v)
        bfs_result = bfs_graph.bfs(0)

        # DFS
        dfs_graph = DFSGraph()
        for u, v in edges:
            dfs_graph.add_edge(u, v)
        dfs_result = dfs_graph.dfs(0)

        # Both should visit all nodes
        self.assertEqual(len(set(bfs_result)), len(set(dfs_result)))
        self.assertIn(0, bfs_result)
        self.assertIn(0, dfs_result)

    def test_graph_with_shortest_path(self):
        """Test graph algorithms with shortest path."""
        from semester_01.lecture_09_graph_algorithms.bfs.algorithm import Graph
        from semester_01.lecture_09_graph_algorithms.dijkstra.algorithm import dijkstra

        graph = Graph()
        graph.add_edge(0, 1)
        graph.add_edge(0, 2)
        graph.add_edge(1, 3)
        graph.add_edge(2, 3)

        # BFS for unweighted
        path = graph.shortest_path(0, 3)
        self.assertIsNotNone(path)
        self.assertIn(0, path)
        self.assertIn(3, path)


class TestDesignPatternIntegration(AlgorithmTestCase):
    """Integration tests for design patterns."""

    def test_factory_with_singleton(self):
        """Test factory pattern creating singleton instances."""
        from semester_02.lecture_07_creational_patterns.factory.algorithm import factory
        from semester_02.lecture_07_creational_patterns.singleton.algorithm import (
            Singleton,
        )

        # Factory should create instances
        # Singleton should return same instance
        instance1 = Singleton()
        instance2 = Singleton()
        self.assertIs(instance1, instance2)

    def test_observer_with_factory(self):
        """Test observer pattern with factory."""
        # Integration test for observer pattern
        pass


class TestPerformanceIntegration(AlgorithmTestCase):
    """Integration tests for performance."""

    def test_large_dataset_processing(self):
        """Test algorithms with large datasets."""
        import random
        from semester_01.lecture_02_efficient_sorting.quick_sort.algorithm import (
            quick_sort,
        )

        # Large dataset
        large_data = [random.randint(0, 10000) for _ in range(10000)]

        # Should complete in reasonable time
        self.assert_performance(
            lambda: quick_sort(large_data.copy()), max_time_seconds=5.0
        )

    def test_memory_efficiency(self):
        """Test memory efficiency of algorithms."""
        import random
        from semester_01.lecture_02_efficient_sorting.merge_sort.algorithm import (
            merge_sort,
        )

        data = [random.randint(0, 1000) for _ in range(1000)]

        # Should not cause memory issues
        result = merge_sort(data.copy())
        self.assert_sorted(result, data)


class TestErrorHandlingIntegration(AlgorithmTestCase):
    """Integration tests for error handling."""

    def test_invalid_input_handling(self):
        """Test algorithms handle invalid input gracefully."""
        from semester_01.lecture_02_efficient_sorting.quick_sort.algorithm import (
            quick_sort,
        )

        # Empty input
        result = quick_sort([])
        self.assertEqual(result, [])

        # None input (should handle gracefully)
        # This depends on implementation

    def test_edge_cases_integration(self):
        """Test edge cases across multiple algorithms."""
        from semester_01.lecture_02_efficient_sorting.quick_sort.algorithm import (
            quick_sort,
        )
        from semester_01.lecture_04_searching.binary_search.algorithm import (
            binary_search,
        )

        # Single element
        single = [1]
        sorted_single = quick_sort(single.copy())
        self.assertEqual(sorted_single, [1])

        # Search in single element
        result = binary_search(sorted_single, 1)
        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
