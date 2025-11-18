# Dfs

**Category**: Graph Algorithm

## Overview

Depth-first search (DFS) is an algorithm for traversing or searching tree or graph data structures. The algorithm starts at the root node and explores as far as possible along each branch before backtracking.

## How It Works

1. Start from source node, mark as visited
2. Recursively visit unvisited neighbors
3. Explore as deep as possible before backtracking
4. Use stack (recursion or explicit) to track path
5. Mark nodes as visited to avoid cycles

## Complexity Analysis

Time: O(V + E) where V is vertices, E is edges. Space: O(V)

## Use Cases

Topological sorting, cycle detection, maze solving, path finding, connected components

## Algorithm Details

### Key Characteristics

- **Stability**: Depends on implementation
- **In-place**: Depends on implementation
- **Adaptive**: Depends on implementation

## Implementation

See `algorithm.py` for the complete implementation with examples and performance analysis.

## References

- Wikipedia: [Depth-first search](https://en.wikipedia.org/wiki/Depth-first_search)
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
