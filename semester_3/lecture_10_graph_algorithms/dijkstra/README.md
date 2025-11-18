# Dijkstra

**Category**: Graph Algorithm

## Overview

Dijkstra's algorithm is an algorithm for finding the shortest paths between nodes in a weighted graph, which may represent, for example, road networks. It was conceived by computer scientist Edsger W. Dijkstra in 1956 and published three years later.

## How It Works

1. Initialize distances: source = 0, all others = infinity
2. Use priority queue to track unvisited nodes
3. Extract node with minimum distance
4. Relax edges: update distances to neighbors if shorter path found
5. Mark node as visited, repeat until all nodes processed

## Complexity Analysis

Time: O((V + E) log V) with binary heap. Space: O(V)

## Use Cases

GPS navigation, network routing, social networks, game pathfinding

## Algorithm Details

### Key Characteristics

- **Stability**: Depends on implementation
- **In-place**: Depends on implementation
- **Adaptive**: Depends on implementation

## Implementation

See `algorithm.py` for the complete implementation with examples and performance analysis.

## References

- Wikipedia: [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra's_algorithm)
- Additional resources available in academic literature and algorithm textbooks

## Examples

Run the algorithm with:
```bash
python algorithm.py
```

## Learning Objectives

By studying this algorithm, you will learn:
1. The fundamental approach and logic
2. Time and space complexity analysis
3. When to use this algorithm vs alternatives
4. Implementation details and optimizations
