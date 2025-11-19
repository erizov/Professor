# Insertion Sort

1. **Name of Algorithm**  
   Insertion Sort

2. **What problem does it solve? (1 sentence)**  
   Maintains a growing sorted prefix by inserting each new value into its proper place.

3. **Intuition (plain-language explanation)**  
   Like sorting playing cards: keep the hand sorted and slide each new card into position.

4. **Inputs & Outputs**  
   - Input: Array or list of comparable items.  
   - Output: Same collection sorted in ascending order.

5. **Step-by-step description (5–10 lines max)**  
1. Treat the first element as sorted.
2. Pick the next element (the key).
3. Shift larger elements in the sorted prefix one step to the right.
4. Insert the key into the freed slot.
5. Advance to the next element and repeat until the array is consumed.

6. **Tiny example (hand-simulated)**  
   [4, 2, 5] → insert 2 before 4 ⇒ [2, 4, 5] → insert 5 (already in place).

7. **Time & Space Complexity**  
   - Time: O(n²) average/worst, O(n) best on nearly-sorted data.  
   - Space: O(1) extra space.

8. **Strengths**  
- Excellent on tiny or almost sorted datasets.
- Stable and in-place.

9. **Weaknesses / limitations**  
- Quadratic when many elements are out of order.
- Heavy shifting work for long lists.

10. **Compare with alternatives**  
    Alternatives: Shell Sort, Merge Sort, Heap Sort

11. **30-second explanation (your own words)**  
    Grow a sorted prefix and carefully insert each new element where it belongs.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
