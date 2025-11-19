# Longest Common Subsequence (LCS)

1. **Name of Algorithm**  
   Longest Common Subsequence (LCS)

2. **What problem does it solve? (1 sentence)**  
   Finds the longest sequence present in order (not necessarily contiguous) in two strings.

3. **Intuition (plain-language explanation)**  
   Walk both strings together; when characters match, include them, otherwise decide whether to drop a char from one string or the other via DP.

4. **Inputs & Outputs**  
   - Input: Strings s (length n) and t (length m).  
   - Output: Length of longest common subsequence (and optionally the subsequence).

5. **Step-by-step description (5–10 lines max)**  
1. Initialize DP table dp[n+1][m+1] to zero.
2. For i=1..n: for j=1..m:
3.   If s[i-1]==t[j-1], dp[i][j]=dp[i-1][j-1]+1.
4.   Else dp[i][j]=max(dp[i-1][j], dp[i][j-1]).
5. Backtrack from dp[n][m] to reconstruct the subsequence.

6. **Tiny example (hand-simulated)**  
   s="ABCBDAB", t="BDCABA" → LCS length 4 ("BCBA").

7. **Time & Space Complexity**  
   - Time: O(n·m).  
   - Space: O(n·m) (can be reduced to O(min(n,m)) for length only).

8. **Strengths**  
- Foundation for diff tools and bioinformatics alignment.
- Provides similarity measure ignoring non-matching sections.

9. **Weaknesses / limitations**  
- Quadratic runtime on string lengths.
- Reconstruction requires storing parent pointers or stack.

10. **Compare with alternatives**  
    Alternatives: Edit Distance, Longest Common Substring, Sequence Alignment

11. **30-second explanation (your own words)**  
    Fills a DP grid where each cell stores the best LCS length up to those prefixes, ensuring optimal substructure reuse.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
