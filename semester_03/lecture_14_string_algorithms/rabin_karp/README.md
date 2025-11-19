# Rabin-Karp

1. **Name of Algorithm**  
   Rabin-Karp

2. **What problem does it solve? (1 sentence)**  
   Finds pattern occurrences using rolling hash to quickly compare pattern hash with text window hashes.

3. **Intuition (plain-language explanation)**  
   Hash the pattern once, then slide a window through text and compare hashes; only do full comparison when hashes match.

4. **Inputs & Outputs**  
   - Input: Text string T (length n) and pattern string P (length m).  
   - Output: All starting indices where P appears in T.

5. **Step-by-step description (5–10 lines max)**  
1. Compute hash of pattern P.
2. Compute hash of first m characters of text.
3. If hashes match, verify with character-by-character comparison.
4. Roll hash forward: remove leftmost char, add rightmost char, update hash.
5. Repeat until end of text.

6. **Tiny example (hand-simulated)**  
   Text "GEEKS FOR GEEKS", pattern "GEEK": hash matches at indices 0 and 10.

7. **Time & Space Complexity**  
   - Time: O(n+m) average, O(n·m) worst if many hash collisions.  
   - Space: O(1) extra space (excluding hash storage).

8. **Strengths**  
- Simple to implement with rolling hash.
- Efficient for multiple pattern searches with same length.

9. **Weaknesses / limitations**  
- Worst-case performance degrades with many collisions.
- Requires careful hash function selection.

10. **Compare with alternatives**  
    Alternatives: KMP, Boyer-Moore, Finite Automaton

11. **30-second explanation (your own words)**  
    Use hashing to quickly filter out non-matches; only verify when hash values agree.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
