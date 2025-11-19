# Depth-First Search

1. **Name of Algorithm**  
   Depth-First Search

2. **What problem does it solve? (1 sentence)**  
   Explores a graph by going as deep as possible along each branch before backtracking.

3. **Intuition (plain-language explanation)**  
   Like navigating a maze by always taking the next unexplored corridor until you hit a dead end, then backing up.

4. **Inputs & Outputs**  
   - Input: Graph representation plus optional start vertex.  
   - Output: Discovery/finish times, parent tree, and traversal order.

5. **Step-by-step description (5–10 lines max)**  
1. Start at chosen vertex, mark it visited, record discovery time.
2. Recursively visit each unvisited neighbor (or use an explicit stack).
3. After exploring neighbors, record finish time and backtrack.
4. Repeat for any unvisited vertex to cover disconnected components.
5. Leverage recorded times for cycle detection, topological sort, and strongly connected components.

6. **Tiny example (hand-simulated)**  
   DFS on graph 0-1-2-3 explores path 0→1→2→3, then backtracks to explore remaining edges.

7. **Time & Space Complexity**  
   - Time: O(|V| + |E|).  
   - Space: O(|V|) recursion stack in worst case.

8. **Strengths**  
- Foundation for algorithms like topological sort and SCCs.
- Memory-light compared to BFS on dense layers.

9. **Weaknesses / limitations**  
- Paths found are not guaranteed shortest.
- Deep recursion can overflow the stack on large graphs.

10. **Compare with alternatives**  
    Alternatives: Breadth-First Search, Iterative Deepening DFS, Tarjan's Algorithm

11. **30-second explanation (your own words)**  
    Explores one branch completely before moving to the next, making it ideal for exhaustive search and backtracking problems.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
