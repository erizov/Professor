# Bfs

# Univer

## 📋 Quick Summary

- **Purpose:** Bfs: Explore level by level - visit all neighbors before moving to the next level, like ripples in water.
- **Complexity:** O(V + E)
- **Category:** Algorithms
- **Key Idea:** Explore level by level - visit all neighbors before moving to the next level, like ripples in water.

Bfs: Explore level by level - visit all neighbors before moving to the next level, like ripples in water.

Explore level by level - visit all neighbors before moving to the next level, like ripples in water.

**BFS** = Breadth First Search. Like exploring a maze room by room, level by level - visit all neighbors first!








This algorithm belongs to the **Sorting** category and employs systematic data processing to achieve its objectives.


> **Note**: Mermaid diagrams are rendered automatically on GitHub. For local viewing, use a Mermaid-compatible Markdown viewer.



## Complexity Analysis

**Time Complexity:** O(n²)
- The algorithm's performance scales according to this complexity class
- Best, average, and worst cases may vary based on input characteristics

**Space Complexity:** O(1)
- Indicates the amount of additional memory required during execution

**Key Data Structures:** queue, stack, hash table/dictionary

## Real-World Applications

Bfs is used in:
- Sorting arrays in programming languages (Python sorted(), Java Collections.sort())
- Database query optimization and indexing
- Operating system process scheduling
- E-commerce product listings and price sorting

## Conceptual Similarities

This algorithm shares conceptual similarities with other algorithms in the Sorting category, following similar design patterns and optimization strategies.

## Related Algorithms

Bfs is often used in combination with:
- Complementary algorithms for preprocessing or post-processing
- Data structures that optimize its performance
- Other algorithms in the same complexity class

## Key Implementation Details

```python
class Graph:
    """Graph representation using adjacency list."""

    def __init__(self, directed: bool = False):
        """
        Initialize graph.

        Args:
            directed: True for directed graph, False for undirected
        """
        self.graph: Dict[int, List[int]] = defaultdict(list)
        self.directed = directed

    def add_edge(self, u: int, v: int) -> None:
        """Add edge to graph."""
        self.graph[u].append(v)
        if not self.directed:
            self.graph[v].append(u)

    def bfs(self, start: int) -> List[int]:
        """
        Perform BFS traversal from start node.

        Args:
            start: Starting node

        Returns:
            List of nodes in BFS order
        """
        visited: Set[int] = set()
        result: List[int] = []
        queue: deque = deque([start])
        visited.add(start)

        while queue:
            node = queue.popleft()
            result.append(node)

            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return result

    def shortest_path(self, start: int, end: int) -> Optional[List[int]]:
        """
        Find shortest path using BFS.

        Args:
            start: Start node
            end: End node

        Returns:
            List representing path, or None if no path exists
        """
        if start == end:
            return [start]

        visited: Set[int] = {start}
        queue: deque = deque([(start, [start])])

        while queue:
            node, path = queue.popleft()

            for neighbor in self.graph[node]:
                if neighbor == end:
                    return path + [neighbor]

                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return None  # No path found

    def shortest_distance(self, start: int, end: int) -> int:
        """
        Find shortest distance (number of edges) using BFS.

        Args:
            start: Start node
            end: End node

        Returns:
            Distance, or -1 if no path
        """
        if start == end:
            return 0

        visited: Set[int] = {start}
        queue: deque = deque([(start, 0)])

        while queue:
            node, dist = queue.popleft()

            for neighbor in self.graph[node]:
                if neighbor == end:
                    return dist + 1

                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))

        return -1  # No path

    def all_paths_distance(self, start: int) -> Dict[int, int]:
        """
        Find shortest distance from start to all reachable nodes.

        Args:
            start: Starting node

        Returns:
            Dictionary mapping node to distance
        """
        distances: Dict[int, int] = {start: 0}
        queue: deque = deque([start])

        while queue:
            node = queue.popleft()
            current_dist = distances[node]

            for neighbor in self.graph[node]:
                if neighbor not in distances:
                    distances[neighbor] = current_dist + 1
                    queue.append(neighbor)

        return distances

    def is_bipartite(self) -> bool:
        """
        Check if graph is bipartite using BFS.

        Returns:
            True if bipartite, False otherwise
        """
        # Color nodes with 0 and 1
        colors: Dict[int, int] = {}

        # Get all nodes
        all_nodes = set(self.graph.keys())
        for neighbors in self.graph.values():
            all_nodes.update(neighbors)

        # Check each component
        for start_node in all_nodes:
            if start_node in colors:
                continue

            # BFS coloring
            queue: deque = deque([start_node])
            colors[start_node] = 0

            while queue:
                node = queue.popleft()
                current_color = colors[node]
                next_color = 1 - current_color

                for neighbor in self.graph[node]:
                    if neighbor not in colors:
                        colors[neighbor] = next_color
                        queue.append(neighbor)
                    elif colors[neighbor] != next_color:
                        return False  # Adjacent nodes same color

        return True
```


## Common Application Errors

- **Incorrect handling of edge cases:** [Algorithm-specific edge case]. Solution: [Specific solution].

- **Misunderstanding complexity implications:** [Algorithm-specific complexity issue]. Solution: [Specific solution].

- **Suboptimal implementation:** [Algorithm-specific performance issue]. Solution: [Specific solution].

- **Incorrect assumptions about input:** [Algorithm-specific input assumption]. Solution: [Specific solution].

- **Not considering alternatives:** [Algorithm-specific alternative consideration]. Solution: [Specific solution].


## Recommended Literature

- "Introduction to Algorithms" (CLRS) - Comprehensive algorithm analysis
- "Algorithm Design Manual" by Steven Skiena
- "Algorithms" by Sedgewick and Wayne
- Research papers on algorithm optimization and analysis
- Framework documentation and implementation guides



---

## 🎯 Try It Yourself

**Try this example:**
```
Input: [example data]

Step 1: Initialize algorithm state
Step 2: Process input data
Step 3: Generate result

Output: [algorithm result]
```



## Common Mistakes

### ❌ Mistake 1: Not handling edge cases
**Solution:** Always check for empty input, single element, or boundary values before processing.

### ❌ Mistake 2: Incorrect initialization
**Solution:** Ensure all variables and data structures are properly initialized before the main algorithm loop.

### ❌ Mistake 3: Off-by-one errors in loops
**Solution:** Carefully verify loop bounds and termination conditions. Test with small examples to catch boundary issues.

### ❌ Mistake 4: Not validating input
**Solution:** Add input validation to ensure data is in expected format and within valid ranges.

### 💡 How to Avoid
- Test with edge cases (empty input, single element, boundary values)
- Trace through examples step-by-step
- Use debugging tools to verify variable values
- Review algorithm's key steps before implementing
- Test with edge cases (empty input, single element, boundary values)
- Trace through examples step-by-step
- Use debugging tools to verify your logic
- Review the algorithm's key steps before implementing