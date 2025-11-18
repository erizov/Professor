# Avl Tree

**Category**: Data Structure

## Overview

An AVL tree (named after inventors Adelson-Velsky and Landis) is a self-balancing binary search tree. In an AVL tree, the heights of the two child subtrees of any node differ by at most one; if at any time they differ by more than one, rebalancing is done to restore this property.

## How It Works

1. Insert/search/delete like a regular BST
2. After each operation, check balance factor (height difference)
3. If imbalance detected, perform rotations (left, right, or double)
4. Rotations restore AVL property while maintaining BST order
5. Balance factor must be -1, 0, or 1 for all nodes

## Complexity Analysis

Time: O(log n) for all operations. Space: O(n)

## Use Cases

When guaranteed O(log n) performance is needed, database indexing, priority queues

## Algorithm Details

### Key Characteristics

- **Stability**: Depends on implementation
- **In-place**: Depends on implementation
- **Adaptive**: Depends on implementation

## Implementation

See `algorithm.py` for the complete implementation with examples and performance analysis.

## References

- Wikipedia: [AVL tree](https://en.wikipedia.org/wiki/AVL_tree)
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
