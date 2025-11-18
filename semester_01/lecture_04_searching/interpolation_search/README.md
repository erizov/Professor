# Interpolation Search

**Category**: Searching

## Overview

Interpolation search is an algorithm for searching for a key in an array that has been ordered by numerical values assigned to the keys. It is an improvement over binary search for instances where the values in a sorted array are uniformly distributed.

## How It Works

1. Calculate probe position using interpolation formula
2. Compare target with element at probe position
3. If match, return index
4. If target is smaller, search left subarray
5. If target is larger, search right subarray

## Complexity Analysis

Time: O(log log n) average for uniform distribution, O(n) worst case. Space: O(1)

## Use Cases

Uniformly distributed sorted arrays, when data is evenly spread

## Algorithm Details

### Key Characteristics

- **Stability**: Depends on implementation
- **In-place**: Depends on implementation
- **Adaptive**: Depends on implementation

## Implementation

See `algorithm.py` for the complete implementation with examples and performance analysis.

## References

- Wikipedia: [Interpolation search](https://en.wikipedia.org/wiki/Interpolation_search)
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
