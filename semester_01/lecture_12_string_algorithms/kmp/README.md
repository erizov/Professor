# Knuth-Morris-Pratt (KMP)

1. **Name of Algorithm**  
   Knuth-Morris-Pratt (KMP)

2. **What problem does it solve? (1 sentence)**  
   Finds all occurrences of a pattern string in a text string efficiently by avoiding redundant character comparisons.

3. **Intuition (plain-language explanation)**  
   When a mismatch occurs, use knowledge of already-matched characters to skip ahead intelligently instead of restarting from scratch.

4. **Inputs & Outputs**  
   - Input: Text string T (length n) and pattern string P (length m).  
   - Output: List of starting indices where P appears in T.

5. **Step-by-step description (5–10 lines max)**  
1. Preprocess pattern P to build a failure function (longest proper prefix that is also a suffix).
2. Initialize text pointer i=0 and pattern pointer j=0.
3. If T[i] == P[j], advance both pointers.
4. If mismatch: if j>0, set j = failure[j-1] (don't move i); else advance i.
5. If j reaches m, found a match at i-m; reset j using failure function and continue.

6. **Tiny example (hand-simulated)**  
   Text "ABABDABACDABABC", pattern "ABABC": failure=[0,0,1,2,0]. Match at index 10.

7. **Time & Space Complexity**  
   - Time: O(n+m) - linear in combined length.  
   - Space: O(m) for failure function.

8. **Strengths**  
- Linear time complexity, no backtracking in text.
- Efficient for multiple pattern searches.

9. **Weaknesses / limitations**  
- Requires preprocessing step.
- More complex than naive string matching.

10. **Compare with alternatives**  
    Alternatives: Boyer-Moore, Rabin-Karp, Aho-Corasick

11. **30-second explanation (your own words)**  
    Precompute where to resume matching after a failure, so the text pointer never moves backward.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
