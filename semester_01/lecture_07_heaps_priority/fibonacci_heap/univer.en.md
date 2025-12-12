# Fibonacci Heap

## Convergence Speed and Complexity Estimate

**Time Complexity (Amortized):**
- **Insert:** O(1) - amortized constant time. New nodes are simply added to the root list, and minimum pointer is updated if necessary. No tree restructuring required.
- **Find Minimum:** O(1) - minimum pointer provides constant-time access to minimum element.
- **Extract Minimum:** O(log n) - amortized. Requires consolidating trees of same degree, which takes O(log n) time due to Fibonacci number properties.
- **Decrease Key:** O(1) - amortized. Key can be decreased and node cut from parent if heap property violated, with cascading cuts in worst case.
- **Delete:** O(log n) - amortized. Implemented as decrease key to -∞ followed by extract minimum.
- **Union (Merge):** O(1) - amortized. Simply concatenate root lists and update minimum pointer.

**Space Complexity:** O(n) - requires space for n nodes, each containing key, pointers (parent, child, left, right), degree, and mark flag.

**Amortized Analysis:** Fibonacci heaps use amortized analysis because individual operations may be expensive, but over a sequence of operations, the average cost is low. The name "Fibonacci" comes from the fact that trees have sizes related to Fibonacci numbers, ensuring logarithmic height.

