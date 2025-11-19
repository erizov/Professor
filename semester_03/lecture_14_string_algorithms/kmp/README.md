# Knuth-Morris-Pratt (KMP) Algorithm

1. **Name of Algorithm**  
   Knuth-Morris-Pratt (KMP) Algorithm

2. **What problem does it solve? (1 sentence)**  
   Finds all occurrences of a pattern string in a text string efficiently by preprocessing the pattern to avoid redundant comparisons, achieving linear time complexity.

3. **Intuition (plain-language explanation)**  
   Like smart searching: KMP is like searching for a word in a book but being smart about it - when you find a mismatch, instead of starting over from the beginning (naive approach), you use what you already know about the pattern to skip ahead intelligently - it's like if you're looking for 'ABABC' and you've matched 'ABAB' but the next character doesn't match, you know you can skip ahead because 'AB' at the start matches 'AB' you just saw, so you don't need to check those again.

4. **Inputs & Outputs**  
   - Input: Text string, pattern string, preprocessing information.  
   - Output: All occurrences of pattern in text, match positions, failure function (LPS array).

5. **Step-by-step description (5–10 lines max)**  
1. Preprocess: build failure function (LPS - Longest Proper Prefix which is also Suffix) for pattern.
2. Initialize: initialize text index i=0 and pattern index j=0.
3. Compare: compare text[i] with pattern[j].
4. Match: if characters match, increment both i and j.
5. Mismatch: if characters don't match and j>0, set j = failure[j-1] (skip ahead using failure function).
6. Mismatch start: if j=0 and mismatch, increment i (move to next text character).
7. Found: if j equals pattern length, pattern found at position (i-j), reset j using failure function.
8. Continue: continue until end of text.
9. Return: return all match positions.
10. Optimize: failure function allows skipping redundant comparisons.

6. **Tiny example (hand-simulated)**  
   KMP: text: 'ABABDABACDABABCABC', pattern: 'ABABC' → preprocess: LPS = [0,0,1,2,0] → search: match 'ABAB', mismatch at 'C' → use LPS: skip to j=2 (since 'AB' matches) → continue: find match at position 10 → KMP finds pattern efficiently.

7. **Time & Space Complexity**  
   - Time: O(n + m) where n is text length, m is pattern length (linear time, vs O(n·m) naive).  
   - Space: O(m) where m is pattern length (for failure function/LPS array).

8. **Strengths**  
- Efficiency: linear time complexity, much faster than naive O(n·m).
- Optimal: optimal for single pattern matching.
- No backtracking: doesn't backtrack in text, only uses pattern information.

9. **Weaknesses / limitations**  
- Preprocessing: requires preprocessing step (O(m) time).
- Single pattern: designed for single pattern, not multiple patterns.
- Complexity: more complex to implement than naive algorithm.

10. **Compare with alternatives**  
    Alternatives: Naive String Matching, Rabin-Karp, Boyer-Moore, Aho-Corasick

11. **30-second explanation (your own words)**  
    Finds all occurrences of a pattern string in a text string efficiently by preprocessing the pattern to avoid redundant comparisons, achieving linear time complexity.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
