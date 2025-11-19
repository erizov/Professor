# Memory Management

1. **Name of Algorithm**  
   Memory Management

2. **What problem does it solve? (1 sentence)**  
Manages computer memory allocation and deallocation for processes, tracking which memory is in use, allocating memory to processes, and reclaiming memory when processes terminate, preventing memory leaks and ensuring efficient memory utilization.

3. **Intuition (plain-language explanation)**  
   Like a hotel manager assigning rooms: the OS manages computer memory like a hotel - when a process needs memory (guest needs room), allocate it (assign room), track what's allocated (room registry), and when process ends (guest checks out), free the memory (clean room for next guest).

4. **Inputs & Outputs**  
   - Input: Memory requests from processes, system memory state, allocation policies, memory size and layout.  
   - Output: Allocated memory addresses for processes, memory mapping tables, freed memory available for reuse.

5. **Step-by-step description (5–10 lines max)**  
1. Track memory state: maintain data structures (free list, bitmap) to track which memory blocks are free or allocated.
2. Allocate memory: when process requests memory, find free block using allocation algorithm (first-fit, best-fit, worst-fit).
3. Mark as allocated: update memory state to mark allocated blocks as in use, associate with requesting process.
4. Return address: provide process with memory address (pointer) to allocated block.
5. Track allocations: maintain mapping of process to allocated memory blocks for cleanup.
6. Deallocate memory: when process terminates or frees memory, mark blocks as free and add to free list.
7. Coalesce free blocks: merge adjacent free blocks to reduce fragmentation.
8. Handle fragmentation: manage external fragmentation (free blocks scattered) and internal fragmentation (wasted space in allocated blocks).

6. **Tiny example (hand-simulated)**  
   Process requests 1KB memory → memory manager finds free 2KB block → allocates 1KB from block → returns address 0x1000 → process uses memory → process terminates → memory manager marks 0x1000-0x1400 as free → coalesces with adjacent free block → now 3KB free block available.

7. **Time & Space Complexity**  
   - Time: O(F) for allocation where F is number of free blocks (depends on algorithm: O(1) for buddy system, O(F) for first-fit), O(1) for deallocation.  
   - Space: O(M) for tracking M memory blocks (metadata overhead, typically 1-5% of total memory).

8. **Strengths**  
- Prevents conflicts: ensures processes don't access each other's memory.
- Efficient utilization: maximizes memory usage through allocation algorithms.
- Automatic: handles memory management transparently to applications.

9. **Weaknesses / limitations**  
- Fragmentation: can lead to wasted memory due to fragmentation.
- Overhead: metadata tracking consumes some memory.
- Complexity: requires careful design to handle edge cases.

10. **Compare with alternatives**  
    Alternatives: Manual Memory Management, Garbage Collection, Reference Counting, Memory Pools

11. **30-second explanation (your own words)**  
Manages computer memory allocation and deallocation for processes, tracking memory state, allocating memory on demand, and reclaiming memory when processes terminate, ensuring efficient memory utilization and preventing conflicts.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
