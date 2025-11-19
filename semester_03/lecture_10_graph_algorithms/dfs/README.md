# Depth-First Search (DFS)

1. **Name of Algorithm**  
   Depth-First Search (DFS)

2. **What problem does it solve? (1 sentence)**  
Explores a graph by going as deep as possible along each branch before backtracking, useful for connectivity and cycle detection.

3. **Intuition (plain-language explanation)**  
   Like exploring a maze: go down one path as far as possible, mark where you've been, backtrack when stuck, then try another path.

4. **Inputs & Outputs**  
   - Input: Graph G(V,E) (adjacency list or matrix), starting vertex s (optional).  
   - Output: Visited vertices in DFS order; discovery/finish times; connected components; cycle detection.

5. **Step-by-step description (5–10 lines max)**  
1. Mark current vertex as visited.
2. For each unvisited neighbor: recursively call DFS on that neighbor.
3. After exploring all neighbors, mark vertex as finished (for timing).
4. Backtrack to previous vertex.

6. **Tiny example (hand-simulated)**  
   Graph: A-B-C, A-D. DFS from A: visit A, go to B, go to C (backtrack), backtrack to A, go to D.

7. **Time & Space Complexity**  
   - Time: O(V+E) for adjacency list, O(V²) for adjacency matrix.  
   - Space: O(V) for recursion stack and visited array.

8. **Strengths**  
- Low memory overhead (recursion stack).
- Natural for backtracking and tree/graph traversal.

9. **Weaknesses / limitations**  
- May not find shortest paths (unlike BFS).
- Deep recursion can cause stack overflow for large graphs.

10. **Compare with alternatives**  
    Alternatives: BFS (level-order), Iterative DFS (explicit stack), Topological Sort (DAG)

11. **30-second explanation (your own words)**  
Recursively explores each branch fully before backtracking, useful for connectivity, cycles, and topological ordering.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
