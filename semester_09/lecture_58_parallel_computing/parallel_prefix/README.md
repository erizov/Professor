# Parallel Prefix (Scan)

1. **Name of Algorithm**  
   Parallel Prefix (Scan)

2. **What problem does it solve? (1 sentence)**  
   Computes all prefix sums (or other associative operations) of an array in parallel, enabling efficient parallel computation of cumulative operations like running sums, maximums, or products.

3. **Intuition (plain-language explanation)**  
   Like calculating running totals in parallel: parallel prefix is like calculating running totals for a list of numbers, but doing it in parallel - instead of calculating each total sequentially (1, 1+2, 1+2+3, ...), you use a tree structure where you combine results at different levels, allowing multiple calculations to happen simultaneously - it's like having multiple people calculate different parts of the running totals and then combining their results.

4. **Inputs & Outputs**  
   - Input: Array of values, associative binary operation (addition, multiplication, maximum, etc.), number of processors.  
   - Output: Prefix array (scan results), parallel computation, cumulative values.

5. **Step-by-step description (5–10 lines max)**  
1. Up-sweep: build binary tree, compute partial results bottom-up (upward pass).
2. Combine: at each level, combine results from left and right subtrees.
3. Store: store intermediate results in tree nodes.
4. Down-sweep: propagate results top-down (downward pass).
5. Distribute: distribute prefix values to appropriate positions.
6. Compute: compute final prefix values using tree structure.
7. Parallelize: execute tree operations in parallel across processors.
8. Combine: combine results from parallel execution.
9. Output: return prefix array with all cumulative values.

6. **Tiny example (hand-simulated)**  
   Parallel prefix: array [1, 2, 3, 4, 5] → up-sweep: build tree, compute sums → level 1: 1, 2, 3, 4, 5 → level 2: 3, 7, 5 → level 3: 10, 5 → root: 15 → down-sweep: propagate → prefix sums: [1, 3, 6, 10, 15] → parallel execution → O(log n) time with n processors.

7. **Time & Space Complexity**  
   - Time: O(log n) with n processors, O(n) with single processor where n is array size.  
   - Space: O(n) where n is array size (tree structure and output array).

8. **Strengths**  
- Efficiency: O(log n) parallel time complexity.
- Versatility: works with any associative operation.
- Scalability: scales well with number of processors.

9. **Weaknesses / limitations**  
- Complexity: algorithm is more complex than sequential scan.
- Overhead: tree construction and communication overhead.
- Associativity: requires associative operation (not all operations are associative).

10. **Compare with alternatives**  
    Alternatives: Sequential Scan, Parallel Reduction, Tree-based Algorithms, Recursive Doubling

11. **30-second explanation (your own words)**  
    Computes all prefix sums (or other associative operations) of an array in parallel, enabling efficient parallel computation of cumulative operations like running sums, maximums, or products.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
