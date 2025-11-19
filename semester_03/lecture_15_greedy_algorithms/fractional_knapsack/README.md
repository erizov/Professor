# Fractional Knapsack

1. **Name of Algorithm**  
   Fractional Knapsack

2. **What problem does it solve? (1 sentence)**  
   Maximizes value in a knapsack of limited capacity by taking fractions of items (unlike 0/1 knapsack where items are indivisible).

3. **Intuition (plain-language explanation)**  
   Greedily take items with highest value-to-weight ratio first: fill knapsack with best items until capacity is exhausted, taking fractions if needed.

4. **Inputs & Outputs**  
   - Input: Items with weights and values, knapsack capacity W.  
   - Output: Maximum value achievable; optionally the fraction of each item taken.

5. **Step-by-step description (5–10 lines max)**  
1. Calculate value-to-weight ratio for each item.
2. Sort items by ratio (descending).
3. Initialize total_value = 0, remaining_capacity = W.
4. For each item in sorted order: take as much as possible (full item or fraction) until capacity is full.
5. Return total_value.

6. **Tiny example (hand-simulated)**  
   Items: (weight=10, value=60), (weight=20, value=100), (weight=30, value=120). Ratios: 6, 5, 4. Capacity=50. Take all of item1 (10), all of item2 (20), 2/3 of item3 (20). Value = 60+100+80 = 240.

7. **Time & Space Complexity**  
   - Time: O(n log n) for sorting, O(n) for selection = O(n log n) total.  
   - Space: O(n) for storing items and ratios.

8. **Strengths**  
- Greedy approach yields optimal solution (unlike 0/1 knapsack).
- Efficient O(n log n) time complexity.

9. **Weaknesses / limitations**  
- Only works when items can be divided (fractional).
- Real-world items are often indivisible (0/1 knapsack requires DP).

10. **Compare with alternatives**  
    Alternatives: 0/1 Knapsack (DP), Multiple Knapsack, Bounded Knapsack

11. **30-second explanation (your own words)**  
    Greedily selects items by value-to-weight ratio, taking full items when possible and fractions when capacity is limited, ensuring optimal value.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
