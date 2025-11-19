# Jump Search

1. **Name of Algorithm**  
   Jump Search

2. **What problem does it solve? (1 sentence)**  
   Balances linear and binary search by jumping ahead fixed blocks in a sorted array.

3. **Intuition (plain-language explanation)**  
   Skip ahead in strides; once you overshoot, do a short linear scan backward.

4. **Inputs & Outputs**  
   - Input: Sorted array and target.  
   - Output: Index of target or -1.

5. **Step-by-step description (5–10 lines max)**  
1. Choose optimal step ≈ √n.
2. Jump ahead by step size until value ≥ target or end reached.
3. Perform linear search backward within the block where target could reside.
4. Return index if found, else -1.

6. **Tiny example (hand-simulated)**  
   [1,3,5,7,9,11,13,15], target 9, step=2: jump indices 0→2→4 (value 9) stop and confirm.

7. **Time & Space Complexity**  
   - Time: O(√n).  
   - Space: O(1).

8. **Strengths**  
- Fewer comparisons than linear search on sorted data.
- Simple to implement.

9. **Weaknesses / limitations**  
- Still slower than binary search.
- Requires random access to jump.

10. **Compare with alternatives**  
    Alternatives: Binary Search, Interpolation Search, Exponential Search

11. **30-second explanation (your own words)**  
    Hop through the array in fixed leaps, then crawl a short distance to find the exact slot.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
