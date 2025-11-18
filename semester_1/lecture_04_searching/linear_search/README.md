# Linear Search

**Category**: Searching

## Overview

Linear search or sequential search is a method for finding an element within a list. It sequentially checks each element of the list until a match is found or the whole list has been searched. Linear search is rarely practical because other search algorithms allow significantly faster searching for all but short lists.

## How It Works

1. Start from the first element
2. Compare each element with the target
3. If a match is found, return the index
4. If the end is reached without a match, return -1

## Complexity Analysis

Time: O(n). Space: O(1)

## Use Cases

Unsorted arrays, small datasets, when simplicity is more important than speed

## Algorithm Details

### Key Characteristics

- **Stability**: Depends on implementation
- **In-place**: Depends on implementation
- **Adaptive**: Depends on implementation

## Implementation

See `algorithm.py` for the complete implementation with examples and performance analysis.

## References

- Wikipedia: [Linear search](https://en.wikipedia.org/wiki/Linear_search)
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
