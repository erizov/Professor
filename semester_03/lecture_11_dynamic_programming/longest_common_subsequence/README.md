# Longest Common Subsequence

**Category**: Dynamic Programming

## Overview

The longest common subsequence (LCS) problem is the problem of finding the longest subsequence common to all sequences in a set of sequences. It differs from the longest common substring problem: unlike substrings, subsequences are not required to occupy consecutive positions within the original sequences.

## How It Works

1. Create 2D DP table
2. Compare characters of both strings
3. If characters match, LCS[i][j] = 1 + LCS[i-1][j-1]
4. If no match, LCS[i][j] = max(LCS[i-1][j], LCS[i][j-1])
5. Trace back to construct actual LCS string

## Complexity Analysis

Time: O(m × n) where m, n are string lengths. Space: O(m × n)

## Use Cases

Version control (diff), DNA sequence comparison, plagiarism detection, text similarity

## Algorithm Details

### Key Characteristics

- **Stability**: Depends on implementation
- **In-place**: Depends on implementation
- **Adaptive**: Depends on implementation

## Implementation

See `algorithm.py` for the complete implementation with examples and performance analysis.

## References

- Wikipedia: [Longest common subsequence problem](https://en.wikipedia.org/wiki/Longest_common_subsequence_problem)
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
