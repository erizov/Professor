# Sparse Attention

1. **Name of Algorithm**  
   Sparse Attention

2. **What problem does it solve? (1 sentence)**  
   Reduces the quadratic complexity of attention mechanisms by computing attention only over a sparse subset of positions, enabling efficient processing of long sequences while maintaining model performance.

3. **Intuition (plain-language explanation)**  
   Like selective reading: sparse attention is like reading a book but only paying close attention to important pages - instead of reading every word carefully (full attention, O(n²)), you skim most pages and focus on key sections (sparse attention, O(n√n) or O(n log n)) - you still understand the book, but much faster, and you can handle much longer books (sequences) this way.

4. **Inputs & Outputs**  
   - Input: Query, key, value matrices, attention pattern, sparsity strategy, sequence length.  
   - Output: Sparse attention output, efficient computation, reduced memory, long sequence processing.

5. **Step-by-step description (5–10 lines max)**  
1. Choose pattern: select sparse attention pattern (local, strided, random, learned).
2. Compute scores: compute attention scores for query-key pairs.
3. Select: select top-k positions or use pattern to determine sparse set.
4. Mask: apply mask to zero out attention to non-selected positions.
5. Attend: compute attention only over selected sparse positions.
6. Aggregate: aggregate attention outputs from sparse positions.
7. Optimize: optimize attention pattern for task (learned sparse attention).
8. Scale: scale to very long sequences with sparse attention.
9. Validate: validate that sparse attention maintains performance.
10. Deploy: deploy for efficient long-sequence processing.

6. **Tiny example (hand-simulated)**  
   Sparse attention: sequence length 10K → full attention: 10K×10K = 100M operations → sparse: local window (512) + strided (every 64th) → attend to: 512 + 156 = 668 positions → operations: 10K×668 = 6.68M (15x reduction) → performance: 95% of full attention → sparse attention efficient.

7. **Time & Space Complexity**  
   - Time: O(n·k) where n is sequence length, k is sparse attention size (k << n), vs O(n²) for full attention.  
   - Space: O(n·k) where k is sparse attention size (much less than O(n²) for full attention matrix).

8. **Strengths**  
- Efficiency: dramatically reduces computational and memory requirements.
- Scalability: enables processing of much longer sequences.
- Performance: can maintain good performance with careful pattern design.

9. **Weaknesses / limitations**  
- Pattern design: requires careful design of attention patterns.
- Information loss: may miss some long-range dependencies.
- Complexity: implementing efficient sparse attention can be complex.

10. **Compare with alternatives**  
    Alternatives: Full Attention, Local Attention, Sliding Window, Linear Attention

11. **30-second explanation (your own words)**  
    Reduces the quadratic complexity of attention mechanisms by computing attention only over a sparse subset of positions, enabling efficient processing of long sequences while maintaining model performance.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
