#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Performance benchmarks for algorithms.
Measures execution time, memory usage, and scalability.
"""

import time
import sys
import statistics
from pathlib import Path
from typing import List, Dict, Callable, Any
import tracemalloc

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from framework.performance_timer import PerformanceTimer


class AlgorithmBenchmark:
    """Benchmark suite for algorithms."""

    def __init__(self):
        self.results: Dict[str, List[float]] = {}

    def benchmark_sorting(self, algorithm_func: Callable, sizes: List[int] = None):
        """Benchmark sorting algorithms."""
        if sizes is None:
            sizes = [100, 500, 1000, 5000, 10000]

        import random

        print(f"\n{'='*70}")
        print(f"Benchmarking: {algorithm_func.__name__}")
        print(f"{'='*70}")
        print(f"{'Size':<10} {'Time (ms)':<15} {'Memory (MB)':<15} {'Ops/sec':<15}")
        print(f"{'-'*70}")

        for size in sizes:
            data = [random.randint(0, 10000) for _ in range(size)]

            # Time measurement
            start_time = time.perf_counter()
            result = algorithm_func(data.copy())
            end_time = time.perf_counter()
            elapsed_ms = (end_time - start_time) * 1000

            # Memory measurement
            tracemalloc.start()
            algorithm_func(data.copy())
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            memory_mb = peak / 1024 / 1024

            # Operations per second
            ops_per_sec = size / (elapsed_ms / 1000) if elapsed_ms > 0 else 0

            print(
                f"{size:<10} {elapsed_ms:<15.3f} {memory_mb:<15.3f} {ops_per_sec:<15.0f}"
            )

            # Store results
            key = f"{algorithm_func.__name__}_{size}"
            self.results[key] = [elapsed_ms, memory_mb, ops_per_sec]

    def benchmark_searching(self, algorithm_func: Callable, sizes: List[int] = None):
        """Benchmark searching algorithms."""
        if sizes is None:
            sizes = [100, 500, 1000, 5000, 10000]

        import random

        print(f"\n{'='*70}")
        print(f"Benchmarking: {algorithm_func.__name__}")
        print(f"{'='*70}")
        print(f"{'Size':<10} {'Time (ms)':<15} {'Memory (MB)':<15}")
        print(f"{'-'*70}")

        for size in sizes:
            data = sorted([random.randint(0, 10000) for _ in range(size)])
            target = data[size // 2]  # Search for middle element

            # Time measurement
            start_time = time.perf_counter()
            result = algorithm_func(data, target)
            end_time = time.perf_counter()
            elapsed_ms = (end_time - start_time) * 1000

            # Memory measurement
            tracemalloc.start()
            algorithm_func(data, target)
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            memory_mb = peak / 1024 / 1024

            print(f"{size:<10} {elapsed_ms:<15.3f} {memory_mb:<15.3f}")

            key = f"{algorithm_func.__name__}_{size}"
            self.results[key] = [elapsed_ms, memory_mb]

    def benchmark_graph(self, algorithm_func: Callable, sizes: List[int] = None):
        """Benchmark graph algorithms."""
        if sizes is None:
            sizes = [10, 50, 100, 500, 1000]

        print(f"\n{'='*70}")
        print(f"Benchmarking: {algorithm_func.__name__}")
        print(f"{'='*70}")
        print(f"{'Nodes':<10} {'Time (ms)':<15} {'Memory (MB)':<15}")
        print(f"{'-'*70}")

        for size in sizes:
            # Create graph
            graph = {}
            for i in range(size):
                graph[i] = []
                # Connect to a few random nodes
                import random

                for _ in range(min(5, size)):
                    neighbor = random.randint(0, size - 1)
                    if neighbor != i and neighbor not in graph[i]:
                        graph[i].append(neighbor)

            # Time measurement
            start_time = time.perf_counter()
            result = algorithm_func(graph, 0)
            end_time = time.perf_counter()
            elapsed_ms = (end_time - start_time) * 1000

            # Memory measurement
            tracemalloc.start()
            algorithm_func(graph, 0)
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            memory_mb = peak / 1024 / 1024

            print(f"{size:<10} {elapsed_ms:<15.3f} {memory_mb:<15.3f}")

            key = f"{algorithm_func.__name__}_{size}"
            self.results[key] = [elapsed_ms, memory_mb]

    def compare_algorithms(self, algorithms: List[Callable], data_size: int = 1000):
        """Compare multiple algorithms."""
        import random

        print(f"\n{'='*70}")
        print(f"Algorithm Comparison (Size: {data_size})")
        print(f"{'='*70}")
        print(f"{'Algorithm':<30} {'Time (ms)':<15} {'Memory (MB)':<15}")
        print(f"{'-'*70}")

        data = [random.randint(0, 10000) for _ in range(data_size)]
        comparison_results = []

        for algo in algorithms:
            # Time measurement
            start_time = time.perf_counter()
            result = algo(data.copy())
            end_time = time.perf_counter()
            elapsed_ms = (end_time - start_time) * 1000

            # Memory measurement
            tracemalloc.start()
            algo(data.copy())
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            memory_mb = peak / 1024 / 1024

            print(f"{algo.__name__:<30} {elapsed_ms:<15.3f} {memory_mb:<15.3f}")
            comparison_results.append((algo.__name__, elapsed_ms, memory_mb))

        return comparison_results

    def generate_report(self, output_file: str = "benchmark_report.txt"):
        """Generate benchmark report."""
        report_path = ROOT / "tests" / "performance" / output_file

        with open(report_path, "w", encoding="utf-8") as f:
            f.write("Algorithm Performance Benchmark Report\n")
            f.write("=" * 70 + "\n\n")

            for key, values in self.results.items():
                f.write(f"{key}:\n")
                f.write(f"  Time: {values[0]:.3f} ms\n")
                if len(values) > 1:
                    f.write(f"  Memory: {values[1]:.3f} MB\n")
                if len(values) > 2:
                    f.write(f"  Ops/sec: {values[2]:.0f}\n")
                f.write("\n")

        print(f"\nReport saved to: {report_path}")


def main():
    """Run performance benchmarks."""
    benchmark = AlgorithmBenchmark()

    # Benchmark sorting algorithms
    try:
        from semester_01.lecture_02_efficient_sorting.quick_sort.algorithm import (
            quick_sort,
        )
        from semester_01.lecture_02_efficient_sorting.merge_sort.algorithm import (
            merge_sort,
        )
        from semester_01.lecture_01_sorting_fundamentals.bubble_sort.algorithm import (
            bubble_sort,
        )

        benchmark.benchmark_sorting(quick_sort, [100, 500, 1000, 5000])
        benchmark.benchmark_sorting(merge_sort, [100, 500, 1000, 5000])
        benchmark.benchmark_sorting(bubble_sort, [100, 500, 1000])

        # Compare sorting algorithms
        benchmark.compare_algorithms([quick_sort, merge_sort, bubble_sort], 1000)
    except ImportError as e:
        print(f"Could not import sorting algorithms: {e}")

    # Benchmark searching algorithms
    try:
        from semester_01.lecture_04_searching.binary_search.algorithm import (
            binary_search,
        )
        from semester_01.lecture_04_searching.linear_search.algorithm import (
            linear_search,
        )

        benchmark.benchmark_searching(binary_search, [100, 500, 1000, 5000, 10000])
        benchmark.benchmark_searching(linear_search, [100, 500, 1000, 5000])

        # Compare searching algorithms
        benchmark.compare_algorithms([binary_search, linear_search], 1000)
    except ImportError as e:
        print(f"Could not import searching algorithms: {e}")

    # Benchmark graph algorithms
    try:
        from semester_01.lecture_09_graph_algorithms.bfs.algorithm import (
            Graph as BFSGraph,
        )
        from semester_01.lecture_09_graph_algorithms.dfs.algorithm import (
            Graph as DFSGraph,
        )

        def bfs_wrapper(graph, start):
            g = BFSGraph()
            for node, neighbors in graph.items():
                for neighbor in neighbors:
                    g.add_edge(node, neighbor)
            return g.bfs(start)

        def dfs_wrapper(graph, start):
            g = DFSGraph()
            for node, neighbors in graph.items():
                for neighbor in neighbors:
                    g.add_edge(node, neighbor)
            return g.dfs(start)

        benchmark.benchmark_graph(bfs_wrapper, [10, 50, 100, 500])
        benchmark.benchmark_graph(dfs_wrapper, [10, 50, 100, 500])
    except ImportError as e:
        print(f"Could not import graph algorithms: {e}")

    # Generate report
    benchmark.generate_report()


if __name__ == "__main__":
    main()
