# Parallel Reduction

1. **Name of Algorithm**  
   Parallel Reduction

2. **What problem does it solve? (1 sentence)**  
   Computes a single aggregate value (sum, product, maximum, etc.) from an array by combining all elements using an associative operation, executing the reduction in parallel across multiple processors.

3. **Intuition (plain-language explanation)**  
   Like a tournament bracket: parallel reduction is like a tournament where you start with many players (array elements), pair them up (combine pairs), winners advance (results), and you keep pairing until one winner remains (final result) - but instead of one match at a time, all matches at each level happen simultaneously (in parallel), making it much faster - the final winner is your aggregate result (sum, max, etc.).

4. **Inputs & Outputs**  
   - Input: Array of values, associative binary operation (addition, multiplication, maximum, minimum, etc.), number of processors.  
   - Output: Single aggregate value, parallel computation result, reduced value.

5. **Step-by-step description (5–10 lines max)**  
1. Partition: divide array into chunks, assign to processors.
2. Local reduce: each processor reduces its chunk to a single value.
3. Combine: combine results from all processors using tree structure.
4. Pair: pair up results and combine them.
5. Repeat: repeat pairing and combining until one value remains.
6. Parallelize: execute all operations at each level in parallel.
7. Synchronize: synchronize processors between levels.
8. Output: return final aggregated value.

6. **Tiny example (hand-simulated)**  
   Parallel reduction: array [1, 2, 3, 4, 5, 6, 7, 8], sum → level 1: [1+2, 3+4, 5+6, 7+8] = [3, 7, 11, 15] (parallel) → level 2: [3+7, 11+15] = [10, 26] (parallel) → level 3: [10+26] = [36] → result: 36 → O(log n) time with n processors → parallel reduction.

7. **Time & Space Complexity**  
   - Time: O(log n) with n processors, O(n) with single processor where n is array size.  
   - Space: O(n) where n is array size (intermediate results storage).

8. **Strengths**  
- Efficiency: O(log n) parallel time complexity.
- Scalability: scales well with number of processors.
- Versatility: works with any associative operation.

9. **Weaknesses / limitations**  
- Associativity: requires associative operation.
- Overhead: synchronization overhead between levels.
- Load balancing: requires careful load balancing for optimal performance.

10. **Compare with alternatives**  
    Alternatives: Sequential Reduction, Tree-based Reduction, MapReduce, Distributed Reduction

11. **30-second explanation (your own words)**  
    Computes a single aggregate value (sum, product, maximum, etc.) from an array by combining all elements using an associative operation, executing the reduction in parallel across multiple processors.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
