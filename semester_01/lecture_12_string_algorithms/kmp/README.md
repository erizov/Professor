# Kmp

**Category**: String Algorithm

## Overview

The Knuth–Morris–Pratt (KMP) algorithm is a string-searching algorithm that searches for occurrences of a "word" W within a main "text string" S by employing the observation that when a mismatch occurs, the word itself embodies sufficient information to determine where the next match could begin.

## How It Works

1. Preprocess pattern to create longest prefix suffix (LPS) array
2. Match pattern with text character by character
3. On mismatch, use LPS array to skip characters already matched
4. Avoid re-checking characters that are known to match
5. Continue until pattern found or text exhausted

## Complexity Analysis

Time: O(n + m) where n is text length, m is pattern length. Space: O(m)

## Use Cases

Text editors, search engines, DNA sequence matching, plagiarism detection

## Algorithm Details

### Key Characteristics

- **Stability**: Depends on implementation
- **In-place**: Depends on implementation
- **Adaptive**: Depends on implementation

## Implementation

See `algorithm.py` for the complete implementation with examples and performance analysis.

## References

- Wikipedia: [Knuth–Morris–Pratt algorithm](https://en.wikipedia.org/wiki/Knuth–Morris–Pratt_algorithm)
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
