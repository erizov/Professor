# Binary Search Tree

**Category**: Data Structure

## Overview

A binary search tree (BST) is a binary tree data structure where each node has a comparable key and satisfies the restriction that the key in any node is larger than the keys in all nodes in that node's left subtree and smaller than the keys in all nodes in that node's right subtree.

## How It Works

1. Start at root
2. Compare value with current node
3. If smaller, go left; if larger, go right
4. If equal, found; if null, not found
5. Insert at null position; delete requires rebalancing

## Complexity Analysis

Time: O(log n) average, O(n) worst case. Space: O(n)

## Use Cases

Dynamic sets, priority queues, symbol tables, database indexing

## Algorithm Details

### Key Characteristics

- **Stability**: Depends on implementation
- **In-place**: Depends on implementation
- **Adaptive**: Depends on implementation

## Implementation

See `algorithm.py` for the complete implementation with examples and performance analysis.

## References

- Wikipedia: [Binary search tree](https://en.wikipedia.org/wiki/Binary_search_tree)
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
