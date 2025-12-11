# Longest Common Subsequence (LCS)

## Principle of Operation

Longest Common Subsequence finds the longest sequence of characters that appear in the same order (but not necessarily next to each other) in both strings. It's like finding common elements in two sequences while keeping their order.

**How it works:**
1. Compare two strings character by character
2. If characters match, include it in the common subsequence and move forward in both strings
3. If characters don't match, try two options:
   - Skip character from first string, continue
   - Skip character from second string, continue
4. Always choose the option that gives longer subsequence
5. Use a table to remember the longest subsequence length for each prefix pair

**Simple analogy:** Imagine you have two sequences: "ABCD" and "ACBD". The common subsequence could be "ABD" (A, then B, then D appear in order in both) or "ACD" (A, then C, then D). The longest is length 3. LCS finds this longest common subsequence.

**Key idea:** Build a table where each cell represents the longest common subsequence length between one prefix of the first string and one prefix of the second string. Start with small prefixes and build up to the full strings.

**Important:** Subsequence means characters in order but not necessarily next to each other. "ABC" is a subsequence of "AXBXC" (A, then B, then C appear in order, even with X's in between).

## Algorithm Complexity

**Time Complexity:** O(m × n)
- m = length of first string
- n = length of second string
- We fill a table with (m+1) rows and (n+1) columns
- Each cell takes constant time to compute

**Space Complexity:** O(m × n)
- Need table to store LCS length for each prefix pair
- Can be optimized to O(min(m, n)) for length only (but can't reconstruct sequence)

**Why it's efficient:** Instead of trying all possible subsequences (exponential), we use a table to remember solutions to smaller problems. This makes it much faster.

## Where It's Used in Practice

**Version Control:**
- **Git, SVN** - showing differences between file versions
- **Diff tools** - comparing text files
- **Merge tools** - finding common parts of conflicting versions

**Text Processing:**
- **Plagiarism detection** - finding common sequences in documents
- **Document comparison** - identifying similar sections
- **Sequence matching** - finding common patterns

**Real-World Applications:**
- **DNA comparison** - finding common subsequences in genetic sequences
- **Code comparison** - finding similar code sections
- **Game development** - pattern matching in game AI

## What It Can Be Compared To

**Like Finding Common Elements:** You look for characters that appear in both strings in the same order, even if they're not next to each other.

**Like Building Up Solutions:** Start with finding LCS of empty strings (length 0), then add characters one by one, always choosing the longer subsequence.

**Similar to Edit Distance:** Both use 2D table with similar structure. Edit distance counts operations, LCS counts matches.

**Different from Longest Common Substring:** Subsequence allows skipping characters (non-contiguous), substring requires characters to be next to each other (contiguous).

## Minimal Code Example

Here's a simple LCS implementation:

```python
def longest_common_subsequence(s1, s2):
    """LCS length using dynamic programming."""
    m, n = len(s1), len(s2)
    # dp[i][j] = LCS length between s1[0:i] and s2[0:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                # Characters match, extend LCS
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                # Characters don't match, take max of skipping either
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    return dp[m][n]

# Example:
print(longest_common_subsequence("ABCD", "ACBD"))  # Output: 3 (ACD or ABD)
print(longest_common_subsequence("AGGTAB", "GXTXAYB"))  # Output: 4 (GTAB)
```

**Key parts:**
- Table stores LCS length for each prefix pair
- If characters match, extend LCS (add 1 to diagonal)
- If don't match, take max of skipping from either string
- Final answer in dp[m][n]

## Common Mistakes

1. **Confusing Subsequence with Substring:**
   - **Wrong:** Implementing substring (contiguous) instead of subsequence
   - **Why it's wrong:** Different algorithm, wrong results
   - **Fix:** Remember subsequence allows skipping characters

2. **Wrong Recurrence:**
   - **Wrong:** Not taking max when characters don't match
   - **Why it's wrong:** Incorrect LCS length
   - **Fix:** When characters don't match, take max of dp[i-1][j] and dp[i][j-1]

3. **Array Index Errors:**
   - **Wrong:** Using s1[i] instead of s1[i-1]
   - **Why it's wrong:** Accesses wrong characters
   - **Fix:** Remember dp[i][j] uses s1[0:i], so use s1[i-1] for i-th character

4. **Not Initializing Base Cases:**
   - **Wrong:** Not setting dp[0][j] = 0 and dp[i][0] = 0
   - **Why it's wrong:** Incorrect base case (LCS with empty string is 0)
   - **Fix:** Initialize first row and column to 0

5. **Trying to Reconstruct with Optimized Space:**
   - **Wrong:** Trying to get actual subsequence with O(min(m,n)) space
   - **Why it's wrong:** Can't reconstruct with space optimization
   - **Fix:** Use full O(m×n) space if you need the actual subsequence

## Recommended Literature

1. **"Grokking Algorithms"** by Aditya Bhargava
   - Simple explanations of dynamic programming
   - Great LCS examples

2. **"Introduction to Algorithms" (CLRS)**
   - Comprehensive coverage of LCS
   - Explains the algorithm in detail

3. **"Algorithm Design Manual"** by Steven Skiena
   - Practical approach with examples
   - Good for understanding applications

4. **Online Resources:**
   - GeeksforGeeks - LCS tutorials
   - Khan Academy - dynamic programming course
   - LeetCode - practice problems
