# Fibonacci Heap

1. **Name of Algorithm**  
   Fibonacci Heap

2. **What problem does it solve? (1 sentence)**  
   Provides extremely fast decrease-key and merge operations for advanced graph algorithms like Dijkstra's.

3. **Intuition (plain-language explanation)**  
   A lazy heap: it defers organizing work until absolutely necessary, making most operations very fast on average.

4. **Inputs & Outputs**  
   - Input: Sequence of insert, extract-min, decrease-key, and merge operations.  
   - Output: Amortized O(1) insert and decrease-key, O(log n) extract-min.

5. **Step-by-step description (5–10 lines max)**  
1. Maintain a collection of heap-ordered trees (forest).
2. Insert: add new single-node tree to forest, O(1).
3. Extract-min: remove min root, merge its children into forest, consolidate trees of same degree, O(log n).
4. Decrease-key: update node, cut from parent if violates heap property, mark parent, O(1) amortized.
5. Merge: combine two forests, O(1).

6. **Tiny example (hand-simulated)**  
   Forest with trees of degrees 0,1,2. Insert creates degree-0 tree. Extract-min consolidates: merge same-degree trees.

7. **Time & Space Complexity**  
   - Time: O(1) amortized insert/decrease-key/merge, O(log n) amortized extract-min.  
   - Space: O(n) with additional pointers for decrease-key operations.

8. **Strengths**  
- Fastest known heap for decrease-key operations.
- Enables O(m + n log n) Dijkstra's algorithm.

9. **Weaknesses / limitations**  
- Complex implementation with many pointer manipulations.
- Large constant factors make it slower than binary heap for small inputs.

10. **Compare with alternatives**  
    Alternatives: Binary Heap, Binomial Heap, Pairing Heap

11. **30-second explanation (your own words)**  
    A sophisticated heap that delays consolidation work, achieving O(1) decrease-key for graph algorithms.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
