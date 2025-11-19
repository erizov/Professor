# Selection Sort

1. **Name of Algorithm**  
   Selection Sort

2. **What problem does it solve? (1 sentence)**  
   Sorts by repeatedly selecting the smallest remaining element and placing it at the front.

3. **Intuition (plain-language explanation)**  
   Scan the pile for the tiniest card, put it next in line, and continue with the leftovers.

4. **Inputs & Outputs**  
   - Input: Array or list of comparable values.  
   - Output: Same collection sorted ascending.

5. **Step-by-step description (5–10 lines max)**  
1. Set the current position i to 0.
2. Find the smallest element from i to end.
3. Swap that element with position i.
4. Increment i and repeat until the list is ordered.

6. **Tiny example (hand-simulated)**  
   [7, 3, 5] → smallest is 3, swap with 7 ⇒ [3, 7, 5]; next smallest is 5, swap ⇒ [3, 5, 7].

7. **Time & Space Complexity**  
   - Time: O(n²) regardless of input order.  
   - Space: O(1) extra space.

8. **Strengths**  
- Performs minimal swaps (n - 1).
- Easy to reason about and implement.

9. **Weaknesses / limitations**  
- Still quadratic in comparisons.
- Not stable without extra work.

10. **Compare with alternatives**  
    Alternatives: Insertion Sort, Heap Sort, Quick Sort

11. **30-second explanation (your own words)**  
    Repeatedly locate the smallest unused value and stick it at the next slot of the sorted prefix.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
