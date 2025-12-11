# Open Addressing (Hash Table Collision Resolution)

## Principle of Operation

Open addressing is a way to handle collisions in hash tables. When two keys hash to the same position, instead of storing both there, we find another empty position in the same table to store the second item.

**How it works:**
1. Each position in the hash table can hold one item
2. When you want to store a key-value pair, compute the hash to find the position
3. If that position is empty, store the item there
4. If that position is already taken (collision), use a "probing" method to find the next empty position
5. Common probing methods: linear (check next position), quadratic (check positions with pattern), double hashing (use second hash function)

**Simple analogy:** Imagine a parking lot where each car has an assigned spot number. When you arrive, you calculate your spot number. If it's empty, you park there. If someone else is already there (collision), you look for the next empty spot nearby. You keep checking nearby spots until you find an empty one.

**Key idea:** Open addressing solves collisions by finding another spot in the same table. It's memory-efficient because everything stays in one table, but requires careful probing to avoid clustering (many items close together).

## Algorithm Complexity

**Time Complexity:** O(1) average, O(n) worst case
- **Average case:** O(1) - when hash function and probing work well together
- **Best case:** O(1) - when no collisions occur, direct access
- **Worst case:** O(n) - when table is nearly full or clustering occurs, need to check many positions

**Space Complexity:** O(m)
- m = size of hash table
- All items stored directly in table, no extra lists needed
- More memory-efficient than chaining

**Load Factor:** The ratio of items to table size. For open addressing, keep load factor lower (< 0.5 for linear probing, < 0.7 for quadratic/double hashing) to avoid too many collisions and slow operations.

## Where It's Used in Practice

**Programming Languages:**
- **Python dictionaries (CPython)** - uses open addressing
- **Rust HashMap** - uses open addressing
- **Go maps** - uses open addressing

**High-Performance Systems:**
- **Game engines** - fast lookups for game data
- **Real-time systems** - predictable performance
- **Caching systems** - memory-efficient storage

**Everyday Applications:**
- **Web servers** - storing session data
- **Databases** - hash indexes
- **Compilers** - symbol tables

## What It Can Be Compared To

**Like a Parking Lot:** When your assigned spot is taken, you look for the next empty spot. You keep checking nearby spots until you find one.

**Like Finding a Seat:** In a theater, if your seat is taken, you look for another empty seat nearby. Open addressing does the same - finds another position when collision occurs.

**Opposite of Chaining:**
- Open addressing stores items in the same table
- Chaining stores items in external lists
- Open addressing is more memory-efficient but can have clustering

**Like Linear Search:** When probing, you check positions one by one (linear probing) or in a pattern (quadratic probing), similar to searching through an array.

## Minimal Code Example

Here's a simple open addressing implementation with linear probing:

```python
class HashTableOpenAddressing:
    """Hash table with open addressing (linear probing)."""
    
    def __init__(self, size=10):
        self.size = size
        self.table = [None] * size  # Array of items
        self.deleted = object()  # Marker for deleted items
    
    def _hash(self, key):
        """Hash function - find starting position."""
        return key % self.size
    
    def _probe(self, key, start_index):
        """Find position for key using linear probing."""
        index = start_index
        while self.table[index] is not None and self.table[index] is not self.deleted:
            if self.table[index] is not self.deleted and self.table[index][0] == key:
                return index  # Key found
            index = (index + 1) % self.size  # Check next position
            if index == start_index:
                raise Exception("Table is full")
        return index  # Found empty or deleted spot
    
    def insert(self, key, value):
        """Store key-value pair."""
        index = self._hash(key)
        index = self._probe(key, index)
        self.table[index] = (key, value)
    
    def get(self, key):
        """Get value by key."""
        index = self._hash(key)
        start = index
        
        while self.table[index] is not None:
            if self.table[index] is not self.deleted and self.table[index][0] == key:
                return self.table[index][1]
            index = (index + 1) % self.size
            if index == start:  # Checked all positions
                break
        return None  # Not found
```

**Key parts:**
- Table is array of items (not lists)
- Hash function finds starting position
- Probing finds next empty position on collision
- Deleted items marked with special marker (tombstone)

## Common Mistakes

1. **Not Using Tombstones:**
   - **Wrong:** Setting deleted positions to None
   - **Why it's wrong:** Breaks probing - search stops at first None, missing items
   - **Fix:** Use special marker (tombstone) for deleted items

2. **Allowing Load Factor Too High:**
   - **Wrong:** Not resizing when table gets too full
   - **Why it's wrong:** Too many collisions, operations become slow
   - **Fix:** Resize table when load factor exceeds threshold (0.5-0.7)

3. **Infinite Loop:**
   - **Wrong:** Not checking if probe wrapped around to start
   - **Why it's wrong:** Infinite loop when table is full
   - **Fix:** Check if `index == start_index` in probe loop

4. **Poor Probing Method:**
   - **Wrong:** Using linear probing without considering clustering
   - **Why it's wrong:** Items cluster together, causing more collisions
   - **Fix:** Use quadratic probing or double hashing for better distribution

5. **Wrong Search Logic:**
   - **Wrong:** Stopping search at first None
   - **Why it's wrong:** May miss items that were inserted after deletion
   - **Fix:** Continue probing through tombstones, only stop at None or when wrapped around

## Recommended Literature

1. **"Grokking Algorithms"** by Aditya Bhargava
   - Simple explanations of hash tables and open addressing
   - Great for beginners

2. **"Introduction to Algorithms" (CLRS)**
   - Comprehensive coverage of hash tables
   - Explains different probing methods

3. **"Data Structures and Algorithms in Python"** by Goodrich, Tamassia, Goldwasser
   - Clear Python implementations
   - Good examples of open addressing

4. **Online Resources:**
   - GeeksforGeeks - hash table tutorials
   - Khan Academy - data structures course
   - Visualgo.net - interactive hash table visualization
