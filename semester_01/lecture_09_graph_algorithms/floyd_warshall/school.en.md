# Floyd-Warshall Algorithm

## Principle of Operation

Floyd-Warshall algorithm finds the shortest path between EVERY pair of vertices in a graph. Unlike Dijkstra or Bellman-Ford which find paths from one starting point, Floyd-Warshall finds all possible shortest paths at once.

**How it works:**
1. Create a table (matrix) with distances between all pairs of vertices
2. Initially, put direct edge distances, or infinity if no direct edge
3. For each vertex k (one at a time):
   - Check if going through vertex k gives a shorter path between any two vertices
   - If yes, update the distance in the table
4. After checking all vertices as "middle points", the table has all shortest paths

**Simple analogy:** Imagine you're planning routes between all cities. First, you only know direct routes. Then you realize: "If I go through City A, can I get from City B to City C faster?" You check this for every city as a middle point, and update your route table. After checking all cities, you have the best routes between every pair.

**Key idea:** Floyd-Warshall uses "dynamic programming" - it builds up solutions by considering paths through more and more intermediate vertices. It's like gradually building a complete map of shortest routes.

## Algorithm Complexity

**Time Complexity:** O(V³)
- V = number of vertices
- Three nested loops: for each intermediate vertex, check all pairs
- Always O(V³) regardless of how many edges the graph has

**Space Complexity:** O(V²)
- Need a V×V table to store distances between all pairs
- Can reuse the same table (update in place)
- For path reconstruction, need another V×V table

**Why it's O(V³):** The algorithm has three nested loops, each going through all V vertices. This gives V × V × V = V³ operations. It's the same whether the graph has few edges (sparse) or many edges (dense).

## Where It's Used in Practice

**Network Routing:**
- **Routing tables** - precomputing shortest paths between all node pairs
- Internet protocols - knowing best routes between all routers
- Network planning - designing optimal network topologies

**Transportation:**
- **GPS systems** - precomputing distances for fast route queries
- Route planning apps - finding shortest routes between any two cities
- Logistics - optimizing delivery routes between all locations

**Social Networks:**
- **Degrees of separation** - finding shortest connection paths between all user pairs
- Network analysis - understanding how connected everyone is
- Influence analysis - finding shortest influence paths

**Games:**
- **Pathfinding precomputation** - precomputing paths for fast game queries
- Level design - ensuring all areas are reachable
- Multi-agent systems - computing distances between all agents

**Real-World Applications:**
- Transitive closure - determining if you can reach any point from any other point
- Negative cycle detection - finding problematic cycles in networks
- Network analysis - understanding complete graph structure

## What It Can Be Compared To

**Like a Complete Distance Table:**
- Instead of calculating distances on-demand, precompute everything
- Like having a complete map with distances between all cities
- Trade-off: uses more memory but queries are instant

**Like Dynamic Programming:**
- Builds up solutions step by step
- First considers paths with no intermediate vertices (direct edges)
- Then paths with 1 intermediate vertex, then 2, and so on
- Classic DP pattern: solving subproblems to build solution

**Like Matrix Multiplication:**
- The algorithm structure looks like matrix operations
- Updates a matrix iteratively
- Some variants actually use matrix multiplication

**Different from Dijkstra/Bellman-Ford:**
- Those find paths from ONE starting point
- Floyd-Warshall finds paths between ALL pairs at once
- Slower for single-source problems, but faster when you need all pairs

**Like Building a Complete Map:**
- Instead of finding one route at a time
- Build the entire route map once
- Then any route query is instant (just look it up)

## Minimal Code Example

Here's a simple Floyd-Warshall implementation:

```python
def floyd_warshall(graph):
    """Find shortest distances between all pairs of vertices."""
    V = len(graph)
    
    # Initialize distance matrix
    # dist[i][j] = distance from i to j
    dist = [[float('inf')] * V for _ in range(V)]
    
    # Set distance to self as 0
    for i in range(V):
        dist[i][i] = 0
    
    # Set direct edge distances
    for u in graph:
        for v, weight in graph[u]:
            dist[u][v] = weight
    
    # Main algorithm: try each vertex as intermediate
    for k in range(V):  # Intermediate vertex
        for i in range(V):  # Source vertex
            for j in range(V):  # Destination vertex
                # If going through k gives shorter path, update it
                if dist[i][k] != float('inf') and dist[k][j] != float('inf'):
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    
    return dist

# Example usage:
graph = {
    0: [(1, 3), (2, 8)],
    1: [(2, 1)],
    2: [(0, 2)]
}
distances = floyd_warshall(graph)
# distances[i][j] = shortest distance from i to j
```

**Key parts:**
- Three nested loops: k (intermediate), i (source), j (destination)
- Check: `dist[i][k] + dist[k][j] < dist[i][j]`?
- Update if shorter path found through intermediate vertex k
- After all iterations, matrix has all shortest paths

## Common Mistakes

1. **Wrong Loop Order:**
   - **Wrong:** Changing the order of nested loops (k, i, j)
   - **Why it's wrong:** Algorithm correctness depends on processing intermediate vertices in outer loop
   - **Fix:** Always have k (intermediate) as outermost loop

2. **Not Initializing Diagonal:**
   - **Wrong:** Forgetting to set `dist[i][i] = 0` for all i
   - **Why it's wrong:** Distance from vertex to itself should be 0
   - **Fix:** Always initialize diagonal to 0

3. **Not Handling Infinity:**
   - **Wrong:** Adding infinity values without checking
   - **Why it's wrong:** Infinity + number = infinity, but need to check first
   - **Fix:** Check `if dist[i][k] != float('inf')` before adding

4. **Using for Single-Source Problems:**
   - **Wrong:** Using Floyd-Warshall when you only need paths from one source
   - **Why it's wrong:** Much slower than Dijkstra or Bellman-Ford for single source
   - **Fix:** Use Dijkstra/Bellman-Ford for single source, Floyd-Warshall only for all pairs

5. **Not Detecting Negative Cycles:**
   - **Wrong:** Not checking if diagonal becomes negative after algorithm
   - **Why it's wrong:** Negative diagonal indicates negative cycle
   - **Fix:** After algorithm, check if any `dist[i][i] < 0` (negative cycle exists)

6. **Wrong Matrix Initialization:**
   - **Wrong:** Not properly initializing with direct edge weights
   - **Why it's wrong:** Algorithm needs correct starting distances
   - **Fix:** Initialize with direct edges, infinity for no edge, 0 for self

## Recommended Literature

1. **"Grokking Algorithms"** by Aditya Bhargava
   - Simple explanations of all-pairs shortest paths
   - Good visualizations of how the algorithm builds up solutions

2. **"Introduction to Algorithms" (CLRS)**
   - Comprehensive coverage with detailed analysis
   - Explains the dynamic programming approach and correctness

3. **"Algorithm Design Manual"** by Steven Skiena
   - Practical approach with real-world examples
   - Discusses when to use Floyd-Warshall vs. other algorithms

4. **"Data Structures and Algorithms in Python"** by Goodrich, Tamassia, Goldwasser
   - Clear Python implementations
   - Good for understanding the matrix update process

5. **Online Resources:**
   - Visualgo.net - interactive Floyd-Warshall visualization
   - Khan Academy - step-by-step tutorials
   - LeetCode - practice problems with all-pairs shortest paths
