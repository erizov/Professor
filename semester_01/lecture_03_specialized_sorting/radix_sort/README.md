# Radix Sort

1. **Name of Algorithm**  
   Radix Sort

2. **What problem does it solve? (1 sentence)**  
   Sorts integers or fixed-length strings by processing digits from least to most significant (or vice versa).

3. **Intuition (plain-language explanation)**  
   Group numbers by each digit place using a stable sorter so positions eventually align globally.

4. **Inputs & Outputs**  
   - Input: List of fixed-length keys (integers, strings).  
   - Output: Keys sorted lexicographically or numerically.

5. **Step-by-step description (5–10 lines max)**  
1. Choose digit order (LSB-first for integers).
2. For each digit position:
3.   - Group elements by digit using a stable bucket (like counting sort).
4.   - Concatenate buckets to reform the list.
5. Stop once the most significant digit is processed.

6. **Tiny example (hand-simulated)**  
   [170, 45, 75, 90] ⇒ bucket by units, then tens, then hundreds ⇒ [45, 75, 90, 170].

7. **Time & Space Complexity**  
   - Time: O(d · (n + k)) where d is digit count and k bucket size.  
   - Space: O(n + k) for buckets.

8. **Strengths**  
- Linear time for fixed d.
- Avoids comparisons entirely.

9. **Weaknesses / limitations**  
- Needs stable sub-sorting and uniform key lengths.
- Extra memory for buckets.

10. **Compare with alternatives**  
    Alternatives: Counting Sort, Bucket Sort, Comparison Sorts

11. **30-second explanation (your own words)**  
    Repeatedly bucket by digit so that by the final pass the entire key ordering emerges.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
