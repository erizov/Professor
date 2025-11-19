# Floyd-Warshall

1. **Name of Algorithm**  
   Floyd-Warshall

2. **What problem does it solve? (1 sentence)**  
   Finds shortest paths between all pairs of vertices in a weighted graph, handling negative weights (but not negative cycles).

3. **Intuition (plain-language explanation)**  
   Dynamic programming: for each intermediate vertex k, update shortest path between i and j by considering paths through k.

4. **Inputs & Outputs**  
   - Input: Weighted graph G(V,E) with V vertices, edge weights (may be negative, no negative cycles).  
   - Output: Matrix of shortest distances between all pairs; optionally the path reconstruction matrix.

5. **Step-by-step description (5–10 lines max)**  
1. Initialize dist[i][j] = weight(i,j) if edge exists, 0 if i==j, ∞ otherwise.
2. For k from 1 to V: for each pair (i,j), set dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]).
3. After all k, dist[i][j] contains shortest path from i to j.
4. Optionally detect negative cycles: if any dist[i][i] < 0 after algorithm, negative cycle exists.

6. **Tiny example (hand-simulated)**  
   Graph: A→B(1), B→C(2), A→C(5). After k=A,B,C: dist[A][C]=3 (via B), dist[A][B]=1, dist[B][C]=2.

7. **Time & Space Complexity**  
   - Time: O(V³) for three nested loops.  
   - Space: O(V²) for distance matrix.

8. **Strengths**  
- Finds all-pairs shortest paths in one pass.
- Handles negative weights (unlike Dijkstra).

9. **Weaknesses / limitations**  
- Cubic time complexity makes it slow for large graphs.
- Memory usage is O(V²) which can be prohibitive.

10. **Compare with alternatives**  
    Alternatives: Dijkstra (single-source, non-negative), Johnson's (all-pairs, sparse graphs), Bellman-Ford (single-source, negative)

11. **30-second explanation (your own words)**  
    Uses dynamic programming to consider all possible intermediate vertices, building shortest paths incrementally for all pairs.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
