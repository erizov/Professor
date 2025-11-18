#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bellman Ford implementation.

This file contains the implementation of the Bellman Ford algorithm.
"""

from typing import List, Optional, Dict, Set


def bellman_ford(graph: Dict[int, List[tuple]], start: int, n: int) -> Dict[int, int]:
    """Bellman-Ford shortest path algorithm."""
    distances = {i: float('inf') for i in range(n)}
    distances[start] = 0
    
    for _ in range(n - 1):
        for u in graph:
            for v, w in graph[u]:
                if distances[u] != float('inf') and distances[u] + w < distances[v]:
                    distances[v] = distances[u] + w
    
    return distances


def main() -> None:
    """Demonstrate Bellman Ford."""
    print("=" * 70)
    print("BELLMAN FORD")
    print("=" * 70)
    
    # Example usage
    print("Algorithm implementation for Bellman Ford")
    print("See implementation above for details.")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