**Comparison with Binary Heap:**
- **Binary Heap:** Insert O(log n), Extract Min O(log n), Decrease Key O(log n)
- **Fibonacci Heap:** Insert O(1), Extract Min O(log n), Decrease Key O(1)
- **Advantage:** Fibonacci heap is superior when many decrease key operations are needed (e.g., Dijkstra's algorithm)

**Convergence:** The heap maintains its structure through lazy operations - nodes are added to root list without immediate consolidation. Consolidation (merging trees of same degree) happens during extract minimum, ensuring the heap property is maintained when needed.

## Where the Algorithm is Used in Real Frameworks and Software

Fibonacci heaps are used in algorithms that require many decrease key operations:

- **Graph Algorithms:**
  - **Dijkstra's algorithm** - finding shortest paths with many edge relaxations (decrease key operations)
  - **Prim's algorithm** - finding minimum spanning trees with frequent key updates
  - **Network flow algorithms** - algorithms requiring efficient priority queue operations

- **Optimization Libraries:**
  - **OR-Tools (Google)** - optimization library using Fibonacci heaps internally
  - **NetworkX** - Python graph library (uses heaps for shortest path algorithms)
  - **Boost C++ Libraries** - graph algorithms using Fibonacci heaps

- **Research and Academia:**
  - **Algorithm research** - theoretical computer science, complexity analysis
  - **Advanced algorithms courses** - teaching amortized analysis and advanced data structures
  - **Algorithm competitions** - for problems requiring efficient priority queue operations

- **Real-World Applications:**
  - **Route planning** - GPS systems using Dijkstra's with Fibonacci heaps
  - **Network routing** - finding optimal paths in computer networks
  - **Resource allocation** - optimization problems with frequent priority updates

**Note:** While Fibonacci heaps have excellent theoretical performance, binary heaps are often preferred in practice due to simpler implementation and better constant factors. Fibonacci heaps excel when decrease key operations dominate.

## What It's Similar To in Concept

Fibonacci heaps share conceptual similarities with:

- **Binomial Heaps:** Both are advanced heap data structures supporting merge operations. Fibonacci heaps are essentially a relaxed version of binomial heaps - they delay consolidation until necessary, achieving better amortized bounds.

- **Lazy Evaluation:** Fibonacci heaps use lazy evaluation - operations are deferred (like adding nodes to root list) and work is done only when necessary (consolidation during extract minimum). This is similar to lazy evaluation in functional programming.

- **Amortized Data Structures:** Like other amortized structures (dynamic arrays, splay trees), Fibonacci heaps trade worst-case performance for better amortized performance. Individual operations may be expensive, but average cost is low.

- **Tree Structures:** Fibonacci heaps are collections of trees (like binomial heaps), but trees can have arbitrary structure (not just binomial trees). Trees are merged only when they have the same degree.

- **Priority Queues:** Like binary heaps, Fibonacci heaps implement priority queue operations, but with better amortized bounds for decrease key and merge operations.

## Which Algorithms It's Often Used With

Fibonacci heaps are frequently combined with:

- **Shortest Path Algorithms:**
  - **Dijkstra's algorithm** - O((V + E) log V) with binary heap, O(E + V log V) with Fibonacci heap
  - **Prim's algorithm** - similar improvement for minimum spanning tree

- **Other Advanced Data Structures:**
  - **Binomial heaps** - for comparison and understanding trade-offs
  - **Pairing heaps** - alternative with similar amortized bounds
  - **Binary heaps** - simpler alternative with different trade-offs

- **Graph Algorithms:**
  - **Minimum spanning tree algorithms** - Prim's, Kruskal's (for comparison)
  - **Network flow algorithms** - algorithms requiring efficient priority queues
  - **Shortest path algorithms** - various shortest path problems

- **Optimization Techniques:**
  - **Amortized analysis** - teaching and understanding amortized complexity
  - **Lazy evaluation** - demonstrating deferred computation benefits

## Key Code (Only Important Parts)

Here's a simplified implementation highlighting the essential structure:

```python
class FibonacciHeapNode:
    """Node in Fibonacci heap."""
    def __init__(self, key: int):
        self.key = key
        self.degree = 0  # Number of children
        self.parent = None
        self.child = None  # One child (others linked via left/right)
        self.left = self  # Circular doubly linked list
        self.right = self
        self.mark = False  # For cascading cuts

class FibonacciHeap:
    """Fibonacci heap - advanced priority queue."""
    
    def __init__(self):
        self.min_node = None  # Pointer to minimum node
        self.n = 0  # Number of nodes
    
    def insert(self, key: int) -> FibonacciHeapNode:
        """Insert key - O(1) amortized."""
        node = FibonacciHeapNode(key)
        if self.min_node is None:
            self.min_node = node
        else:
            # Add to root list (circular doubly linked)
            self._add_to_root_list(node)
            if key < self.min_node.key:
                self.min_node = node
        self.n += 1
        return node
    
    def extract_min(self) -> Optional[int]:
        """Extract minimum - O(log n) amortized."""
        if self.min_node is None:
            return None
        
        min_node = self.min_node
        # Add children to root list
        if min_node.child:
            child = min_node.child
            while True:
                next_child = child.right
                self._add_to_root_list(child)
                child.parent = None
                if next_child == min_node.child:
                    break
                child = next_child
        
        # Remove min_node from root list
        self._remove_from_root_list(min_node)
        
        if min_node == min_node.right:
            self.min_node = None
        else:
            self.min_node = min_node.right
            self._consolidate()  # Merge trees of same degree
        
        self.n -= 1
        return min_node.key
    
    def decrease_key(self, node: FibonacciHeapNode, new_key: int) -> None:
        """Decrease key - O(1) amortized."""
        if new_key > node.key:
            raise ValueError("New key must be smaller")
        
        node.key = new_key
        parent = node.parent
        
        if parent and node.key < parent.key:
            self._cut(node, parent)
            self._cascading_cut(parent)
        
        if node.key < self.min_node.key:
            self.min_node = node
    
    def _consolidate(self) -> None:
        """Merge trees of same degree - O(log n) amortized."""
        # Array to track trees by degree
        degree_array = [None] * (self.n.bit_length() + 1)
        
        # Process all trees in root list
        current = self.min_node
        roots = []
        while True:
            roots.append(current)
            current = current.right
            if current == self.min_node:
                break
        
        for node in roots:
            degree = node.degree
            while degree_array[degree] is not None:
                other = degree_array[degree]
                if node.key > other.key:
                    node, other = other, node
                self._link(other, node)  # Make other child of node
                degree_array[degree] = None
                degree += 1
            degree_array[degree] = node
        
        # Rebuild root list and find new minimum
        self.min_node = None
        for node in degree_array:
            if node:
                if self.min_node is None:
                    self.min_node = node
                else:
                    self._add_to_root_list(node)
                    if node.key < self.min_node.key:
                        self.min_node = node
```

**Key Points:**
- Circular doubly linked lists for root list and child lists
- Lazy consolidation - merge trees only during extract minimum
- Cascading cuts - maintain heap property efficiently
- Amortized O(1) insert and decrease key, O(log n) extract minimum

## Common Application Errors

1. **Not Maintaining Circular Lists:**
   - **Error:** Not properly maintaining circular doubly linked list structure
   - **Impact:** Incorrect tree structure, broken heap property
   - **Solution:** Always update left/right pointers when adding/removing nodes

2. **Forgetting Cascading Cuts:**
   - **Error:** Not performing cascading cuts after cutting a node
   - **Impact:** Heap structure degrades, losing amortized bounds
   - **Solution:** Always call cascading cut after cutting a marked node

3. **Incorrect Consolidation:**
   - **Error:** Not merging trees of same degree correctly
   - **Impact:** Heap structure incorrect, extract minimum fails
   - **Solution:** Use array to track trees by degree, merge systematically

4. **Not Updating Minimum Pointer:**
   - **Error:** Forgetting to update min_node after operations
   - **Impact:** Find minimum returns wrong value
   - **Solution:** Always update min_node when inserting or after extract minimum

5. **Memory Management:**
   - **Error:** Not properly cleaning up removed nodes
   - **Impact:** Memory leaks, incorrect structure
   - **Solution:** Properly remove nodes from lists and clear pointers

6. **Confusing with Binary Heap:**
   - **Error:** Implementing binary heap operations instead of Fibonacci heap
   - **Impact:** Missing amortized O(1) operations, incorrect complexity
   - **Solution:** Understand that Fibonacci heap uses lazy evaluation and tree merging

## Recommended Literature

1. **"Introduction to Algorithms" (CLRS)** - Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein
   - Comprehensive coverage of Fibonacci heaps with detailed amortized analysis and proof of complexity bounds

2. **"Algorithm Design Manual"** - Steven S. Skiena
   - Practical discussion of Fibonacci heaps with implementation details and when to use them vs. binary heaps

3. **"Data Structures and Algorithms in Python"** - Michael T. Goodrich, Roberto Tamassia, Michael H. Goldwasser
   - Clear explanation of Fibonacci heaps with Python-specific implementations

4. **"The Art of Computer Programming, Volume 3"** - Donald E. Knuth
   - Original description and analysis of heap data structures

5. **Online Resources:**
   - Wikipedia - Fibonacci heap with detailed explanation and examples
   - GeeksforGeeks - Fibonacci heap tutorials
   - Visualgo.net - heap visualizations (though Fibonacci heap may not be available)
