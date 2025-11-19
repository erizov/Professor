# Dijkstra's Algorithm

1. **Name of Algorithm**  
   Dijkstra's Algorithm

2. **What problem does it solve? (1 sentence)**  
   Computes shortest paths from a single source in graphs with non-negative edge weights.

3. **Intuition (plain-language explanation)**  
   Grow a settled set of nodes: always expand the vertex with the smallest tentative distance because no shorter route to it can exist.

4. **Inputs & Outputs**  
   - Input: Graph with non-negative edge weights and source vertex.  
   - Output: Shortest path distances and predecessors for each reachable vertex.

5. **Step-by-step description (5–10 lines max)**  
1. Initialize distance[source]=0, others=∞; push source into priority queue.
2. Extract vertex u with smallest distance.
3. For each edge (u,v,w), relax: if dist[u]+w < dist[v], update and push v.
4. Mark u as settled so it will not be processed again.
5. Continue until queue empty; reconstruct paths from predecessor array.

6. **Tiny example (hand-simulated)**  
   Edges A→B(2), A→C(5), B→C(1). Algorithm finds dist[C]=3 via A→B→C.

7. **Time & Space Complexity**  
   - Time: O((|V| + |E|) log |V|) with binary heap.  
   - Space: O(|V|) for distance array and priority queue entries.

8. **Strengths**  
- Fast on sparse graphs with non-negative weights.
- Widely used in routing, navigation, and network optimization.

9. **Weaknesses / limitations**  
- Fails with negative edge weights.
- Priority queue operations dominate costs on dense graphs.

10. **Compare with alternatives**  
    Alternatives: Bellman-Ford, A*, Johnson's Algorithm

11. **30-second explanation (your own words)**  
    Repeatedly selects the closest unsettled vertex and relaxes its edges, guaranteeing optimal distances when weights are non-negative.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
