# Jump Search

**Category**: Searching

## Overview

Jump search is a searching algorithm for sorted arrays. The basic idea is to check fewer elements by jumping ahead by fixed steps or skipping some elements in place of searching all elements. It works better than linear search but requires the array to be sorted.

## How It Works

1. Jump ahead by fixed step size (typically √n)
2. If current element is greater than target, perform linear search backwards
3. If current element is less than target, continue jumping
4. Repeat until target found or array exhausted

## Complexity Analysis

Time: O(√n). Space: O(1)

## Use Cases

Sorted arrays, when binary search is not available, uniform data distribution

## Algorithm Details

### Key Characteristics

- **Stability**: Depends on implementation
- **In-place**: Depends on implementation
- **Adaptive**: Depends on implementation

## Implementation

See `algorithm.py` for the complete implementation with examples and performance analysis.

## References

- Wikipedia: [Jump search](https://en.wikipedia.org/wiki/Jump_search)
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
