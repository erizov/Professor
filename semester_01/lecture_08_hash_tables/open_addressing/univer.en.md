# Open Addressing (Hash Table Collision Resolution)

## Convergence Speed and Complexity Estimate

**Time Complexity:**
- **Average Case:** O(1) - constant time for insert, search, and delete operations when hash function and probing sequence provide uniform distribution and load factor is reasonable (typically < 0.5 for linear probing, < 0.7 for quadratic/double hashing). Each operation requires computing hash and potentially probing through table.
- **Best Case:** O(1) - when no collisions occur, operations are direct array access at computed index.
- **Worst Case:** O(n) - when table is nearly full or clustering occurs, probing sequence may need to check all n table slots before finding empty slot or target key.

**Space Complexity:** O(m) where m is table size. Unlike chaining, all entries are stored directly in the table array. No additional space for chains/lists. However, table size m is typically larger than number of elements n to maintain low load factor.

**Load Factor Impact:** With load factor α = n/m (number of elements / table size):
- **Linear Probing:** Optimal α < 0.5 - beyond this, clustering causes performance degradation
- **Quadratic Probing:** Optimal α < 0.7 - better distribution than linear probing
- **Double Hashing:** Optimal α < 0.7 - best distribution among probing methods
- **Solution:** Rehash when load factor exceeds threshold (typically 0.5-0.7 depending on method)

**Probing Methods:**
- **Linear Probing:** h(k, i) = (h₁(k) + i) mod m - simple but prone to clustering
- **Quadratic Probing:** h(k, i) = (h₁(k) + c₁i + c₂i²) mod m - reduces clustering
- **Double Hashing:** h(k, i) = (h₁(k) + i·h₂(k)) mod m - best distribution, requires second hash function

**Convergence:** Open addressing doesn't have convergence like iterative algorithms. Operations complete when empty slot is found (insert) or key is found/not found (search/delete). However, performance converges to optimal O(1) when hash function and probing provide uniform distribution and load factor is maintained below threshold.

## Where the Algorithm is Used in Real Frameworks and Software

Open addressing is widely used in hash table implementations, especially when memory efficiency is important:

- **Programming Language Standard Libraries:**
  - **Python dictionaries (CPython)** - uses open addressing with pseudo-random probing
  - **Rust HashMap** - uses open addressing (Robin Hood hashing variant)
  - **Go maps** - uses open addressing with bucket-based approach
  - **Swift dictionaries** - uses open addressing

- **High-Performance Systems:**
  - **Game engines** - entity component systems, fast lookups
  - **Real-time systems** - predictable memory layout, cache-friendly
  - **Embedded systems** - memory-constrained environments
  - **Database systems** - hash indexes, join hash tables

- **Caching Systems:**
  - **CPU caches** - hardware-implemented, similar principles
  - **Web server caches** - memory-efficient key-value storage
  - **Application-level caches** - session storage, memoization

- **Compiler Design:**
  - **Symbol tables** - fast identifier lookup
  - **String interning** - managing string literals
  - **Constant folding** - storing computed constants

- **Real-World Applications:**
  - **Web frameworks** - routing tables, parameter storage
  - **Network protocols** - connection tracking, flow tables
  - **File systems** - directory caches, inode tables
  - **Scientific computing** - sparse matrix storage

## What It's Similar To in Concept

Open addressing shares conceptual similarities with:

- **Array-Based Storage:** Unlike chaining which uses external data structures, open addressing stores all entries directly in the table array. More memory-efficient but requires careful probing strategy.

- **Linear/Quadratic Search:** Probing sequences (especially linear probing) resemble sequential search through array, but starting from computed hash position rather than beginning of array.

- **Cuckoo Hashing:** Both store entries directly in table, but cuckoo hashing uses multiple hash functions and eviction strategy, while open addressing uses probing sequence.

- **Cache Memory:** CPU caches use similar principle - compute index, check if data present, if collision check nearby locations (cache lines). Open addressing mimics this behavior.

- **Database Hashing:** Similar to how databases use hash partitioning - compute partition, if full find alternative location. Open addressing does this at fine-grained level.

## Which Algorithms It's Often Used With

Open addressing is frequently combined with:

- **Hash Functions:**
  - **Primary hash function** - computes initial index
  - **Secondary hash function** - for double hashing probing
  - **Universal hashing** - for security and uniform distribution
  - **Cryptographic hashes** - for security-sensitive applications

- **Probing Strategies:**
  - **Linear Probing** - simplest, h(k,i) = (h(k) + i) mod m
  - **Quadratic Probing** - h(k,i) = (h(k) + c₁i + c₂i²) mod m
  - **Double Hashing** - h(k,i) = (h₁(k) + i·h₂(k)) mod m
  - **Robin Hood Hashing** - variant that reduces variance in probe lengths

