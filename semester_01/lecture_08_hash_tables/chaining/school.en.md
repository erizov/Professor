# Chaining (Hash Table Collision Resolution)

## Principle of Operation

Chaining is a way to handle collisions in hash tables. When two different keys hash to the same position (collision), instead of overwriting, we store both in a list (chain) at that position.

**How it works:**
1. Each position in the hash table contains a list (chain)
2. When you want to store a key-value pair, compute the hash to find the position
3. If that position is empty, create a new list and add the pair
4. If that position already has items (collision), add the new pair to the existing list
5. To find a key, hash it, then search through the list at that position

**Simple analogy:** Imagine a library with numbered shelves. Each shelf can hold multiple books. When you want to store a book, you calculate its shelf number. If the shelf is empty, you put the book there. If the shelf already has books (collision), you just add your book to that shelf. To find a book, you calculate its shelf number and look through all books on that shelf.

**Key idea:** Chaining solves collisions by allowing multiple items at the same position, stored in a list. It's simple and works well when collisions are rare.

## Algorithm Complexity

**Time Complexity:** O(1) average, O(n) worst case
- **Average case:** O(1) - when hash function distributes keys evenly and there aren't too many collisions
- **Best case:** O(1) - when no collisions occur, direct access
- **Worst case:** O(n) - when all keys hash to the same position, creating one long list

**Space Complexity:** O(n + m)
- n = number of items stored
- m = size of hash table
- Each item needs space, plus the table itself

**Load Factor:** The ratio of items to table size (n/m). When load factor is low (< 0.75), operations are fast. When it's high (> 1.0), chains get long and operations slow down.

## Where It's Used in Practice

**Programming Languages:**
- **Java HashMap** - uses chaining to handle collisions
- **Python dictionaries** - some implementations use chaining
- **C++ unordered_map** - often uses chaining

**Databases:**
- **Hash indexes** - for fast lookups in databases
- **Join operations** - hash joins use chaining

**Everyday Applications:**
- **Spell checkers** - storing dictionary words
- **Caching** - storing frequently used data
- **Symbol tables** - in compilers, storing variable names

## What It Can Be Compared To

**Like a Library:** Each shelf (hash position) can hold multiple books (items). When a shelf is full, you just add more books to that shelf.

**Like Separate Rooms:** Unlike open addressing where you look for another room in the same building, chaining keeps all items that hash to the same position together in a list.

**Like Linked Lists:** Each hash position is essentially a linked list. When collisions happen, items are added to the list.

**Opposite of Open Addressing:**
- Chaining stores items in external lists
- Open addressing stores items elsewhere in the same table
- Chaining is simpler but uses more memory

## Minimal Code Example

Here's a simple chaining implementation:

```python
class HashTableChaining:
    """Hash table with chaining."""
    
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]  # List of lists
    
    def _hash(self, key):
        """Hash function - find position."""
        return key % self.size
    
    def insert(self, key, value):
        """Store key-value pair."""
        index = self._hash(key)
        bucket = self.table[index]
        
        # Check if key already exists
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)  # Update existing
                return
        
        # Add new item to chain
        bucket.append((key, value))
    
    def get(self, key):
        """Get value by key."""
        index = self._hash(key)
        bucket = self.table[index]
        
        # Search through chain
        for k, v in bucket:
            if k == key:
                return v
        
        return None  # Not found
```

**Key parts:**
- Table is list of lists (chains)
- Hash function finds position
- Collisions handled by adding to list
- Search through chain to find item

## Common Mistakes

1. **Not Handling Load Factor:**
   - **Wrong:** Allowing too many items without resizing table
   - **Why it's wrong:** Chains get very long, operations become slow
   - **Fix:** Resize table when load factor gets too high (usually > 0.75)

2. **Poor Hash Function:**
   - **Wrong:** Using hash function that creates many collisions
   - **Why it's wrong:** All items go to same position, creating one long chain
   - **Fix:** Use good hash function that distributes keys evenly

3. **Not Updating Existing Keys:**
   - **Wrong:** Adding duplicate keys instead of updating values
   - **Why it's wrong:** Multiple entries with same key, confusing results
   - **Fix:** Always check if key exists before adding, update if found

4. **Inefficient Search:**
   - **Wrong:** Not optimizing search through long chains
   - **Why it's wrong:** O(n) search when chain is long
   - **Fix:** Keep load factor low, or use balanced trees for long chains

5. **Memory Leaks:**
   - **Wrong:** Not removing deleted items properly
   - **Why it's wrong:** Memory not freed, wasting space
   - **Fix:** Properly remove items from chains when deleted

## Recommended Literature

1. **"Grokking Algorithms"** by Aditya Bhargava
   - Simple explanations of hash tables and collision resolution
   - Great for beginners

2. **"Introduction to Algorithms" (CLRS)**
   - Comprehensive coverage of hash tables
   - Explains why chaining works and when to use it

3. **"Data Structures and Algorithms in Python"** by Goodrich, Tamassia, Goldwasser
   - Clear Python implementations
   - Good examples of hash tables

4. **Online Resources:**
   - GeeksforGeeks - hash table tutorials
   - Khan Academy - data structures course
   - Visualgo.net - interactive hash table visualization
