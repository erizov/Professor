# Priority Queue

## Convergence Speed and Complexity Estimate

**Time Complexity:**
- **Best Case:** O(log n) - for insert and extract operations when implemented with binary heap. The heap property maintenance requires logarithmic time.
- **Average Case:** O(log n) - consistent performance for enqueue (insert) and dequeue (extract) operations.
- **Worst Case:** O(log n) - same as best case! Priority queues implemented with heaps guarantee logarithmic performance.

**Space Complexity:** O(n) - requires space for n elements. When implemented with binary heap, uses array representation which is space-efficient.

**Convergence:** Operations converge by maintaining the priority ordering through heap operations. Insert operations bubble up to maintain heap property, extract operations bubble down after removing the root.

## Where the Algorithm is Used in Real Frameworks and Software

Priority Queues are fundamental abstract data types used extensively:

- **Programming Languages and Standard Libraries:**
  - **Python's `heapq` module** - provides priority queue functionality
  - **Java's `PriorityQueue`** - standard library implementation
  - **C++ STL `priority_queue`** - template-based priority queue
  - **Many language standard libraries** provide priority queue implementations

- **Algorithm Implementations:**
  - **Dijkstra's algorithm** - uses priority queue for finding shortest paths in graphs
  - **Prim's algorithm** - uses priority queue for minimum spanning tree
  - **A* pathfinding** - uses priority queue for optimal path search
  - **Huffman coding** - uses priority queue for building Huffman trees

- **System Software:**
  - **Operating system schedulers** - priority-based process/thread scheduling
  - **Event-driven simulation** - scheduling events by priority/time
  - **Task schedulers** in real-time and embedded systems
  - **Network packet scheduling** - priority-based packet transmission

- **Real-World Applications:**
  - **Job scheduling** systems (print queues, task queues)
  - **Hospital emergency rooms** - patient triage by priority
  - **CPU scheduling** - processes with different priorities
  - **Game AI** - A* pathfinding for NPC movement

## What It's Similar To in Concept

Priority Queues share conceptual similarities with:

- **Queues (FIFO):** Both are abstract data types for managing elements, but priority queues order by priority rather than insertion order. Regular queues are FIFO (first in, first out), priority queues are priority-based.

- **Stacks (LIFO):** Both manage elements, but stacks use LIFO (last in, first out) while priority queues use priority ordering.

- **Binary Heaps:** Binary heaps are the most common implementation of priority queues. The heap property ensures highest-priority element is at root.

- **Sorted Lists/Arrays:** Both maintain ordering, but priority queues optimize for insert/extract operations (O(log n)) while sorted arrays require O(n) for insertion.

## Which Algorithms It's Often Used With

Priority Queues are frequently combined with:

- **Graph Algorithms:**
  - **Dijkstra's algorithm** - min-priority queue for shortest paths
  - **Prim's algorithm** - priority queue for MST edges
  - **A* search** - priority queue with f(n) = g(n) + h(n) heuristic

- **Greedy Algorithms:**
  - **Activity selection** - scheduling by finish time (priority)
  - **Huffman coding** - building trees by frequency (priority)
  - **Interval scheduling** - selecting non-overlapping intervals

- **Sorting Algorithms:**
  - **Heap Sort** - uses priority queue (heap) for sorting
  - Demonstrates relationship between data structures and sorting

## Key Code (Only Important Parts)

Here's a concise implementation highlighting the essential logic:

```python
import heapq

class PriorityQueue:
    def __init__(self):
        self.heap = []
    
    def push(self, item, priority):
        """Add item with priority."""
        heapq.heappush(self.heap, (priority, item))
    
    def pop(self):
        """Remove and return highest priority item."""
        if self.heap:
            priority, item = heapq.heappop(self.heap)
            return item
        return None
    
    def peek(self):
        """Return highest priority item without removing."""
        if self.heap:
            return self.heap[0][1]  # Item is second element of tuple
        return None
    
    def is_empty(self):
        """Check if queue is empty."""
        return len(self.heap) == 0
```

**Key Points:**
- Typically implemented using binary heap
- Elements stored as (priority, item) tuples
- Lower priority number = higher priority (for min-heap)
- Push: O(log n) - insert into heap
- Pop: O(log n) - extract min from heap
- Peek: O(1) - access root without removal

## Common Application Errors

1. **Incorrect Priority Ordering:**
   - **Error:** Confusing whether lower or higher numbers mean higher priority
   - **Impact:** Elements processed in wrong order, algorithm produces incorrect results
   - **Solution:** Define convention clearly: min-heap (lower number = higher priority) or max-heap (higher number = higher priority), and use consistently

2. **Not Using Heap for Implementation:**
   - **Error:** Implementing with sorted list/array instead of heap
   - **Impact:** O(n) insert instead of O(log n), poor performance for frequent operations
   - **Solution:** Use binary heap (or library heap implementation like Python's heapq) for O(log n) operations

3. **Tuple Ordering Issues:**
   - **Error:** Storing (item, priority) instead of (priority, item), causing incorrect ordering
   - **Impact:** Elements sorted by item value instead of priority
   - **Solution:** Always store (priority, item) so heap compares by priority first

4. **Not Handling Empty Queue:**
   - **Error:** Calling pop() or peek() without checking if queue is empty
   - **Impact:** Errors or incorrect behavior when queue is empty
   - **Solution:** Always check `is_empty()` or handle None return from pop()

5. **Priority Updates:**
   - **Error:** Needing to update priority of existing element (not directly supported by standard heap)
   - **Impact:** Cannot efficiently change priority of element already in queue
   - **Solution:** Use more advanced structures (Fibonacci heap) or mark old entry as invalid and insert new one

## Recommended Literature

1. **"Introduction to Algorithms" (CLRS)** - Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein
   - Comprehensive analysis of priority queues including heap implementation and applications in graph algorithms

2. **"Algorithm Design Manual"** - Steven S. Skiena
   - Practical discussion of priority queues, including when their ordering makes them preferable to regular queues

3. **"Algorithms"** - Robert Sedgewick, Kevin Wayne
   - Excellent coverage of priority queues with applications in Dijkstra's and Prim's algorithms

4. **"Data Structures and Algorithms in Python"** - Michael T. Goodrich, Roberto Tamassia, Michael H. Goldwasser
   - Clear explanation of priority queues with Python-specific implementations using heapq

5. **"Algorithm Design"** - Jon Kleinberg, Éva Tardos
   - Detailed discussion of priority queues in the context of greedy algorithms and graph algorithms
