#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Performance timing and resource measurement framework.

Provides utilities to measure execution time, memory usage, and
other resource constraints for algorithms.
"""

import time
import sys
import tracemalloc
from typing import Callable, Dict, Any, Tuple, List
from functools import wraps
import json
from pathlib import Path


class PerformanceTimer:
    """
    Timer for measuring algorithm performance.

    Measures:
    - Execution time
    - Memory usage
    - Space complexity
    """

    def __init__(self, algorithm_name: str):
        """
        Initialize performance timer.

        Args:
            algorithm_name: Name of the algorithm being measured
        """
        self.algorithm_name = algorithm_name
        self.measurements: List[Dict[str, Any]] = []

    def measure(
        self, func: Callable, *args: Any, **kwargs: Any
    ) -> Tuple[Any, Dict[str, Any]]:
        """
        Measure function performance.

        Args:
            func: Function to measure
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Tuple of (result, metrics_dict)
        """
        # Start memory tracking
        tracemalloc.start()

        # Measure execution time
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()

        # Get memory usage
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # Calculate metrics
        metrics = {
            "execution_time_ms": (end_time - start_time) * 1000,
            "memory_current_kb": current / 1024,
            "memory_peak_kb": peak / 1024,
            "input_size": self._get_input_size(args, kwargs),
        }

        self.measurements.append(metrics)
        return result, metrics

    def _get_input_size(self, args: Tuple, kwargs: Dict) -> int:
        """Estimate input size from arguments."""
        size = 0
        for arg in args:
            if hasattr(arg, "__len__"):
                size += len(arg)
        for val in kwargs.values():
            if hasattr(val, "__len__"):
                size += len(val)
        return size

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of all measurements."""
        if not self.measurements:
            return {}

        times = [m["execution_time_ms"] for m in self.measurements]
        memories = [m["memory_peak_kb"] for m in self.measurements]

        return {
            "algorithm": self.algorithm_name,
            "runs": len(self.measurements),
            "time": {
                "min_ms": min(times),
                "max_ms": max(times),
                "avg_ms": sum(times) / len(times),
            },
            "memory": {
                "min_kb": min(memories),
                "max_kb": max(memories),
                "avg_kb": sum(memories) / len(memories),
            },
        }

    def print_summary(self) -> None:
        """Print formatted summary."""
        summary = self.get_summary()
        if not summary:
            print("No measurements recorded")
            return

        print("\n" + "=" * 70)
        print(f"Performance Summary: {summary['algorithm']}")
        print("=" * 70)
        print(f"Runs: {summary['runs']}")
        print("\nExecution Time:")
        print(f"  Min: {summary['time']['min_ms']:.3f} ms")
        print(f"  Avg: {summary['time']['avg_ms']:.3f} ms")
        print(f"  Max: {summary['time']['max_ms']:.3f} ms")
        print("\nMemory Usage:")
        print(f"  Min: {summary['memory']['min_kb']:.2f} KB")
        print(f"  Avg: {summary['memory']['avg_kb']:.2f} KB")
        print(f"  Max: {summary['memory']['max_kb']:.2f} KB")
        print("=" * 70)


def benchmark(dataset_sizes: List[int] = None) -> Callable:
    """
    Decorator to benchmark algorithm with different dataset sizes.

    Args:
        dataset_sizes: List of input sizes to test

    Returns:
        Decorated function
    """
    if dataset_sizes is None:
        dataset_sizes = [10, 100, 1000, 10000]

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            timer = PerformanceTimer(func.__name__)

            print(f"\nBenchmarking {func.__name__}...")
            print("-" * 70)

            for size in dataset_sizes:
                # Generate test data
                if "sort" in func.__name__.lower():
                    import random

                    data = [random.randint(1, 1000) for _ in range(size)]
                else:
                    data = list(range(size))

                # Measure
                _, metrics = timer.measure(func, data.copy())

                print(
                    f"n={size:6d}: "
                    f"{metrics['execution_time_ms']:8.3f} ms, "
                    f"{metrics['memory_peak_kb']:8.2f} KB"
                )

            timer.print_summary()
            return func(*args, **kwargs)

        return wrapper

    return decorator


