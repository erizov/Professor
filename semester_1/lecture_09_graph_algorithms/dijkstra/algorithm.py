#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dijkstra's Algorithm implementation.

Finds shortest paths from a source vertex to all other vertices in a
weighted graph with non-negative edge weights.
"""

import sys
from pathlib import Path
from collections import defaultdict
from heapq import heappush, heappop
from typing import Dict, List, Tuple, Optional

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer
from framework.logging_utils import get_logger
logger = get_logger(__name__)


class Graph:
    """Weighted graph representation using adjacency list."""
    
    def __init__(self, directed: bool = False):
        """
        Initialize weighted graph.
        
        Args:
            directed: True for directed graph, False for undirected
        """
        self.graph: Dict[int, List[Tuple[int, float]]] = defaultdict(list)
        self.directed = directed
    
    def add_edge(self, u: int, v: int, weight: float) -> None:
        """Add weighted edge to graph."""
        self.graph[u].append((v, weight))
        if not self.directed:
            self.graph[v].append((u, weight))
    
    def dijkstra(self, start: int) -> Tuple[Dict[int, float], 
                                            Dict[int, Optional[int]]]:
        """
        Find shortest distances from start to all vertices.
        
        Args:
            start: Source vertex
            
        Returns:
            Tuple of (distances, previous) dictionaries
            - distances: shortest distance from start to each vertex
            - previous: previous vertex in shortest path
        """
        # Initialize distances
        distances: Dict[int, float] = {start: 0.0}
        previous: Dict[int, Optional[int]] = {start: None}
        
        # Priority queue: (distance, vertex)
        pq: List[Tuple[float, int]] = [(0.0, start)]
        visited: set = set()
        
        while pq:
            current_dist, current = heappop(pq)
            
            # Skip if already processed with shorter distance
            if current in visited:
                continue
            
            visited.add(current)
            
            # Relax edges
            for neighbor, weight in self.graph[current]:
                if neighbor in visited:
                    continue
                
                new_dist = current_dist + weight
                
                # Update if found shorter path
                if neighbor not in distances or new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    previous[neighbor] = current
                    heappush(pq, (new_dist, neighbor))
        
        return distances, previous
    
    def shortest_path(self, start: int, end: int) -> Optional[List[int]]:
        """
        Find shortest path from start to end.
        
        Args:
            start: Source vertex
            end: Destination vertex
            
        Returns:
            List of vertices in shortest path, or None if no path
        """
        distances, previous = self.dijkstra(start)
        
        if end not in distances:
            return None  # No path exists
        
        # Reconstruct path
        path: List[int] = []
        current = end
        
        while current is not None:
            path.append(current)
            current = previous[current]
        
        return path[::-1]
    
    def shortest_distance(self, start: int, end: int) -> Optional[float]:
        """
        Get shortest distance from start to end.
        
        Args:
            start: Source vertex
            end: Destination vertex
            
        Returns:
            Shortest distance, or None if no path
        """
        distances, _ = self.dijkstra(start)
        return distances.get(end)


def main() -> None:
    """Demonstration of Dijkstra's Algorithm."""
    logger.info("=" * 70)
    logger.info("DIJKSTRA'S ALGORITHM DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Basic shortest path
    logger.info("Example 1: Basic Shortest Path Finding")
    logger.info("-" * 70)
    
    g1 = Graph(directed=False)
    # Graph: 0-1-2-3 with weights
    g1.add_edge(0, 1, 4.0)
    g1.add_edge(1, 2, 2.0)
    g1.add_edge(2, 3, 1.0)
    g1.add_edge(0, 2, 5.0)  # Alternative path
    
    distances, previous = g1.dijkstra(0)
    
    logger.info("Graph edges (weighted):")
    logger.info("  0 --4-- 1")
    logger.info("  |       |")
    logger.info("  5       2")
    logger.info("  |       |")
    logger.info("  2 --1-- 3")
    logger.info()
    logger.info("Shortest distances from vertex 0:")
    for vertex in sorted(distances.keys()):
        logger.info(f"  To vertex {vertex}: {distances[vertex]}")
    logger.info()
    
    # Example 2: Path reconstruction
    logger.info("Example 2: Path Reconstruction")
    logger.info("-" * 70)
    
    path = g1.shortest_path(0, 3)
    distance = g1.shortest_distance(0, 3)
    
    logger.info(f"Shortest path from 0 to 3: {' → '.join(map(str, path))}")
    logger.info(f"Total distance: {distance}")
    logger.info()
    
    # Example 3: More complex graph
    logger.info("Example 3: Complex Weighted Graph")
    logger.info("-" * 70)
    
    g2 = Graph(directed=True)
    # Directed graph with multiple paths
    g2.add_edge(0, 1, 1.0)
    g2.add_edge(0, 2, 4.0)
    g2.add_edge(1, 2, 2.0)
    g2.add_edge(1, 3, 5.0)
    g2.add_edge(2, 3, 1.0)
    g2.add_edge(3, 4, 3.0)
    g2.add_edge(2, 4, 6.0)
    
    distances2, _ = g2.dijkstra(0)
    
    logger.info("Directed graph with multiple paths:")
    logger.info("Shortest distances from vertex 0:")
    for vertex in sorted(distances2.keys()):
        logger.info(f"  To vertex {vertex}: {distances2[vertex]}")
    
    # Show all paths
    logger.info("\nShortest paths:")
    for target in [1, 2, 3, 4]:
        path = g2.shortest_path(0, target)
        if path:
            logger.info(f"  0 → {target}: {' → '.join(map(str, path))} "
                  f"(distance: {distances2[target]})")
    logger.info()
    
    # Example 4: Comparison with unweighted BFS
    logger.info("Example 4: Dijkstra vs BFS (Weighted vs Unweighted)")
    logger.info("-" * 70)
    
    g3 = Graph(directed=False)
    # Same structure, but weighted
    g3.add_edge(0, 1, 10.0)  # Long edge
    g3.add_edge(0, 2, 1.0)   # Short edge
    g3.add_edge(2, 1, 1.0)   # Short edge
    
    dijkstra_dist = g3.shortest_distance(0, 1)
    logger.info(f"Graph: 0 --10-- 1, 0 --1-- 2 --1-- 1")
    logger.info(f"Dijkstra (weighted): 0 → 1 distance = {dijkstra_dist}")
    logger.info("BFS (unweighted) would find: 0 → 1 (1 hop, but wrong for weights)")
    logger.info("Dijkstra correctly finds: 0 → 2 → 1 (2 hops, but shorter total)")
    logger.info()
    
    # Example 5: Negative weights warning
    logger.info("Example 5: Important Limitation")
    logger.info("-" * 70)
    logger.info("⚠️  Dijkstra's algorithm does NOT work with negative weights!")
    logger.info("    For graphs with negative weights, use Bellman-Ford algorithm.")
    logger.info()
    
    # Example 6: Performance measurement
    logger.info("Example 6: Performance on Different Graph Sizes")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("Dijkstra's Algorithm")
    
    for n in [100, 500, 1000]:
        # Create connected graph
        g_large = Graph(directed=False)
        for i in range(n - 1):
            g_large.add_edge(i, i + 1, 1.0)
        # Add some cross edges
        for i in range(0, n - 1, 10):
            if i + 10 < n:
                g_large.add_edge(i, i + 10, 2.0)
        
        def run_dijkstra():
            return g_large.dijkstra(0)
        
        _, metrics = timer.measure(run_dijkstra)
        logger.info(f"Graph with {n} vertices:")
        logger.info(f"  Time: {metrics['execution_time_ms']:.3f} ms")
        logger.info(f"  Memory: {metrics['memory_peak_kb']:.2f} KB")
    
    logger.info()
    logger.info("=" * 70)
    logger.info("\nComplexity Summary:")
    logger.info("  Time:  O((V + E) log V) with binary heap")
    logger.info("        O(V²) with array (simpler implementation)")
    logger.info("  Space: O(V) - distances and priority queue")
    logger.info("        V = vertices, E = edges")
    logger.info("\nKey Advantages:")
    logger.info("  - Finds shortest path in weighted graphs")
    logger.info("  - Efficient with priority queue")
    logger.info("  - Works for both directed and undirected")
    logger.info("  - Single-source shortest paths")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Does NOT work with negative weights")
    logger.info("  - Slower than BFS for unweighted graphs")
    logger.info("  - Requires non-negative edge weights")
    logger.info("\nWhen to Use:")
    logger.info("  - Weighted graphs with non-negative weights")
    logger.info("  - GPS navigation (shortest route)")
    logger.info("  - Network routing")
    logger.info("  - Social network analysis (weighted connections)")
    logger.info("\nWhen NOT to Use:")
    logger.info("  - Graphs with negative weights (use Bellman-Ford)")
    logger.info("  - Unweighted graphs (use BFS - faster)")
    logger.info("  - All-pairs shortest paths (use Floyd-Warshall)")
    logger.info("\nCommon Use Cases:")
    logger.info("  - GPS navigation systems")
    logger.info("  - Network routing protocols")
    logger.info("  - Social network analysis")
    logger.info("  - Resource allocation")
    logger.info("  - Game pathfinding (with weights)")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()