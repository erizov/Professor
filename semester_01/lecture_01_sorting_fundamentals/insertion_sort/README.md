# Insertion Sort

**Category**: Sorting

## Overview

Insertion sort is a simple sorting algorithm that builds the final sorted array one item at a time. It is much less efficient on large lists than more advanced algorithms such as quicksort, heapsort, or merge sort. However, insertion sort provides several advantages: simple implementation, efficient for small data sets, adaptive, stable, in-place, and online.

## How It Works

1. Start with the second element (index 1)
2. Compare it with elements before it
3. Shift larger elements one position to the right
4. Insert the current element in the correct position
5. Repeat for all remaining elements

## Complexity Analysis

Time: O(n²) average and worst case, O(n) best case. Space: O(1)

## Use Cases

Small datasets, nearly sorted data, as part of hybrid algorithms like Timsort

## Algorithm Details

### Key Characteristics

- **Stability**: Depends on implementation
- **In-place**: Depends on implementation
- **Adaptive**: Depends on implementation

## Implementation

See `algorithm.py` for the complete implementation with examples and performance analysis.

## References

- Wikipedia: [Insertion sort](https://en.wikipedia.org/wiki/Insertion_sort)
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
