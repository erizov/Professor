# Radix Sort

1. **Name of Algorithm**  
   Radix Sort

2. **What problem does it solve? (1 sentence)**  
   Sorts integers or fixed-length strings by processing digits/characters from least to most significant position.

3. **Intuition (plain-language explanation)**  
   Sort by ones place, then tens, then hundreds—each pass makes the array more sorted until fully ordered.

4. **Inputs & Outputs**  
   - Input: Array of integers or fixed-length strings.  
   - Output: Sorted array.

5. **Step-by-step description (5–10 lines max)**  
1. Find maximum value to determine number of digits.
2. For each digit position from least to most significant:
3.   Use counting sort (or stable sort) to sort by current digit.
4.   Update array with sorted order.
5. After processing all digits, array is fully sorted.

6. **Tiny example (hand-simulated)**  
   [170, 45, 75, 90, 2, 802, 24, 66]: sort by ones → [170,90,2,802,24,45,75,66]; by tens → [2,802,24,45,66,170,75,90]; by hundreds → [2,24,45,66,75,90,170,802].

7. **Time & Space Complexity**  
   - Time: O(d·(n+k)) where d is number of digits, k is radix (usually 10).  
   - Space: O(n+k) for counting sort auxiliary arrays.

8. **Strengths**  
- Linear time for fixed-width integers.
- Stable and deterministic.

9. **Weaknesses / limitations**  
- Requires fixed-width keys or padding.
- Not in-place; needs auxiliary space.

10. **Compare with alternatives**  
    Alternatives: Counting Sort, Bucket Sort, Quick Sort

11. **30-second explanation (your own words)**  
    Sort digit by digit from right to left, using a stable sort at each position to maintain relative order.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
