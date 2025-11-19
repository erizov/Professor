# Bubble Sort

1. **Name of Algorithm**  
   Bubble Sort

2. **What problem does it solve? (1 sentence)**  
   Orders a short list of comparable values by repeatedly swapping out-of-order neighbors.

3. **Intuition (plain-language explanation)**  
   Imagine shaking a list so adjacent items compare and the heavier ones slowly drift to the end each pass.

4. **Inputs & Outputs**  
   - Input: Array or list of comparable elements.  
   - Output: Same collection arranged in non-decreasing order.

5. **Step-by-step description (5–10 lines max)**  
1. Start at the first index.
2. Compare the current element with the next element.
3. Swap if the pair is out of order.
4. Move one position forward and repeat until the pass ends.
5. Shrink the unsorted tail and loop until a pass produces no swaps.

6. **Tiny example (hand-simulated)**  
   [5, 3, 2] → swap 5/3 ⇒ [3, 5, 2]; swap 5/2 ⇒ [3, 2, 5]; next pass swaps 3/2 ⇒ [2, 3, 5].

7. **Time & Space Complexity**  
   - Time: O(n²) average/worst, O(n) best when already sorted.  
   - Space: O(1) extra space.

8. **Strengths**  
- Simple to code and reason about.
- Detects nearly-sorted input quickly if optimized to stop early.

9. **Weaknesses / limitations**  
- Quadratic runtime makes it impractical for medium or large inputs.
- Performs many redundant comparisons.

10. **Compare with alternatives**  
    Alternatives: Insertion Sort, Selection Sort, Merge Sort

11. **30-second explanation (your own words)**  
    Keep comparing neighbors so misplaced values crawl to the edges; repeat until no swaps happen.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
