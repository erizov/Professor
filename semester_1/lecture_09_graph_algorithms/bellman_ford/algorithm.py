#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bellman-Ford Algorithm implementation.

Finds shortest paths from a source vertex to all other vertices in a
weighted graph. Can handle negative edge weights and detect negative cycles.
"""

import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer
from framework.logging_utils import get_logger
logger = get_logger(__name__)


class Edge:
    """Represents a weighted edge."""
    
    def __init__(self, u: int, v: int, weight: float):
        self.u = u
        self.v = v
        self.weight = weight
    
    def __repr__(self) -> str:
        return f"({self.u} → {self.v}, w={self.weight})"


class Graph:
    """Weighted graph representation using edge list."""
    
    def __init__(self, num_vertices: int, directed: bool = True):
        """
        Initialize graph.
        
        Args:
            num_vertices: Number of vertices
            directed: True for directed graph, False for undirected
        """
        self.num_vertices = num_vertices
        self.edges: List[Edge] = []
        self.directed = directed
    
    def add_edge(self, u: int, v: int, weight: float) -> None:
        """Add weighted edge to graph."""
        self.edges.append(Edge(u, v, weight))
        if not self.directed:
            self.edges.append(Edge(v, u, weight))
    
    def bellman_ford(self, start: int) -> Tuple[Dict[int, float], 
                                                Dict[int, Optional[int]], 
                                                bool]:
        """
        Find shortest distances using Bellman-Ford algorithm.
        
        Args:
            start: Source vertex
            
        Returns:
            Tuple of (distances, previous, has_negative_cycle)
            - distances: shortest distance from start to each vertex
            - previous: previous vertex in shortest path
            - has_negative_cycle: True if negative cycle detected
        """
        # Initialize distances
        distances: Dict[int, float] = {start: 0.0}
        previous: Dict[int, Optional[int]] = {start: None}
        
        # Initialize all other distances to infinity
        for i in range(self.num_vertices):
            if i != start:
                distances[i] = float('inf')
        
        # Relax edges (V-1) times
        for _ in range(self.num_vertices - 1):
            for edge in self.edges:
                u, v, weight = edge.u, edge.v, edge.weight
                
                if distances[u] != float('inf'):
                    new_dist = distances[u] + weight
                    
                    if new_dist < distances[v]:
                        distances[v] = new_dist
                        previous[v] = u
        
        # Check for negative cycles
        has_negative_cycle = False
        for edge in self.edges:
            u, v, weight = edge.u, edge.v, edge.weight
            
            if distances[u] != float('inf'):
                if distances[u] + weight < distances[v]:
                    has_negative_cycle = True
                    break
        
        return distances, previous, has_negative_cycle
    
    def shortest_path(self, start: int, end: int) -> Optional[List[int]]:
        """
        Find shortest path from start to end.
        
        Args:
            start: Source vertex
            end: Destination vertex
            
        Returns:
            List of vertices in shortest path, or None if no path or
            negative cycle detected
        """
        distances, previous, has_negative_cycle = self.bellman_ford(start)
        
        if has_negative_cycle:
            logger.info("Warning: Negative cycle detected! Path may not be valid.")
            return None
        
        if end not in distances or distances[end] == float('inf'):
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
            Shortest distance, or None if no path or negative cycle
        """
        distances, _, has_negative_cycle = self.bellman_ford(start)
        
        if has_negative_cycle:
            return None
        
        dist = distances.get(end)
        return dist if dist != float('inf') else None


