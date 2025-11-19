# Bucket Sort

1. **Name of Algorithm**  
   Bucket Sort

2. **What problem does it solve? (1 sentence)**  
   Sorts uniformly distributed real numbers by scattering them into buckets and sorting each bucket.

3. **Intuition (plain-language explanation)**  
   Partition the [0,1) range into buckets so each holds a small local list that can be sorted quickly.

4. **Inputs & Outputs**  
   - Input: List of real numbers typically normalized to [0, 1).  
   - Output: Sorted list of those numbers.

5. **Step-by-step description (5–10 lines max)**  
1. Create k empty buckets.
2. Distribute each element into the appropriate bucket based on value.
3. Sort individual buckets (often using insertion sort).
4. Concatenate the buckets in order.

6. **Tiny example (hand-simulated)**  
   [0.42, 0.32, 0.23] ⇒ bucket 0.2–0.3 gets [0.23], 0.3–0.4 gets [0.32], 0.4–0.5 gets [0.42] ⇒ concatenated order [0.23, 0.32, 0.42].

7. **Time & Space Complexity**  
   - Time: Average O(n) when distribution is uniform; worst O(n²) if items clump.  
   - Space: O(n + k) for bucket storage.

8. **Strengths**  
- Near-linear when values spread evenly.
- Buckets can be processed in parallel.

9. **Weaknesses / limitations**  
- Performance degrades on skewed data.
- Requires knowledge of value distribution.

10. **Compare with alternatives**  
    Alternatives: Radix Sort, Counting Sort, Comparison Sorts

11. **30-second explanation (your own words)**  
    Exploit the distribution shape so each bucket is tiny, making local sorts trivial.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
