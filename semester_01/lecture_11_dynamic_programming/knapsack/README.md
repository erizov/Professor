# 0/1 Knapsack

1. **Name of Algorithm**  
   0/1 Knapsack

2. **What problem does it solve? (1 sentence)**  
   Selects items with weights and values to maximize value without exceeding capacity, using each item at most once.

3. **Intuition (plain-language explanation)**  
   Build solutions bottom-up: for each item, choose to take it or leave it based on remaining capacity and value gain.

4. **Inputs & Outputs**  
   - Input: List of item weights and values plus knapsack capacity W.  
   - Output: Maximum achievable value and optionally the chosen item set.

5. **Step-by-step description (5–10 lines max)**  
1. Create DP table dp[i][w] = best value using first i items and capacity w.
2. Initialize base row/column with zeros.
3. For each item i and capacity w: if weight[i] > w, copy dp[i-1][w]; otherwise take max(dp[i-1][w], value[i] + dp[i-1][w-weight[i]]).
4. Fill table row by row to capacity W.
5. Trace back from dp[n][W] to recover chosen items.

6. **Tiny example (hand-simulated)**  
   Items {(2,3),(3,4),(4,5)}, capacity 5. Optimal takes items 1 and 2 for value 7.

7. **Time & Space Complexity**  
   - Time: O(nW) where n items and capacity W.  
   - Space: O(nW) table or O(W) with rolling array optimization.

8. **Strengths**  
- Deterministic optimal solution when W is moderate.
- Classic DP illustrating trade-offs in subset selection problems.

9. **Weaknesses / limitations**  
- Pseudo-polynomial: runtime grows with numeric capacity.
- Not suitable when fractional choices are allowed.

10. **Compare with alternatives**  
    Alternatives: Fractional Knapsack, Branch and Bound, Meet-in-the-middle

11. **30-second explanation (your own words)**  
    Dynamic programming weighs the value of including each item versus skipping it, constrained by the remaining capacity.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
