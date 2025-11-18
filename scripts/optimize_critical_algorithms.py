#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Profile and optimize critical algorithms.
Identifies performance bottlenecks and suggests optimizations.
"""

import cProfile
import pstats
import time
from pathlib import Path
from typing import Dict, List, Tuple
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Critical algorithms to optimize
CRITICAL_ALGORITHMS = [
    ('semester_01/lecture_02_efficient_sorting/quick_sort', 'quick_sort'),
    ('semester_01/lecture_02_efficient_sorting/merge_sort', 'merge_sort'),
    ('semester_01/lecture_02_efficient_sorting/heap_sort', 'heap_sort'),
    ('semester_01/lecture_04_searching/binary_search', 'binary_search'),
    ('semester_01/lecture_09_graph_algorithms/bfs', 'bfs'),
    ('semester_01/lecture_09_graph_algorithms/dfs', 'dfs'),
    ('semester_01/lecture_09_graph_algorithms/dijkstra', 'dijkstra'),
]

def profile_algorithm(module_path: str, func_name: str, test_data) -> Dict:
    """Profile an algorithm."""
    try:
        # Import algorithm
        module = __import__(module_path.replace('/', '.').replace('\\', '.'), fromlist=[func_name])
        func = getattr(module, func_name)
        
        # Profile
        profiler = cProfile.Profile()
        profiler.enable()
        result = func(test_data)
        profiler.disable()
        
        # Get stats
        stats = pstats.Stats(profiler)
        stats.sort_stats('cumulative')
        
        # Extract metrics
        total_time = stats.total_tt
        call_count = stats.total_calls
        per_call = total_time / call_count if call_count > 0 else 0
        
        return {
            'total_time': total_time,
            'call_count': call_count,
            'per_call': per_call,
            'result': result is not None
        }
    except Exception as e:
        return {'error': str(e)}

def benchmark_algorithm(module_path: str, func_name: str, sizes: List[int]) -> Dict:
    """Benchmark algorithm with different input sizes."""
    import random
    
    results = {}
    for size in sizes:
        # Generate test data
        if 'sort' in func_name:
            test_data = [random.randint(0, 1000) for _ in range(size)]
        elif 'search' in func_name:
            test_data = sorted([random.randint(0, 1000) for _ in range(size)])
        else:
            test_data = list(range(size))
        
        # Measure time
        start = time.perf_counter()
        try:
            module = __import__(module_path.replace('/', '.').replace('\\', '.'), fromlist=[func_name])
            func = getattr(module, func_name)
            if 'search' in func_name:
                result = func(test_data, test_data[size // 2])
            else:
                result = func(test_data)
            end = time.perf_counter()
            elapsed = (end - start) * 1000  # ms
            results[size] = {'time_ms': elapsed, 'success': True}
        except Exception as e:
            results[size] = {'error': str(e), 'success': False}
    
    return results

def generate_optimization_report() -> str:
    """Generate optimization report."""
    report = "# Algorithm Performance Optimization Report\n\n"
    report += "## Critical Algorithms Performance Analysis\n\n"
    
    for path, name in CRITICAL_ALGORITHMS:
        algo_path = ROOT / path
        if not (algo_path / "algorithm.py").exists():
            continue
        
        report += f"### {name.replace('_', ' ').title()}\n\n"
        
        # Benchmark
        sizes = [100, 500, 1000, 5000]
        benchmarks = benchmark_algorithm(path, name, sizes)
        
        report += "**Performance Benchmarks:**\n\n"
        report += "| Size | Time (ms) | Status |\n"
        report += "|------|-----------|--------|\n"
        for size, result in benchmarks.items():
            if result.get('success'):
                report += f"| {size} | {result['time_ms']:.3f} | ✓ |\n"
            else:
                report += f"| {size} | N/A | ✗ ({result.get('error', 'Error')}) |\n"
        report += "\n"
        
        # Optimization suggestions
        report += "**Optimization Suggestions:**\n\n"
        if 'sort' in name:
            report += "- Consider using built-in sort for small arrays\n"
            report += "- Optimize pivot selection for quick sort\n"
            report += "- Use insertion sort for small subarrays\n"
        elif 'search' in name:
            report += "- Ensure input is sorted for binary search\n"
            report += "- Consider interpolation search for uniform distributions\n"
        elif 'graph' in name:
            report += "- Use adjacency list for sparse graphs\n"
            report += "- Consider iterative implementation to avoid stack overflow\n"
        
        report += "\n"
    
    return report

def main():
    """Profile and optimize critical algorithms."""
    print("Profiling critical algorithms...")
    
    report = generate_optimization_report()
    report_path = ROOT / "PERFORMANCE_OPTIMIZATION_REPORT.md"
    report_path.write_text(report, encoding='utf-8')
    print(f"[OK] Generated optimization report: {report_path}")
    
    print("\n[COMPLETE] Performance analysis complete")

if __name__ == "__main__":
    main()

