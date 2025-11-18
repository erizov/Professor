# Bucket Sort

**Category**: Sorting

## Overview

Bucket sort, or bin sort, is a sorting algorithm that works by distributing the elements of an array into a number of buckets. Each bucket is then sorted individually, either using a different sorting algorithm, or by recursively applying the bucket sorting algorithm.

## How It Works

1. Create empty buckets
2. Distribute array elements into buckets based on value range
3. Sort each bucket individually (using insertion sort or another algorithm)
4. Concatenate all buckets back into the original array

## Complexity Analysis

Time: O(n + k) average, O(n²) worst case. Space: O(n + k)

## Use Cases

Uniformly distributed data, floating point numbers, when data is distributed over a range

## Algorithm Details

### Key Characteristics

- **Stability**: Depends on implementation
- **In-place**: Depends on implementation
- **Adaptive**: Depends on implementation

## Implementation

See `algorithm.py` for the complete implementation with examples and performance analysis.

## References

- Wikipedia: [Bucket sort](https://en.wikipedia.org/wiki/Bucket_sort)
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