def main() -> None:
    """Demonstration of Bellman-Ford Algorithm."""
    logger.info("=" * 70)
    logger.info("BELLMAN-FORD ALGORITHM DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Basic shortest path
    logger.info("Example 1: Basic Shortest Path Finding")
    logger.info("-" * 70)
    
    g1 = Graph(5, directed=True)
    g1.add_edge(0, 1, -1.0)
    g1.add_edge(0, 2, 4.0)
    g1.add_edge(1, 2, 3.0)
    g1.add_edge(1, 3, 2.0)
    g1.add_edge(1, 4, 2.0)
    g1.add_edge(3, 2, 5.0)
    g1.add_edge(3, 1, 1.0)
    g1.add_edge(4, 3, -3.0)
    
    distances, previous, has_cycle = g1.bellman_ford(0)
    
    logger.info("Graph with negative weights (no negative cycle):")
    logger.info("Shortest distances from vertex 0:")
    for vertex in sorted(distances.keys()):
        dist = distances[vertex]
        if dist == float('inf'):
            logger.info(f"  To vertex {vertex}: ∞ (unreachable)")
        else:
            logger.info(f"  To vertex {vertex}: {dist}")
    
    logger.info(f"\nNegative cycle detected: {has_cycle}")
    logger.info()
    
    # Example 2: Path reconstruction
    logger.info("Example 2: Path Reconstruction")
    logger.info("-" * 70)
    
    path = g1.shortest_path(0, 3)
    distance = g1.shortest_distance(0, 3)
    
    if path:
        logger.info(f"Shortest path from 0 to 3: {' → '.join(map(str, path))}")
        logger.info(f"Total distance: {distance}")
    logger.info()
    
    # Example 3: Negative cycle detection
    logger.info("Example 3: Negative Cycle Detection")
    logger.info("-" * 70)
    
    g2 = Graph(4, directed=True)
    # Create a negative cycle: 1 → 2 → 3 → 1 with negative total
    g2.add_edge(0, 1, 1.0)
    g2.add_edge(1, 2, -2.0)
    g2.add_edge(2, 3, -1.0)
    g2.add_edge(3, 1, 1.0)  # Creates negative cycle
    
    distances2, _, has_cycle2 = g2.bellman_ford(0)
    
    logger.info("Graph with negative cycle:")
    logger.info(f"Negative cycle detected: {has_cycle2}")
    
    if has_cycle2:
        logger.info("⚠️  Warning: Graph contains negative cycle!")
        logger.info("   Shortest paths are undefined (can be infinitely negative)")
    else:
        logger.info("Shortest distances:")
        for vertex in sorted(distances2.keys()):
            dist = distances2[vertex]
            if dist == float('inf'):
                logger.info(f"  To vertex {vertex}: ∞")
            else:
                logger.info(f"  To vertex {vertex}: {dist}")
    logger.info()
    
    # Example 4: Comparison with Dijkstra
    logger.info("Example 4: Bellman-Ford vs Dijkstra")
    logger.info("-" * 70)
    
    logger.info("Key Differences:")
    logger.info("  Bellman-Ford:")
    logger.info("    ✓ Works with negative weights")
    logger.info("    ✓ Detects negative cycles")
    logger.info("    ✗ Slower: O(V*E)")
    logger.info("    ✗ Works on any graph structure")
    logger.info()
    logger.info("  Dijkstra:")
    logger.info("    ✗ Does NOT work with negative weights")
    logger.info("    ✗ Cannot detect negative cycles")
    logger.info("    ✓ Faster: O((V+E) log V)")
    logger.info("    ✓ More efficient for non-negative weights")
    logger.info()
    logger.info("  Recommendation:")
    logger.info("    - Use Dijkstra for non-negative weights (faster)")
    logger.info("    - Use Bellman-Ford for negative weights or cycle detection")
    logger.info()
    
    # Example 5: All paths from source
    logger.info("Example 5: All Shortest Paths from Source")
    logger.info("-" * 70)
    
    g3 = Graph(6, directed=True)
    g3.add_edge(0, 1, 5.0)
    g3.add_edge(0, 2, 3.0)
    g3.add_edge(1, 3, 6.0)
    g3.add_edge(1, 4, -4.0)
    g3.add_edge(2, 1, -2.0)
    g3.add_edge(2, 4, 4.0)
    g3.add_edge(3, 5, 2.0)
    g3.add_edge(4, 3, 1.0)
    g3.add_edge(4, 5, -2.0)
    
    distances3, _, has_cycle3 = g3.bellman_ford(0)
    
    logger.info("All shortest paths from vertex 0:")
    for target in range(1, 6):
        path = g3.shortest_path(0, target)
        dist = distances3.get(target, float('inf'))
        
        if path:
            logger.info(f"  0 → {target}: {' → '.join(map(str, path))} "
                  f"(distance: {dist})")
        elif dist == float('inf'):
            logger.info(f"  0 → {target}: No path")
    logger.info()
    
    # Example 6: Performance measurement
    logger.info("Example 6: Performance on Different Graph Sizes")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("Bellman-Ford Algorithm")
    
    for n in [50, 100, 200]:
        # Create graph with n vertices
        g_large = Graph(n, directed=True)
        # Add edges to create connected graph
        for i in range(n - 1):
            g_large.add_edge(i, i + 1, 1.0)
        # Add some cross edges
        for i in range(0, n - 1, 5):
            if i + 5 < n:
                g_large.add_edge(i, i + 5, -0.5)
        
        def run_bellman_ford():
            return g_large.bellman_ford(0)
        
        _, metrics = timer.measure(run_bellman_ford)
        logger.info(f"Graph with {n} vertices, {len(g_large.edges)} edges:")
        logger.info(f"  Time: {metrics['execution_time_ms']:.3f} ms")
        logger.info(f"  Memory: {metrics['memory_peak_kb']:.2f} KB")
    
    logger.info()
    logger.info("=" * 70)
    logger.info("\nComplexity Summary:")
    logger.info("  Time:  O(V * E) - V vertices, E edges")
    logger.info("  Space: O(V) - distances and previous arrays")
    logger.info("\nKey Advantages:")
    logger.info("  - Works with negative edge weights")
    logger.info("  - Detects negative cycles")
    logger.info("  - Simpler than Dijkstra (no priority queue needed)")
    logger.info("  - Works on any graph structure")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Slower than Dijkstra for non-negative weights")
    logger.info("  - O(V*E) time complexity")
    logger.info("  - Less efficient for sparse graphs")
    logger.info("\nWhen to Use:")
    logger.info("  - Graphs with negative edge weights")
    logger.info("  - Need to detect negative cycles")
    logger.info("  - Currency exchange rate calculations")
    logger.info("  - Network routing with negative costs")
    logger.info("  - When Dijkstra cannot be used")
    logger.info("\nWhen NOT to Use:")
    logger.info("  - Graphs with only non-negative weights (use Dijkstra)")
    logger.info("  - Very large graphs (consider Floyd-Warshall for all-pairs)")
    logger.info("  - When performance is critical and weights are non-negative")
    logger.info("\nCommon Use Cases:")
    logger.info("  - Currency arbitrage detection")
    logger.info("  - Network routing with negative costs")
    logger.info("  - Distance-vector routing protocols")
    logger.info("  - Finding longest paths (by negating weights)")
    logger.info("  - Cycle detection in weighted graphs")
    logger.info("\nAlgorithm Steps:")
    logger.info("  1. Initialize distances (source = 0, others = ∞)")
    logger.info("  2. Relax all edges (V-1) times")
    logger.info("  3. Check for negative cycles (one more relaxation)")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()