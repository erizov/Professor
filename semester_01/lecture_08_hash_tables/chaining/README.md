# Hash Table with Chaining

1. **Name of Algorithm**  
   Hash Table with Chaining

2. **What problem does it solve? (1 sentence)**  
   Stores key-value pairs with O(1) average-case lookup by using hash function and collision resolution via linked lists.

3. **Intuition (plain-language explanation)**  
   Like a library with numbered shelves: hash function tells you which shelf, chaining handles when multiple books share a shelf.

4. **Inputs & Outputs**  
   - Input: Key-value pairs and operations: insert, get, delete.  
   - Output: Fast O(1) average-case retrieval of values by key.

5. **Step-by-step description (5–10 lines max)**  
1. Choose hash function h(k) that maps keys to bucket indices.
2. Insert: compute h(key), add (key,value) to linked list at that bucket.
3. Get: compute h(key), search linked list at bucket for matching key.
4. Delete: compute h(key), remove node from linked list at bucket.
5. Handle collisions: multiple keys hashing to same bucket share the list.

6. **Tiny example (hand-simulated)**  
   Hash table size 5, keys 7,12,17. h(7)=2, h(12)=2 (collision), h(17)=2 (collision). Bucket 2: [7→12→17].

7. **Time & Space Complexity**  
   - Time: O(1) average case, O(n) worst case if all keys hash to same bucket.  
   - Space: O(n) for n key-value pairs plus overhead for buckets.

8. **Strengths**  
- Very fast average-case performance.
- Simple collision resolution, easy to implement.

9. **Weaknesses / limitations**  
- Worst-case O(n) if hash function is poor or keys are adversarial.
- Requires good hash function and load factor management.

10. **Compare with alternatives**  
    Alternatives: Open Addressing, Cuckoo Hashing, Robin Hood Hashing

11. **30-second explanation (your own words)**  
    A fast lookup structure that uses a hash function to map keys to buckets, with linked lists handling collisions.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
