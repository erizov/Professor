# Hash Table

1. **Name of Algorithm**  
   Hash Table

2. **What problem does it solve? (1 sentence)**  
   Provides constant-time average access to key-value pairs using hashing and collision resolution.

3. **Intuition (plain-language explanation)**  
   Like placing labeled folders into numbered drawers: the hash function turns a key into a drawer index so you jump straight there.

4. **Inputs & Outputs**  
   - Input: Key-value pairs with operations insert, lookup, delete.  
   - Output: Table of buckets where each bucket stores entries that hash to the same index.

5. **Step-by-step description (5–10 lines max)**  
1. Select hash function h(key) that maps keys to indices 0..m-1.
2. Insert: compute index, place entry in bucket (or follow collision policy).
3. Lookup: hash key, scan bucket/probe sequence for matching key.
4. Delete: hash key, remove entry while preserving collision structure.
5. Resize when load factor grows to keep operations near O(1).

6. **Tiny example (hand-simulated)**  
   Table size 7, keys 'cat','dog','eel'. Hash to indices 2,5,2 respectively; bucket 2 stores ['cat','eel'].

7. **Time & Space Complexity**  
   - Time: Average O(1) for insert/lookup/delete; worst-case O(n) if collisions degenerate.  
   - Space: O(n) for entries plus bucket overhead.

8. **Strengths**  
- Extremely fast average-case performance.
- Simple API for associative arrays and caches.

9. **Weaknesses / limitations**  
- Needs high-quality hash functions and resizing strategy.
- No inherent ordering of keys.

10. **Compare with alternatives**  
    Alternatives: Binary Search Tree, Skip List, B-Tree

11. **30-second explanation (your own words)**  
    Maps keys to array indices via a hash function so most operations touch a single bucket, yielding near-constant time.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
