# Boyer-Moore

1. **Name of Algorithm**  
   Boyer-Moore

2. **What problem does it solve? (1 sentence)**  
   Finds pattern occurrences in text by scanning from right to left and skipping ahead when mismatches occur.

3. **Intuition (plain-language explanation)**  
   Start matching from the end of the pattern; when a mismatch happens, use two heuristics to jump ahead as far as possible.

4. **Inputs & Outputs**  
   - Input: Text string T (length n) and pattern string P (length m).  
   - Output: All starting positions where P occurs in T.

5. **Step-by-step description (5–10 lines max)**  
1. Preprocess P to build bad character table (rightmost occurrence of each char).
2. Preprocess P to build good suffix table (longest suffix that matches a prefix).
3. Align P with start of T, compare from right to left.
4. On mismatch: skip by max(bad character shift, good suffix shift).
5. Continue until pattern slides past end of text.

6. **Tiny example (hand-simulated)**  
   Text "THIS IS A TEST", pattern "TEST": bad char 'T' at end allows skipping ahead.

7. **Time & Space Complexity**  
   - Time: O(n/m) best case, O(n·m) worst case, typically sub-linear in practice.  
   - Space: O(m + |alphabet|) for preprocessing tables.

8. **Strengths**  
- Often faster than linear algorithms in practice due to large skips.
- Excellent for long patterns and large alphabets.

9. **Weaknesses / limitations**  
- Worst-case quadratic time possible.
- More complex preprocessing than KMP.

10. **Compare with alternatives**  
Alternatives: KMP, Rabin-Karp, Sunday Algorithm

11. **30-second explanation (your own words)**  
    Match backwards and use character mismatches to skip ahead intelligently, often faster than forward matching.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