class ResourceAnalyzer:
    """Analyze resource constraints and recommendations."""

    @staticmethod
    def analyze_constraints(
        algorithm_name: str,
        time_complexity: str,
        space_complexity: str,
        metrics: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Analyze algorithm under different constraints.

        Args:
            algorithm_name: Name of algorithm
            time_complexity: Big O time complexity
            space_complexity: Big O space complexity
            metrics: Measured performance metrics

        Returns:
            Analysis with recommendations
        """
        analysis = {
            "algorithm": algorithm_name,
            "complexity": {"time": time_complexity, "space": space_complexity},
            "measured": metrics,
            "constraints": {
                "low_memory": None,
                "low_cpu": None,
                "distributed": None,
                "edge": None,
            },
            "recommendations": [],
        }

        # Low memory analysis
        avg_memory = metrics.get("memory", {}).get("avg_kb", 0)
        if avg_memory < 100:
            analysis["constraints"]["low_memory"] = "EXCELLENT"
            analysis["recommendations"].append(
                "Suitable for memory-constrained environments"
            )
        elif avg_memory < 1000:
            analysis["constraints"]["low_memory"] = "GOOD"
        else:
            analysis["constraints"]["low_memory"] = "REQUIRES_OPTIMIZATION"
            analysis["recommendations"].append(
                "Consider memory optimization for constrained systems"
            )

        # Low CPU analysis
        avg_time = metrics.get("time", {}).get("avg_ms", 0)
        if "O(n log n)" in time_complexity or "O(log n)" in time_complexity:
            analysis["constraints"]["low_cpu"] = "GOOD"
        elif "O(n²)" in time_complexity or "O(n³)" in time_complexity:
            analysis["constraints"]["low_cpu"] = "POOR"
            analysis["recommendations"].append(
                "Not recommended for CPU-constrained environments"
            )

        # Distributed analysis
        if "O(1)" in space_complexity or "O(log n)" in space_complexity:
            analysis["constraints"]["distributed"] = "GOOD"
            analysis["recommendations"].append(
                "Low communication overhead for distributed systems"
            )

        # Edge deployment
        if avg_memory < 100 and avg_time < 10:
            analysis["constraints"]["edge"] = "EXCELLENT"
            analysis["recommendations"].append("Ideal for edge deployment")

        return analysis

    @staticmethod
    def save_analysis(analysis: Dict[str, Any], output_path: Path) -> None:
        """Save analysis to JSON file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(analysis, f, indent=2)

    @staticmethod
    def print_analysis(analysis: Dict[str, Any]) -> None:
        """Print formatted analysis."""
        print("\n" + "=" * 70)
        print(f"Resource Constraint Analysis: {analysis['algorithm']}")
        print("=" * 70)

        print("\nComplexity:")
        print(f"  Time:  {analysis['complexity']['time']}")
        print(f"  Space: {analysis['complexity']['space']}")

        print("\nConstraint Suitability:")
        for constraint, rating in analysis["constraints"].items():
            if rating:
                print(f"  {constraint.replace('_', ' ').title()}: " f"{rating}")

        if analysis["recommendations"]:
            print("\nRecommendations:")
            for i, rec in enumerate(analysis["recommendations"], 1):
                print(f"  {i}. {rec}")

        print("=" * 70)


def compare_algorithms(
    algorithms: List[Tuple[str, Callable]], dataset_size: int = 1000
) -> None:
    """
    Compare multiple algorithms side-by-side.

    Args:
        algorithms: List of (name, function) tuples
        dataset_size: Size of test dataset
    """
    import random

    print("\n" + "=" * 70)
    print(f"Algorithm Comparison (n={dataset_size})")
    print("=" * 70)
    print(f"{'Algorithm':<30} {'Time (ms)':<12} {'Memory (KB)':<12}")
    print("-" * 70)

    data = [random.randint(1, 1000) for _ in range(dataset_size)]

    for name, func in algorithms:
        timer = PerformanceTimer(name)
        _, metrics = timer.measure(func, data.copy())

        print(
            f"{name:<30} "
            f"{metrics['execution_time_ms']:>10.3f}  "
            f"{metrics['memory_peak_kb']:>10.2f}"
        )

    print("=" * 70)
