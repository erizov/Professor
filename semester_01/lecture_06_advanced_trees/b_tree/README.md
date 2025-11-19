# B-Tree

1. **Name of Algorithm**  
   B-Tree

2. **What problem does it solve? (1 sentence)**  
   Efficiently stores and retrieves large datasets on disk by minimizing disk I/O through wide, shallow trees.

3. **Intuition (plain-language explanation)**  
   Like a library filing system: instead of narrow tall shelves, use wide shallow ones so you can grab multiple books at once.

4. **Inputs & Outputs**  
   - Input: Large dataset of key-value pairs, typically stored on disk.  
   - Output: Multi-way search tree optimized for external storage access.

5. **Step-by-step description (5–10 lines max)**  
1. Each node contains multiple keys (typically 100-1000) and child pointers.
2. Search: traverse from root, compare with node keys, follow appropriate child.
3. Insert: find leaf, add key; if node overflows, split and promote middle key.
4. Delete: remove key; if node underflows, merge with sibling or borrow key.
5. Maintain property: all leaves at same depth, nodes between t-1 and 2t-1 keys.

6. **Tiny example (hand-simulated)**  
   B-tree of order 3: root [10,20] has children [5,7], [15,17], [25,27]. Insert 12: goes to middle child, no split needed.

7. **Time & Space Complexity**  
   - Time: O(log n) with base of node capacity (typically 100-1000), making it effectively O(log n / log t).  
   - Space: O(n) total storage, but nodes are large (disk pages).

8. **Strengths**  
- Minimizes disk I/O by reading large nodes (pages) at once.
- Widely used in databases and file systems for indexing.

9. **Weaknesses / limitations**  
- More complex than binary trees for in-memory operations.
- Requires careful tuning of node size for optimal performance.

10. **Compare with alternatives**  
    Alternatives: B+ Tree, LSM Tree, Hash Index

11. **30-second explanation (your own words)**  
    A multi-way tree that stores many keys per node to reduce disk reads, perfect for database indexing.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
