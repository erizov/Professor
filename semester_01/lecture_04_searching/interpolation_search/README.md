# Interpolation Search

1. **Name of Algorithm**  
   Interpolation Search

2. **What problem does it solve? (1 sentence)**  
   Searches uniformly distributed sorted data by estimating the likely position of the target.

3. **Intuition (plain-language explanation)**  
   Instead of always probing the middle, interpolate where the target might land based on value range.

4. **Inputs & Outputs**  
   - Input: Sorted list with roughly uniform distribution and the target.  
   - Output: Index or -1.

5. **Step-by-step description (5–10 lines max)**  
1. Maintain low and high indices.
2. Estimate pos = low + (target - arr[low]) * (high - low) / (arr[high] - arr[low]).
3. If arr[pos] equals target, return pos.
4. If target < arr[pos], move high to pos - 1; else move low to pos + 1.
5. Repeat until low > high or value found.

6. **Tiny example (hand-simulated)**  
   In [10,20,30,40,50], searching 40 calculates pos near index 3 immediately.

7. **Time & Space Complexity**  
   - Time: O(log log n) average on uniform data, O(n) worst if distribution is skewed.  
   - Space: O(1).

8. **Strengths**  
- Fewer probes than binary search on uniform keys.
- Still simple arithmetic and comparisons.

9. **Weaknesses / limitations**  
- Performance collapses on clustered data.
- Requires numeric keys with known range.

10. **Compare with alternatives**  
    Alternatives: Binary Search, Jump Search, Exponential Search

11. **30-second explanation (your own words)**  
    Guess where the target should live based on proportional distance, probe there, and tighten the bounds.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
