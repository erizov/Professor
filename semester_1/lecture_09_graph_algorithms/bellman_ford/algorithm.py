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
            print("Warning: Negative cycle detected! Path may not be valid.")
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
    print("=" * 70)
    print("BELLMAN-FORD ALGORITHM DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Basic shortest path
    print("Example 1: Basic Shortest Path Finding")
    print("-" * 70)
    
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
    
    print("Graph with negative weights (no negative cycle):")
    print("Shortest distances from vertex 0:")
    for vertex in sorted(distances.keys()):
        dist = distances[vertex]
        if dist == float('inf'):
            print(f"  To vertex {vertex}: ∞ (unreachable)")
        else:
            print(f"  To vertex {vertex}: {dist}")
    
    print(f"\nNegative cycle detected: {has_cycle}")
    print()
    
    # Example 2: Path reconstruction
    print("Example 2: Path Reconstruction")
    print("-" * 70)
    
    path = g1.shortest_path(0, 3)
    distance = g1.shortest_distance(0, 3)
    
    if path:
        print(f"Shortest path from 0 to 3: {' → '.join(map(str, path))}")
        print(f"Total distance: {distance}")
    print()
    
    # Example 3: Negative cycle detection
    print("Example 3: Negative Cycle Detection")
    print("-" * 70)
    
    g2 = Graph(4, directed=True)
    # Create a negative cycle: 1 → 2 → 3 → 1 with negative total
    g2.add_edge(0, 1, 1.0)
    g2.add_edge(1, 2, -2.0)
    g2.add_edge(2, 3, -1.0)
    g2.add_edge(3, 1, 1.0)  # Creates negative cycle
    
    distances2, _, has_cycle2 = g2.bellman_ford(0)
    
    print("Graph with negative cycle:")
    print(f"Negative cycle detected: {has_cycle2}")
    
    if has_cycle2:
        print("⚠️  Warning: Graph contains negative cycle!")
        print("   Shortest paths are undefined (can be infinitely negative)")
    else:
        print("Shortest distances:")
        for vertex in sorted(distances2.keys()):
            dist = distances2[vertex]
            if dist == float('inf'):
                print(f"  To vertex {vertex}: ∞")
            else:
                print(f"  To vertex {vertex}: {dist}")
    print()
    
    # Example 4: Comparison with Dijkstra
    print("Example 4: Bellman-Ford vs Dijkstra")
    print("-" * 70)
    
    print("Key Differences:")
    print("  Bellman-Ford:")
    print("    ✓ Works with negative weights")
    print("    ✓ Detects negative cycles")
    print("    ✗ Slower: O(V*E)")
    print("    ✗ Works on any graph structure")
    print()
    print("  Dijkstra:")
    print("    ✗ Does NOT work with negative weights")
    print("    ✗ Cannot detect negative cycles")
    print("    ✓ Faster: O((V+E) log V)")
    print("    ✓ More efficient for non-negative weights")
    print()
    print("  Recommendation:")
    print("    - Use Dijkstra for non-negative weights (faster)")
    print("    - Use Bellman-Ford for negative weights or cycle detection")
    print()
    
    # Example 5: All paths from source
    print("Example 5: All Shortest Paths from Source")
    print("-" * 70)
    
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
    
    print("All shortest paths from vertex 0:")
    for target in range(1, 6):
        path = g3.shortest_path(0, target)
        dist = distances3.get(target, float('inf'))
        
        if path:
            print(f"  0 → {target}: {' → '.join(map(str, path))} "
                  f"(distance: {dist})")
        elif dist == float('inf'):
            print(f"  0 → {target}: No path")
    print()
    
    # Example 6: Performance measurement
    print("Example 6: Performance on Different Graph Sizes")
    print("-" * 70)
    
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
        print(f"Graph with {n} vertices, {len(g_large.edges)} edges:")
        print(f"  Time: {metrics['execution_time_ms']:.3f} ms")
        print(f"  Memory: {metrics['memory_peak_kb']:.2f} KB")
    
    print()
    print("=" * 70)
    print("\nComplexity Summary:")
    print("  Time:  O(V * E) - V vertices, E edges")
    print("  Space: O(V) - distances and previous arrays")
    print("\nKey Advantages:")
    print("  - Works with negative edge weights")
    print("  - Detects negative cycles")
    print("  - Simpler than Dijkstra (no priority queue needed)")
    print("  - Works on any graph structure")
    print("\nKey Disadvantages:")
    print("  - Slower than Dijkstra for non-negative weights")
    print("  - O(V*E) time complexity")
    print("  - Less efficient for sparse graphs")
    print("\nWhen to Use:")
    print("  - Graphs with negative edge weights")
    print("  - Need to detect negative cycles")
    print("  - Currency exchange rate calculations")
    print("  - Network routing with negative costs")
    print("  - When Dijkstra cannot be used")
    print("\nWhen NOT to Use:")
    print("  - Graphs with only non-negative weights (use Dijkstra)")
    print("  - Very large graphs (consider Floyd-Warshall for all-pairs)")
    print("  - When performance is critical and weights are non-negative")
    print("\nCommon Use Cases:")
    print("  - Currency arbitrage detection")
    print("  - Network routing with negative costs")
    print("  - Distance-vector routing protocols")
    print("  - Finding longest paths (by negating weights)")
    print("  - Cycle detection in weighted graphs")
    print("\nAlgorithm Steps:")
    print("  1. Initialize distances (source = 0, others = ∞)")
    print("  2. Relax all edges (V-1) times")
    print("  3. Check for negative cycles (one more relaxation)")
    print("=" * 70)


if __name__ == "__main__":
    main()

