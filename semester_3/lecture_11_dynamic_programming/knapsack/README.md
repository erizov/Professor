# Knapsack

**Category**: Dynamic Programming

## Overview

The knapsack problem is a problem in combinatorial optimization: Given a set of items, each with a weight and a value, determine the number of each item to include in a collection so that the total weight is less than or equal to a given limit and the total value is as large as possible.

## How It Works

1. Use dynamic programming: create 2D table
2. For each item, consider including or excluding it
3. If weight allows, take maximum of (value with item, value without item)
4. Fill table bottom-up
5. Trace back to find selected items

## Complexity Analysis

Time: O(n × W) where n is items, W is capacity. Space: O(n × W)

## Use Cases

Resource allocation, portfolio optimization, cutting stock problem, budget allocation

## Algorithm Details

### Key Characteristics

- **Stability**: Depends on implementation
- **In-place**: Depends on implementation
- **Adaptive**: Depends on implementation

## Implementation

See `algorithm.py` for the complete implementation with examples and performance analysis.

## References

- Wikipedia: [Knapsack problem](https://en.wikipedia.org/wiki/Knapsack_problem)
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
