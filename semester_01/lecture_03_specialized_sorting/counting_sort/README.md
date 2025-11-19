# Counting Sort

1. **Name of Algorithm**  
   Counting Sort

2. **What problem does it solve? (1 sentence)**  
   Sorts integers in a small range by counting occurrences of each value, then placing them in order.

3. **Intuition (plain-language explanation)**  
   Count how many times each number appears, then write them out in order based on the counts.

4. **Inputs & Outputs**  
   - Input: Array of integers with range [0, k] where k is small (typically k = O(n)).  
   - Output: Sorted array.

5. **Step-by-step description (5–10 lines max)**  
1. Create count array of size k+1, initialize to zero.
2. Count occurrences: for each element, increment count[element].
3. Compute cumulative counts: count[i] += count[i-1] for i=1..k.
4. Build output array: place each element at position count[element]-1, decrement count[element].
5. Copy output back to original array if needed.

6. **Tiny example (hand-simulated)**  
   [4,2,2,8,3,3,1] → counts: [0,1,2,2,1,0,0,0,1] → cumulative: [0,1,3,5,6,6,6,6,7] → sorted: [1,2,2,3,3,4,8].

7. **Time & Space Complexity**  
   - Time: O(n+k) where k is the range size.  
   - Space: O(n+k) for count and output arrays.

8. **Strengths**  
- Linear time when range is small.
- Stable sorting algorithm.

9. **Weaknesses / limitations**  
- Only works for integers in a limited range.
- Space overhead for count array.

10. **Compare with alternatives**  
    Alternatives: Radix Sort, Bucket Sort, Pigeonhole Sort

11. **30-second explanation (your own words)**  

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
