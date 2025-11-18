# Heap Sort

**Category**: Sorting

## Overview

Heapsort is a comparison-based sorting algorithm. Heapsort can be thought of as an improved selection sort: like selection sort, heapsort divides its input into a sorted and an unsorted region, and it iteratively shrinks the unsorted region by extracting the largest element from it and inserting it into the sorted region.

## How It Works

1. Build a max heap from the input array
2. The largest element is at the root
3. Swap the root with the last element and reduce heap size
4. Heapify the root to maintain heap property
5. Repeat until heap size is 1

## Complexity Analysis

Time: O(n log n) in all cases. Space: O(1)

## Use Cases

When worst-case O(n log n) is required, embedded systems, real-time systems

## Algorithm Details

### Key Characteristics

- **Stability**: Depends on implementation
- **In-place**: Depends on implementation
- **Adaptive**: Depends on implementation

## Implementation

See `algorithm.py` for the complete implementation with examples and performance analysis.

## References

- Wikipedia: [Heapsort](https://en.wikipedia.org/wiki/Heapsort)
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
