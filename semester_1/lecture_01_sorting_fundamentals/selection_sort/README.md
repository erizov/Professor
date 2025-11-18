# Selection Sort

**Category**: Sorting

## Overview

Selection sort is an in-place comparison sorting algorithm. It has an O(n²) time complexity, which makes it inefficient on large lists, and generally performs worse than the similar insertion sort. Selection sort is noted for its simplicity and has performance advantages over more complicated algorithms in certain situations, particularly where auxiliary memory is limited.

## How It Works

1. Find the minimum element in the unsorted portion
2. Swap it with the first element of the unsorted portion
3. Move the boundary of the sorted portion one element to the right
4. Repeat until the entire array is sorted

## Complexity Analysis

Time: O(n²) in all cases. Space: O(1)

## Use Cases

Small datasets, when memory writes are expensive, educational purposes

## Algorithm Details

### Key Characteristics

- **Stability**: Depends on implementation
- **In-place**: Depends on implementation
- **Adaptive**: Depends on implementation

## Implementation

See `algorithm.py` for the complete implementation with examples and performance analysis.

## References

- Wikipedia: [Selection sort](https://en.wikipedia.org/wiki/Selection_sort)
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
