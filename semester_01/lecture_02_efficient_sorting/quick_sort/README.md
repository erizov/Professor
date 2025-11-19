# Quick Sort

1. **Name of Algorithm**  
   Quick Sort

2. **What problem does it solve? (1 sentence)**  
Efficient in-place sort that partitions around a pivot and recursively sorts partitions.

3. **Intuition (plain-language explanation)**  
   Pick a pivot, move smaller items left and larger right, then repeat on the two sides.

4. **Inputs & Outputs**  
   - Input: Array of comparable values.  
   - Output: Array sorted ascending or descending based on comparator.

5. **Step-by-step description (5–10 lines max)**  
1. Choose a pivot element.
2. Partition the array so items < pivot go left, > pivot go right.
3. Recursively quick sort the left partition.
5. Concatenate left + pivot + right segments.

6. **Tiny example (hand-simulated)**  
   [9, 4, 7, 3] with pivot 7 ⇒ [4, 3 | 7 | 9] ⇒ sort left [4, 3] ⇒ [3, 4]; right [9] stays ⇒ [3, 4, 7, 9].

7. **Time & Space Complexity**  
   - Time: O(n log n) average, O(n²) worst if pivots are poor.  
   - Space: O(log n) recursion stack average.

8. **Strengths**  
- In-place and typically very fast.
- Cache-friendly sequential memory access.

9. **Weaknesses / limitations**  
- Worst-case quadratic when pivots are unbalanced.
- Not stable by default.

10. **Compare with alternatives**  
    Alternatives: Merge Sort, Heap Sort, IntroSort

11. **30-second explanation (your own words)**  
    Divide around an intelligently chosen pivot so the partitions shrink quickly, leading to near-logarithmic depth.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
