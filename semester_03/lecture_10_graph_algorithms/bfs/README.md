# Breadth-First Search (BFS)

1. **Name of Algorithm**  
   Breadth-First Search (BFS)

2. **What problem does it solve? (1 sentence)**  
   Explores a graph level by level, visiting all neighbors before moving to the next depth, finding shortest unweighted paths.

3. **Intuition (plain-language explanation)**  
   Like ripples in water: start from source, visit all immediate neighbors first, then their neighbors, maintaining a queue of vertices to explore.

4. **Inputs & Outputs**  
   - Input: Graph G(V,E) (adjacency list or matrix), source vertex s.  
   - Output: Visited vertices in BFS order; distances/parents for shortest path reconstruction.

5. **Step-by-step description (5–10 lines max)**  
1. Initialize queue with source s, mark s as visited.
2. While queue not empty: dequeue vertex u.
3. For each unvisited neighbor v of u: mark v visited, set distance[v]=distance[u]+1, enqueue v.
4. Continue until queue is empty.

6. **Tiny example (hand-simulated)**  
   Graph: A-B-C, A-D. BFS from A: visit A (level 0), then B and D (level 1), then C (level 2).

7. **Time & Space Complexity**  
   - Time: O(V+E) for adjacency list, O(V²) for adjacency matrix.  
   - Space: O(V) for queue and visited array.

8. **Strengths**  
- Finds shortest unweighted paths efficiently.
- Guarantees level-order traversal.

9. **Weaknesses / limitations**  
- Only works for unweighted graphs (use Dijkstra for weighted).
- Memory usage grows with graph breadth.

10. **Compare with alternatives**  
    Alternatives: DFS (depth-first), Dijkstra (weighted shortest paths), A* (heuristic search)

11. **30-second explanation (your own words)**  
    Uses a queue to explore vertices level by level, ensuring shortest paths in unweighted graphs.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
