#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Breadth-First Search (BFS) implementation.

Graph traversal algorithm that explores all neighbors at current depth
before moving to next depth level.
"""

import sys
from pathlib import Path
from collections import defaultdict, deque
from typing import List, Set, Dict, Optional
import logging

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
try:
    from framework.performance_timer import PerformanceTimer
except ImportError:
    # Framework module not available - using fallback
    pass
try:
    from framework.logging_utils import get_logger
except ImportError:
    # Framework module not available - using fallback
    pass

logger = get_logger(__name__)


class Graph:
    """Graph representation using adjacency list."""

    def __init__(self, directed: bool = False):
        """
        Initialize graph.

        Args:
            directed: True for directed graph, False for undirected
        """
        self.graph: Dict[int, List[int]] = defaultdict(list)
        self.directed = directed

    def add_edge(self, u: int, v: int) -> None:
        """Add edge to graph."""
        self.graph[u].append(v)
        if not self.directed:
            self.graph[v].append(u)

    def bfs(self, start: int) -> List[int]:
        """
        Perform BFS traversal from start node.

        Args:
            start: Starting node

        Returns:
            List of nodes in BFS order
        """
        visited: Set[int] = set()
        result: List[int] = []
        queue: deque = deque([start])
        visited.add(start)

        while queue:
            node = queue.popleft()
            result.append(node)

            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return result

    def shortest_path(self, start: int, end: int) -> Optional[List[int]]:
        """
        Find shortest path using BFS.

        Args:
            start: Start node
            end: End node

        Returns:
            List representing path, or None if no path exists
        """
        if start == end:
            return [start]

        visited: Set[int] = {start}
        queue: deque = deque([(start, [start])])

        while queue:
            node, path = queue.popleft()

            for neighbor in self.graph[node]:
                if neighbor == end:
                    return path + [neighbor]

                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return None  # No path found

    def shortest_distance(self, start: int, end: int) -> int:
        """
        Find shortest distance (number of edges) using BFS.

        Args:
            start: Start node
            end: End node

        Returns:
            Distance, or -1 if no path
        """
        if start == end:
            return 0

        visited: Set[int] = {start}
        queue: deque = deque([(start, 0)])

        while queue:
            node, dist = queue.popleft()

            for neighbor in self.graph[node]:
                if neighbor == end:
                    return dist + 1

                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))

        return -1  # No path

    def all_paths_distance(self, start: int) -> Dict[int, int]:
        """
        Find shortest distance from start to all reachable nodes.

        Args:
            start: Starting node

        Returns:
            Dictionary mapping node to distance
        """
        distances: Dict[int, int] = {start: 0}
        queue: deque = deque([start])

        while queue:
            node = queue.popleft()
            current_dist = distances[node]

            for neighbor in self.graph[node]:
                if neighbor not in distances:
                    distances[neighbor] = current_dist + 1
                    queue.append(neighbor)

        return distances

    def is_bipartite(self) -> bool:
        """
        Check if graph is bipartite using BFS.

        Returns:
            True if bipartite, False otherwise
        """
        # Color nodes with 0 and 1
        colors: Dict[int, int] = {}

        # Get all nodes
        all_nodes = set(self.graph.keys())
        for neighbors in self.graph.values():
            all_nodes.update(neighbors)

        # Check each component
        for start_node in all_nodes:
            if start_node in colors:
                continue

            # BFS coloring
            queue: deque = deque([start_node])
            colors[start_node] = 0

            while queue:
                node = queue.popleft()
                current_color = colors[node]
                next_color = 1 - current_color

                for neighbor in self.graph[node]:
                    if neighbor not in colors:
                        colors[neighbor] = next_color
                        queue.append(neighbor)
                    elif colors[neighbor] != next_color:
                        return False  # Adjacent nodes same color

        return True


def main() -> None:
    """Demonstration of BFS."""
    logger.info("=" * 70)
    logger.info("BREADTH-FIRST SEARCH (BFS) DEMONSTRATION")
    logger.info("=" * 70)
    logger.info("")

    # Example 1: Basic BFS
    logger.info("Example 1: Basic BFS Traversal")
    logger.info("-" * 70)

    g1 = Graph(directed=False)
    edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]

    for u, v in edges:
        g1.add_edge(u, v)

    logger.info("Graph edges: %s", edges)
    logger.info(f"BFS from node 0: {g1.bfs(0)}")
    logger.info("Note: BFS visits level by level")
    logger.info("")

    # Example 2: Shortest path
    logger.info("Example 2: Finding Shortest Path")
    logger.info("-" * 70)

    g2 = Graph(directed=False)
    g2.add_edge(0, 1)
    g2.add_edge(0, 2)
    g2.add_edge(1, 3)
    g2.add_edge(2, 3)
    g2.add_edge(3, 4)
    g2.add_edge(1, 4)

    path = g2.shortest_path(0, 4)
    dist = g2.shortest_distance(0, 4)
    logger.info(f"Shortest path from 0 to 4: {path}")
    logger.info(f"Distance: {dist} edges")

    # Alternative path
    alt_path = g2.shortest_path(0, 3)
    logger.info(f"Shortest path from 0 to 3: {alt_path}")
    logger.info("")

    # Example 3: All distances from source
    logger.info("Example 3: Distances to All Nodes")
    logger.info("-" * 70)

    g3 = Graph(directed=False)
    g3.add_edge(0, 1)
    g3.add_edge(0, 2)
    g3.add_edge(1, 3)
    g3.add_edge(2, 4)
    g3.add_edge(3, 5)
    g3.add_edge(4, 5)

    distances = g3.all_paths_distance(0)
    logger.info("Distances from node 0:")
    for node, dist in sorted(distances.items()):
        logger.info(f"  Node {node}: distance = {dist}")
    logger.info("")

    # Example 4: Bipartite check
    logger.info("Example 4: Bipartite Graph Detection")
    logger.info("-" * 70)

    # Bipartite graph (alternating colors possible)
    g4_bi = Graph(directed=False)
    g4_bi.add_edge(0, 1)
    g4_bi.add_edge(0, 3)
    g4_bi.add_edge(1, 2)
    g4_bi.add_edge(3, 2)

    logger.info("Graph 1: [(0,1), (0,3), (1,2), (3,2)]")
    logger.info(f"Is bipartite: {g4_bi.is_bipartite()}")

    # Not bipartite (odd cycle)
    g4_not = Graph(directed=False)
    g4_not.add_edge(0, 1)
    g4_not.add_edge(1, 2)
    g4_not.add_edge(2, 0)  # Triangle

    logger.info("\nGraph 2: [(0,1), (1,2), (2,0)] - Triangle")
    logger.info(f"Is bipartite: {g4_not.is_bipartite()}")
    logger.info("")

    # Example 5: BFS on directed graph
    logger.info("Example 5: BFS on Directed Graph")
    logger.info("-" * 70)

    g5 = Graph(directed=True)
    g5.add_edge(0, 1)
    g5.add_edge(0, 2)
    g5.add_edge(1, 2)
    g5.add_edge(2, 3)
    g5.add_edge(1, 3)

    logger.info("Directed edges: 0→1, 0→2, 1→2, 2→3, 1→3")
    logger.info(f"BFS from 0: {g5.bfs(0)}")
    logger.info("")

    # Example 6: Level-order traversal
    logger.info("Example 6: Level-Order Grouping")
    logger.info("-" * 70)

    g6 = Graph(directed=False)
    g6.add_edge(0, 1)
    g6.add_edge(0, 2)
    g6.add_edge(1, 3)
    g6.add_edge(1, 4)
    g6.add_edge(2, 5)

    # Group by levels
    distances = g6.all_paths_distance(0)
    levels: Dict[int, List[int]] = defaultdict(list)
    for node, dist in distances.items():
        levels[dist].append(node)

    logger.info("Nodes grouped by level:")
    for level in sorted(levels.keys()):
        logger.info(f"  Level {level}: {levels[level]}")
    logger.info("")

    # Example 7: Performance measurement
    logger.info("Example 7: Performance on Different Graph Sizes")
    logger.info("-" * 70)

    timer = PerformanceTimer("BFS")

    for n in [100, 1000, 5000]:
        # Create connected graph
        g_large = Graph(directed=False)
        for i in range(n - 1):
            g_large.add_edge(i, i + 1)

        _, metrics = timer.measure(g_large.bfs, 0)
        logger.info(f"Graph with {n} nodes:")
        logger.info(f"  Time: {metrics['execution_time_ms']:.3f} ms")

    logger.info("")
    logger.info("=" * 70)
    logger.info("\nComplexity Summary:")
    logger.info("  Time:  O(V + E) - V vertices, E edges")
    logger.info("  Space: O(V) - queue storage")
    logger.info("\nKey Advantages:")
    logger.info("  - Finds shortest path (unweighted)")
    logger.info("  - Level-order traversal")
    logger.info("  - Good for nearby nodes")
    logger.info("  - Iterative (no stack overflow)")
    logger.info("\nKey Disadvantages:")
    logger.info("  - More memory than DFS")
    logger.info("  - Not suitable for deep graphs")
    logger.info("  - Queue operations overhead")
    logger.info("\nBFS vs DFS:")
    logger.info("  - BFS: Shortest path, level-order")
    logger.info("  - DFS: Memory efficient, path exists")
    logger.info("  - Choose based on problem needs")
    logger.info("\nCommon Use Cases:")
    logger.info("  - Shortest path (unweighted)")
    logger.info("  - Level-order traversal")
    logger.info("  - Bipartite checking")
    logger.info("  - Finding connected components")
    logger.info("  - Web crawling")
    logger.info("  - Social network analysis")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()
