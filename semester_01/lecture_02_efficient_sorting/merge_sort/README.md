# Merge Sort

**Category**: Sorting

## Overview

Merge sort is an efficient, general-purpose, comparison-based sorting algorithm. Most implementations produce a stable sort, which means that the order of equal elements is the same in the input and output. Merge sort is a divide and conquer algorithm that was invented by John von Neumann in 1945.

## How It Works

1. Divide the array into two halves
2. Recursively sort both halves
3. Merge the two sorted halves back together
4. The merge process compares elements from both halves and combines them in sorted order

## Complexity Analysis

Time: O(n log n) in all cases. Space: O(n)

## Use Cases

Large datasets, when stability is required, external sorting, linked lists

## Algorithm Details

### Key Characteristics

- **Stability**: Depends on implementation
- **In-place**: Depends on implementation
- **Adaptive**: Depends on implementation

## Implementation

See `algorithm.py` for the complete implementation with examples and performance analysis.

## References

- Wikipedia: [Merge sort](https://en.wikipedia.org/wiki/Merge_sort)
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
