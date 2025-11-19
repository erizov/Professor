# Merge Sort

1. **Name of Algorithm**  
   Merge Sort

2. **What problem does it solve? (1 sentence)**  
   Efficiently sorts large lists by divide-and-conquer merging of sorted halves.

3. **Intuition (plain-language explanation)**  
   Split the deck until each pile has one card, then merge piles back together in order.

4. **Inputs & Outputs**  
   - Input: Array or list of comparable elements.  
   - Output: Sorted array.

5. **Step-by-step description (5–10 lines max)**  
1. Divide the array into two halves.
2. Recursively sort each half.
3. Merge the two sorted halves by repeatedly taking the smaller front element.
4. Continue merging until a single sorted list remains.

6. **Tiny example (hand-simulated)**  
   [8, 3, 5, 2] → split into [8, 3] & [5, 2] → sort halves ⇒ [3, 8], [2, 5] → merge ⇒ [2, 3, 5, 8].

7. **Time & Space Complexity**  
   - Time: O(n log n) for all cases.  
   - Space: O(n) auxiliary storage for merges.

8. **Strengths**  
- Predictable performance and stable.
- Great for linked lists and external sorting.

9. **Weaknesses / limitations**  
- Requires extra memory for merging.
- Recursive overhead on constrained environments.

10. **Compare with alternatives**  
    Alternatives: Quick Sort, Heap Sort, TimSort

11. **30-second explanation (your own words)**  
    Keep splitting into halves until singles, then merge each pair while keeping them sorted.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
