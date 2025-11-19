# Linear Search

1. **Name of Algorithm**  
   Linear Search

2. **What problem does it solve? (1 sentence)**  
   Finds the position of a target value by scanning elements sequentially.

3. **Intuition (plain-language explanation)**  
   Check each item in order until the desired one appears or the list ends.

4. **Inputs & Outputs**  
   - Input: List/array and target value.  
   - Output: Index of the target or -1 if absent.

5. **Step-by-step description (5–10 lines max)**  
1. Start at index 0.
2. Compare current element with target.
3. If equal, return the index.
4. Otherwise advance to the next index.
5. Stop after the final element and return -1 if not found.

6. **Tiny example (hand-simulated)**  
   Search 7 in [4, 7, 1]: compare 4 (no), compare 7 (yes) ⇒ index 1.

7. **Time & Space Complexity**  
   - Time: O(n) average and worst; O(1) best if first element matches.  
   - Space: O(1).

8. **Strengths**  
- Works on unsorted collections.
- Simple to implement and reason about.

9. **Weaknesses / limitations**  
- Slow on large datasets due to full scan.
- Cannot skip work without extra structure.

10. **Compare with alternatives**  
    Alternatives: Binary Search, Hash Lookup, Jump Search

11. **30-second explanation (your own words)**  
    Walk through each entry until the goal appears; trivial but potentially time-consuming.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
