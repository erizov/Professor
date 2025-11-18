# Radix Sort

**Category**: Sorting

## Overview

Radix sort is a non-comparative sorting algorithm. It avoids comparison by creating and distributing elements into buckets according to their radix. For elements with more than one significant digit, this bucketing process is repeated for each digit, while preserving the ordering of the prior step, until all digits have been considered.

## How It Works

1. Sort elements by least significant digit (LSD) or most significant digit (MSD)
2. Group elements into buckets based on digit value
3. Recombine buckets in order
4. Repeat for next significant digit
5. Continue until all digits processed

## Complexity Analysis

Time: O(d × (n + k)) where d is number of digits, k is radix. Space: O(n + k)

## Use Cases

Sorting integers, strings, fixed-width data types

## Algorithm Details

### Key Characteristics

- **Stability**: Depends on implementation
- **In-place**: Depends on implementation
- **Adaptive**: Depends on implementation

## Implementation

See `algorithm.py` for the complete implementation with examples and performance analysis.

## References

- Wikipedia: [Radix sort](https://en.wikipedia.org/wiki/Radix_sort)
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
