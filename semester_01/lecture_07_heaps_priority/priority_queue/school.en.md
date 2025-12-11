# Priority Queue

## Principle of Operation

A Priority Queue is like a special line where the most important person goes first, not the person who arrived first. It's like an emergency room where patients with the most serious injuries are seen first, regardless of when they arrived.

Think of it like a to-do list where urgent tasks are always at the top. You can add tasks with different priorities, and when you need to do something, you always take the most urgent one first.

### Simple Example

Imagine a to-do list with priorities (lower number = more urgent):

1. **Add tasks:** "Homework" (priority 3), "Eat lunch" (priority 1), "Call friend" (priority 2)
2. **Organize:** Most urgent first → "Eat lunch" (1), "Call friend" (2), "Homework" (3)
3. **Do next task:** Take "Eat lunch" (most urgent)
4. **Add new task:** "Study for test" (priority 1) - goes to top!
5. **Do next:** Take "Study for test" (now most urgent)

The key is that items are organized by priority, not by when they were added!

## Algorithm Complexity in O-notation

- **Best Case:** O(log n) - adding or removing items is always fast.
- **Average Case:** O(log n) - consistent performance no matter how many items you have.
- **Worst Case:** O(log n) - same as best case! Priority queues guarantee fast operations.

**Space Complexity:** O(n) - you need space to store all n items.

## Where It Is Used in Practice

Priority Queues are used in many real programs:

- **Real Applications:**
  - **Hospital emergency rooms** - patients seen by urgency, not arrival time
  - **Task schedulers** - computers decide which program to run next
  - **GPS navigation** - finding shortest routes
  - **Game AI** - characters find best paths

- **When It's Perfect:**
  - When you need to process items by importance, not order
  - When priorities can change
  - When you need to quickly find the most important item

- **Why It's Special:**
  - Always gives you the most important item first
  - Very fast for adding and removing (O(log n))
  - Used in many important algorithms

## What Can the Algorithm Be Compared To

Priority Queues can be compared to:

- **Emergency Room:** Like a hospital where the sickest patients are seen first, not those who arrived first.

- **VIP Line:** Like a special line where VIPs go first, regardless of when they arrived.

- **Smart To-Do List:** Like a to-do list that automatically organizes tasks by importance.

## Minimal Code Example (Only Important Parts)

Here's a simple Python implementation:

```python
import heapq

class PriorityQueue:
    def __init__(self):
        self.heap = []
    
    def add_task(self, task, priority):
        """Add task with priority (lower number = higher priority)."""
        heapq.heappush(self.heap, (priority, task))
    
    def get_next_task(self):
        """Get the most urgent task."""
        if self.heap:
            priority, task = heapq.heappop(self.heap)
            return task
        return None
    
    def peek(self):
        """See next task without removing it."""
        if self.heap:
            return self.heap[0][1]  # Task is second part of tuple
        return None
```

**Key Points:**
- Items stored as (priority, item) pairs
- Lower priority number = more urgent (usually)
- Add: O(log n) - insert into heap
- Remove: O(log n) - take from top
- Always gives most urgent item first!

## Common Mistakes

1. **Wrong Priority Order:**
   - **Mistake:** Confusing whether lower or higher numbers mean higher priority
   - **Why it's bad:** Items processed in wrong order
   - **Fix:** Decide: lower number = higher priority (or vice versa), and use consistently

2. **Wrong Tuple Order:**
   - **Mistake:** Storing (item, priority) instead of (priority, item)
   - **Why it's bad:** Items sorted by name instead of priority
   - **Fix:** Always store (priority, item) so it sorts by priority

3. **Not Using Heap:**
   - **Mistake:** Using a regular list and sorting it each time
   - **Why it's bad:** Very slow (O(n log n) instead of O(log n))
   - **Fix:** Use a heap (like Python's heapq) for fast operations

4. **Forgetting Empty Check:**
   - **Mistake:** Trying to get item from empty queue
   - **Why it's bad:** Causes errors
   - **Fix:** Always check if queue is empty before getting items

5. **Not Understanding Priority:**
   - **Mistake:** Thinking it's like a regular queue (first in, first out)
   - **Why it's bad:** Expects wrong behavior
   - **Fix:** Remember: priority queue = most important first, not first come first served

## Recommended Literature

1. **"Grokking Algorithms" by Aditya Bhargava**
   - Excellent beginner-friendly book that explains Priority Queues simply

2. **"Introduction to Algorithms" (CLRS)**
   - Comprehensive textbook covering Priority Queues

3. **"Algorithms Unlocked" by Thomas H. Cormen**
   - Accessible introduction that explains when Priority Queues are useful

4. **Online Resources:**
   - Khan Academy's computer science courses
   - Visualgo.net for interactive Priority Queue visualizations
   - GeeksforGeeks for code examples and explanations
