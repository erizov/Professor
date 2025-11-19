# Dijkstra's Algorithm

1. **Name of Algorithm**  
   Dijkstra's Algorithm

2. **What problem does it solve? (1 sentence)**  
   Finds shortest paths from a source to all vertices in a weighted graph with non-negative edge weights.

3. **Intuition (plain-language explanation)**  
   Greedily expands the closest unvisited vertex: maintain a priority queue of vertices by distance, always process the nearest one first.

4. **Inputs & Outputs**  
   - Input: Weighted graph G(V,E) with non-negative weights, source vertex s.  
   - Output: Shortest distances from s to all vertices; optionally the shortest path tree.

5. **Step-by-step description (5–10 lines max)**  
1. Initialize: dist[s]=0, others=∞, priority queue Q contains all vertices.
2. While Q not empty: extract vertex u with minimum distance from Q.
3. For each neighbor v of u: if dist[u]+weight(u,v) < dist[v], update dist[v] and decrease-key in Q.
4. Mark u as processed, repeat until Q is empty.

6. **Tiny example (hand-simulated)**  
   Graph: A→B(4), A→C(2), C→B(1), C→D(5), B→D(1). From A: dist[B]=3 (via C), dist[C]=2, dist[D]=4 (via C and B).

7. **Time & Space Complexity**  
   - Time: O((V+E) log V) with binary heap, O(V²) with array.  
   - Space: O(V) for distance array and priority queue.

8. **Strengths**  
- Efficient for single-source shortest paths with non-negative weights.
- Optimal for dense graphs with proper data structures.

9. **Weaknesses / limitations**  
- Fails with negative edge weights (use Bellman-Ford).
- Requires priority queue for efficiency.

10. **Compare with alternatives**  
    Alternatives: Bellman-Ford (negative weights), Floyd-Warshall (all pairs), A* (heuristic)

11. **30-second explanation (your own words)**  
    Greedily processes vertices in order of increasing distance from source, guaranteeing shortest paths when all weights are non-negative.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
