# Bucket Sort

1. **Name of Algorithm**  
   Bucket Sort

2. **What problem does it solve? (1 sentence)**  
   Sorts uniformly distributed numbers by distributing them into buckets, sorting each bucket, then concatenating.

3. **Intuition (plain-language explanation)**  
   Like sorting mail into post office boxes: put each item in the right bucket, sort buckets individually, then combine.

4. **Inputs & Outputs**  
   - Input: Array of numbers uniformly distributed over a known range [min, max].  
   - Output: Sorted array.

5. **Step-by-step description (5–10 lines max)**  
1. Create n empty buckets (or fewer, based on range).
2. Distribute array elements into buckets: bucket[i] = floor(n * (arr[i] - min) / (max - min)).
3. Sort each bucket individually (using insertion sort or another algorithm).
4. Concatenate all buckets in order.

6. **Tiny example (hand-simulated)**  
   [0.42, 0.32, 0.33, 0.52, 0.37, 0.47] → buckets: [0.32,0.33,0.37], [0.42,0.47], [0.52] → sorted.

7. **Time & Space Complexity**  
   - Time: O(n+k) average when uniformly distributed, O(n²) worst if all items in one bucket.  
   - Space: O(n+k) for buckets.

8. **Strengths**  
- Linear average time for uniform distributions.
- Stable if bucket sorting is stable.

9. **Weaknesses / limitations**  
- Requires uniform distribution for efficiency.
- Extra space for buckets.

10. **Compare with alternatives**  
    Alternatives: Counting Sort, Radix Sort, Quick Sort

11. **30-second explanation (your own words)**  
    Divide the range into buckets, scatter items into appropriate buckets, sort buckets, then merge them back.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
