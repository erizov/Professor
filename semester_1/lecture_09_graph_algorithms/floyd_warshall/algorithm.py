#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Floyd-Warshall Algorithm implementation.

Finds shortest paths between all pairs of vertices in a weighted graph.
Can handle negative edge weights (but not negative cycles).
"""

import sys
from pathlib import Path
from typing import List, Tuple, Optional

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer
from framework.logging_utils import get_logger
logger = get_logger(__name__)


class Graph:
    """Weighted graph representation using adjacency matrix."""
    
    def __init__(self, num_vertices: int, directed: bool = True):
        """
        Initialize graph with adjacency matrix.
        
        Args:
            num_vertices: Number of vertices
            directed: True for directed graph, False for undirected
        """
        self.num_vertices = num_vertices
        self.directed = directed
        # Initialize with infinity (no edge)
        self.distances: List[List[float]] = [
            [float('inf')] * num_vertices for _ in range(num_vertices)
        ]
        # Initialize diagonal (distance to self is 0)
        for i in range(num_vertices):
            self.distances[i][i] = 0.0
        # For path reconstruction
        self.next_vertex: List[List[Optional[int]]] = [
            [None] * num_vertices for _ in range(num_vertices)
        ]
    
    def add_edge(self, u: int, v: int, weight: float) -> None:
        """Add weighted edge to graph."""
        self.distances[u][v] = weight
        self.next_vertex[u][v] = v
        if not self.directed:
            self.distances[v][u] = weight
            self.next_vertex[v][u] = u
    
    def floyd_warshall(self) -> Tuple[List[List[float]], bool]:
        """
        Find shortest distances between all pairs of vertices.
        
        Returns:
            Tuple of (distances, has_negative_cycle)
            - distances: 2D matrix of shortest distances
            - has_negative_cycle: True if negative cycle detected
        """
        # Create copy of distances
        dist = [row[:] for row in self.distances]
        
        # Floyd-Warshall algorithm
        for k in range(self.num_vertices):
            for i in range(self.num_vertices):
                for j in range(self.num_vertices):
                    # If path through k is shorter
                    if dist[i][k] != float('inf') and \
                       dist[k][j] != float('inf'):
                        if dist[i][j] > dist[i][k] + dist[k][j]:
                            dist[i][j] = dist[i][k] + dist[k][j]
                            self.next_vertex[i][j] = self.next_vertex[i][k]
        
        # Check for negative cycles
        has_negative_cycle = False
        for i in range(self.num_vertices):
            if dist[i][i] < 0:
                has_negative_cycle = True
                break
        
        return dist, has_negative_cycle
    
    def shortest_path(self, start: int, end: int) -> Optional[List[int]]:
        """
        Reconstruct shortest path from start to end.
        
        Args:
            start: Source vertex
            end: Destination vertex
            
        Returns:
            List of vertices in shortest path, or None if no path
        """
        dist, has_cycle = self.floyd_warshall()
        
        if has_cycle:
            logger.info("Warning: Negative cycle detected!")
            return None
        
        if dist[start][end] == float('inf'):
            return None  # No path exists
        
        # Reconstruct path
        if self.next_vertex[start][end] is None:
            return [start] if start == end else None
        
        path = [start]
        current = start
        
        while current != end:
            current = self.next_vertex[current][end]
            path.append(current)
        
        return path
    
    def shortest_distance(self, start: int, end: int) -> Optional[float]:
        """
        Get shortest distance from start to end.
        
        Args:
            start: Source vertex
            end: Destination vertex
            
        Returns:
            Shortest distance, or None if no path or negative cycle
        """
        dist, has_cycle = self.floyd_warshall()
        
        if has_cycle:
            return None
        
        d = dist[start][end]
        return d if d != float('inf') else None


def main() -> None:
    """Demonstration of Floyd-Warshall Algorithm."""
    logger.info("=" * 70)
    logger.info("FLOYD-WARSHALL ALGORITHM DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Basic all-pairs shortest paths
    logger.info("Example 1: All-Pairs Shortest Paths")
    logger.info("-" * 70)
    
    g1 = Graph(4, directed=True)
    g1.add_edge(0, 1, 3.0)
    g1.add_edge(0, 3, 7.0)
    g1.add_edge(1, 0, 8.0)
    g1.add_edge(1, 2, 2.0)
    g1.add_edge(2, 0, 5.0)
    g1.add_edge(2, 3, 1.0)
    g1.add_edge(3, 0, 2.0)
    
    distances, has_cycle = g1.floyd_warshall()
    
    logger.info("Shortest distances between all pairs:")
    logger.info("    ")
    for j in range(4):
        logger.info(f"  {j}")
    logger.info()
    
    for i in range(4):
        logger.info(f"  {i}:")
        for j in range(4):
            dist = distances[i][j]
            if dist == float('inf'):
                logger.info("  ∞")
            else:
                logger.info(f" {dist:3.0f}")
        logger.info()
    logger.info()
    
    # Example 2: Path reconstruction
    logger.info("Example 2: Path Reconstruction")
    logger.info("-" * 70)
    
    paths_to_show = [(0, 3), (1, 0), (2, 3)]
    for start, end in paths_to_show:
        path = g1.shortest_path(start, end)
        distance = g1.shortest_distance(start, end)
        if path:
            logger.info(f"Path from {start} to {end}: "
                  f"{' → '.join(map(str, path))} "
                  f"(distance: {distance})")
    logger.info()
    
    # Example 3: Comparison with Dijkstra
    logger.info("Example 3: Floyd-Warshall vs Dijkstra vs Bellman-Ford")
    logger.info("-" * 70)
    
    logger.info("Algorithm Comparison:")
    logger.info("  Floyd-Warshall:")
    logger.info("    ✓ All-pairs shortest paths")
    logger.info("    ✓ Works with negative weights (no cycles)")
    logger.info("    ✗ O(V³) time complexity")
    logger.info("    ✗ O(V²) space complexity")
    logger.info()
    logger.info("  Dijkstra (run V times):")
    logger.info("    ✓ All-pairs shortest paths")
    logger.info("    ✗ Does NOT work with negative weights")
    logger.info("    ✓ O(V * (V + E) log V) - better for sparse graphs")
    logger.info()
    logger.info("  Bellman-Ford (run V times):")
    logger.info("    ✓ All-pairs shortest paths")
    logger.info("    ✓ Works with negative weights")
    logger.info("    ✗ O(V² * E) - slower than Floyd-Warshall")
    logger.info()
    logger.info("  Recommendation:")
    logger.info("    - Use Floyd-Warshall for dense graphs or all-pairs")
    logger.info("    - Use Dijkstra for sparse graphs with non-negative weights")
    logger.info("    - Use Bellman-Ford for sparse graphs with negative weights")
    logger.info()
    
    # Example 4: Negative weights (no cycle)
    logger.info("Example 4: Graph with Negative Weights (No Cycle)")
    logger.info("-" * 70)
    
    g2 = Graph(4, directed=True)
    g2.add_edge(0, 1, 1.0)
    g2.add_edge(0, 2, 4.0)
    g2.add_edge(1, 2, -3.0)  # Negative weight
    g2.add_edge(1, 3, 2.0)
    g2.add_edge(2, 3, 3.0)
    
    distances2, has_cycle2 = g2.floyd_warshall()
    
    logger.info("Graph with negative weights (no negative cycle):")
    logger.info(f"Negative cycle detected: {has_cycle2}")
    logger.info("Shortest distances:")
    for i in range(4):
        for j in range(4):
            if i != j:
                dist = distances2[i][j]
                if dist != float('inf'):
                    logger.info(f"  {i} → {j}: {dist}")
    logger.info()
    
    # Example 5: Negative cycle detection
    logger.info("Example 5: Negative Cycle Detection")
    logger.info("-" * 70)
    
    g3 = Graph(3, directed=True)
    g3.add_edge(0, 1, 1.0)
    g3.add_edge(1, 2, -3.0)
    g3.add_edge(2, 0, 2.0)  # Creates negative cycle
    
    distances3, has_cycle3 = g3.floyd_warshall()
    
    logger.info("Graph with negative cycle:")
    logger.info(f"Negative cycle detected: {has_cycle3}")
    if has_cycle3:
        logger.info("⚠️  Warning: Graph contains negative cycle!")
        logger.info("   Shortest paths are undefined")
    logger.info()
    
    # Example 6: Performance measurement
    logger.info("Example 6: Performance on Different Graph Sizes")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("Floyd-Warshall Algorithm")
    
    for n in [10, 20, 50]:
        g_large = Graph(n, directed=True)
        # Create connected graph
        for i in range(n):
            for j in range(n):
                if i != j and (i + j) % 3 == 0:
                    g_large.add_edge(i, j, float(i + j))
        
        _, metrics = timer.measure(g_large.floyd_warshall)
        logger.info(f"Graph with {n} vertices:")
        logger.info(f"  Time: {metrics['execution_time_ms']:.3f} ms")
        logger.info(f"  Memory: {metrics['memory_peak_kb']:.2f} KB")
        logger.info(f"  Note: O(V³) complexity - grows quickly!")
    
    logger.info()
    logger.info("=" * 70)
    logger.info("\nComplexity Summary:")
    logger.info("  Time:  O(V³) - V vertices")
    logger.info("  Space: O(V²) - distance matrix")
    logger.info("\nKey Advantages:")
    logger.info("  - Finds all-pairs shortest paths in one run")
    logger.info("  - Works with negative edge weights (no cycles)")
    logger.info("  - Simple implementation")
    logger.info("  - Good for dense graphs")
    logger.info("\nKey Disadvantages:")
    logger.info("  - O(V³) time complexity (slow for large graphs)")
    logger.info("  - O(V²) space complexity")
    logger.info("  - Cannot handle negative cycles")
    logger.info("  - Less efficient than Dijkstra for sparse graphs")
    logger.info("\nWhen to Use:")
    logger.info("  - Need all-pairs shortest paths")
    logger.info("  - Dense graphs")
    logger.info("  - Graphs with negative weights (no cycles)")
    logger.info("  - Small to medium graphs (V < 1000)")
    logger.info("\nWhen NOT to Use:")
    logger.info("  - Very large graphs (V > 1000)")
    logger.info("  - Sparse graphs (use Dijkstra instead)")
    logger.info("  - Only need single-source shortest paths")
    logger.info("  - Graphs with negative cycles")
    logger.info("\nCommon Use Cases:")
    logger.info("  - Network routing (all pairs)")
    logger.info("  - Social network analysis (shortest paths)")
    logger.info("  - Transportation networks")
    logger.info("  - Game pathfinding (precomputed paths)")
    logger.info("  - Distance matrix computation")
    logger.info("\nAlgorithm Steps:")
    logger.info("  1. Initialize distance matrix (direct edges)")
    logger.info("  2. For each intermediate vertex k:")
    logger.info("     For each pair (i, j):")
    logger.info("       Update: dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])")
    logger.info("  3. Check for negative cycles (diagonal < 0)")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()