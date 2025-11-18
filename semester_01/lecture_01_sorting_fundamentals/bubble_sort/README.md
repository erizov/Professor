# Bubble Sort

**Category**: Sorting

## Overview

Bubble sort is a simple sorting algorithm that repeatedly steps through the list, compares adjacent elements and swaps them if they are in the wrong order. The pass through the list is repeated until the list is sorted. The algorithm gets its name from the way smaller elements "bubble" to the top of the list.

## How It Works

1. Start from the beginning of the array
2. Compare each pair of adjacent elements
3. If they are in the wrong order, swap them
4. Continue until no more swaps are needed
5. The largest element "bubbles up" to the end in each pass

## Complexity Analysis

Time: O(n²) average and worst case, O(n) best case (optimized). Space: O(1)

## Use Cases

Educational purposes, very small datasets, nearly sorted data, when simplicity is critical

## Algorithm Details

### Key Characteristics

- **Stability**: Depends on implementation
- **In-place**: Depends on implementation
- **Adaptive**: Depends on implementation

## Implementation

See `algorithm.py` for the complete implementation with examples and performance analysis.

## References

- Wikipedia: [Bubble sort](https://en.wikipedia.org/wiki/Bubble_sort)
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
