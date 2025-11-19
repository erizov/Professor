# 0/1 Knapsack

1. **Name of Algorithm**  
   0/1 Knapsack

2. **What problem does it solve? (1 sentence)**  
   Selects items with maximum total value without exceeding knapsack capacity, where each item can be taken at most once (0 or 1).

3. **Intuition (plain-language explanation)**  
   For each item, decide: take it (if capacity allows) or skip it. Use DP to cache results of subproblems (remaining capacity, remaining items).

4. **Inputs & Outputs**  
   - Input: Items with weights and values, knapsack capacity W, number of items n.  
   - Output: Maximum value achievable; optionally the set of items selected.

5. **Step-by-step description (5–10 lines max)**  
1. Create DP table dp[i][w] = max value using first i items with capacity w.
2. Base case: dp[0][w] = 0 for all w (no items).
3. For each item i and capacity w: dp[i][w] = max(dp[i-1][w], value[i] + dp[i-1][w-weight[i]]).
4. First term: skip item i; second term: take item i (if weight[i] <= w).
5. Answer is dp[n][W]; backtrack to recover selected items.

6. **Tiny example (hand-simulated)**  
   Items: (w=1,v=1), (w=3,v=4), (w=4,v=5), (w=5,v=7). Capacity=7. DP yields max value=9 by taking items 2 and 3.

7. **Time & Space Complexity**  
   - Time: O(n·W) where n is items, W is capacity.  
   - Space: O(n·W) for table, or O(W) with space optimization.

8. **Strengths**  
- Optimal solution for 0/1 knapsack problem.
- Classic DP problem with many variations.

9. **Weaknesses / limitations**  
- Pseudo-polynomial time (depends on W, not just n).
- Not efficient for very large capacities.

10. **Compare with alternatives**  
    Alternatives: Fractional Knapsack (greedy), Unbounded Knapsack, Multiple Knapsack

11. **30-second explanation (your own words)**  
    Dynamic programming builds optimal solution by considering each item and all possible remaining capacities, choosing whether to include the item.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
