# Binary Search

**Category**: Searching

## Overview

Binary search is a search algorithm that finds the position of a target value within a sorted array. Binary search compares the target value to the middle element of the array. If they are not equal, the half in which the target cannot lie is eliminated and the search continues on the remaining half.

## How It Works

1. Compare target with the middle element
2. If target matches, return the index
3. If target is smaller, search the left half
4. If target is larger, search the right half
5. Repeat until found or search space is exhausted

## Complexity Analysis

Time: O(log n). Space: O(1) iterative, O(log n) recursive

## Use Cases

Searching in sorted arrays, finding insertion points, range queries

## Algorithm Details

### Key Characteristics

- **Stability**: Depends on implementation
- **In-place**: Depends on implementation
- **Adaptive**: Depends on implementation

## Implementation

See `algorithm.py` for the complete implementation with examples and performance analysis.

## References

- Wikipedia: [Binary search algorithm](https://en.wikipedia.org/wiki/Binary_search_algorithm)
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
