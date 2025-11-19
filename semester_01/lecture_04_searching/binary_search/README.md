# Binary Search

1. **Name of Algorithm**  
   Binary Search

2. **What problem does it solve? (1 sentence)**  
   Finds a target in a sorted list by repeatedly halving the search interval.

3. **Intuition (plain-language explanation)**  
   Like guessing a number: choose the midpoint, discard the half where the answer cannot live, repeat.

4. **Inputs & Outputs**  
   - Input: Sorted array and target value.  
   - Output: Index of target or -1 if missing.

5. **Step-by-step description (5–10 lines max)**  
1. Set low and high pointers to the bounds.
2. Compute mid = (low + high) // 2.
3. If array[mid] equals target, return mid.
4. If target < array[mid], move high to mid - 1.
5. Else move low to mid + 1 and repeat until low > high.

6. **Tiny example (hand-simulated)**  
   Search 9 in [1,3,5,7,9,11]: mid=5→value=7 < 9, shift low ⇒ new mid=9 found at index 4.

7. **Time & Space Complexity**  
   - Time: O(log n).  
   - Space: O(1) iterative, O(log n) recursive.

8. **Strengths**  
- Very fast on massive sorted arrays.
- Predictable logarithmic performance.

9. **Weaknesses / limitations**  
- Requires sorted data with random access.
- Insertion/deletion may break order.

10. **Compare with alternatives**  
    Alternatives: Interpolation Search, Binary Search Tree, Hash Table

11. **30-second explanation (your own words)**  
    Keep cutting the remaining range in half so the number of candidates collapses exponentially.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