- **Hash Table Operations:**
  - **Rehashing** - resizing table when load factor too high
  - **Dynamic resizing** - growing/shrinking table
  - **Tombstone handling** - marking deleted entries for proper probing

- **Alternative Collision Resolution:**
  - **Chaining** - alternative method (external chains vs. internal probing)
  - **Cuckoo Hashing** - alternative with better worst-case guarantees
  - **Perfect Hashing** - for static sets with no collisions

## Key Code (Only Important Parts)

Here's a concise implementation highlighting the essential logic:

```python
class HashTableOpenAddressing:
    """Hash table with open addressing (linear probing)."""
    
    def __init__(self, size: int = 10):
        self.size = size
        self.table: List[Optional[tuple]] = [None] * size
        self.deleted = object()  # Marker for deleted entries
    
    def _hash(self, key: int) -> int:
        """Primary hash function."""
        return key % self.size
    
    def _probe(self, key: int, start_index: int) -> int:
        """Linear probing - find slot for key."""
        index = start_index
        while self.table[index] is not None and self.table[index] is not self.deleted:
            # If key found, return its index
            if self.table[index] is not self.deleted and self.table[index][0] == key:
                return index
            # Probe next slot (linear probing)
            index = (index + 1) % self.size
            if index == start_index:
                raise Exception("Hash table is full")
        return index  # Found empty or deleted slot
    
    def insert(self, key: int, value: any) -> None:
        """Insert key-value pair."""
        index = self._hash(key)
        index = self._probe(key, index)
        self.table[index] = (key, value)
    
    def get(self, key: int) -> Optional[any]:
        """Get value by key."""
        index = self._hash(key)
        start = index
        
        while self.table[index] is not None:
            if self.table[index] is not self.deleted and self.table[index][0] == key:
                return self.table[index][1]
            index = (index + 1) % self.size
            if index == start:  # Wrapped around, key not found
                break
        return None
    
    def delete(self, key: int) -> bool:
        """Delete key-value pair using tombstone."""
        index = self._hash(key)
        start = index
        
        while self.table[index] is not None:
            if self.table[index] is not self.deleted and self.table[index][0] == key:
                self.table[index] = self.deleted  # Mark as deleted
                return True
            index = (index + 1) % self.size
            if index == start:
                break
        return False
```

**Key Points:**
- All entries stored directly in table array
- Probing sequence finds alternative slots on collision
- Tombstone marker (deleted) needed for proper probing
- Operations: O(1) average, O(n) worst case (clustering)
- More memory-efficient than chaining but requires careful load factor management

## Common Application Errors

1. **Not Using Tombstones for Deleted Entries:**
   - **Error:** Setting deleted slots to None instead of using tombstone marker
   - **Impact:** Breaks probing sequence - search stops at first None, missing keys that were probed past deleted entry
   - **Solution:** Use special marker (tombstone) for deleted entries, only treat as empty during insertion

2. **Allowing Load Factor Too High:**
   - **Error:** Not rehashing when load factor exceeds threshold
   - **Impact:** Clustering occurs, performance degrades to O(n)
   - **Solution:** Monitor load factor and rehash when it exceeds threshold (0.5 for linear, 0.7 for quadratic/double hashing)

3. **Infinite Loop in Probing:**
   - **Error:** Not checking if probe sequence wrapped around to start
   - **Impact:** Infinite loop when table is full
   - **Solution:** Check if `index == start_index` in probe loop, raise exception if table full

4. **Poor Probing Sequence:**
   - **Error:** Using linear probing without considering clustering
   - **Impact:** Primary clustering causes performance degradation
   - **Solution:** Use quadratic probing or double hashing for better distribution

5. **Not Handling Wraparound:**
   - **Error:** Not using modulo arithmetic for probe sequence
   - **Impact:** Index out of bounds errors
   - **Solution:** Always use `(index + step) % table_size` for probing

6. **Incorrect Search Logic:**
   - **Error:** Stopping search at first None instead of continuing through tombstones
   - **Impact:** May not find keys that were inserted after deletion
   - **Solution:** Continue probing through tombstones, only stop at None or when wrapped around

## Recommended Literature

1. **"Introduction to Algorithms" (CLRS)** - Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein
   - Comprehensive coverage of open addressing with analysis of different probing methods and expected performance

2. **"Algorithm Design Manual"** - Steven S. Skiena
   - Practical discussion of hash tables with implementation details and comparison of chaining vs. open addressing

3. **"Data Structures and Algorithms in Python"** - Michael T. Goodrich, Roberto Tamassia, Michael H. Goldwasser
   - Clear explanation of open addressing with Python-specific implementations and load factor considerations

4. **"The Art of Computer Programming, Volume 3"** - Donald E. Knuth
   - Deep mathematical analysis of hashing, including analysis of probe sequence lengths and clustering

5. **"Hash Tables"** - Wikipedia and various online resources
   - Good overview of different probing strategies (linear, quadratic, double hashing) and their trade-offs
