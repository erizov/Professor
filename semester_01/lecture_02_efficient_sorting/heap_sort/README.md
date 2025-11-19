# Heap Sort

1. **Name of Algorithm**  
   Heap Sort

2. **What problem does it solve? (1 sentence)**  
   Sorts by turning the input into a heap and repeatedly extracting the max (or min).

3. **Intuition (plain-language explanation)**  
   Build a priority queue so the largest element can be removed and placed at the end one by one.

4. **Inputs & Outputs**  
   - Input: Array of comparable items.  
   - Output: Array sorted in-place.

5. **Step-by-step description (5–10 lines max)**  
1. Heapify the entire array (build max-heap).
2. Swap the root (largest value) with the last element.
3. Reduce the heap size by one and heapify the root.
4. Repeat extraction and heapify until one element remains.

6. **Tiny example (hand-simulated)**  
   [4, 1, 3, 2] → build max-heap [4,2,3,1] → swap 4/1 ⇒ [1,2,3,4]; heapify remaining ⇒ [3,2,1,4] → continue until sorted.

7. **Time & Space Complexity**  
   - Time: O(n log n) for all cases.  
   - Space: O(1) extra space besides recursion-free heapify.

8. **Strengths**  
- Predictable O(n log n) time.
- In-place with no recursion required.

9. **Weaknesses / limitations**  
- Not stable.
- Constant factors higher than quick sort on average.

10. **Compare with alternatives**  
    Alternatives: Quick Sort, Merge Sort, IntroSort

11. **30-second explanation (your own words)**  
    Leverage the heap property so the largest item is always on top, remove it, and restore the heap repeatedly.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
