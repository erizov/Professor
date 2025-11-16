#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Thread Pool Design Pattern.

Maintains a pool of worker threads that are waiting for tasks to execute.
Reuses threads to avoid the overhead of thread creation and destruction.
"""

import sys
from pathlib import Path
import threading
import queue
import time
from typing import Callable, Any, Optional
from concurrent.futures import ThreadPoolExecutor, Future

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer
from framework.logging_utils import get_logger
logger = get_logger(__name__)


# Simple Thread Pool Implementation
class ThreadPool:
    """Simple thread pool implementation."""
    
    def __init__(self, num_threads: int = 4):
        """
        Initialize thread pool.
        
        Args:
            num_threads: Number of worker threads
        """
        self.num_threads = num_threads
        self.task_queue = queue.Queue()
        self.workers: List[threading.Thread] = []
        self.shutdown_flag = False
        self._start_workers()
    
    def _start_workers(self) -> None:
        """Start worker threads."""
        for i in range(self.num_threads):
            worker = threading.Thread(
                target=self._worker,
                name=f"Worker-{i}",
                daemon=True
            )
            worker.start()
            self.workers.append(worker)
    
    def _worker(self) -> None:
        """Worker thread function."""
        while not self.shutdown_flag:
            try:
                task, args, kwargs = self.task_queue.get(timeout=1)
                try:
                    task(*args, **kwargs)
                except Exception as e:
                    logger.info(f"Error executing task: {e}")
                finally:
                    self.task_queue.task_done()
            except queue.Empty:
                continue
    
    def submit(self, task: Callable, *args, **kwargs) -> None:
        """
        Submit task to thread pool.
        
        Args:
            task: Function to execute
            *args: Positional arguments
            **kwargs: Keyword arguments
        """
        if self.shutdown_flag:
            raise RuntimeError("ThreadPool is shutdown")
        self.task_queue.put((task, args, kwargs))
    
    def shutdown(self, wait: bool = True) -> None:
        """
        Shutdown thread pool.
        
        Args:
            wait: Wait for tasks to complete
        """
        self.shutdown_flag = True
        if wait:
            self.task_queue.join()


# Task Function Examples
def cpu_intensive_task(n: int) -> int:
    """CPU intensive task."""
    result = 0
    for i in range(n):
        result += i * i
    return result


def io_task(task_id: int, duration: float) -> str:
    """I/O task (simulated)."""
    time.sleep(duration)
    return f"Task {task_id} completed"


def process_data(data: str) -> str:
    """Process data task."""
    return f"Processed: {data.upper()}"


def main() -> None:
    """Demonstration of Thread Pool Pattern."""
    logger.info("=" * 70)
    logger.info("THREAD POOL DESIGN PATTERN DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Simple Thread Pool
    logger.info("Example 1: Simple Thread Pool")
    logger.info("-" * 70)
    
    pool = ThreadPool(num_threads=3)
    
    # Submit tasks
    logger.info("Submitting 5 tasks to thread pool:")
    for i in range(5):
        task_id = i + 1
        pool.submit(io_task, task_id, 0.1)
        logger.info(f"  Submitted task {task_id}")
    
    logger.info("Waiting for tasks to complete...")
    pool.shutdown(wait=True)
    logger.info("All tasks completed!")
    logger.info()
    
    # Example 2: Using concurrent.futures.ThreadPoolExecutor
    logger.info("Example 2: Using ThreadPoolExecutor (Python Standard Library)")
    logger.info("-" * 70)
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Submit tasks and get futures
        futures = []
        for i in range(5):
            future = executor.submit(cpu_intensive_task, 100000)
            futures.append(future)
            logger.info(f"  Submitted CPU task {i+1}")
        
        # Get results
        results = []
        for i, future in enumerate(futures):
            result = future.result()
            results.append(result)
            logger.info(f"  Task {i+1} result: {result}")
    logger.info()
    
    # Example 3: I/O Bound Tasks
    logger.info("Example 3: I/O Bound Tasks")
    logger.info("-" * 70)
    
    def fetch_url(url: str) -> str:
        """Simulate URL fetch."""
        time.sleep(0.1)  # Simulate network delay
        return f"Content from {url}"
    
    urls = [f"http://example.com/page{i}" for i in range(1, 6)]
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(fetch_url, url) for url in urls]
        results = [f.result() for f in futures]
    
    elapsed = time.time() - start_time
    
    logger.info(f"Fetched {len(results)} URLs in {elapsed:.3f} seconds")
    for result in results:
        logger.info(f"  {result}")
    logger.info()
    
    # Example 4: Performance Comparison
    logger.info("Example 4: Performance Comparison (Sequential vs Thread Pool)")
    logger.info("-" * 70)
    
    tasks = [lambda: cpu_intensive_task(50000) for _ in range(10)]
    
    # Sequential execution
    timer = PerformanceTimer("Sequential")
    start = time.time()
    sequential_results = [task() for task in tasks]
    sequential_time = time.time() - start
    logger.info(f"Sequential execution: {sequential_time:.3f} seconds")
    
    # Thread pool execution
    start = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(task) for task in tasks]
        pool_results = [f.result() for f in futures]
    pool_time = time.time() - start
    logger.info(f"Thread pool execution: {pool_time:.3f} seconds")
    logger.info(f"Speedup: {sequential_time / pool_time:.2f}x")
    logger.info()
    
    # Example 5: Data Processing Pipeline
    logger.info("Example 5: Data Processing Pipeline")
    logger.info("-" * 70)
    
    data_items = [f"item{i}" for i in range(1, 6)]
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Process data in parallel
        futures = [executor.submit(process_data, item) for item in data_items]
        processed = [f.result() for f in futures]
    
    logger.info("Processed data:")
    for item in processed:
        logger.info(f"  {item}")
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nPattern Summary:")
    logger.info("\nIntent:")
    logger.info("  Maintains a pool of worker threads that are waiting for")
    logger.info("  tasks to execute. Reuses threads to avoid the overhead")
    logger.info("  of thread creation and destruction.")
    logger.info("\nKey Advantages:")
    logger.info("  - Reuses threads (reduces overhead)")
    logger.info("  - Controls resource usage")
    logger.info("  - Better performance for I/O bound tasks")
    logger.info("  - Manages thread lifecycle")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Overhead for very short tasks")
    logger.info("  - Thread context switching overhead")
    logger.info("  - Can be complex to implement")
    logger.info("\nWhen to Use:")
    logger.info("  - I/O bound operations")
    logger.info("  - Many short-lived tasks")
    logger.info("  - Need to limit concurrent threads")
    logger.info("  - Want to reuse threads")
    logger.info("\nCommon Use Cases:")
    logger.info("  - Web servers (request handling)")
    logger.info("  - Database connection pools")
    logger.info("  - File processing")
    logger.info("  - Network I/O operations")
    logger.info("  - Parallel data processing")
    logger.info("\nThread Pool Sizing:")
    logger.info("  - CPU bound: num_threads = num_cores")
    logger.info("  - I/O bound: num_threads = num_cores * (1 + wait_time/cpu_time)")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()