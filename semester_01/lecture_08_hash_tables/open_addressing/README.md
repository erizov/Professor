# Open Addressing

1. **Name of Algorithm**  
   Open Addressing

2. **What problem does it solve? (1 sentence)**  
   Resolves hash table collisions by probing alternative slots instead of storing overflow lists.

3. **Intuition (plain-language explanation)**  
   If a parking spot is taken, keep moving to the next slot according to a probe rule until you find an empty space.

4. **Inputs & Outputs**  
   - Input: Fixed-size table and probe sequence (linear, quadratic, double hashing).  
   - Output: Array where each slot holds at most one key-value pair plus optional tombstone markers.

5. **Step-by-step description (5–10 lines max)**  
1. Hash key to initial index i0 = h(key).
2. If slot empty, place entry; otherwise compute next probe index via strategy.
3. Repeat probing until an empty slot or tombstone is found.
4. Lookup follows the same probe sequence until key or empty slot encountered.
5. Deletion marks slot as tombstone to preserve probe chains.

6. **Tiny example (hand-simulated)**  
   Linear probing size 5: insert keys hashing to index 2. Occupied? Try 3, then 4, then wrap to 0.

7. **Time & Space Complexity**  
   - Time: Average O(1) with low load factor; degrades toward O(n) as table fills.  
   - Space: O(m) for table of m slots; no extra pointers.

8. **Strengths**  
- Excellent cache locality because all data lives in the array.
- No extra heap allocations compared to chaining.

9. **Weaknesses / limitations**  
- Primary clustering can create long probe sequences.
- Deletion logic complicated by tombstones and probe-chain maintenance.

10. **Compare with alternatives**  
    Alternatives: Separate Chaining, Cuckoo Hashing, Robin Hood Hashing

11. **30-second explanation (your own words)**  
    Keeps every key directly in the array, using probe sequences to find the next available slot whenever collisions occur.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
