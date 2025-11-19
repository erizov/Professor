#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Floyd Warshall implementation.

This file contains the implementation of the Floyd Warshall algorithm.
"""

from typing import List, Optional, Dict, Set


def floyd_warshall(graph: List[List[int]], n: int) -> List[List[int]]:
    """Floyd-Warshall all-pairs shortest path algorithm."""
    dist = [row[:] for row in graph]

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] != float("inf") and dist[k][j] != float("inf"):
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

    return dist


def main() -> None:
    """Demonstrate Floyd Warshall."""
    print("=" * 70)
    print("FLOYD WARSHALL")
    print("=" * 70)

    # Example usage
    print("Algorithm implementation for Floyd Warshall")
    print("See implementation above for details.")

    print("=" * 70)


if __name__ == "__main__":
    main()
