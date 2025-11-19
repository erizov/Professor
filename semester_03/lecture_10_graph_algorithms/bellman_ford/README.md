# Bellman-Ford

1. **Name of Algorithm**  
   Bellman-Ford

2. **What problem does it solve? (1 sentence)**  
   Finds shortest paths from a source to all vertices in a weighted graph, even with negative edge weights (detects negative cycles).

3. **Intuition (plain-language explanation)**  
   Relax all edges repeatedly: after V-1 iterations, shortest paths are found; if another relaxation improves a distance, a negative cycle exists.

4. **Inputs & Outputs**  
   - Input: Weighted directed graph G(V,E), source vertex s, edge weights (may be negative).  
   - Output: Shortest distances from s to all vertices; optionally detects negative cycles.

5. **Step-by-step description (5–10 lines max)**  
1. Initialize distance array: dist[s]=0, others=∞.
2. Relax all edges V-1 times: for each edge (u,v) with weight w, if dist[u]+w < dist[v], update dist[v]=dist[u]+w.
3. After V-1 iterations, check for negative cycles: if any edge (u,v) still relaxes, negative cycle exists.
4. Return distances (or report cycle if detected).

6. **Tiny example (hand-simulated)**  
   Graph: A→B(1), B→C(-2), C→A(1). After 3 iterations: dist[A]=0, dist[B]=1, dist[C]=-1. Cycle check: C→A relaxes → negative cycle detected.

7. **Time & Space Complexity**  
   - Time: O(V·E) for V-1 iterations over E edges.  
   - Space: O(V) for distance array.

8. **Strengths**  
- Handles negative edge weights (unlike Dijkstra).
- Detects negative cycles in the graph.

9. **Weaknesses / limitations**  
- Slower than Dijkstra for positive weights (O(V·E) vs O(E log V)).
- Requires V-1 full passes over all edges.

10. **Compare with alternatives**  
    Alternatives: Dijkstra (positive weights), Floyd-Warshall (all pairs), SPFA (optimized variant)

11. **30-second explanation (your own words)**  
    Repeatedly relaxes all edges V-1 times; if distances can still improve after that, a negative cycle exists.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
