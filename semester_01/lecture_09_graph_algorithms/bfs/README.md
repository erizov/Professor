# Breadth-First Search

1. **Name of Algorithm**  
   Breadth-First Search

2. **What problem does it solve? (1 sentence)**  
   Traverses graphs level by level to find the shortest path in unweighted graphs and to explore reachable vertices.

3. **Intuition (plain-language explanation)**  
   Expand the frontier like ripples in a pond: visit all vertices one edge away before moving farther out.

4. **Inputs & Outputs**  
   - Input: Graph G(V,E) and optional start vertex.  
   - Output: Visit order, distance in edges, and predecessor tree for shortest paths.

5. **Step-by-step description (5–10 lines max)**  
1. Mark the start vertex as discovered, set distance 0, and enqueue it.
2. While the queue is not empty, dequeue vertex u.
3. For each neighbor v of u: if undiscovered, mark it, set parent[v]=u, dist[v]=dist[u]+1, enqueue v.
4. Continue until queue empty to explore connected component.
5. Use predecessor pointers to reconstruct shortest paths.

6. **Tiny example (hand-simulated)**  
   Graph 0-1-2-3 with extra edge 0-2. BFS from 0 visits 0,1,2,3; dist[3]=2 via 0→2→3.

7. **Time & Space Complexity**  
   - Time: O(|V| + |E|).  
   - Space: O(|V|) for queue, visited, and parent arrays.

8. **Strengths**  
- Guarantees shortest paths in unweighted graphs.
- Useful for level-order traversal, bipartite checking, and finding connected components.

9. **Weaknesses / limitations**  
- Requires memory proportional to the frontier size.
- Does not handle weights without modification.

10. **Compare with alternatives**  
    Alternatives: Depth-First Search, Dijkstra, A*

11. **30-second explanation (your own words)**  
    Uses a queue to expand vertices in increasing distance from the source, ensuring level-order exploration.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
