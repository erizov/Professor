# Counting Sort

**Category**: Sorting

## Overview

Counting sort is an algorithm for sorting a collection of objects according to keys that are small positive integers. It operates by counting the number of objects that have each distinct key value, and using arithmetic on those counts to determine the positions of each key value in the output sequence.

## How It Works

1. Count the frequency of each distinct value
2. Calculate cumulative counts to determine positions
3. Place each element in its correct position based on counts
4. Copy back to original array

## Complexity Analysis

Time: O(n + k) where k is the range of input. Space: O(k)

## Use Cases

Sorting integers with small range, as subroutine in radix sort

## Algorithm Details

### Key Characteristics

- **Stability**: Depends on implementation
- **In-place**: Depends on implementation
- **Adaptive**: Depends on implementation

## Implementation

See `algorithm.py` for the complete implementation with examples and performance analysis.

## References

- Wikipedia: [Counting sort](https://en.wikipedia.org/wiki/Counting_sort)
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
