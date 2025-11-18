#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deadlock Detection implementation.

This file contains the implementation of the Deadlock Detection algorithm.
"""

from typing import List, Optional, Dict, Set


class DeadlockDetection:
    """Deadlock detection algorithm."""
    def __init__(self):
        self.wait_for_graph: Dict[int, List[int]] = {}
    
    def add_wait(self, process: int, resource: int) -> None:
        """Add wait relationship."""
        if process not in self.wait_for_graph:
            self.wait_for_graph[process] = []
        self.wait_for_graph[process].append(resource)
    
    def detect_deadlock(self) -> List[List[int]]:
        """Detect deadlocks using cycle detection."""
        visited = set()
        rec_stack = set()
        cycles = []
        
        def dfs(node: int, path: List[int]) -> None:
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            for neighbor in self.wait_for_graph.get(node, []):
                if neighbor not in visited:
                    dfs(neighbor, path[:])
                elif neighbor in rec_stack:
                    # Found cycle
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])
            
            rec_stack.remove(node)
        
        for node in self.wait_for_graph:
            if node not in visited:
                dfs(node, [])
        
        return cycles


def main() -> None:
    """Demonstrate Deadlock Detection."""
    print("=" * 70)
    print("DEADLOCK DETECTION")
    print("=" * 70)
    
    # Example usage
    print("Algorithm implementation for Deadlock Detection")
    print("See implementation above for details.")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
