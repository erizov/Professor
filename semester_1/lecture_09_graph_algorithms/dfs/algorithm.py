#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Depth-First Search (DFS) implementation.

Graph traversal algorithm that explores as far as possible along each
branch before backtracking.
"""

import sys
from pathlib import Path
from collections import defaultdict
from typing import List, Set, Dict, Callable

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer


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
    
    def dfs(self, start: int, 
            visit_callback: Callable[[int], None] = None) -> List[int]:
        """
        Perform DFS traversal from start node.
        
        Args:
            start: Starting node
            visit_callback: Optional callback for each visited node
            
        Returns:
            List of nodes in DFS order
        """
        visited: Set[int] = set()
        result: List[int] = []
        
        def dfs_recursive(node: int) -> None:
            visited.add(node)
            result.append(node)
            
            if visit_callback:
                visit_callback(node)
            
            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    dfs_recursive(neighbor)
        
        dfs_recursive(start)
        return result
    
    def dfs_iterative(self, start: int) -> List[int]:
        """
        Iterative DFS using explicit stack.
        
        Args:
            start: Starting node
            
        Returns:
            List of nodes in DFS order
        """
        visited: Set[int] = set()
        result: List[int] = []
        stack: List[int] = [start]
        
        while stack:
            node = stack.pop()
            
            if node not in visited:
                visited.add(node)
                result.append(node)
                
                # Add neighbors in reverse order for consistent ordering
                for neighbor in reversed(self.graph[node]):
                    if neighbor not in visited:
                        stack.append(neighbor)
        
        return result
    
    def dfs_all(self) -> List[List[int]]:
        """
        Perform DFS on all connected components.
        
        Returns:
            List of components (each component is a list of nodes)
        """
        visited: Set[int] = set()
        components: List[List[int]] = []
        
        def dfs_component(node: int, component: List[int]) -> None:
            visited.add(node)
            component.append(node)
            
            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    dfs_component(neighbor, component)
        
        # Visit all nodes
        all_nodes = set(self.graph.keys())
        for node in self.graph.values():
            all_nodes.update(node)
        
        for node in all_nodes:
            if node not in visited:
                component: List[int] = []
                dfs_component(node, component)
                components.append(component)
        
        return components
    
    def has_cycle(self) -> bool:
        """
        Detect cycle using DFS.
        
        Returns:
            True if cycle exists, False otherwise
        """
        visited: Set[int] = set()
        rec_stack: Set[int] = set()
        
        def has_cycle_util(node: int, parent: int = -1) -> bool:
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    if has_cycle_util(neighbor, node):
                        return True
                elif neighbor != parent:  # For undirected graphs
                    return True
            
            rec_stack.remove(node)
            return False
        
        all_nodes = set(self.graph.keys())
        for node in all_nodes:
            if node not in visited:
                if has_cycle_util(node):
                    return True
        
        return False
    
    def topological_sort(self) -> List[int]:
        """
        Topological sort using DFS (only for DAG).
        
        Returns:
            Topologically sorted list of nodes
        """
        if not self.directed:
            raise ValueError("Topological sort only for directed graphs")
        
        visited: Set[int] = set()
        stack: List[int] = []
        
        def topological_sort_util(node: int) -> None:
            visited.add(node)
            
            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    topological_sort_util(neighbor)
            
            stack.append(node)
        
        all_nodes = set(self.graph.keys())
        for node in all_nodes:
            if node not in visited:
                topological_sort_util(node)
        
        return stack[::-1]


def main() -> None:
    """Demonstration of DFS."""
    print("=" * 70)
    print("DEPTH-FIRST SEARCH (DFS) DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Basic DFS on undirected graph
    print("Example 1: Basic DFS on Undirected Graph")
    print("-" * 70)
    
    g1 = Graph(directed=False)
    edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]
    
    for u, v in edges:
        g1.add_edge(u, v)
    
    print("Graph edges:", edges)
    print(f"DFS from node 0 (recursive): {g1.dfs(0)}")
    print(f"DFS from node 0 (iterative): {g1.dfs_iterative(0)}")
    print()
    
    # Example 2: DFS on directed graph
    print("Example 2: DFS on Directed Graph")
    print("-" * 70)
    
    g2 = Graph(directed=True)
    edges2 = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)]
    
    for u, v in edges2:
        g2.add_edge(u, v)
    
    print("Graph edges:", edges2)
    print(f"DFS from node 0: {g2.dfs(0)}")
    print()
    
    # Example 3: Connected components
    print("Example 3: Finding Connected Components")
    print("-" * 70)
    
    g3 = Graph(directed=False)
    # Two separate components
    g3.add_edge(0, 1)
    g3.add_edge(1, 2)
    g3.add_edge(3, 4)
    g3.add_edge(4, 5)
    g3.add_edge(4, 6)
    
    components = g3.dfs_all()
    print(f"Number of components: {len(components)}")
    for i, comp in enumerate(components):
        print(f"  Component {i+1}: {comp}")
    print()
    
    # Example 4: Cycle detection
    print("Example 4: Cycle Detection")
    print("-" * 70)
    
    # Graph with cycle
    g4_cycle = Graph(directed=False)
    g4_cycle.add_edge(0, 1)
    g4_cycle.add_edge(1, 2)
    g4_cycle.add_edge(2, 0)  # Creates cycle
    
    print("Graph with cycle: [(0,1), (1,2), (2,0)]")
    print(f"Has cycle: {g4_cycle.has_cycle()}")
    
    # Graph without cycle
    g4_no_cycle = Graph(directed=False)
    g4_no_cycle.add_edge(0, 1)
    g4_no_cycle.add_edge(1, 2)
    g4_no_cycle.add_edge(0, 3)
    
    print("\nGraph without cycle: [(0,1), (1,2), (0,3)]")
    print(f"Has cycle: {g4_no_cycle.has_cycle()}")
    print()
    
    # Example 5: Topological sort
    print("Example 5: Topological Sort (DAG)")
    print("-" * 70)
    
    g5 = Graph(directed=True)
    # Task dependencies
    g5.add_edge(5, 2)  # Task 5 before 2
    g5.add_edge(5, 0)  # Task 5 before 0
    g5.add_edge(4, 0)  # Task 4 before 0
    g5.add_edge(4, 1)  # Task 4 before 1
    g5.add_edge(2, 3)  # Task 2 before 3
    g5.add_edge(3, 1)  # Task 3 before 1
    
    print("Task dependencies (DAG):")
    print("  5 → 2, 5 → 0, 4 → 0, 4 → 1, 2 → 3, 3 → 1")
    top_sort = g5.topological_sort()
    print(f"Topological order: {top_sort}")
    print("(Tasks should be executed in this order)")
    print()
    
    # Example 6: DFS with callback
    print("Example 6: DFS with Visit Callback")
    print("-" * 70)
    
    g6 = Graph(directed=False)
    g6.add_edge(0, 1)
    g6.add_edge(0, 2)
    g6.add_edge(1, 3)
    
    print("DFS traversal with callback:")
    def visit_node(node):
        print(f"  Visiting node: {node}")
    
    g6.dfs(0, visit_callback=visit_node)
    print()
    
    # Example 7: Performance measurement
    print("Example 7: Performance on Different Graph Sizes")
    print("-" * 70)
    
    timer = PerformanceTimer("DFS")
    
    for n in [100, 1000, 5000]:
        # Create connected graph
        g_large = Graph(directed=False)
        for i in range(n - 1):
            g_large.add_edge(i, i + 1)
        
        _, metrics = timer.measure(g_large.dfs, 0)
        print(f"Graph with {n} nodes:")
        print(f"  Time: {metrics['execution_time_ms']:.3f} ms")
        print(f"  Nodes visited: {n}")
    
    print()
    print("=" * 70)
    print("\nComplexity Summary:")
    print("  Time:  O(V + E) - V vertices, E edges")
    print("  Space: O(V) - recursion stack or explicit stack")
    print("\nKey Advantages:")
    print("  - Memory efficient for deep graphs")
    print("  - Good for finding paths")
    print("  - Can detect cycles")
    print("  - Natural for recursive problems")
    print("\nKey Disadvantages:")
    print("  - May not find shortest path")
    print("  - Stack overflow risk (recursive)")
    print("  - Order depends on edge order")
    print("\nCommon Use Cases:")
    print("  - Topological sorting")
    print("  - Cycle detection")
    print("  - Path finding")
    print("  - Connected components")
    print("  - Maze solving")
    print("  - Dependency resolution")
    print("=" * 70)


if __name__ == "__main__":
    main()

