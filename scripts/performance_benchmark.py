#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Performance benchmarking tool.
Runs benchmarks on algorithms and stores results in database.
"""

import time
import sys
import importlib.util
from pathlib import Path
from typing import Dict, List, Tuple
import sqlite3
import tracemalloc
import statistics

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "database" / "algorithms.db"
sys.path.insert(0, str(ROOT))


def benchmark_algorithm(algorithm_path: Path, input_sizes: List[int],
                       algorithm_name: str) -> List[Dict]:
    """
    Benchmark an algorithm with different input sizes.
    
    Args:
        algorithm_path: Path to algorithm.py file
        input_sizes: List of input sizes to test
        algorithm_name: Name of the algorithm
        
    Returns:
        List of benchmark results
    """
    results = []
    
    # Import algorithm module
    spec = importlib.util.spec_from_file_location("algorithm", algorithm_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # Find main function
    func = None
    for attr_name in [algorithm_name, algorithm_name.replace('_', ''),
                     'main', 'sort', 'search']:
        if hasattr(module, attr_name):
            func = getattr(module, attr_name)
            if callable(func):
                break
    
    if not func:
        print(f"Warning: Could not find function in {algorithm_path}")
        return results
    
    for size in input_sizes:
        # Generate test data
        test_data = generate_test_data(algorithm_name, size)
        
        # Run multiple iterations
        times = []
        memory_usage = []
        
        for _ in range(5):  # 5 iterations for average
            # Time measurement
            start_time = time.perf_counter()
            
            # Memory measurement
            tracemalloc.start()
            
            try:
                if 'search' in algorithm_name.lower():
                    # For search algorithms, need target
                    result = func(test_data, test_data[len(test_data) // 2])
                else:
                    result = func(test_data)
                
                end_time = time.perf_counter()
                elapsed = (end_time - start_time) * 1000  # Convert to ms
                
                # Get memory usage
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                memory_mb = peak / (1024 * 1024)
                
                times.append(elapsed)
                memory_usage.append(memory_mb)
            except Exception as e:
                print(f"Error benchmarking {algorithm_name} with size {size}: {e}")
                tracemalloc.stop()
                break
        
        if times:
            results.append({
                'algorithm_name': algorithm_name,
                'input_size': size,
                'execution_time_ms': statistics.mean(times),
                'execution_time_std': statistics.stdev(times) if len(times) > 1 else 0,
                'memory_usage_mb': statistics.mean(memory_usage),
                'operations_per_sec': size / (statistics.mean(times) / 1000) if statistics.mean(times) > 0 else 0,
                'language': 'python'
            })
    
    return results


def generate_test_data(algorithm_name: str, size: int) -> List:
    """Generate test data for algorithm."""
    import random
    
    if 'sort' in algorithm_name.lower():
        return [random.randint(0, 1000) for _ in range(size)]
    elif 'search' in algorithm_name.lower():
        return sorted([random.randint(0, 1000) for _ in range(size)])
    elif 'graph' in algorithm_name.lower():
        # Generate simple graph
        return list(range(size))
    else:
        return list(range(size))


def store_benchmark_results(results: List[Dict]):
    """Store benchmark results in database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    for result in results:
        # Get algorithm ID
        cursor.execute('SELECT id FROM algorithms WHERE name = ?', 
                      (result['algorithm_name'],))
        row = cursor.fetchone()
        
        if row:
            algorithm_id = row[0]
            
            # Insert or update performance metric
            cursor.execute('''
                INSERT INTO performance_metrics
                (algorithm_id, input_size, execution_time_ms, memory_usage_mb,
                 operations_per_sec, language)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                algorithm_id,
                result['input_size'],
                result['execution_time_ms'],
                result['memory_usage_mb'],
                result['operations_per_sec'],
                result['language']
            ))
    
    conn.commit()
    conn.close()


def benchmark_all_algorithms(input_sizes: List[int] = [100, 500, 1000, 5000],
                            limit: int = None):
    """
    Benchmark all algorithms.
    
    Args:
        input_sizes: List of input sizes to test
        limit: Limit number of algorithms to benchmark (None for all)
    """
    algorithm_dirs = list(ROOT.rglob("*/algorithm.py"))
    
    if limit:
        algorithm_dirs = algorithm_dirs[:limit]
    
    total = len(algorithm_dirs)
    processed = 0
    
    print(f"Benchmarking {total} algorithms...")
    
    for algo_file in algorithm_dirs:
        algo_dir = algo_file.parent
        algorithm_name = algo_dir.name
        
        print(f"[{processed + 1}/{total}] Benchmarking {algorithm_name}...")
        
        try:
            results = benchmark_algorithm(algo_file, input_sizes, algorithm_name)
            if results:
                store_benchmark_results(results)
                processed += 1
        except Exception as e:
            print(f"Error benchmarking {algorithm_name}: {e}")
    
    print(f"\n[COMPLETE] Benchmarked {processed} algorithms")


if __name__ == '__main__':
    # Benchmark top 20 algorithms
    benchmark_all_algorithms(input_sizes=[100, 500, 1000], limit=20)

