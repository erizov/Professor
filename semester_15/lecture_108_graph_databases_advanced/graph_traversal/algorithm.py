#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Graph Traversal implementation.

This file contains the implementation of the Graph Traversal algorithm.
"""

from typing import List, Optional, Dict, Set


class GraphTraversal:
    """Graph traversal algorithms."""
    def __init__(self):
        self.graph: Dict[str, List[str]] = {}
    
    def add_edge(self, u: str, v: str) -> None:
        """Add edge."""
        if u not in self.graph:
            self.graph[u] = []
        if v not in self.graph[u]:
            self.graph[u].append(v)
    
    def dfs(self, start: str) -> List[str]:
        """Depth-first search."""
        visited = set()
        result = []
        
        def dfs_helper(node: str):
            if node in visited:
                return
            visited.add(node)
            result.append(node)
            for neighbor in self.graph.get(node, []):
                dfs_helper(neighbor)
        
        dfs_helper(start)
        return result
    
    def bfs(self, start: str) -> List[str]:
        """Breadth-first search."""
        from collections import deque
        queue = deque([start])
        visited = {start}
        result = []
        
        while queue:
            node = queue.popleft()
            result.append(node)
            for neighbor in self.graph.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return result


def main() -> None:
    """Demonstrate Graph Traversal."""
    print("=" * 70)
    print("GRAPH TRAVERSAL")
    print("=" * 70)
    
    # Example usage
    print("Algorithm implementation for Graph Traversal")
    print("See implementation above for details.")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
