# Hash Table

## Convergence Speed and Complexity Estimate

**Time Complexity:**
- **Best Case:** O(1) - when there are no collisions, hash table operations (insert, search, delete) take constant time.
- **Average Case:** O(1) - with a good hash function and load factor management, operations average constant time.
- **Worst Case:** O(n) - when all keys hash to the same bucket (poor hash function or adversarial input), operations degrade to linear time as they must search through a linked list.

**Space Complexity:** O(n) - requires space for n key-value pairs. Additional space is needed for the underlying array (typically 1.5-2× the number of elements to maintain good load factor).

**Convergence:** Hash table operations converge immediately after computing the hash function and accessing the appropriate bucket. With proper collision resolution (chaining or open addressing), convergence is typically O(1) average case.

## Where the Algorithm is Used in Real Frameworks and Software

Hash Tables are among the most fundamental and widely used data structures:

- **Programming Languages and Standard Libraries:**
  - **Python's `dict`** - implemented using hash tables
  - **Java's `HashMap` and `Hashtable`** - hash table implementations
  - **C++ STL `unordered_map` and `unordered_set`** - hash table-based containers
  - **JavaScript objects** - many implementations use hash tables
  - **Ruby's Hash** - hash table implementation

- **Database Systems:**
  - **Database indexes** - hash indexes for exact key lookups
  - **Join operations** - hash joins for efficient table joins
  - **Caching systems** - Redis, Memcached use hash tables
  - **Key-value stores** - many NoSQL databases (DynamoDB, Cassandra) use hash concepts

- **System Software:**
  - **Symbol tables** in compilers and interpreters
  - **File system caches** - in-memory caches for file metadata
  - **Network routing tables** - for fast IP address lookups
  - **Browser caches** - storing web page data

- **Real-World Applications:**
  - **Web applications** - session storage, user data
  - **Game development** - fast lookups for game objects
  - **Search engines** - inverted indexes use hash concepts
  - **Cryptography** - hash functions for data integrity

## What It's Similar To in Concept

Hash Tables share conceptual similarities with:

- **Arrays:** Both provide O(1) access, but arrays use integer indices while hash tables use arbitrary keys mapped to indices via hash function.

- **Binary Search Trees:** Both store key-value pairs, but hash tables provide average O(1) operations while BSTs provide O(log n) with ordering guarantees.

- **Direct-Address Tables:** Hash tables are a generalization where keys are mapped to indices via hash function, rather than using keys directly as indices.

- **Associative Arrays:** Hash tables are the most common implementation of associative arrays (maps, dictionaries) in programming languages.

## Which Algorithms It's Often Used With

Hash Tables are frequently combined with:

- **Collision Resolution Techniques:**
  - **Chaining** - linked lists or trees in each bucket
  - **Open Addressing** - linear probing, quadratic probing, double hashing
  - **Cuckoo Hashing** - using multiple hash functions

- **Other Data Structures:**
  - **Sets** - hash sets are implemented using hash tables
  - **Bloom Filters** - use multiple hash functions
  - **Hash-based data structures** - hash maps, hash sets, concurrent hash maps

- **Algorithms:**
  - **Two-sum problem** - using hash table for O(n) solution
  - **Frequency counting** - counting occurrences efficiently
  - **Duplicate detection** - finding duplicates in O(n) time

## Key Code (Only Important Parts)

Here's a concise implementation highlighting the essential logic:

```python
class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]  # Chaining
    
    def _hash(self, key):
        """Hash function: maps key to bucket index."""
        return hash(key) % self.size
    
    def insert(self, key, value):
        """Insert key-value pair."""
        index = self._hash(key)
        # Check if key already exists
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)  # Update
                return
        # Add new key-value pair
        self.table[index].append((key, value))
    
    def get(self, key):
        """Get value by key."""
        index = self._hash(key)
        for k, v in self.table[index]:
            if k == key:
                return v
        return None  # Key not found
    
    def delete(self, key):
        """Delete key-value pair."""
        index = self._hash(key)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                del self.table[index][i]
                return True
        return False  # Key not found
```

**Key Points:**
- Hash function maps keys to bucket indices
- Collision resolution: chaining (linked lists) or open addressing
- Load factor = n/m (n elements, m buckets) - keep < 0.75 for good performance
- Rehashing: resize table when load factor gets too high
- Average O(1) operations, worst case O(n) with poor hash function

## Common Application Errors

1. **Poor Hash Function:**
   - **Error:** Using hash function that doesn't distribute keys uniformly (e.g., `key % prime` where prime is too small)
   - **Impact:** Many collisions, worst-case O(n) performance instead of O(1)
   - **Solution:** Use well-designed hash functions, consider cryptographic hash functions for better distribution

2. **Not Handling Collisions:**
   - **Error:** Assuming hash function produces unique indices for all keys
   - **Impact:** Data loss when multiple keys hash to same index
   - **Solution:** Always implement collision resolution (chaining or open addressing)

3. **Load Factor Too High:**
   - **Error:** Not resizing table when load factor exceeds threshold (typically 0.75)
   - **Impact:** Performance degrades as collisions increase
   - **Solution:** Monitor load factor and resize (typically double size) when threshold exceeded

4. **Mutable Keys:**
   - **Error:** Using mutable objects (like lists) as keys, then modifying them after insertion
   - **Impact:** Hash value changes, key becomes unfindable
   - **Solution:** Only use immutable types (strings, numbers, tuples of immutables) as keys

5. **Not Handling None/Null Keys:**
   - **Error:** Hash function doesn't handle None/null keys properly
   - **Impact:** Errors when trying to hash None values
   - **Solution:** Handle None/null as special case in hash function

## Recommended Literature

1. **"Introduction to Algorithms" (CLRS)** - Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein
   - Comprehensive analysis of hash tables including hash functions, collision resolution, and universal hashing

2. **"Algorithm Design Manual"** - Steven S. Skiena
   - Practical discussion of hash tables, including when their O(1) average performance makes them preferable

3. **"Algorithms"** - Robert Sedgewick, Kevin Wayne
   - Excellent coverage of hash tables with analysis of different collision resolution strategies

4. **"Data Structures and Algorithms in Python"** - Michael T. Goodrich, Roberto Tamassia, Michael H. Goldwasser
   - Clear explanation of hash tables with Python-specific implementations and collision resolution examples

5. **"The Art of Computer Programming, Volume 3: Sorting and Searching"** - Donald Knuth
   - Authoritative reference on hash tables including analysis of hash functions and collision resolution methods
