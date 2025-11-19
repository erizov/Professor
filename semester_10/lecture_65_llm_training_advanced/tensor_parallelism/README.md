# Tensor Parallelism

1. **Name of Algorithm**  
   Tensor Parallelism

2. **What problem does it solve? (1 sentence)**  
   Splits individual tensor operations (matrix multiplications) across multiple devices by partitioning tensors along specific dimensions, enabling parallel computation of large matrix operations.

3. **Intuition (plain-language explanation)**  
Like splitting a large multiplication problem: tensor parallelism is like splitting a huge multiplication problem across multiple calculators - if you need to multiply two huge matrices, you split each matrix into pieces, give each calculator (GPU) a piece, they multiply their pieces in parallel, and you combine the results - this allows you to handle matrix multiplications too large for a single calculator (GPU) by using multiple calculators together.

4. **Inputs & Outputs**  
   - Input: Large tensors, matrix operations, multiple GPUs, tensor dimensions, partitioning strategy.  
   - Output: Parallel tensor operations, distributed computation, scaled operations, combined results.

5. **Step-by-step description (5–10 lines max)**  
1. Identify operations: identify large tensor operations to parallelize (attention, feedforward).
2. Choose dimension: choose dimension to split (row-wise, column-wise, or both).
3. Partition: partition input tensors across GPUs along chosen dimension.
4. Distribute: distribute tensor partitions to different GPUs.
5. Compute: each GPU computes its portion of the operation in parallel.
6. Communicate: GPUs communicate intermediate results (all-reduce, all-gather) as needed.
7. Combine: combine results from all GPUs to form complete output tensor.
8. Synchronize: synchronize GPUs to ensure correct computation.
9. Optimize: optimize communication patterns for efficiency.
10. Scale: scale to larger tensors with more GPUs.

6. **Tiny example (hand-simulated)**  
   Tensor parallelism: attention matrix multiplication (4096×4096) → 4 GPUs → row-wise split: each GPU gets 1024 rows → compute: each GPU multiplies its 1024×4096 partition → communicate: all-reduce for output → combine: 4096×4096 result → 4x parallelism → tensor parallelism operational.

7. **Time & Space Complexity**  
   - Time: O(n²/(p) + c) where n is tensor size, p is number of GPUs, c is communication overhead.  
   - Space: O(n²/p) per GPU where n is tensor size, p is number of GPUs (tensors partitioned).

8. **Strengths**  
- Fine-grained: enables fine-grained parallelism within operations.
- Efficiency: efficient for large tensor operations.
- Scalability: scales well with number of GPUs for large tensors.

9. **Weaknesses / limitations**  
- Communication: requires frequent communication between GPUs.
- Overhead: communication overhead can limit speedup.
- Complexity: implementing tensor parallelism can be complex.

10. **Compare with alternatives**  
    Alternatives: Model Parallelism, Pipeline Parallelism, Data Parallelism, Hybrid Parallelism

11. **30-second explanation (your own words)**  
    Splits individual tensor operations (matrix multiplications) across multiple devices by partitioning tensors along specific dimensions, enabling parallel computation of large matrix operations.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
