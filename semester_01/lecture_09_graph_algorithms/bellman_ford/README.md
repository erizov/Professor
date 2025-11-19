# Bellman-Ford Algorithm

1. **Name of Algorithm**  
Bellman-Ford Algorithm

2. **What problem does it solve? (1 sentence)**  
   Computes single-source shortest paths even when negative edge weights are present (assuming no negative cycles).

3. **Intuition (plain-language explanation)**  
   Relax every edge repeatedly so distances shrink over successive passes; if they still shrink after |V|-1 rounds, a negative cycle exists.

4. **Inputs & Outputs**  
   - Input: Directed weighted graph G(V,E) and source vertex s.  
   - Output: Shortest path distances (and optionally predecessors) from s or detection of negative cycles.

5. **Step-by-step description (5–10 lines max)**  
1. Initialize distance[s]=0 and all other distances to +∞.
2. Repeat |V|-1 times: for each edge (u,v,w), relax by setting dist[v] = min(dist[v], dist[u] + w).
3. Track predecessors when an edge improves a distance.
4. Perform one more pass; if any edge can still relax, report a negative cycle.
5. Return distance and predecessor arrays.

6. **Tiny example (hand-simulated)**  
   Edges (0→1,5), (0→2,4), (2→1,-6), (1→3,3): after relaxation, dist[3]=2 via 0→2→1→3.

7. **Time & Space Complexity**  
   - Time: O(|V|·|E|).  
   - Space: O(|V|) for distance and predecessor arrays.

8. **Strengths**  
- Handles negative weights safely.
- Simple dynamic programming formulation.

9. **Weaknesses / limitations**  
- Slower than Dijkstra on graphs without negative edges.
- Detecting negative cycles requires an additional pass.

10. **Compare with alternatives**  
Alternatives: Dijkstra, Johnson's Algorithm, SPFA

11. **30-second explanation (your own words)**  
    Iteratively relaxes all edges to propagate better distances, making it robust for graphs with negative weights.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
