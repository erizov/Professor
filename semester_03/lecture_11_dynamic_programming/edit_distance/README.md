# Edit Distance (Levenshtein)

1. **Name of Algorithm**  
   Edit Distance (Levenshtein)

2. **What problem does it solve? (1 sentence)**  
   Finds the minimum number of insertions, deletions, and substitutions to transform one string into another.

3. **Intuition (plain-language explanation)**  
   Compare strings letter by letter; when they diverge, decide whether to insert, delete, or substitute the mismatch with minimal total cost.

4. **Inputs & Outputs**  
   - Input: Two strings s and t (lengths n and m).  
   - Output: Minimum edit operations required; optionally the sequence of edits.

5. **Step-by-step description (5–10 lines max)**  
1. Create DP table dp of size (n+1) × (m+1).
2. Initialize first row/column with index values (cost of deletions/insertions).
3. For each i,j: if s[i-1]==t[j-1], dp[i][j]=dp[i-1][j-1].
4. Otherwise dp[i][j] = 1 + min(dp[i-1][j] (delete), dp[i][j-1] (insert), dp[i-1][j-1] (substitute)).
5. Answer is dp[n][m]; backtrack to recover edit script if needed.

6. **Tiny example (hand-simulated)**  
   Transform "cat" → "cut": substitute 'a'→'u' (1 edit). DP table yields cost 1.

7. **Time & Space Complexity**  
   - Time: O(n·m).  
   - Space: O(n·m) or O(min(n,m)) with rolling array.

8. **Strengths**  
- Robust similarity metric for strings.
- Easily extended with custom costs.

9. **Weaknesses / limitations**  
- Quadratic time for long strings.
- Memory heavy without optimizations.

10. **Compare with alternatives**  
    Alternatives: Hamming Distance, Damerau-Levenshtein, Longest Common Subsequence

11. **30-second explanation (your own words)**  
    Dynamic programming over prefixes chooses the cheapest combination of insert/delete/substitute to align two strings.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
