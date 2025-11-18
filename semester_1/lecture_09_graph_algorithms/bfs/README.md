# Bfs

**Category**: Graph Algorithm

## Overview

Breadth-first search (BFS) is an algorithm for traversing or searching tree or graph data structures. It starts at the tree root (or some arbitrary node of a graph) and explores all nodes at the present depth prior to moving on to nodes at the next depth level.

## How It Works

1. Start from source node, mark as visited
2. Add to queue
3. While queue not empty: dequeue node, visit it
4. Add all unvisited neighbors to queue
5. Mark neighbors as visited, repeat

## Complexity Analysis

Time: O(V + E) where V is vertices, E is edges. Space: O(V)

## Use Cases

Shortest path in unweighted graphs, level-order tree traversal, social networks, web crawling

## Algorithm Details

### Key Characteristics

- **Stability**: Depends on implementation
- **In-place**: Depends on implementation
- **Adaptive**: Depends on implementation

## Implementation

See `algorithm.py` for the complete implementation with examples and performance analysis.

## References

- Wikipedia: [Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search)
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
