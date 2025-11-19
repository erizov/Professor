# Parallel Algorithms

1. **Name of Algorithm**  
   Parallel Algorithms

2. **What problem does it solve? (1 sentence)**  
   Designs algorithms that execute multiple operations simultaneously across multiple processors or cores, reducing execution time and improving throughput for computationally intensive problems.

3. **Intuition (plain-language explanation)**  
   Like a team working together: parallel algorithms are like having a team of people work on a project simultaneously instead of one person doing everything sequentially - you divide the work (problem decomposition), assign tasks to team members (processors), they work in parallel (simultaneous execution), and you combine their results (result aggregation) - the goal is to finish faster by doing work in parallel, though coordination overhead (communication) limits how much faster you can go.

4. **Inputs & Outputs**  
   - Input: Problem data, number of processors, parallel computation model, communication patterns.  
   - Output: Parallel execution, reduced computation time, improved throughput, scalable performance.

5. **Step-by-step description (5–10 lines max)**  
1. Analyze problem: identify parallelism opportunities in problem.
2. Decompose: decompose problem into independent or loosely coupled subproblems.
3. Choose model: select parallel computation model (PRAM, BSP, MapReduce, etc.).
4. Design algorithm: design algorithm with parallel execution in mind.
5. Partition data: partition data across processors.
6. Execute: execute operations in parallel across processors.
7. Communicate: coordinate and communicate between processors if needed.
8. Synchronize: synchronize processors at coordination points.
9. Combine: aggregate results from parallel computations.
10. Analyze: analyze speedup, efficiency, and scalability.

6. **Tiny example (hand-simulated)**  
   Parallel algorithm: matrix multiplication C = A × B → decompose: partition matrices into blocks → assign: each processor computes one block of C → parallel: all processors compute simultaneously → communicate: processors exchange data as needed → combine: assemble final matrix C → speedup: 8 processors → 6x speedup (not 8x due to communication overhead) → parallel algorithm.

7. **Time & Space Complexity**  
   - Time: O(n³/p + n²) for matrix multiplication where n is matrix size, p is processors (theoretical), actual depends on communication overhead.  
   - Space: O(n²/p) per processor where n is problem size, p is processors (data partitioned).

8. **Strengths**  
- Speedup: reduces execution time for parallelizable problems.
- Scalability: can scale to large numbers of processors.
- Throughput: improves overall system throughput.

9. **Weaknesses / limitations**  
- Overhead: communication and synchronization overhead limits speedup.
- Complexity: parallel algorithms are more complex than sequential ones.
- Scalability: not all problems scale well with number of processors.

10. **Compare with alternatives**  
    Alternatives: Sequential Algorithms, Distributed Algorithms, GPU Algorithms, Vectorized Algorithms

11. **30-second explanation (your own words)**  
    Designs algorithms that execute multiple operations simultaneously across multiple processors or cores, reducing execution time and improving throughput for computationally intensive problems.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
