# Dfs

# Univer

## 📋 Quick Summary

- **Purpose:** Dfs: Go deep first - explore as far as possible along each branch before backtracking.
- **Complexity:** O(V + E)
- **Category:** Algorithms
- **Key Idea:** Go deep first - explore as far as possible along each branch before backtracking.

Dfs: Go deep first - explore as far as possible along each branch before backtracking.

Go deep first - explore as far as possible along each branch before backtracking.

**DFS** = Depth First Search. Like exploring a maze - go as deep as possible down one path before trying another.








This algorithm belongs to the **Sorting** category and employs systematic data processing to achieve its objectives.


> **Note**: Mermaid diagrams are rendered automatically on GitHub. For local viewing, use a Mermaid-compatible Markdown viewer.



## Complexity Analysis

**Time Complexity:** O(n²)
- The algorithm's performance scales according to this complexity class
- Best, average, and worst cases may vary based on input characteristics

**Space Complexity:** O(1)
- Indicates the amount of additional memory required during execution

**Key Data Structures:** stack, hash table/dictionary

## Real-World Applications

Dfs is used in:
- Sorting arrays in programming languages (Python sorted(), Java Collections.sort())
- Database query optimization and indexing
- Operating system process scheduling
- E-commerce product listings and price sorting

## Conceptual Similarities

This algorithm shares conceptual similarities with other algorithms in the Sorting category, following similar design patterns and optimization strategies.

## Related Algorithms

Dfs is often used in combination with:
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

    def dfs(
        self, start: int, visit_callback: Callable[[int], None] = None
    ) -> List[int]:
        """
        Perform DFS traversal from start node.

        Args:
            start: Starting node
            visit_callback: Optional callback for each visited node

        Returns:
            List of nodes in DFS order
        """
        visited: Set[int] = set()
        result: List[int] = []

        def dfs_recursive(node: int) -> None:
            visited.add(node)
            result.append(node)

            if visit_callback:
                visit_callback(node)

            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    dfs_recursive(neighbor)

        dfs_recursive(start)
        return result

    def dfs_iterative(self, start: int) -> List[int]:
        """
        Iterative DFS using explicit stack.

        Args:
            start: Starting node

        Returns:
            List of nodes in DFS order
        """
        visited: Set[int] = set()
        result: List[int] = []
        stack: List[int] = [start]

        while stack:
            node = stack.pop()

            if node not in visited:
                visited.add(node)
                result.append(node)

                # Add neighbors in reverse order for consistent ordering
                for neighbor in reversed(self.graph[node]):
                    if neighbor not in visited:
                        stack.append(neighbor)

        return result

    def dfs_all(self) -> List[List[int]]:
        """
        Perform DFS on all connected components.

        Returns:
            List of components (each component is a list of nodes)
        """
        visited: Set[int] = set()
        components: List[List[int]] = []

        def dfs_component(node: int, component: List[int]) -> None:
            visited.add(node)
            component.append(node)

            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    dfs_component(neighbor, component)

        # Visit all nodes
        all_nodes = set(self.graph.keys())
        for node in self.graph.values():
            all_nodes.update(node)

        for node in all_nodes:
            if node not in visited:
                component: List[int] = []
                dfs_component(node, component)
                components.append(component)

        return components

    def has_cycle(self) -> bool:
        """
        Detect cycle using DFS.

        Returns:
            True if cycle exists, False otherwise
        """
        visited: Set[int] = set()
        rec_stack: Set[int] = set()

        def has_cycle_util(node: int, parent: int = -1) -> bool:
            visited.add(node)
            rec_stack.add(node)

            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    if has_cycle_util(neighbor, node):
                        return True
                elif neighbor != parent:  # For undirected graphs
                    return True

            rec_stack.remove(node)
            return False

        all_nodes = set(self.graph.keys())
        for node in all_nodes:
            if node not in visited:
                if has_cycle_util(node):
                    return True

        return False

    def topological_sort(self) -> List[int]:
        """
        Topological sort using DFS (only for DAG).

        Returns:
            Topologically sorted list of nodes
        """
        if not self.directed:
            raise ValueError("Topological sort only for directed graphs")

        visited: Set[int] = set()
        stack: List[int] = []

        def topological_sort_util(node: int) -> None:
            visited.add(node)

            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    topological_sort_util(neighbor)

            stack.append(node)

        all_nodes = set(self.graph.keys())
        for node in all_nodes:
            if node not in visited:
                topological_sort_util(node)

        return stack[::-1]
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