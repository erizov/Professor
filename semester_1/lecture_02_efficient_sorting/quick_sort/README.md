# Quick Sort

**Category**: Sorting

## Overview

Quicksort is an efficient sorting algorithm. Developed by British computer scientist Tony Hoare in 1959 and published in 1961, it is still a commonly used algorithm for sorting. When implemented well, it can be somewhat faster than merge sort and about two or three times faster than heapsort.

## How It Works

1. Choose a pivot element from the array
2. Partition the array: elements smaller than pivot go left, larger go right
3. Recursively apply quicksort to the left and right subarrays
4. Combine the results (pivot is already in correct position)

## Complexity Analysis

Time: O(n log n) average, O(n²) worst case. Space: O(log n)

## Use Cases

General-purpose sorting, large datasets, when average performance matters more than worst case

## Algorithm Details

### Key Characteristics

- **Stability**: Depends on implementation
- **In-place**: Depends on implementation
- **Adaptive**: Depends on implementation

## Implementation

See `algorithm.py` for the complete implementation with examples and performance analysis.

## References

- Wikipedia: [Quicksort](https://en.wikipedia.org/wiki/Quicksort)
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
