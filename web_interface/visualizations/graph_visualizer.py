#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Graph algorithm visualizer.
Creates animated visualizations for graph traversal algorithms.
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx
from typing import List, Tuple, Dict, Set
import numpy as np


class GraphVisualizer:
    """Visualize graph algorithms step by step."""
    
    def __init__(self, graph: Dict[int, List[int]], directed: bool = False):
        """
        Initialize graph visualizer.
        
        Args:
            graph: Adjacency list representation {node: [neighbors]}
            directed: Whether graph is directed
        """
        self.graph = graph
        self.directed = directed
        self.steps = []
        self.G = nx.DiGraph() if directed else nx.Graph()
        
        # Build networkx graph
        for node, neighbors in graph.items():
            for neighbor in neighbors:
                self.G.add_edge(node, neighbor)
    
    def record_step(self, visited: Set[int], current: int = None, 
                   queue: List[int] = None, path: List[int] = None):
        """
        Record a step in the algorithm.
        
        Args:
            visited: Set of visited nodes
            current: Current node being processed
            queue: Current queue/frontier
            path: Current path (for pathfinding)
        """
        self.steps.append({
            'visited': visited.copy(),
            'current': current,
            'queue': queue.copy() if queue else [],
            'path': path.copy() if path else []
        })
    
    def visualize_bfs(self, start: int) -> animation.FuncAnimation:
        """Visualize BFS algorithm."""
        visited = set()
        queue = [start]
        visited.add(start)
        
        self.record_step(visited, start, queue)
        
        while queue:
            current = queue.pop(0)
            self.record_step(visited, current, queue)
            
            for neighbor in self.graph.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    self.record_step(visited, current, queue)
        
        return self._create_animation()
    
    def visualize_dfs(self, start: int) -> animation.FuncAnimation:
        """Visualize DFS algorithm."""
        visited = set()
        stack = [start]
        path = []
        
        while stack:
            current = stack.pop()
            
            if current not in visited:
                visited.add(current)
                path.append(current)
                self.record_step(visited, current, stack, path)
                
                for neighbor in reversed(self.graph.get(current, [])):
                    if neighbor not in visited:
                        stack.append(neighbor)
        
        return self._create_animation()
    
    def visualize_dijkstra(self, start: int, end: int = None) -> animation.FuncAnimation:
        """Visualize Dijkstra's algorithm."""
        import heapq
        
        distances = {node: float('inf') for node in self.graph}
        distances[start] = 0
        visited = set()
        pq = [(0, start)]
        path = {start: [start]}
        
        self.record_step(visited, start, [start])
        
        while pq:
            dist, current = heapq.heappop(pq)
            
            if current in visited:
                continue
            
            visited.add(current)
            self.record_step(visited, current, [n for _, n in pq], path.get(current, []))
            
            if end and current == end:
                break
            
            for neighbor in self.graph.get(current, []):
                if neighbor not in visited:
                    new_dist = dist + 1  # Assuming unit weights
                    if new_dist < distances[neighbor]:
                        distances[neighbor] = new_dist
                        path[neighbor] = path[current] + [neighbor]
                        heapq.heappush(pq, (new_dist, neighbor))
                        self.record_step(visited, current, [n for _, n in pq], path.get(neighbor, []))
        
        return self._create_animation()
    
    def _create_animation(self) -> animation.FuncAnimation:
        """Create matplotlib animation from recorded steps."""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Layout
        pos = nx.spring_layout(self.G, k=1, iterations=50)
        
        def animate(frame):
            ax.clear()
            
            if frame < len(self.steps):
                step = self.steps[frame]
                visited = step['visited']
                current = step.get('current')
                queue = step.get('queue', [])
                path = step.get('path', [])
                
                # Draw all edges
                nx.draw_networkx_edges(self.G, pos, ax=ax, alpha=0.3, 
                                      edge_color='gray', arrows=self.directed)
                
                # Draw unvisited nodes
                unvisited = set(self.G.nodes()) - visited
                if unvisited:
                    nx.draw_networkx_nodes(self.G, pos, nodelist=list(unvisited),
                                          node_color='lightblue', node_size=500,
                                          ax=ax)
                
                # Draw visited nodes
                if visited:
                    nx.draw_networkx_nodes(self.G, pos, nodelist=list(visited),
                                          node_color='lightgreen', node_size=500,
                                          ax=ax)
                
                # Draw current node
                if current is not None:
                    nx.draw_networkx_nodes(self.G, pos, nodelist=[current],
                                          node_color='red', node_size=700,
                                          ax=ax)
                
                # Draw path
                if path and len(path) > 1:
                    path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
                    nx.draw_networkx_edges(self.G, pos, edgelist=path_edges,
                                          edge_color='red', width=3, ax=ax,
                                          arrows=self.directed)
                
                # Draw labels
                nx.draw_networkx_labels(self.G, pos, ax=ax, font_size=10)
                
                title = f'Step {frame + 1}/{len(self.steps)}'
                if current is not None:
                    title += f' - Current: {current}'
                if queue:
                    title += f' - Queue: {queue[:5]}'
                ax.set_title(title)
            
            ax.axis('off')
        
        anim = animation.FuncAnimation(
            fig, animate, frames=len(self.steps),
            interval=500, repeat=False, blit=False
        )
        
        return anim
    
    def save_animation(self, filename: str, fps: int = 2):
        """Save animation to file."""
        anim = self._create_animation()
        anim.save(filename, writer='pillow', fps=fps)
        plt.close()


def visualize_graph_algorithm(algorithm_name: str, graph: Dict[int, List[int]],
                              start: int, end: int = None, output_file: str = None):
    """
    Visualize a graph algorithm.
    
    Args:
        algorithm_name: Name of algorithm ('bfs', 'dfs', 'dijkstra')
        graph: Adjacency list representation
        start: Start node
        end: End node (for pathfinding)
        output_file: Optional file to save animation
    """
    visualizer = GraphVisualizer(graph)
    
    if algorithm_name.lower() == 'bfs':
        anim = visualizer.visualize_bfs(start)
    elif algorithm_name.lower() == 'dfs':
        anim = visualizer.visualize_dfs(start)
    elif algorithm_name.lower() == 'dijkstra':
        anim = visualizer.visualize_dijkstra(start, end)
    else:
        raise ValueError(f"Unknown algorithm: {algorithm_name}")
    
    if output_file:
        visualizer.save_animation(output_file)
    else:
        plt.show()
    
    return visualizer


if __name__ == '__main__':
    # Example usage
    graph = {
        0: [1, 2],
        1: [0, 3, 4],
        2: [0, 5],
        3: [1],
        4: [1, 5],
        5: [2, 4]
    }
    visualize_graph_algorithm('bfs', graph, 0, output_file='bfs_traversal.gif')

