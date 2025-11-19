#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Graph Algorithms - Demonstration.

This lecture covers graph algorithms including
DFS, BFS, Dijkstra, and Bellman-Ford.
"""

from typing import Dict, List, Set
from collections import deque


def dfs(graph: Dict[int, List[int]], start: int) -> List[int]:
    """Depth-first search."""
    visited: Set[int] = set()
    result: List[int] = []

    def _dfs(node: int) -> None:
        visited.add(node)
        result.append(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                _dfs(neighbor)

    _dfs(start)
    return result


def main() -> None:
    """Demonstrate graph algorithms."""
    print("=" * 70)
    print("GRAPH ALGORITHMS")
    print("=" * 70)

    graph = {0: [1, 2], 1: [2], 2: [0, 3], 3: [3]}

    result = dfs(graph, 2)
    print(f"DFS starting from 2: {result}")
    print("=" * 70)


if __name__ == "__main__":
    main()
