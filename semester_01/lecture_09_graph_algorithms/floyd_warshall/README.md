# Floyd-Warshall Algorithm

1. **Name of Algorithm**  
   Floyd-Warshall Algorithm

2. **What problem does it solve? (1 sentence)**  
   Computes all-pairs shortest paths on weighted graphs (positive or negative edges, excluding negative cycles).

3. **Intuition (plain-language explanation)**  
   Dynamic programming over intermediate vertices: allow paths to use the first k vertices and iteratively increase k.

4. **Inputs & Outputs**  
   - Input: Weighted adjacency matrix for graph with n vertices.  
   - Output: n×n matrix of shortest path distances (and optionally predecessor matrix).

5. **Step-by-step description (5–10 lines max)**  
1. Initialize dist[i][j] with edge weights, set dist[i][i]=0.
2. For k from 1 to n: for each pair (i,j), set dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]).
3. Optionally maintain next[i][j] to reconstruct paths.
4. After loops, dist contains shortest distances using any intermediate vertex.
5. Detect negative cycles if any dist[i][i] < 0.

6. **Tiny example (hand-simulated)**  
   For 3-vertex graph, algorithm considers whether going through vertex 2 improves distance from 1 to 3 and updates matrix accordingly.

7. **Time & Space Complexity**  
   - Time: O(n^3).  
   - Space: O(n^2).

8. **Strengths**  
- Handles negative weights and finds all-pairs distances in one pass.
- Simple triple-loop implementation.

9. **Weaknesses / limitations**  
- Cubic runtime becomes expensive for large graphs.
- Requires dense matrix storage even for sparse graphs.

10. **Compare with alternatives**  
    Alternatives: Repeated Dijkstra, Johnson's Algorithm, APSP via matrix multiplication

11. **30-second explanation (your own words)**  
    Systematically checks whether including each vertex k shortens the path between i and j, yielding all-pairs solutions.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
