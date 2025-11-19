#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data Parallelism implementation.

This file contains the implementation of the Data Parallelism algorithm.
"""

from typing import List, Optional, Dict, Set


class DataParallelism:
    """Data parallelism implementation."""

    def __init__(self, num_workers: int = 4):
        self.num_workers = num_workers

    def parallel_map(self, func: callable, data: List[any]) -> List[any]:
        """Parallel map operation."""
        from concurrent.futures import ThreadPoolExecutor

        with ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            results = list(executor.map(func, data))
        return results

    def parallel_reduce(
        self, func: callable, data: List[any], initial: any = None
    ) -> any:
        """Parallel reduce operation."""
        chunks = [data[i :: self.num_workers] for i in range(self.num_workers)]
        from concurrent.futures import ThreadPoolExecutor

        with ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            chunk_results = list(
                executor.map(
                    lambda chunk: self._reduce_chunk(func, chunk, initial), chunks
                )
            )
        result = initial
        for chunk_result in chunk_results:
            result = func(result, chunk_result)
        return result

    def _reduce_chunk(self, func: callable, chunk: List[any], initial: any) -> any:
        """Reduce single chunk."""
        result = initial
        for item in chunk:
            result = func(result, item)
        return result


def main() -> None:
    """Demonstrate Data Parallelism."""
    print("=" * 70)
    print("DATA PARALLELISM")
    print("=" * 70)

    # Example usage
    print("Algorithm implementation for Data Parallelism")
    print("See implementation above for details.")

    print("=" * 70)


if __name__ == "__main__":
    main()
