#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dijkstra implementation.

This file contains the implementation of the Dijkstra algorithm.
"""

from typing import List, Optional, Dict, Set


def dijkstra(graph: Dict[int, List[tuple]], start: int) -> Dict[int, int]:
    """Dijkstra's shortest path algorithm."""
    from heapq import heappush, heappop

    distances = {node: float("inf") for node in graph}
    distances[start] = 0
    pq = [(0, start)]
    visited = set()

    while pq:
        current_dist, current = heappop(pq)
        if current in visited:
            continue
        visited.add(current)

        for neighbor, weight in graph.get(current, []):
            distance = current_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heappush(pq, (distance, neighbor))

    return distances


def main() -> None:
    """Demonstrate Dijkstra."""
    print("=" * 70)
    print("DIJKSTRA")
    print("=" * 70)

    # Example usage
    print("Algorithm implementation for Dijkstra")
    print("See implementation above for details.")

    print("=" * 70)


if __name__ == "__main__":
    main()
