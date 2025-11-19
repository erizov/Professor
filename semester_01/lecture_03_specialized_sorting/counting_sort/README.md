# Counting Sort

1. **Name of Algorithm**  
   Counting Sort

2. **What problem does it solve? (1 sentence)**  
   Sorts integers from a limited range by counting occurrences instead of comparing.

3. **Intuition (plain-language explanation)**  
   Count how many times each value appears, then rebuild the list in order using counts as guides.

4. **Inputs & Outputs**  
   - Input: List of integers within a known small range.  
   - Output: Stable sorted list of the same integers.

5. **Step-by-step description (5–10 lines max)**  
1. Determine the min and max values.
2. Allocate a counts array covering the range.
3. Tally each element’s frequency.
4. Optionally convert counts to prefix sums for stability.
5. Write elements back in order using the counts.

6. **Tiny example (hand-simulated)**  
   [4, 2, 2, 5] ⇒ counts: {2:2, 4:1, 5:1} ⇒ output [2, 2, 4, 5].

7. **Time & Space Complexity**  
   - Time: O(n + k) where k is range size.  
   - Space: O(k) for the counting array.

8. **Strengths**  
- Linear time when k ≪ n log n.
- Stable if prefix sums are used.

9. **Weaknesses / limitations**  
- Requires known, limited range.
- Extra memory proportional to range size.

10. **Compare with alternatives**  
    Alternatives: Radix Sort, Bucket Sort, Comparison Sorts

11. **30-second explanation (your own words)**  
    Use frequency counts rather than comparisons, making it lightning-fast on bounded integer domains.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
