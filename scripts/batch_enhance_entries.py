#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch enhance template entries with comprehensive algorithm information.

This script processes entries in batches and enhances them with detailed
information from standard CS knowledge and reputable sources.
"""

import json
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "scripts" / "data" / "learning_template_entries.json"

# Enhanced entries for well-known algorithms
ENHANCED_ENTRIES = {
    "semester_01/lecture_05_trees/avl_tree/README.md": {
        "name": "AVL Tree",
        "problem": "Maintains a self-balancing binary search tree where the heights of left and right subtrees differ by at most one.",
        "intuition": "Like a see-saw that automatically adjusts itself: whenever one side gets too heavy, it rotates to balance out.",
        "inputs": "Sequence of insert/delete/search operations on key-value pairs.",
        "outputs": "Balanced binary search tree with O(log n) height guarantees.",
        "steps": [
            "Insert or delete a node using standard BST rules.",
            "Check the balance factor (height difference) of each ancestor.",
            "If imbalance detected (|balance| > 1), perform rotations.",
            "Single rotation for outside cases (left-left or right-right).",
            "Double rotation for inside cases (left-right or right-left).",
            "Update heights and continue up the tree until balanced."
        ],
        "example": "Insert 3,2,1: After 3 and 2, insert 1 causes left-left imbalance. Rotate right around 3: [2(1,3)].",
        "time_complexity": "O(log n) for all operations (insert, delete, search).",
        "space_complexity": "O(n) to store n nodes.",
        "strengths": [
            "Guaranteed O(log n) height ensures predictable performance.",
            "Strict balancing prevents worst-case O(n) behavior."
        ],
        "weaknesses": [
            "More complex than basic BST due to rotation overhead.",
            "Requires storing balance factors or heights per node."
        ],
        "alternatives": ["Red-Black Tree", "Splay Tree", "B-Tree"],
        "explanation": "A self-adjusting BST that keeps itself balanced by rotating nodes when one subtree becomes too tall."
    },
    "semester_01/lecture_06_advanced_trees/b_tree/README.md": {
        "name": "B-Tree",
        "problem": "Efficiently stores and retrieves large datasets on disk by minimizing disk I/O through wide, shallow trees.",
        "intuition": "Like a library filing system: instead of narrow tall shelves, use wide shallow ones so you can grab multiple books at once.",
        "inputs": "Large dataset of key-value pairs, typically stored on disk.",
        "outputs": "Multi-way search tree optimized for external storage access.",
        "steps": [
            "Each node contains multiple keys (typically 100-1000) and child pointers.",
            "Search: traverse from root, compare with node keys, follow appropriate child.",
            "Insert: find leaf, add key; if node overflows, split and promote middle key.",
            "Delete: remove key; if node underflows, merge with sibling or borrow key.",
            "Maintain property: all leaves at same depth, nodes between t-1 and 2t-1 keys."
        ],
        "example": "B-tree of order 3: root [10,20] has children [5,7], [15,17], [25,27]. Insert 12: goes to middle child, no split needed.",
        "time_complexity": "O(log n) with base of node capacity (typically 100-1000), making it effectively O(log n / log t).",
        "space_complexity": "O(n) total storage, but nodes are large (disk pages).",
        "strengths": [
            "Minimizes disk I/O by reading large nodes (pages) at once.",
            "Widely used in databases and file systems for indexing."
        ],
        "weaknesses": [
            "More complex than binary trees for in-memory operations.",
            "Requires careful tuning of node size for optimal performance."
        ],
        "alternatives": ["B+ Tree", "LSM Tree", "Hash Index"],
        "explanation": "A multi-way tree that stores many keys per node to reduce disk reads, perfect for database indexing."
    },
    "semester_01/lecture_06_advanced_trees/red_black_tree/README.md": {
        "name": "Red-Black Tree",
        "problem": "Maintains a balanced binary search tree with relaxed balancing rules compared to AVL trees.",
        "intuition": "A BST with color coding: red and black nodes follow rules that keep the tree roughly balanced without strict height requirements.",
        "inputs": "Sequence of insert/delete/search operations on key-value pairs.",
        "outputs": "Balanced binary search tree with O(log n) worst-case height.",
        "steps": [
            "Insert node as red (maintains black height property).",
            "If parent is black, done; if red, check uncle color.",
            "If uncle is red: recolor parent, uncle, and grandparent.",
            "If uncle is black: rotate to fix red-red violation.",
            "Root is always black; all paths have same black node count."
        ],
        "example": "Insert 5,3,7,1: After 1, red-red violation with 3. Uncle 7 is red, so recolor: 3 and 7 become black, 5 becomes red.",
        "time_complexity": "O(log n) for all operations; slightly faster than AVL due to fewer rotations.",
        "space_complexity": "O(n) with one color bit per node.",
        "strengths": [
            "Fewer rotations than AVL trees, better for frequent updates.",
            "Used in many standard library implementations (Java TreeMap, C++ map)."
        ],
        "weaknesses": [
            "Less strictly balanced than AVL (height can be up to 2*log(n+1)).",
            "More complex than basic BST."
        ],
        "alternatives": ["AVL Tree", "Splay Tree", "Treap"],
        "explanation": "A self-balancing BST using red/black coloring rules that ensure no path is more than twice as long as any other."
    },
    "semester_01/lecture_06_advanced_trees/trie/README.md": {
        "name": "Trie",
        "problem": "Efficiently stores and searches strings with shared prefixes, enabling fast prefix matching and autocomplete.",
        "intuition": "Like a phone book organized by first letter, then second, then third: each level narrows down the search.",
        "inputs": "Set of strings (words, keys) and query operations (insert, search, prefix match).",
        "outputs": "Tree structure where each path from root to node represents a string prefix.",
        "steps": [
            "Root represents empty string.",
            "Each node has children for each possible next character.",
            "Insert: traverse/create path for each character, mark end node.",
            "Search: follow path character by character, check if end marker exists.",
            "Prefix search: traverse to prefix node, collect all descendants."
        ],
        "example": "Insert 'cat', 'car': root → 'c' → 'a' → 't' (end) and 'a' → 'r' (end). Search 'car': follow c-a-r, found.",
        "time_complexity": "O(m) for search/insert where m is string length; O(n*m) to build from n strings.",
        "space_complexity": "O(ALPHABET_SIZE * N * M) worst case, but can be compressed.",
        "strengths": [
            "Fast prefix matching and autocomplete queries.",
            "Efficient for dictionary lookups and spell checkers."
        ],
        "weaknesses": [
            "High memory usage for sparse tries.",
            "Slower than hash tables for exact lookups."
        ],
        "alternatives": ["Hash Table", "Ternary Search Tree", "Radix Tree"],
        "explanation": "A tree where each path spells out a string, making prefix searches as fast as following the path."
    },
    "semester_01/lecture_05_trees/binary_search_tree/README.md": {
        "name": "Binary Search Tree",
        "problem": "Stores keys so that lookups, inserts, and deletes can exploit sorted order with O(log n) average time.",
        "intuition": "Think of a game of twenty questions: each comparison decides whether to go left (smaller) or right (larger) until you reach the answer.",
        "inputs": "Comparable keys with optional values; operations like insert, search, delete.",
        "outputs": "Tree structure where in-order traversal yields sorted keys.",
        "steps": [
            "Start at the root node and compare the target key.",
            "If key < current node, recurse or iterate into the left child.",
            "If key > current node, recurse or iterate into the right child.",
            "If key equals the node, update or return the value.",
            "During deletion, replace removed nodes with predecessor or successor to preserve ordering."
        ],
        "example": "Insert 8,3,10,1,6: 8 is root, 3 goes left, 10 right, 1 left of 3, 6 right of 3.",
        "time_complexity": "Average O(log n); worst-case O(n) on skewed trees.",
        "space_complexity": "O(n) to store n nodes.",
        "strengths": [
            "Maintains sorted order with simple pointer structure.",
            "Supports inorder traversal to produce sorted output quickly."
        ],
        "weaknesses": [
            "Unbalanced input degrades operations to O(n).",
            "Needs balancing variants (AVL, Red-Black) for guaranteed performance."
        ],
        "alternatives": ["AVL Tree", "Red-Black Tree", "Skip List"],
        "explanation": "A search tree where each node’s left subtree holds smaller keys and the right subtree holds larger ones, enabling logarithmic search when balanced."
    },
    "semester_01/lecture_05_trees/binary_tree/README.md": {
        "name": "Binary Tree",
        "problem": "Represents hierarchical relationships where each node may have up to two children.",
        "intuition": "Picture a family tree where every person can have a left and right child pointer, letting you organize data hierarchically.",
        "inputs": "Nodes containing data plus optional left/right child references.",
        "outputs": "Tree structure supporting traversals such as preorder, inorder, and postorder.",
        "steps": [
            "Create a root node (which may be empty).",
            "Attach left/right children as required by the domain problem.",
            "Traverse using preorder (node-left-right), inorder (left-node-right), or postorder (left-right-node).",
            "Breadth-first traversal visits nodes level by level.",
            "Perform application-specific work (search, aggregation) during traversals."
        ],
        "example": "Tree with root 1, left child 2, right child 3: inorder traversal yields [2,1,3].",
        "time_complexity": "Traversals and searches touch each node once: O(n).",
        "space_complexity": "O(n) for nodes plus O(h) recursion depth where h is tree height.",
        "strengths": [
            "Flexible backbone for heaps, BSTs, and expression trees.",
            "Natural fit for recursive definitions and divide-and-conquer algorithms."
        ],
        "weaknesses": [
            "By itself offers no ordering or balancing guarantees.",
            "Pointer-heavy representation can hurt cache locality."
        ],
        "alternatives": ["General Tree", "Binary Search Tree", "Heap"],
        "explanation": "A generic two-child-per-node structure that underpins many specialized tree variants and traversals."
    },
    "semester_01/lecture_07_heaps_priority/binary_heap/README.md": {
        "name": "Binary Heap",
        "problem": "Maintains a complete binary tree where parent nodes are always greater (max-heap) or smaller (min-heap) than children.",
        "intuition": "Like a family tree where parents always outrank children: the top person is the most important, and you can quickly promote someone up the ranks.",
        "inputs": "Sequence of insert/extract operations on priority values.",
        "outputs": "Heap structure with O(1) access to max/min element.",
        "steps": [
            "Store heap in array: parent at i, children at 2i+1 and 2i+2.",
            "Insert: add to end, bubble up by swapping with parent if out of order.",
            "Extract: remove root, move last element to root, bubble down by swapping with larger/smaller child.",
            "Maintain heap property: parent >= children (max-heap) or parent <= children (min-heap)."
        ],
        "example": "Max-heap [9,7,5,3,2]: Insert 8 → [9,7,5,3,2,8] → bubble up: [9,8,5,3,2,7] (8 swapped with 7's parent).",
        "time_complexity": "O(log n) insert/extract, O(1) peek, O(n) build from array.",
        "space_complexity": "O(n) array storage.",
        "strengths": [
            "Simple array-based implementation, cache-friendly.",
            "Efficient for priority queues and heap sort."
        ],
        "weaknesses": [
            "No efficient search or decrease-key without additional structures.",
            "Not suitable for merging heaps efficiently."
        ],
        "alternatives": ["Fibonacci Heap", "Binomial Heap", "Pairing Heap"],
        "explanation": "A complete binary tree stored in an array that keeps the highest (or lowest) priority item at the top with O(log n) updates."
    },
    "semester_01/lecture_07_heaps_priority/fibonacci_heap/README.md": {
        "name": "Fibonacci Heap",
        "problem": "Provides extremely fast decrease-key and merge operations for advanced graph algorithms like Dijkstra's.",
        "intuition": "A lazy heap: it defers organizing work until absolutely necessary, making most operations very fast on average.",
        "inputs": "Sequence of insert, extract-min, decrease-key, and merge operations.",
        "outputs": "Amortized O(1) insert and decrease-key, O(log n) extract-min.",
        "steps": [
            "Maintain a collection of heap-ordered trees (forest).",
            "Insert: add new single-node tree to forest, O(1).",
            "Extract-min: remove min root, merge its children into forest, consolidate trees of same degree, O(log n).",
            "Decrease-key: update node, cut from parent if violates heap property, mark parent, O(1) amortized.",
            "Merge: combine two forests, O(1)."
        ],
        "example": "Forest with trees of degrees 0,1,2. Insert creates degree-0 tree. Extract-min consolidates: merge same-degree trees.",
        "time_complexity": "O(1) amortized insert/decrease-key/merge, O(log n) amortized extract-min.",
        "space_complexity": "O(n) with additional pointers for decrease-key operations.",
        "strengths": [
            "Fastest known heap for decrease-key operations.",
            "Enables O(m + n log n) Dijkstra's algorithm."
        ],
        "weaknesses": [
            "Complex implementation with many pointer manipulations.",
            "Large constant factors make it slower than binary heap for small inputs."
        ],
        "alternatives": ["Binary Heap", "Binomial Heap", "Pairing Heap"],
        "explanation": "A sophisticated heap that delays consolidation work, achieving O(1) decrease-key for graph algorithms."
    },
    "semester_01/lecture_07_heaps_priority/priority_queue/README.md": {
        "name": "Priority Queue",
        "problem": "Manages elements where highest (or lowest) priority item is always accessible, regardless of insertion order.",
        "intuition": "Like a hospital emergency room: the most urgent case gets treated first, even if others arrived earlier.",
        "inputs": "Sequence of enqueue (insert) and dequeue (extract) operations with priority values.",
        "outputs": "Always returns the highest priority element on dequeue.",
        "steps": [
            "Choose underlying data structure (binary heap, Fibonacci heap, etc.).",
            "Enqueue: insert element with its priority value.",
            "Dequeue: extract and return element with highest/lowest priority.",
            "Update priority: modify existing element's priority (if supported).",
            "Maintain heap property to ensure O(log n) operations."
        ],
        "example": "Enqueue tasks: (A,5), (B,9), (C,3). Dequeue returns B (priority 9), then A (5), then C (3).",
        "time_complexity": "O(log n) enqueue/dequeue with binary heap; O(1) amortized with Fibonacci heap.",
        "space_complexity": "O(n) to store n elements.",
        "strengths": [
            "Essential for scheduling, graph algorithms, and event simulation.",
            "Efficient access to extremal elements."
        ],
        "weaknesses": [
            "No efficient random access or search operations.",
            "Requires total ordering of priorities."
        ],
        "alternatives": ["Sorted Array", "Balanced BST", "Skip List"],
        "explanation": "A data structure that always gives you the most important item first, perfect for scheduling and optimization."
    },
    "semester_01/lecture_08_hash_tables/chaining/README.md": {
        "name": "Hash Table with Chaining",
        "problem": "Stores key-value pairs with O(1) average-case lookup by using hash function and collision resolution via linked lists.",
        "intuition": "Like a library with numbered shelves: hash function tells you which shelf, chaining handles when multiple books share a shelf.",
        "inputs": "Key-value pairs and operations: insert, get, delete.",
        "outputs": "Fast O(1) average-case retrieval of values by key.",
        "steps": [
            "Choose hash function h(k) that maps keys to bucket indices.",
            "Insert: compute h(key), add (key,value) to linked list at that bucket.",
            "Get: compute h(key), search linked list at bucket for matching key.",
            "Delete: compute h(key), remove node from linked list at bucket.",
            "Handle collisions: multiple keys hashing to same bucket share the list."
        ],
        "example": "Hash table size 5, keys 7,12,17. h(7)=2, h(12)=2 (collision), h(17)=2 (collision). Bucket 2: [7→12→17].",
        "time_complexity": "O(1) average case, O(n) worst case if all keys hash to same bucket.",
        "space_complexity": "O(n) for n key-value pairs plus overhead for buckets.",
        "strengths": [
            "Very fast average-case performance.",
            "Simple collision resolution, easy to implement."
        ],
        "weaknesses": [
            "Worst-case O(n) if hash function is poor or keys are adversarial.",
            "Requires good hash function and load factor management."
        ],
        "alternatives": ["Open Addressing", "Cuckoo Hashing", "Robin Hood Hashing"],
        "explanation": "A fast lookup structure that uses a hash function to map keys to buckets, with linked lists handling collisions."
    },
    "semester_01/lecture_08_hash_tables/hash_table/README.md": {
        "name": "Hash Table",
        "problem": "Provides constant-time average access to key-value pairs using hashing and collision resolution.",
        "intuition": "Like placing labeled folders into numbered drawers: the hash function turns a key into a drawer index so you jump straight there.",
        "inputs": "Key-value pairs with operations insert, lookup, delete.",
        "outputs": "Table of buckets where each bucket stores entries that hash to the same index.",
        "steps": [
            "Select hash function h(key) that maps keys to indices 0..m-1.",
            "Insert: compute index, place entry in bucket (or follow collision policy).",
            "Lookup: hash key, scan bucket/probe sequence for matching key.",
            "Delete: hash key, remove entry while preserving collision structure.",
            "Resize when load factor grows to keep operations near O(1)."
        ],
        "example": "Table size 7, keys 'cat','dog','eel'. Hash to indices 2,5,2 respectively; bucket 2 stores ['cat','eel'].",
        "time_complexity": "Average O(1) for insert/lookup/delete; worst-case O(n) if collisions degenerate.",
        "space_complexity": "O(n) for entries plus bucket overhead.",
        "strengths": [
            "Extremely fast average-case performance.",
            "Simple API for associative arrays and caches."
        ],
        "weaknesses": [
            "Needs high-quality hash functions and resizing strategy.",
            "No inherent ordering of keys."
        ],
        "alternatives": ["Binary Search Tree", "Skip List", "B-Tree"],
        "explanation": "Maps keys to array indices via a hash function so most operations touch a single bucket, yielding near-constant time."
    },
    "semester_01/lecture_08_hash_tables/open_addressing/README.md": {
        "name": "Open Addressing",
        "problem": "Resolves hash table collisions by probing alternative slots instead of storing overflow lists.",
        "intuition": "If a parking spot is taken, keep moving to the next slot according to a probe rule until you find an empty space.",
        "inputs": "Fixed-size table and probe sequence (linear, quadratic, double hashing).",
        "outputs": "Array where each slot holds at most one key-value pair plus optional tombstone markers.",
        "steps": [
            "Hash key to initial index i0 = h(key).",
            "If slot empty, place entry; otherwise compute next probe index via strategy.",
            "Repeat probing until an empty slot or tombstone is found.",
            "Lookup follows the same probe sequence until key or empty slot encountered.",
            "Deletion marks slot as tombstone to preserve probe chains."
        ],
        "example": "Linear probing size 5: insert keys hashing to index 2. Occupied? Try 3, then 4, then wrap to 0.",
        "time_complexity": "Average O(1) with low load factor; degrades toward O(n) as table fills.",
        "space_complexity": "O(m) for table of m slots; no extra pointers.",
        "strengths": [
            "Excellent cache locality because all data lives in the array.",
            "No extra heap allocations compared to chaining."
        ],
        "weaknesses": [
            "Primary clustering can create long probe sequences.",
            "Deletion logic complicated by tombstones and probe-chain maintenance."
        ],
        "alternatives": ["Separate Chaining", "Cuckoo Hashing", "Robin Hood Hashing"],
        "explanation": "Keeps every key directly in the array, using probe sequences to find the next available slot whenever collisions occur."
    },
    "semester_01/lecture_09_graph_algorithms/bellman_ford/README.md": {
        "name": "Bellman-Ford Algorithm",
        "problem": "Computes single-source shortest paths even when negative edge weights are present (assuming no negative cycles).",
        "intuition": "Relax every edge repeatedly so distances shrink over successive passes; if they still shrink after |V|-1 rounds, a negative cycle exists.",
        "inputs": "Directed weighted graph G(V,E) and source vertex s.",
        "outputs": "Shortest path distances (and optionally predecessors) from s or detection of negative cycles.",
        "steps": [
            "Initialize distance[s]=0 and all other distances to +∞.",
            "Repeat |V|-1 times: for each edge (u,v,w), relax by setting dist[v] = min(dist[v], dist[u] + w).",
            "Track predecessors when an edge improves a distance.",
            "Perform one more pass; if any edge can still relax, report a negative cycle.",
            "Return distance and predecessor arrays."
        ],
        "example": "Edges (0→1,5), (0→2,4), (2→1,-6), (1→3,3): after relaxation, dist[3]=2 via 0→2→1→3.",
        "time_complexity": "O(|V|·|E|).",
        "space_complexity": "O(|V|) for distance and predecessor arrays.",
        "strengths": [
            "Handles negative weights safely.",
            "Simple dynamic programming formulation."
        ],
        "weaknesses": [
            "Slower than Dijkstra on graphs without negative edges.",
            "Detecting negative cycles requires an additional pass."
        ],
        "alternatives": ["Dijkstra", "Johnson's Algorithm", "SPFA"],
        "explanation": "Iteratively relaxes all edges to propagate better distances, making it robust for graphs with negative weights."
    },
    "semester_01/lecture_09_graph_algorithms/bfs/README.md": {
        "name": "Breadth-First Search",
        "problem": "Traverses graphs level by level to find the shortest path in unweighted graphs and to explore reachable vertices.",
        "intuition": "Expand the frontier like ripples in a pond: visit all vertices one edge away before moving farther out.",
        "inputs": "Graph G(V,E) and optional start vertex.",
        "outputs": "Visit order, distance in edges, and predecessor tree for shortest paths.",
        "steps": [
            "Mark the start vertex as discovered, set distance 0, and enqueue it.",
            "While the queue is not empty, dequeue vertex u.",
            "For each neighbor v of u: if undiscovered, mark it, set parent[v]=u, dist[v]=dist[u]+1, enqueue v.",
            "Continue until queue empty to explore connected component.",
            "Use predecessor pointers to reconstruct shortest paths."
        ],
        "example": "Graph 0-1-2-3 with extra edge 0-2. BFS from 0 visits 0,1,2,3; dist[3]=2 via 0→2→3.",
        "time_complexity": "O(|V| + |E|).",
        "space_complexity": "O(|V|) for queue, visited, and parent arrays.",
        "strengths": [
            "Guarantees shortest paths in unweighted graphs.",
            "Useful for level-order traversal, bipartite checking, and finding connected components."
        ],
        "weaknesses": [
            "Requires memory proportional to the frontier size.",
            "Does not handle weights without modification."
        ],
        "alternatives": ["Depth-First Search", "Dijkstra", "A*"],
        "explanation": "Uses a queue to expand vertices in increasing distance from the source, ensuring level-order exploration."
    },
    "semester_01/lecture_09_graph_algorithms/dfs/README.md": {
        "name": "Depth-First Search",
        "problem": "Explores a graph by going as deep as possible along each branch before backtracking.",
        "intuition": "Like navigating a maze by always taking the next unexplored corridor until you hit a dead end, then backing up.",
        "inputs": "Graph representation plus optional start vertex.",
        "outputs": "Discovery/finish times, parent tree, and traversal order.",
        "steps": [
            "Start at chosen vertex, mark it visited, record discovery time.",
            "Recursively visit each unvisited neighbor (or use an explicit stack).",
            "After exploring neighbors, record finish time and backtrack.",
            "Repeat for any unvisited vertex to cover disconnected components.",
            "Leverage recorded times for cycle detection, topological sort, and strongly connected components."
        ],
        "example": "DFS on graph 0-1-2-3 explores path 0→1→2→3, then backtracks to explore remaining edges.",
        "time_complexity": "O(|V| + |E|).",
        "space_complexity": "O(|V|) recursion stack in worst case.",
        "strengths": [
            "Foundation for algorithms like topological sort and SCCs.",
            "Memory-light compared to BFS on dense layers."
        ],
        "weaknesses": [
            "Paths found are not guaranteed shortest.",
            "Deep recursion can overflow the stack on large graphs."
        ],
        "alternatives": ["Breadth-First Search", "Iterative Deepening DFS", "Tarjan's Algorithm"],
        "explanation": "Explores one branch completely before moving to the next, making it ideal for exhaustive search and backtracking problems."
    },
    "semester_01/lecture_09_graph_algorithms/dijkstra/README.md": {
        "name": "Dijkstra's Algorithm",
        "problem": "Computes shortest paths from a single source in graphs with non-negative edge weights.",
        "intuition": "Grow a settled set of nodes: always expand the vertex with the smallest tentative distance because no shorter route to it can exist.",
        "inputs": "Graph with non-negative edge weights and source vertex.",
        "outputs": "Shortest path distances and predecessors for each reachable vertex.",
        "steps": [
            "Initialize distance[source]=0, others=∞; push source into priority queue.",
            "Extract vertex u with smallest distance.",
            "For each edge (u,v,w), relax: if dist[u]+w < dist[v], update and push v.",
            "Mark u as settled so it will not be processed again.",
            "Continue until queue empty; reconstruct paths from predecessor array."
        ],
        "example": "Edges A→B(2), A→C(5), B→C(1). Algorithm finds dist[C]=3 via A→B→C.",
        "time_complexity": "O((|V| + |E|) log |V|) with binary heap.",
        "space_complexity": "O(|V|) for distance array and priority queue entries.",
        "strengths": [
            "Fast on sparse graphs with non-negative weights.",
            "Widely used in routing, navigation, and network optimization."
        ],
        "weaknesses": [
            "Fails with negative edge weights.",
            "Priority queue operations dominate costs on dense graphs."
        ],
        "alternatives": ["Bellman-Ford", "A*", "Johnson's Algorithm"],
        "explanation": "Repeatedly selects the closest unsettled vertex and relaxes its edges, guaranteeing optimal distances when weights are non-negative."
    },
    "semester_01/lecture_09_graph_algorithms/floyd_warshall/README.md": {
        "name": "Floyd-Warshall Algorithm",
        "problem": "Computes all-pairs shortest paths on weighted graphs (positive or negative edges, excluding negative cycles).",
        "intuition": "Dynamic programming over intermediate vertices: allow paths to use the first k vertices and iteratively increase k.",
        "inputs": "Weighted adjacency matrix for graph with n vertices.",
        "outputs": "n×n matrix of shortest path distances (and optionally predecessor matrix).",
        "steps": [
            "Initialize dist[i][j] with edge weights, set dist[i][i]=0.",
            "For k from 1 to n: for each pair (i,j), set dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]).",
            "Optionally maintain next[i][j] to reconstruct paths.",
            "After loops, dist contains shortest distances using any intermediate vertex.",
            "Detect negative cycles if any dist[i][i] < 0."
        ],
        "example": "For 3-vertex graph, algorithm considers whether going through vertex 2 improves distance from 1 to 3 and updates matrix accordingly.",
        "time_complexity": "O(n^3).",
        "space_complexity": "O(n^2).",
        "strengths": [
            "Handles negative weights and finds all-pairs distances in one pass.",
            "Simple triple-loop implementation."
        ],
        "weaknesses": [
            "Cubic runtime becomes expensive for large graphs.",
            "Requires dense matrix storage even for sparse graphs."
        ],
        "alternatives": ["Repeated Dijkstra", "Johnson's Algorithm", "APSP via matrix multiplication"],
        "explanation": "Systematically checks whether including each vertex k shortens the path between i and j, yielding all-pairs solutions."
    },
    "semester_01/lecture_11_dynamic_programming/knapsack/README.md": {
        "name": "0/1 Knapsack",
        "problem": "Selects items with weights and values to maximize value without exceeding capacity, using each item at most once.",
        "intuition": "Build solutions bottom-up: for each item, choose to take it or leave it based on remaining capacity and value gain.",
        "inputs": "List of item weights and values plus knapsack capacity W.",
        "outputs": "Maximum achievable value and optionally the chosen item set.",
        "steps": [
            "Create DP table dp[i][w] = best value using first i items and capacity w.",
            "Initialize base row/column with zeros.",
            "For each item i and capacity w: if weight[i] > w, copy dp[i-1][w]; otherwise take max(dp[i-1][w], value[i] + dp[i-1][w-weight[i]]).",
            "Fill table row by row to capacity W.",
            "Trace back from dp[n][W] to recover chosen items."
        ],
        "example": "Items {(2,3),(3,4),(4,5)}, capacity 5. Optimal takes items 1 and 2 for value 7.",
        "time_complexity": "O(nW) where n items and capacity W.",
        "space_complexity": "O(nW) table or O(W) with rolling array optimization.",
        "strengths": [
            "Deterministic optimal solution when W is moderate.",
            "Classic DP illustrating trade-offs in subset selection problems."
        ],
        "weaknesses": [
            "Pseudo-polynomial: runtime grows with numeric capacity.",
            "Not suitable when fractional choices are allowed."
        ],
        "alternatives": ["Fractional Knapsack", "Branch and Bound", "Meet-in-the-middle"],
        "explanation": "Dynamic programming weighs the value of including each item versus skipping it, constrained by the remaining capacity."
    },
    "semester_02/lecture_06_solid_principles/single_responsibility/README.md": {
        "name": "Single Responsibility Principle",
        "problem": "Ensures each class or module has exactly one reason to change.",
        "intuition": "Treat classes like specialists: one job, done well, so changes in one concern don’t ripple through unrelated code.",
        "inputs": "Object-oriented modules with multiple responsibilities entangled.",
        "outputs": "Refactored components where each focuses on a single responsibility.",
        "steps": [
            "Identify all reasons why the class might change (UI tweaks, business rules, persistence, etc.).",
            "Group behaviors by responsibility and highlight unrelated clusters.",
            "Extract new classes/functions for secondary responsibilities.",
            "Inject dependencies so each class collaborates instead of owning all logic.",
            "Add tests per responsibility to prove isolation."
        ],
        "example": "A Report class both formats PDFs and queries the database → split into ReportGenerator + ReportRepository.",
        "time_complexity": "Refactoring effort proportional to responsibilities discovered.",
        "space_complexity": "Extra classes/files for separated responsibilities.",
        "strengths": [
            "Improves cohesion and readability.",
            "Reduces blast radius when business rules evolve."
        ],
        "weaknesses": [
            "May introduce more classes/interfaces to navigate.",
            "Requires discipline to maintain separation over time."
        ],
        "alternatives": ["Modularization", "Functional Decomposition", "Componentization"],
        "explanation": "Keep each module focused on one reason to change so maintenance stays local and predictable."
    },
    "semester_02/lecture_06_solid_principles/open_closed/README.md": {
        "name": "Open/Closed Principle",
        "problem": "Code should be open for extension but closed for modification.",
        "intuition": "Once stable, classes become plug-in sockets: add new behavior via extension points instead of editing core logic.",
        "inputs": "Existing class that needs new behavior variations.",
        "outputs": "Abstractions that allow new features through inheritance, composition, or configuration.",
        "steps": [
            "Identify areas where features keep forcing edits to the same class.",
            "Extract abstractions (interfaces, base classes, strategy objects).",
            "Move variable behavior behind the abstraction boundary.",
            "Register new implementations without touching existing code.",
            "Cover extension points with tests to guard regressions."
        ],
        "example": "ShippingCalculator switches via if/else per region → introduce ShippingStrategy interface and register new strategies.",
        "time_complexity": "Depends on the breadth of extension points.",
        "space_complexity": "Additional classes or configuration objects to host extensions.",
        "strengths": [
            "Limits regression risk when adding features.",
            "Encourages plugin-style architectures."
        ],
        "weaknesses": [
            "Requires upfront abstraction design.",
            "Over-abstraction can make code harder to follow."
        ],
        "alternatives": ["Strategy Pattern", "Dependency Injection", "Feature Toggles"],
        "explanation": "Design modules so you add new behavior by plugging in new classes, not by editing the old ones."
    },
    "semester_02/lecture_06_solid_principles/liskov_substitution/README.md": {
        "name": "Liskov Substitution Principle",
        "problem": "Derived classes must behave like their base class so clients can substitute them without surprises.",
        "intuition": "If a square is a rectangle, any rectangle-using code should still work when given a square; inheritance should not break contracts.",
        "inputs": "Class hierarchies where overrides narrow behavior or violate expectations.",
        "outputs": "Subclasses that preserve base invariants, preconditions, and postconditions.",
        "steps": [
            "Document the base class contract (inputs, outputs, side effects).",
            "Ensure subclasses do not strengthen preconditions or weaken postconditions.",
            "Avoid throwing new exceptions or changing returned types unexpectedly.",
            "Prefer composition when behavior diverges significantly.",
            "Add substitution tests to validate behavior parity."
        ],
        "example": "Bird base class fly() → Penguin subclass overrides to throw; violates LSP, so extract FlightlessBird behavior instead.",
        "time_complexity": "Focused on design correctness rather than runtime.",
        "space_complexity": "May require extra wrapper classes for composition.",
        "strengths": [
            "Keeps polymorphism reliable for clients.",
            "Prevents brittle inheritance hierarchies."
        ],
        "weaknesses": [
            "Hard to enforce without strong contracts/tests.",
            "Legacy hierarchies may need large refactors."
        ],
        "alternatives": ["Composition over Inheritance", "Design by Contract", "Interface Segregation"],
        "explanation": "Subclasses should honor the promises of their parents so client code can substitute them freely."
    },
    "semester_02/lecture_06_solid_principles/interface_segregation/README.md": {
        "name": "Interface Segregation Principle",
        "problem": "Clients should not be forced to depend on methods they do not use.",
        "intuition": "Give each client a tailored remote control; bloated interfaces force consumers to worry about buttons they never press.",
        "inputs": "Large interfaces implemented by many classes with empty or throwing methods.",
        "outputs": "Smaller, client-specific interfaces implemented by relevant classes.",
        "steps": [
            "List interface methods and map them to actual client usage.",
            "Identify clusters of methods used together by specific clients.",
            "Split the interface into cohesive sub-interfaces.",
            "Update classes to implement only the interfaces they need.",
            "Refactor clients to depend on the refined contracts."
        ],
        "example": "IMultiFunctionDevice exposes print/scan/fax; a scanner-only device should not implement fax, so split into IPrinter, IScanner, IFax.",
        "time_complexity": "Refactor effort grows with number of clients.",
        "space_complexity": "More interface definitions to maintain.",
        "strengths": [
            "Reduces stub methods and unused dependencies.",
            "Improves readability and compile-time safety."
        ],
        "weaknesses": [
            "Too many interfaces can overwhelm newcomers.",
            "Requires coordination when clients share overlapping needs."
        ],
        "alternatives": ["Adapter Pattern", "Role Interfaces", "Service Facades"],
        "explanation": "Favor many small interfaces over one large one so consumers only depend on what they actually use."
    },
    "semester_02/lecture_06_solid_principles/dependency_inversion/README.md": {
        "name": "Dependency Inversion Principle",
        "problem": "High-level modules should not depend on low-level details; both should rely on abstractions.",
        "intuition": "Make policies depend on interfaces, not concrete wiring—like plugging different chargers into the same standard outlet.",
        "inputs": "Tightly coupled modules where business logic instantiates infrastructure details.",
        "outputs": "Abstractions (interfaces, ports) with concrete implementations supplied via inversion of control.",
        "steps": [
            "Identify high-level policies that currently create or depend on concrete classes.",
            "Define abstractions capturing the required behavior.",
            "Make high-level code depend on the abstractions instead of concretes.",
            "Provide implementations via constructors, factories, or DI containers.",
            "Write integration tests that swap implementations to ensure decoupling."
        ],
        "example": "OrderService new EmailNotifier() → instead depend on Notifier interface and inject EmailNotifier or SmsNotifier.",
        "time_complexity": "Adds indirection proportional to number of dependencies.",
        "space_complexity": "Requires extra interfaces and binding configuration.",
        "strengths": [
            "Improves testability via mocks/stubs.",
            "Encourages reusable high-level policies."
        ],
        "weaknesses": [
            "More abstractions can complicate debugging.",
            "Needs tooling (DI containers) to stay manageable at scale."
        ],
        "alternatives": ["Service Locator", "Inversion of Control Containers", "Plugin Architecture"],
        "explanation": "Depend on abstractions so high-level logic stays stable while low-level details swap freely."
    },
    "semester_02/lecture_08_structural_patterns/adapter/README.md": {
        "name": "Adapter Pattern",
        "problem": "Allows incompatible interfaces to collaborate without modifying existing code.",
        "intuition": "Like a power plug converter: adapt one shape to another so both sides work together.",
        "inputs": "Client expecting interface A and an existing service implementing interface B.",
        "outputs": "Adapter class translating client calls to the adaptee’s API.",
        "steps": [
            "Identify the target interface the client expects.",
            "Wrap the existing class (adaptee) inside an adapter implementing the target interface.",
            "Translate each operation: convert parameters, call adaptee, convert results.",
            "Inject or instantiate the adapter where the client previously used the adaptee.",
            "Write tests ensuring the adapter faithfully forwards behavior."
        ],
        "example": "Legacy XmlLogger used by new JsonLogger clients; Adapter implements JsonLogger interface but delegates to XmlLogger.",
        "time_complexity": "Negligible overhead—method dispatch plus conversions.",
        "space_complexity": "O(1) extra state per adapter instance.",
        "strengths": [
            "Enables reuse of existing classes without altering them.",
            "Supports incremental migrations between APIs."
        ],
        "weaknesses": [
            "Adds another indirection layer to maintain.",
            "Complex mappings can become brittle."
        ],
        "alternatives": ["Facade Pattern", "Decorator Pattern", "Wrapper Classes"],
        "explanation": "Introduce a thin wrapper that exposes the interface you need while delegating real work to an incompatible class."
    },
    "semester_02/lecture_08_structural_patterns/bridge/README.md": {
        "name": "Bridge Pattern",
        "problem": "Decouples abstractions from their implementations so both can vary independently.",
        "intuition": "Think of a remote control talking to different TVs: the remote is the abstraction, the TV electronics are implementations.",
        "inputs": "Hierarchy where multiple dimensions of variation (e.g., shape vs. rendering API) would otherwise explode subclasses.",
        "outputs": "Two orthogonal class hierarchies linked via composition.",
        "steps": [
            "Split the abstraction (high-level operations) from the implementation (platform-specific work).",
            "Define an implementation interface with primitive operations.",
            "Have the abstraction hold a reference to the implementation and delegate calls.",
            "Subclass both sides independently as variation requires.",
            "Provide wiring (factories/DI) to pair abstraction with concrete implementation."
        ],
        "example": "Shape abstraction (Circle, Square) delegates draw() to Renderer implementation (VectorRenderer, RasterRenderer).",
        "time_complexity": "Same as underlying implementation plus indirection.",
        "space_complexity": "One reference from abstraction to implementation.",
        "strengths": [
            "Prevents class explosion when combining variation axes.",
            "Allows runtime swapping of implementations."
        ],
        "weaknesses": [
            "More moving parts compared to simple inheritance.",
            "Requires careful naming to keep roles clear."
        ],
        "alternatives": ["Strategy Pattern", "Abstract Factory", "Adapter"],
        "explanation": "Compose abstractions with implementations so each can evolve on its own timeline without recompiling the other."
    },
    "semester_02/lecture_08_structural_patterns/composite/README.md": {
        "name": "Composite Pattern",
        "problem": "Treats individual objects and compositions uniformly (tree structures).",
        "intuition": "File systems treat files and directories with the same interface; composites hold children, leaves perform real work.",
        "inputs": "Recursive structures needing hierarchical operations (rendering UI trees, calculating totals).",
        "outputs": "Component interface with Leaf and Composite implementations.",
        "steps": [
            "Define a common Component interface with operations clients need.",
            "Implement Leaf for atomic objects.",
            "Implement Composite storing child components; delegate operations to children.",
            "Expose child-management methods (add/remove) on Composite.",
            "Ensure clients only depend on the Component interface."
        ],
        "example": "Graphic objects: Line, Circle (leaves) and Group (composite) so drawing occurs recursively.",
        "time_complexity": "Operations typically traverse entire subtree: O(n) where n is number of nodes touched.",
        "space_complexity": "O(n) to store tree plus recursion stack.",
        "strengths": [
            "Simplifies client code—treat everything as Component.",
            "Naturally models hierarchical data."
        ],
        "weaknesses": [
            "Hard to restrict which composites may contain which components.",
            "Can complicate operations needing parent references."
        ],
        "alternatives": ["Visitor Pattern", "Decorator Pattern", "Flyweight"],
        "explanation": "Build tree structures where clients operate on components without caring if they’re leaves or composites."
    },
    "semester_02/lecture_08_structural_patterns/decorator/README.md": {
        "name": "Decorator Pattern",
        "problem": "Adds responsibilities to objects dynamically without subclass explosion.",
        "intuition": "Like wrapping a gift multiple times: each wrapper adds behavior while still exposing the same interface.",
        "inputs": "Base component with optional features (logging, caching, compression).",
        "outputs": "Decorator classes implementing the same interface and holding a reference to the wrapped component.",
        "steps": [
            "Define a Component interface implemented by the base class.",
            "Create Decorator base class implementing Component and storing a Component reference.",
            "Implement concrete decorators that augment behavior before/after delegating.",
            "Wrap components with decorators at runtime to compose features.",
            "Ensure removal/reordering of decorators remains simple."
        ],
        "example": "DataSource decorated with CompressionDecorator then EncryptionDecorator before writing to disk.",
        "time_complexity": "Adds linear overhead proportional to number of decorators.",
        "space_complexity": "O(k) extra objects for k decorators.",
        "strengths": [
            "Flexible combination of features at runtime.",
            "Avoids deep inheritance hierarchies."
        ],
        "weaknesses": [
            "Debugging stack of decorators can be tricky.",
            "Many small objects increase complexity."
        ],
        "alternatives": ["Proxy Pattern", "Aspect-Oriented Programming", "Subclassing"],
        "explanation": "Wrap an object with other objects conforming to the same interface to add responsibilities dynamically."
    },
    "semester_02/lecture_08_structural_patterns/facade/README.md": {
        "name": "Facade Pattern",
        "problem": "Provides a simplified interface to a complex subsystem.",
        "intuition": "Think customer service hotline: one number routes requests to myriad internal departments.",
        "inputs": "Subsystem with many classes and configuration steps overwhelming clients.",
        "outputs": "Facade class exposing coarse-grained operations that orchestrate underlying components.",
        "steps": [
            "Map common client workflows that touch multiple subsystem classes.",
            "Create a Facade exposing methods for each workflow.",
            "Inside facade methods, coordinate subsystem objects in the right sequence.",
            "Keep subsystem classes accessible for advanced clients when needed.",
            "Document facade responsibilities clearly."
        ],
        "example": "VideoConverter facade hides codecs, bitrates, and file IO from client code.",
        "time_complexity": "Same as orchestrated workflow; facade adds minimal overhead.",
        "space_complexity": "Facade may cache subsystem instances for reuse.",
        "strengths": [
            "Reduces learning curve for complicated APIs.",
            "Decouples clients from subsystem evolution."
        ],
        "weaknesses": [
            "Facade can become a god-object if it grows unchecked.",
            "Still requires subsystem access for edge cases."
        ],
        "alternatives": ["Adapter Pattern", "Mediator Pattern", "Service Layer"],
        "explanation": "Offer a single entry point that bundles complex operations so clients interact with a friendly API."
    },
    "semester_02/lecture_08_structural_patterns/proxy/README.md": {
        "name": "Proxy Pattern",
        "problem": "Provides a surrogate object controlling access to a real subject (lazy loading, security, remote access).",
        "intuition": "Like a personal assistant screening calls before they reach the executive.",
        "inputs": "Original service object that needs access control, caching, or remote indirection.",
        "outputs": "Proxy implementing the same interface and delegating to the real subject with extra logic.",
        "steps": [
            "Define subject interface shared by both real object and proxy.",
            "Proxy holds reference to real subject, instantiating it lazily if necessary.",
            "Override operations to add pre/post behavior (checks, caching, logging).",
            "Ensure client interacts only with the proxy interface.",
            "Handle cleanup (connection closing, resource disposal) inside proxy."
        ],
        "example": "Virtual proxy delaying image loading until it must be displayed.",
        "time_complexity": "Varies with added behavior (e.g., caching may improve average time).",
        "space_complexity": "Proxy holds pointer to real subject plus any cache state.",
        "strengths": [
            "Adds cross-cutting concerns transparently.",
            "Supports remote proxies for distributed systems."
        ],
        "weaknesses": [
            "Another abstraction layer to test and maintain.",
            "Improper proxies can hide performance issues."
        ],
        "alternatives": ["Decorator Pattern", "Aspect-Oriented Programming", "Mediator"],
        "explanation": "Insert a stand-in object that looks like the real one but adds access control, caching, or remote communication."
    },
    "semester_02/lecture_09_behavioral_patterns/chain_of_responsibility/README.md": {
        "name": "Chain of Responsibility",
        "problem": "Decouples senders from receivers by giving more than one object a chance to handle a request.",
        "intuition": "Like escalating a customer ticket: each handler decides to process it or pass it along the chain.",
        "inputs": "Request object flowing through ordered handlers.",
        "outputs": "First handler that can process the request takes action; others remain unaware.",
        "steps": [
            "Define a Handler interface with set_next() and handle(request).",
            "Implement concrete handlers that either process or forward the request.",
            "Link handlers into a chain at runtime.",
            "Client sends the request to the first handler only.",
            "Optionally report when no handler could process the request."
        ],
        "example": "Auth pipeline: BasicAuthHandler → TokenAuthHandler → OAuthHandler, each checking credentials before escalating.",
        "time_complexity": "O(n) in length of chain in worst case.",
        "space_complexity": "O(1) per handler, O(n) to store chain links.",
        "strengths": [
            "Avoids monolithic if/else blocks.",
            "Supports flexible ordering and additions."
        ],
        "weaknesses": [
            "May be hard to ensure a request is eventually handled.",
            "Debugging requires understanding chain order."
        ],
        "alternatives": ["Middleware Pipelines", "Strategy Pattern", "Observer"],
        "explanation": "Pass requests down a linked list of handlers until one handles it, keeping senders unaware of the concrete receiver."
    },
    "semester_02/lecture_09_behavioral_patterns/command/README.md": {
        "name": "Command Pattern",
        "problem": "Encapsulates a request as an object so it can be queued, logged, undone, or replayed.",
        "intuition": "Just like a remote control storing button presses as commands you can redo/undo later.",
        "inputs": "Receiver object performing work and invoker scheduling commands.",
        "outputs": "Command objects implementing execute() (and optionally undo()).",
        "steps": [
            "Define Command interface with execute()/undo().",
            "Implement concrete commands wrapping receiver operations.",
            "Invoker stores commands and triggers execute at the right time.",
            "Maintain history stack if undo/redo is needed.",
            "Optionally serialize commands for auditing or retries."
        ],
        "example": "Text editor operations (InsertTextCommand, DeleteSelectionCommand) recorded for undo functionality.",
        "time_complexity": "Exec time equals receiver operation plus bookkeeping.",
        "space_complexity": "O(n) to store command history.",
        "strengths": [
            "Decouples senders from receivers.",
            "Enables undo/redo, macro recording, and asynchronous execution."
        ],
        "weaknesses": [
            "Lots of small command classes.",
            "Stateful commands must carefully manage context for undo."
        ],
        "alternatives": ["Event Sourcing", "Strategy Pattern", "Lambda commands"],
        "explanation": "Wrap each action in a command object so invokers can queue, log, or undo requests independently of receivers."
    },
    "semester_02/lecture_09_behavioral_patterns/iterator/README.md": {
        "name": "Iterator Pattern",
        "problem": "Provides a standard way to traverse elements of a collection without exposing its internals.",
        "intuition": "Like flipping through a photo album with an index finger that remembers your current spot.",
        "inputs": "Collection with potentially complex storage (trees, graphs, aggregates).",
        "outputs": "Iterator objects supporting next(), has_next(), and optional remove().",
        "steps": [
            "Define Iterator interface with traversal methods.",
            "Have collection expose factory method returning new iterator.",
            "Iterator maintains traversal state (current index/node).",
            "Clients use iterator to loop without knowing collection structure.",
            "Provide specialized iterators (reverse, breadth-first) as needed."
        ],
        "example": "Composite pattern provides a depth-first iterator to traverse nested components.",
        "time_complexity": "O(n) to traverse n elements.",
        "space_complexity": "O(1) to O(h) depending on iteration strategy (h = height for tree traversals).",
        "strengths": [
            "Supports multiple concurrent traversals.",
            "Keeps collection encapsulation intact."
        ],
        "weaknesses": [
            "Custom iterators can be verbose to implement.",
            "Modifications during iteration need careful coordination."
        ],
        "alternatives": ["Generator Functions", "Visitor Pattern", "Indexed loops"],
        "explanation": "Expose a traversal object so clients iterate over aggregates without coupling to internal representation."
    },
    "semester_02/lecture_09_behavioral_patterns/observer/README.md": {
        "name": "Observer Pattern",
        "problem": "Notifies multiple dependents automatically when a subject’s state changes.",
        "intuition": "Publish/subscribe: when the weather station updates, all registered displays react immediately.",
        "inputs": "Subject maintaining state and observers interested in changes.",
        "outputs": "Subscription mechanism where observers register for callbacks.",
        "steps": [
            "Subject exposes attach(), detach(), and notify() methods.",
            "Observers implement an interface (update(subject)).",
            "Subject calls notify() after state changes, iterating observers.",
            "Observers pull new state from subject or receive it as arguments.",
            "Ensure thread-safety and order guarantees if required."
        ],
        "example": "Stock ticker pushing price updates to dashboards and alert services.",
        "time_complexity": "O(n) per notification where n is number of observers.",
        "space_complexity": "O(n) to track observer references.",
        "strengths": [
            "Loose coupling between subjects and observers.",
            "Supports dynamic subscriptions at runtime."
        ],
        "weaknesses": [
            "Notification storms if observers perform heavy work.",
            "Difficult to debug notification order and memory leaks from forgotten detach()."
        ],
        "alternatives": ["Event Bus", "Reactive Streams", "Mediator Pattern"],
        "explanation": "Let observers subscribe to a subject so they are automatically notified whenever the subject changes state."
    },
    "semester_02/lecture_09_behavioral_patterns/strategy/README.md": {
        "name": "Strategy Pattern",
        "problem": "Defines a family of interchangeable algorithms that can be selected at runtime.",
        "intuition": "Choose the best route on a GPS: driving, walking, cycling strategies share interface but differ internally.",
        "inputs": "Context needing to swap algorithms (sorting, pricing, compression).",
        "outputs": "Strategy interface with concrete implementations and a context delegating work.",
        "steps": [
            "Identify behavior that varies independently from the rest of the class.",
            "Extract a Strategy interface declaring the behavior.",
            "Implement concrete strategies for each variation.",
            "Context holds a reference to a strategy and delegates calls.",
            "Provide mechanism to switch strategies dynamically if needed."
        ],
        "example": "PaymentProcessor uses CreditCardStrategy, PayPalStrategy, or CryptoStrategy based on user selection.",
        "time_complexity": "Same as selected strategy; selection overhead is O(1).",
        "space_complexity": "O(1) for context reference; additional strategies cost class storage.",
        "strengths": [
            "Eliminates conditionals for algorithm selection.",
            "Promotes testable, pluggable behaviors."
        ],
        "weaknesses": [
            "Requires clients to understand and select appropriate strategy.",
            "Too many tiny classes if not organized carefully."
        ],
        "alternatives": ["Policy Objects", "Function Pointers/Lambdas", "State Pattern"],
        "explanation": "Encapsulate interchangeable behaviors behind a common interface so contexts can switch algorithms without branching."
    },
    "semester_02/lecture_09_behavioral_patterns/template_method/README.md": {
        "name": "Template Method Pattern",
        "problem": "Defines the skeleton of an algorithm in a base class while letting subclasses override specific steps.",
        "intuition": "Recipe template: the base class outlines the process, subclasses supply the ingredient variations.",
        "inputs": "Algorithm with invariant structure but customizable steps.",
        "outputs": "Abstract class with template method calling primitive operations that subclasses override.",
        "steps": [
            "Identify invariant workflow steps and variable steps.",
            "Implement template_method() in base class orchestrating the workflow.",
            "Mark variable steps as abstract or provide default hooks.",
            "Subclasses override the hook methods to customize behavior.",
            "Optional hooks allow subclasses to insert logic before/after key steps."
        ],
        "example": "DocumentExporter defines export(): open → format → save; subclasses override format().",
        "time_complexity": "Equals sum of step complexities; overhead is minimal virtual dispatch.",
        "space_complexity": "O(1) additional space.",
        "strengths": [
            "Promotes code reuse for algorithm skeletons.",
            "Enforces consistent workflow across subclasses."
        ],
        "weaknesses": [
            "Inheritance-based, so variations require subclassing.",
            "Difficult to change algorithm order without altering base class."
        ],
        "alternatives": ["Strategy Pattern", "Hooks/Callbacks", "Pipeline Pattern"],
        "explanation": "Put the invariant algorithm flow in a base class and let subclasses override specific steps via hook methods."
    },
    "semester_02/lecture_07_creational_patterns/abstract_factory/README.md": {
        "name": "Abstract Factory Pattern",
        "problem": "Creates families of related objects without specifying their concrete classes.",
        "intuition": "Like selecting a furniture style: the abstract factory hands you matching chair/sofa/table sets without exposing exact classes.",
        "inputs": "Client needing themed objects (UI widgets per OS, database drivers per vendor).",
        "outputs": "Factory interface with methods for each product family plus concrete factories per variant.",
        "steps": [
            "Identify product families that must stay consistent together.",
            "Define abstract product interfaces for each family member.",
            "Declare an AbstractFactory specifying creation methods.",
            "Implement concrete factories returning concrete products in the same style.",
            "Clients work only with factory and product interfaces; swap factories to change families."
        ],
        "example": "GUI library supplies MacFactory and WindowsFactory producing consistent buttons, checkboxes, menus.",
        "time_complexity": "Object creation remains O(1); pattern adds indirection.",
        "space_complexity": "O(n) for concrete factory/product classes.",
        "strengths": [
            "Ensures product consistency across families.",
            "Encapsulates object creation behind interfaces."
        ],
        "weaknesses": [
            "Adding a new product type requires touching all factories.",
            "More abstraction layers to maintain."
        ],
        "alternatives": ["Factory Method", "Builder Pattern", "Prototype"],
        "explanation": "Provide an interface that creates entire families of related objects so clients can change themes by swapping factories."
    },
    "semester_02/lecture_07_creational_patterns/builder/README.md": {
        "name": "Builder Pattern",
        "problem": "Constructs complex objects step-by-step, allowing different representations with the same construction process.",
        "intuition": "Like ordering a custom burger: the builder tracks each ingredient while the director ensures the steps stay consistent.",
        "inputs": "Complex object with many optional parts or configurations.",
        "outputs": "Builder interface declaring construction steps and a Director orchestrating them.",
        "steps": [
            "Define Builder with methods for each part (setEngine, addSeats, etc.).",
            "Implement concrete builders producing different representations (e.g., CarBuilder vs. ManualBuilder).",
            "Director controls the order of steps for a given recipe.",
            "Client retrieves finished object from builder.",
            "Optionally let clients bypass Director for custom builds."
        ],
        "example": "VehicleBuilder constructs Car objects while ManualBuilder outputs a car manual using the same steps.",
        "time_complexity": "Linear in number of build steps.",
        "space_complexity": "Builder stores interim state until product is assembled.",
        "strengths": [
            "Separates complex construction from representation.",
            "Supports progressive object creation and validation."
        ],
        "weaknesses": [
            "Requires multiple builder classes when variants explode.",
            "Director adds ceremony for simple objects."
        ],
        "alternatives": ["Fluent Interfaces", "Factory Method", "Composite constructors"],
        "explanation": "Encapsulate construction steps in builders so the same process can create different representations of a complex object."
    },
    "semester_02/lecture_07_creational_patterns/factory/README.md": {
        "name": "Factory Method Pattern",
        "problem": "Defers instantiation to subclasses, letting them decide which concrete class to create.",
        "intuition": "A base class provides a hook for creating collaborators; subclasses override to supply specific types.",
        "inputs": "Superclass defining algorithm that depends on product objects.",
        "outputs": "factory_method() returning a Product interface implemented by subclasses.",
        "steps": [
            "Define Product interface implemented by concrete products.",
            "Create Creator base class with factory_method() returning Product.",
            "Implement default algorithm in Creator that calls factory_method().",
            "Subclass Creator to override factory_method() and return concrete products.",
            "Clients use Creator interface; subclass decides actual product."
        ],
        "example": "Application::createDocument() overridden by TextApp and SpreadsheetApp to return respective documents.",
        "time_complexity": "Same as product creation plus virtual call overhead.",
        "space_complexity": "O(n) for subclasses implementing factory method.",
        "strengths": [
            "Promotes loose coupling between creators and products.",
            "Allows new products by subclassing without touching base logic."
        ],
        "weaknesses": [
            "Requires subclass for each product variant.",
            "Can lead to parallel class hierarchies."
        ],
        "alternatives": ["Abstract Factory", "Simple Factory", "Builder"],
        "explanation": "Let subclasses decide which product to instantiate by overriding a factory method used by shared creator logic."
    },
    "semester_02/lecture_07_creational_patterns/prototype/README.md": {
        "name": "Prototype Pattern",
        "problem": "Creates new objects by cloning existing ones when instantiation cost is high or classes are dynamic.",
        "intuition": "Make copies from a mold: keep prototypes and clone them instead of constructing from scratch.",
        "inputs": "Prototype registry storing exemplar objects capable of deep/shallow cloning.",
        "outputs": "clone() operations returning duplicated objects with optional tweaks.",
        "steps": [
            "Implement prototype interface with clone() method.",
            "Store registered prototypes in a lookup table.",
            "To create a new object, retrieve prototype and clone it.",
            "Customize cloned instance (e.g., set new IDs).",
            "Ensure deep copies for mutable nested objects to avoid shared state."
        ],
        "example": "Graphics editor clones shapes (circles, arrows) to duplicate user-drawn elements quickly.",
        "time_complexity": "Depends on clone depth; typically O(size of object graph).",
        "space_complexity": "O(size) to duplicate object graph per clone.",
        "strengths": [
            "Avoids complex constructor logic for each new instance.",
            "Supports runtime addition of new prototype types."
        ],
        "weaknesses": [
            "Implementing deep cloning can be tricky.",
            "Hidden coupling when prototypes share mutable state."
        ],
        "alternatives": ["Builder Pattern", "Abstract Factory", "Serialization copy"],
        "explanation": "Register exemplar objects and copy them to produce new instances whenever direct construction is expensive or dynamic."
    },
    "semester_02/lecture_07_creational_patterns/singleton/README.md": {
        "name": "Singleton Pattern",
        "problem": "Ensures a class has only one instance and provides a global access point.",
        "intuition": "System-wide resource manager (e.g., print spooler) that must exist exactly once.",
        "inputs": "Class needing single shared state across application.",
        "outputs": "Private constructor, static get_instance() method, and stored singleton instance.",
        "steps": [
            "Make constructor private/protected to prevent external instantiation.",
            "Expose static method that returns the single instance.",
            "Instantiate lazily or eagerly inside the static method.",
            "Ensure thread safety in multi-threaded environments.",
            "Prevent cloning/serialization from creating additional instances."
        ],
        "example": "ConfigurationManager loads config once and offers global access to settings.",
        "time_complexity": "get_instance() typically O(1); synchronization can add contention.",
        "space_complexity": "O(1) for stored instance.",
        "strengths": [
            "Ensures single point of coordination.",
            "Lazy initialization reduces startup cost."
        ],
        "weaknesses": [
            "Global state hampers testability and introduces hidden dependencies.",
            "Difficult to scale/distribute.",
            "Thread-safe implementations can be verbose."
        ],
        "alternatives": ["Dependency Injection", "Static Classes", "Module-level singletons"],
        "explanation": "Control instantiation so exactly one object exists and is accessible globally, but use sparingly due to testability concerns."
    },
    "semester_01/lecture_05_trees/avl_tree/README.md": {
        "name": "AVL Tree",
        "problem": "Maintains a self-balancing binary search tree where the heights of left and right subtrees differ by at most one.",
        "intuition": "Like a see-saw that automatically adjusts itself: whenever one side gets too heavy, it rotates to balance out.",
        "inputs": "Sequence of insert/delete/search operations on key-value pairs.",
        "outputs": "Balanced binary search tree with O(log n) height guarantees.",
        "steps": [
            "Insert or delete a node using standard BST rules.",
            "Check the balance factor (height difference) of each ancestor.",
            "If imbalance detected (|balance| > 1), perform rotations.",
            "Single rotation for outside cases (left-left or right-right).",
            "Double rotation for inside cases (left-right or right-left).",
            "Update heights and continue up the tree until balanced."
        ],
        "example": "Insert 3,2,1: After 3 and 2, insert 1 causes left-left imbalance. Rotate right around 3: [2(1,3)].",
        "time_complexity": "O(log n) for all operations (insert, delete, search).",
        "space_complexity": "O(n) to store n nodes.",
        "strengths": [
            "Guaranteed O(log n) height ensures predictable performance.",
            "Strict balancing prevents worst-case O(n) behavior."
        ],
        "weaknesses": [
            "More complex than basic BST due to rotation overhead.",
            "Requires storing balance factors or heights per node."
        ],
        "alternatives": ["Red-Black Tree", "Splay Tree", "B-Tree"],
        "explanation": "A self-adjusting BST that keeps itself balanced by rotating nodes when one subtree becomes too tall."
    },
    "semester_01/lecture_05_trees/binary_search_tree/README.md": {
        "name": "Binary Search Tree",
        "problem": "Stores keys so that lookups, inserts, and deletes can exploit sorted order with O(log n) average time.",
        "intuition": "Think of a game of twenty questions: each comparison decides whether to go left (smaller) or right (larger) until you reach the answer.",
        "inputs": "Comparable keys with optional values; operations like insert, search, delete.",
        "outputs": "Tree structure where in-order traversal yields sorted keys.",
        "steps": [
            "Start at the root node and compare the target key.",
            "If key < current node, recurse or iterate into the left child.",
            "If key > current node, recurse or iterate into the right child.",
            "If key equals the node, update or return the value.",
            "During deletion, replace removed nodes with predecessor or successor to preserve ordering."
        ],
        "example": "Insert 8,3,10,1,6: 8 is root, 3 goes left, 10 right, 1 left of 3, 6 right of 3.",
        "time_complexity": "Average O(log n); worst-case O(n) on skewed trees.",
        "space_complexity": "O(n) to store n nodes.",
        "strengths": [
            "Maintains sorted order with simple pointer structure.",
            "Supports inorder traversal to produce sorted output quickly."
        ],
        "weaknesses": [
            "Unbalanced input degrades operations to O(n).",
            "Needs balancing variants (AVL, Red-Black) for guaranteed performance."
        ],
        "alternatives": ["AVL Tree", "Red-Black Tree", "Skip List"],
        "explanation": "A search tree where each node’s left subtree holds smaller keys and the right subtree holds larger ones, enabling logarithmic search when balanced."
    },
    "semester_01/lecture_05_trees/binary_tree/README.md": {
        "name": "Binary Tree",
        "problem": "Represents hierarchical relationships where each node may have up to two children.",
        "intuition": "Picture a family tree where every person can have a left and right child pointer, letting you organize data hierarchically.",
        "inputs": "Nodes containing data plus optional left/right child references.",
        "outputs": "Tree structure supporting traversals such as preorder, inorder, and postorder.",
        "steps": [
            "Create a root node (which may be empty).",
            "Attach left/right children as required by the domain problem.",
            "Traverse using preorder (node-left-right), inorder (left-node-right), or postorder (left-right-node).",
            "Breadth-first traversal visits nodes level by level.",
            "Perform application-specific work (search, aggregation) during traversals."
        ],
        "example": "Tree with root 1, left child 2, right child 3: inorder traversal yields [2,1,3].",
        "time_complexity": "Traversals and searches touch each node once: O(n).",
        "space_complexity": "O(n) for nodes plus O(h) recursion depth where h is tree height.",
        "strengths": [
            "Flexible backbone for heaps, BSTs, and expression trees.",
            "Natural fit for recursive definitions and divide-and-conquer algorithms."
        ],
        "weaknesses": [
            "By itself offers no ordering or balancing guarantees.",
            "Pointer-heavy representation can hurt cache locality."
        ],
        "alternatives": ["General Tree", "Binary Search Tree", "Heap"],
        "explanation": "A generic two-child-per-node structure that underpins many specialized tree variants and traversals."
    },
    "semester_01/lecture_06_advanced_trees/avl_tree/README.md": {
        "name": "AVL Tree",
        "problem": "Maintains a self-balancing binary search tree where the heights of left and right subtrees differ by at most one.",
        "intuition": "Like a see-saw that automatically adjusts itself: whenever one side gets too heavy, it rotates to balance out.",
        "inputs": "Sequence of insert/delete/search operations on key-value pairs.",
        "outputs": "Balanced binary search tree with O(log n) height guarantees.",
        "steps": [
            "Insert or delete a node using standard BST rules.",
            "Check the balance factor (height difference) of each ancestor.",
            "If imbalance detected (|balance| > 1), perform rotations.",
            "Single rotation for outside cases (left-left or right-right).",
            "Double rotation for inside cases (left-right or right-left).",
            "Update heights and continue up the tree until balanced."
        ],
        "example": "Insert 3,2,1: After 3 and 2, insert 1 causes left-left imbalance. Rotate right around 3: [2(1,3)].",
        "time_complexity": "O(log n) for all operations (insert, delete, search).",
        "space_complexity": "O(n) to store n nodes.",
        "strengths": [
            "Guaranteed O(log n) height ensures predictable performance.",
            "Strict balancing prevents worst-case O(n) behavior."
        ],
        "weaknesses": [
            "More complex than basic BST due to rotation overhead.",
            "Requires storing balance factors or heights per node."
        ],
        "alternatives": ["Red-Black Tree", "Splay Tree", "B-Tree"],
        "explanation": "A self-adjusting BST that keeps itself balanced by rotating nodes when one subtree becomes too tall."
    },
    "semester_01/lecture_06_advanced_trees/b_tree/README.md": {
        "name": "B-Tree",
        "problem": "Efficiently stores and retrieves large datasets on disk by minimizing disk I/O through wide, shallow trees.",
        "intuition": "Like a library filing system: instead of narrow tall shelves, use wide shallow ones so you can grab multiple books at once.",
        "inputs": "Large dataset of key-value pairs, typically stored on disk.",
        "outputs": "Multi-way search tree optimized for external storage access.",
        "steps": [
            "Each node contains multiple keys (typically 100-1000) and child pointers.",
            "Search: traverse from root, compare with node keys, follow appropriate child.",
            "Insert: find leaf, add key; if node overflows, split and promote middle key.",
            "Delete: remove key; if node underflows, merge with sibling or borrow key.",
            "Maintain property: all leaves at same depth, nodes between t-1 and 2t-1 keys."
        ],
        "example": "B-tree of order 3: root [10,20] has children [5,7], [15,17], [25,27]. Insert 12: goes to middle child, no split needed.",
        "time_complexity": "O(log n) with base of node capacity (typically 100-1000), making it effectively O(log n / log t).",
        "space_complexity": "O(n) total storage, but nodes are large (disk pages).",
        "strengths": [
            "Minimizes disk I/O by reading large nodes (pages) at once.",
            "Widely used in databases and file systems for indexing."
        ],
        "weaknesses": [
            "More complex than binary trees for in-memory operations.",
            "Requires careful tuning of node size for optimal performance."
        ],
        "alternatives": ["B+ Tree", "LSM Tree", "Hash Index"],
        "explanation": "A multi-way tree that stores many keys per node to reduce disk reads, perfect for database indexing."
    },
    "semester_01/lecture_06_advanced_trees/red_black_tree/README.md": {
        "name": "Red-Black Tree",
        "problem": "Maintains a balanced binary search tree with relaxed balancing rules compared to AVL trees.",
        "intuition": "A BST with color coding: red and black nodes follow rules that keep the tree roughly balanced without strict height requirements.",
        "inputs": "Sequence of insert/delete/search operations on key-value pairs.",
        "outputs": "Balanced binary search tree with O(log n) worst-case height.",
        "steps": [
            "Insert node as red (maintains black height property).",
            "If parent is black, done; if red, check uncle color.",
            "If uncle is red: recolor parent, uncle, and grandparent.",
            "If uncle is black: rotate to fix red-red violation.",
            "Root is always black; all paths have same black node count."
        ],
        "example": "Insert 5,3,7,1: After 1, red-red violation with 3. Uncle 7 is red, so recolor: 3 and 7 become black, 5 becomes red.",
        "time_complexity": "O(log n) for all operations; slightly faster than AVL due to fewer rotations.",
        "space_complexity": "O(n) with one color bit per node.",
        "strengths": [
            "Fewer rotations than AVL trees, better for frequent updates.",
            "Used in many standard library implementations (Java TreeMap, C++ map)."
        ],
        "weaknesses": [
            "Less strictly balanced than AVL (height can be up to 2*log(n+1)).",
            "More complex than basic BST."
        ],
        "alternatives": ["AVL Tree", "Splay Tree", "Treap"],
        "explanation": "A self-balancing BST using red/black coloring rules that ensure no path is more than twice as long as any other."
    },
    "semester_01/lecture_06_advanced_trees/trie/README.md": {
        "name": "Trie",
        "problem": "Efficiently stores and searches strings with shared prefixes, enabling fast prefix matching and autocomplete.",
        "intuition": "Like a phone book organized by first letter, then second, then third: each level narrows down the search.",
        "inputs": "Set of strings (words, keys) and query operations (insert, search, prefix match).",
        "outputs": "Tree structure where each path from root to node represents a string prefix.",
        "steps": [
            "Root represents empty string.",
            "Each node has children for each possible next character.",
            "Insert: traverse/create path for each character, mark end node.",
            "Search: follow path character by character, check if end marker exists.",
            "Prefix search: traverse to prefix node, collect all descendants."
        ],
        "example": "Insert 'cat', 'car': root → 'c' → 'a' → 't' (end) and 'a' → 'r' (end). Search 'car': follow c-a-r, found.",
        "time_complexity": "O(m) per operation where m is key length (assuming fixed alphabet).",
        "space_complexity": "O(ALPHABET_SIZE × number_of_nodes); can be optimized with compression.",
        "strengths": [
            "Fast prefix queries and lexicographic enumeration.",
            "Supports autocomplete, spell-check, and dictionary applications."
        ],
        "weaknesses": [
            "High memory usage for sparse datasets.",
            "Does not inherently store ordering beyond lexicographic traversal."
        ],
        "alternatives": ["Hash Table", "Ternary Search Tree", "Radix Tree"],
        "explanation": "Store strings character by character so common prefixes share nodes, allowing quick prefix-based lookups."
    },
    "semester_03/lecture_11_dynamic_programming/edit_distance/README.md": {
        "name": "Edit Distance (Levenshtein)",
        "problem": "Finds the minimum number of insertions, deletions, and substitutions to transform one string into another.",
        "intuition": "Compare strings letter by letter; when they diverge, decide whether to insert, delete, or substitute the mismatch with minimal total cost.",
        "inputs": "Two strings s and t (lengths n and m).",
        "outputs": "Minimum edit operations required; optionally the sequence of edits.",
        "steps": [
            "Create DP table dp of size (n+1) × (m+1).",
            "Initialize first row/column with index values (cost of deletions/insertions).",
            "For each i,j: if s[i-1]==t[j-1], dp[i][j]=dp[i-1][j-1].",
            "Otherwise dp[i][j] = 1 + min(dp[i-1][j] (delete), dp[i][j-1] (insert), dp[i-1][j-1] (substitute)).",
            "Answer is dp[n][m]; backtrack to recover edit script if needed."
        ],
        "example": "Transform \"cat\" → \"cut\": substitute 'a'→'u' (1 edit). DP table yields cost 1.",
        "time_complexity": "O(n·m).",
        "space_complexity": "O(n·m) or O(min(n,m)) with rolling array.",
        "strengths": [
            "Robust similarity metric for strings.",
            "Easily extended with custom costs."
        ],
        "weaknesses": [
            "Quadratic time for long strings.",
            "Memory heavy without optimizations."
        ],
        "alternatives": ["Hamming Distance", "Damerau-Levenshtein", "Longest Common Subsequence"],
        "explanation": "Dynamic programming over prefixes chooses the cheapest combination of insert/delete/substitute to align two strings."
    },
    "semester_03/lecture_11_dynamic_programming/longest_common_subsequence/README.md": {
        "name": "Longest Common Subsequence (LCS)",
        "problem": "Finds the longest sequence present in order (not necessarily contiguous) in two strings.",
        "intuition": "Walk both strings together; when characters match, include them, otherwise decide whether to drop a char from one string or the other via DP.",
        "inputs": "Strings s (length n) and t (length m).",
        "outputs": "Length of longest common subsequence (and optionally the subsequence).",
        "steps": [
            "Initialize DP table dp[n+1][m+1] to zero.",
            "For i=1..n: for j=1..m:",
            "  If s[i-1]==t[j-1], dp[i][j]=dp[i-1][j-1]+1.",
            "  Else dp[i][j]=max(dp[i-1][j], dp[i][j-1]).",
            "Backtrack from dp[n][m] to reconstruct the subsequence."
        ],
        "example": "s=\"ABCBDAB\", t=\"BDCABA\" → LCS length 4 (\"BCBA\").",
        "time_complexity": "O(n·m).",
        "space_complexity": "O(n·m) (can be reduced to O(min(n,m)) for length only).",
        "strengths": [
            "Foundation for diff tools and bioinformatics alignment.",
            "Provides similarity measure ignoring non-matching sections."
        ],
        "weaknesses": [
            "Quadratic runtime on string lengths.",
            "Reconstruction requires storing parent pointers or stack."
        ],
        "alternatives": ["Edit Distance", "Longest Common Substring", "Sequence Alignment"],
        "explanation": "Fills a DP grid where each cell stores the best LCS length up to those prefixes, ensuring optimal substructure reuse."
    },
    "semester_03/lecture_11_dynamic_programming/fibonacci/README.md": {
        "name": "Dynamic Programming Fibonacci",
        "problem": "Computes nth Fibonacci number efficiently by caching results instead of using exponential recursion.",
        "intuition": "Store results of smaller fib values so each number is computed once; akin to filling a table bottom-up.",
        "inputs": "Integer n ≥ 0.",
        "outputs": "The nth Fibonacci number (0-indexed).",
        "steps": [
            "Handle base cases fib(0)=0, fib(1)=1.",
            "Initialize array dp of size n+1.",
            "Iterate i from 2..n: dp[i]=dp[i-1]+dp[i-2].",
            "Optionally reduce to two variables for constant space.",
            "Return dp[n]."
        ],
        "example": "n=6 → sequence 0,1,1,2,3,5,8 → fib(6)=8.",
        "time_complexity": "O(n).",
        "space_complexity": "O(n) for table or O(1) with rolling values.",
        "strengths": [
            "Demonstrates memoization/bottom-up DP basics.",
            "Linear time versus exponential recursive approach."
        ],
        "weaknesses": [
            "Simple example; real problems may require more intricate states.",
            "Large n requires big integers or modulo arithmetic."
        ],
        "alternatives": ["Matrix Exponentiation", "Closed-form (Binet) Formula", "Fast Doubling Method"],
        "explanation": "Replace naive recursion with iterative accumulation while caching prior values so each Fibonacci number is computed exactly once."
    },
    "semester_01/lecture_12_string_algorithms/kmp/README.md": {
        "name": "Knuth-Morris-Pratt (KMP)",
        "problem": "Finds all occurrences of a pattern string in a text string efficiently by avoiding redundant character comparisons.",
        "intuition": "When a mismatch occurs, use knowledge of already-matched characters to skip ahead intelligently instead of restarting from scratch.",
        "inputs": "Text string T (length n) and pattern string P (length m).",
        "outputs": "List of starting indices where P appears in T.",
        "steps": [
            "Preprocess pattern P to build a failure function (longest proper prefix that is also a suffix).",
            "Initialize text pointer i=0 and pattern pointer j=0.",
            "If T[i] == P[j], advance both pointers.",
            "If mismatch: if j>0, set j = failure[j-1] (don't move i); else advance i.",
            "If j reaches m, found a match at i-m; reset j using failure function and continue."
        ],
        "example": "Text \"ABABDABACDABABC\", pattern \"ABABC\": failure=[0,0,1,2,0]. Match at index 10.",
        "time_complexity": "O(n+m) - linear in combined length.",
        "space_complexity": "O(m) for failure function.",
        "strengths": [
            "Linear time complexity, no backtracking in text.",
            "Efficient for multiple pattern searches."
        ],
        "weaknesses": [
            "Requires preprocessing step.",
            "More complex than naive string matching."
        ],
        "alternatives": ["Boyer-Moore", "Rabin-Karp", "Aho-Corasick"],
        "explanation": "Precompute where to resume matching after a failure, so the text pointer never moves backward."
    },
    "semester_03/lecture_14_string_algorithms/boyer_moore/README.md": {
        "name": "Boyer-Moore",
        "problem": "Finds pattern occurrences in text by scanning from right to left and skipping ahead when mismatches occur.",
        "intuition": "Start matching from the end of the pattern; when a mismatch happens, use two heuristics to jump ahead as far as possible.",
        "inputs": "Text string T (length n) and pattern string P (length m).",
        "outputs": "All starting positions where P occurs in T.",
        "steps": [
            "Preprocess P to build bad character table (rightmost occurrence of each char).",
            "Preprocess P to build good suffix table (longest suffix that matches a prefix).",
            "Align P with start of T, compare from right to left.",
            "On mismatch: skip by max(bad character shift, good suffix shift).",
            "Continue until pattern slides past end of text."
        ],
        "example": "Text \"THIS IS A TEST\", pattern \"TEST\": bad char 'T' at end allows skipping ahead.",
        "time_complexity": "O(n/m) best case, O(n·m) worst case, typically sub-linear in practice.",
        "space_complexity": "O(m + |alphabet|) for preprocessing tables.",
        "strengths": [
            "Often faster than linear algorithms in practice due to large skips.",
            "Excellent for long patterns and large alphabets."
        ],
        "weaknesses": [
            "Worst-case quadratic time possible.",
            "More complex preprocessing than KMP."
        ],
        "alternatives": ["KMP", "Rabin-Karp", "Sunday Algorithm"],
        "explanation": "Match backwards and use character mismatches to skip ahead intelligently, often faster than forward matching."
    },
    "semester_03/lecture_14_string_algorithms/rabin_karp/README.md": {
        "name": "Rabin-Karp",
        "problem": "Finds pattern occurrences using rolling hash to quickly compare pattern hash with text window hashes.",
        "intuition": "Hash the pattern once, then slide a window through text and compare hashes; only do full comparison when hashes match.",
        "inputs": "Text string T (length n) and pattern string P (length m).",
        "outputs": "All starting indices where P appears in T.",
        "steps": [
            "Compute hash of pattern P.",
            "Compute hash of first m characters of text.",
            "If hashes match, verify with character-by-character comparison.",
            "Roll hash forward: remove leftmost char, add rightmost char, update hash.",
            "Repeat until end of text."
        ],
        "example": "Text \"GEEKS FOR GEEKS\", pattern \"GEEK\": hash matches at indices 0 and 10.",
        "time_complexity": "O(n+m) average, O(n·m) worst if many hash collisions.",
        "space_complexity": "O(1) extra space (excluding hash storage).",
        "strengths": [
            "Simple to implement with rolling hash.",
            "Efficient for multiple pattern searches with same length."
        ],
        "weaknesses": [
            "Worst-case performance degrades with many collisions.",
            "Requires careful hash function selection."
        ],
        "alternatives": ["KMP", "Boyer-Moore", "Finite Automaton"],
        "explanation": "Use hashing to quickly filter out non-matches; only verify when hash values agree."
    },
    "semester_01/lecture_03_specialized_sorting/bucket_sort/README.md": {
        "name": "Bucket Sort",
        "problem": "Sorts uniformly distributed numbers by distributing them into buckets, sorting each bucket, then concatenating.",
        "intuition": "Like sorting mail into post office boxes: put each item in the right bucket, sort buckets individually, then combine.",
        "inputs": "Array of numbers uniformly distributed over a known range [min, max].",
        "outputs": "Sorted array.",
        "steps": [
            "Create n empty buckets (or fewer, based on range).",
            "Distribute array elements into buckets: bucket[i] = floor(n * (arr[i] - min) / (max - min)).",
            "Sort each bucket individually (using insertion sort or another algorithm).",
            "Concatenate all buckets in order."
        ],
        "example": "[0.42, 0.32, 0.33, 0.52, 0.37, 0.47] → buckets: [0.32,0.33,0.37], [0.42,0.47], [0.52] → sorted.",
        "time_complexity": "O(n+k) average when uniformly distributed, O(n²) worst if all items in one bucket.",
        "space_complexity": "O(n+k) for buckets.",
        "strengths": [
            "Linear average time for uniform distributions.",
            "Stable if bucket sorting is stable."
        ],
        "weaknesses": [
            "Requires uniform distribution for efficiency.",
            "Extra space for buckets."
        ],
        "alternatives": ["Counting Sort", "Radix Sort", "Quick Sort"],
        "explanation": "Divide the range into buckets, scatter items into appropriate buckets, sort buckets, then merge them back."
    },
    "semester_01/lecture_03_specialized_sorting/counting_sort/README.md": {
        "name": "Counting Sort",
        "problem": "Sorts integers in a small range by counting occurrences of each value, then placing them in order.",
        "intuition": "Count how many times each number appears, then write them out in order based on the counts.",
        "inputs": "Array of integers with range [0, k] where k is small (typically k = O(n)).",
        "outputs": "Sorted array.",
        "steps": [
            "Create count array of size k+1, initialize to zero.",
            "Count occurrences: for each element, increment count[element].",
            "Compute cumulative counts: count[i] += count[i-1] for i=1..k.",
            "Build output array: place each element at position count[element]-1, decrement count[element].",
            "Copy output back to original array if needed."
        ],
        "example": "[4,2,2,8,3,3,1] → counts: [0,1,2,2,1,0,0,0,1] → cumulative: [0,1,3,5,6,6,6,6,7] → sorted: [1,2,2,3,3,4,8].",
        "time_complexity": "O(n+k) where k is the range size.",
        "space_complexity": "O(n+k) for count and output arrays.",
        "strengths": [
            "Linear time when range is small.",
            "Stable sorting algorithm."
        ],
        "weaknesses": [
            "Only works for integers in a limited range.",
            "Space overhead for count array."
        ],
        "alternatives": ["Radix Sort", "Bucket Sort", "Pigeonhole Sort"],
        "explanation": "Count how many of each value exist, then write them out in order based on those counts."
    },
    "semester_01/lecture_03_specialized_sorting/radix_sort/README.md": {
        "name": "Radix Sort",
        "problem": "Sorts integers or fixed-length strings by processing digits/characters from least to most significant position.",
        "intuition": "Sort by ones place, then tens, then hundreds—each pass makes the array more sorted until fully ordered.",
        "inputs": "Array of integers or fixed-length strings.",
        "outputs": "Sorted array.",
        "steps": [
            "Find maximum value to determine number of digits.",
            "For each digit position from least to most significant:",
            "  Use counting sort (or stable sort) to sort by current digit.",
            "  Update array with sorted order.",
            "After processing all digits, array is fully sorted."
        ],
        "example": "[170, 45, 75, 90, 2, 802, 24, 66]: sort by ones → [170,90,2,802,24,45,75,66]; by tens → [2,802,24,45,66,170,75,90]; by hundreds → [2,24,45,66,75,90,170,802].",
        "time_complexity": "O(d·(n+k)) where d is number of digits, k is radix (usually 10).",
        "space_complexity": "O(n+k) for counting sort auxiliary arrays.",
        "strengths": [
            "Linear time for fixed-width integers.",
            "Stable and deterministic."
        ],
        "weaknesses": [
            "Requires fixed-width keys or padding.",
            "Not in-place; needs auxiliary space."
        ],
        "alternatives": ["Counting Sort", "Bucket Sort", "Quick Sort"],
        "explanation": "Sort digit by digit from right to left, using a stable sort at each position to maintain relative order."
    },
    "semester_01/lecture_11_dynamic_programming/longest_common_subsequence/README.md": {
        "name": "Longest Common Subsequence (LCS)",
        "problem": "Finds the longest sequence present in order (not necessarily contiguous) in two strings.",
        "intuition": "Walk both strings together; when characters match, include them, otherwise decide whether to drop a char from one string or the other via DP.",
        "inputs": "Strings s (length n) and t (length m).",
        "outputs": "Length of longest common subsequence (and optionally the subsequence).",
        "steps": [
            "Initialize DP table dp[n+1][m+1] to zero.",
            "For i=1..n: for j=1..m:",
            "  If s[i-1]==t[j-1], dp[i][j]=dp[i-1][j-1]+1.",
            "  Else dp[i][j]=max(dp[i-1][j], dp[i][j-1]).",
            "Backtrack from dp[n][m] to reconstruct the subsequence."
        ],
        "example": "s=\"ABCBDAB\", t=\"BDCABA\" → LCS length 4 (\"BCBA\").",
        "time_complexity": "O(n·m).",
        "space_complexity": "O(n·m) (can be reduced to O(min(n,m)) for length only).",
        "strengths": [
            "Foundation for diff tools and bioinformatics alignment.",
            "Provides similarity measure ignoring non-matching sections."
        ],
        "weaknesses": [
            "Quadratic runtime on string lengths.",
            "Reconstruction requires storing parent pointers or stack."
        ],
        "alternatives": ["Edit Distance", "Longest Common Substring", "Sequence Alignment"],
        "explanation": "Fills a DP grid where each cell stores the best LCS length up to those prefixes, ensuring optimal substructure reuse."
    },
    "semester_01/lecture_11_dynamic_programming/edit_distance/README.md": {
        "name": "Edit Distance (Levenshtein)",
        "problem": "Finds the minimum number of insertions, deletions, and substitutions to transform one string into another.",
        "intuition": "Compare strings letter by letter; when they diverge, decide whether to insert, delete, or substitute the mismatch with minimal total cost.",
        "inputs": "Two strings s and t (lengths n and m).",
        "outputs": "Minimum edit distance (number of operations) and optionally the edit script.",
        "steps": [
            "Initialize DP table dp[n+1][m+1]: dp[0][j]=j (insertions), dp[i][0]=i (deletions).",
            "For each i,j: if s[i-1]==t[j-1], dp[i][j]=dp[i-1][j-1].",
            "Otherwise dp[i][j] = 1 + min(dp[i-1][j] (delete), dp[i][j-1] (insert), dp[i-1][j-1] (substitute)).",
            "Answer is dp[n][m]; backtrack to recover edit script if needed."
        ],
        "example": "Transform \"cat\" → \"cut\": substitute 'a'→'u' (1 edit). DP table yields cost 1.",
        "time_complexity": "O(n·m).",
        "space_complexity": "O(n·m) or O(min(n,m)) with rolling array.",
        "strengths": [
            "Robust similarity metric for strings.",
            "Easily extended with custom costs."
        ],
        "weaknesses": [
            "Quadratic time for long strings.",
            "Memory heavy without optimizations."
        ],
        "alternatives": ["Hamming Distance", "Damerau-Levenshtein", "Longest Common Subsequence"],
        "explanation": "Dynamic programming over prefixes chooses the cheapest combination of insert/delete/substitute to align two strings."
    },
    "semester_01/lecture_11_dynamic_programming/fibonacci/README.md": {
        "name": "Dynamic Programming Fibonacci",
        "problem": "Computes nth Fibonacci number efficiently by caching results instead of using exponential recursion.",
        "intuition": "Store results of smaller fib values so each number is computed once; akin to filling a table bottom-up.",
        "inputs": "Integer n ≥ 0.",
        "outputs": "Fibonacci number F(n) where F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2).",
        "steps": [
            "Initialize dp[0]=0, dp[1]=1.",
            "For i=2 to n: dp[i] = dp[i-1] + dp[i-2].",
            "Optionally reduce to two variables for constant space.",
            "Return dp[n]."
        ],
        "example": "n=6 → sequence 0,1,1,2,3,5,8 → fib(6)=8.",
        "time_complexity": "O(n).",
        "space_complexity": "O(n) for table or O(1) with rolling values.",
        "strengths": [
            "Demonstrates memoization/bottom-up DP basics.",
            "Linear time versus exponential recursive approach."
        ],
        "weaknesses": [
            "Simple example; real problems may require more intricate states.",
            "Large n requires big integers or modulo arithmetic."
        ],
        "alternatives": ["Matrix Exponentiation", "Closed-form (Binet) Formula", "Fast Doubling Method"],
        "explanation": "Replace naive recursion with iterative accumulation while caching prior values so each Fibonacci number is computed exactly once."
    },
    "semester_03/lecture_12_ml_algorithms/decision_tree/README.md": {
        "name": "Decision Tree",
        "problem": "Builds a tree structure that makes decisions by splitting data on feature values to classify or predict outcomes.",
        "intuition": "Like a flowchart: ask yes/no questions about features, branch based on answers, and reach a conclusion at the leaves.",
        "inputs": "Training dataset with features and labels (classification) or target values (regression).",
        "outputs": "Tree model that can classify new instances or predict continuous values.",
        "steps": [
            "Start with root node containing all training data.",
            "For each node, find the best feature and threshold to split on (maximize information gain or minimize Gini impurity).",
            "Create child nodes for each split outcome.",
            "Recursively build subtrees until stopping criteria (max depth, min samples, pure nodes).",
            "Assign class label or value to leaf nodes based on majority class or mean value."
        ],
        "example": "Classify fruit: if color=red and size>5cm → apple; if color=yellow → banana; else → orange.",
        "time_complexity": "O(n·m·log n) for training, where n is samples and m is features.",
        "space_complexity": "O(n·m) for storing tree structure.",
        "strengths": [
            "Interpretable and easy to visualize.",
            "Handles non-linear relationships and feature interactions."
        ],
        "weaknesses": [
            "Prone to overfitting without regularization.",
            "Sensitive to small data changes (unstable)."
        ],
        "alternatives": ["Random Forest", "Gradient Boosting", "Neural Networks"],
        "explanation": "Recursively partition data by asking questions about features until reaching pure groups that can be labeled."
    },
    "semester_03/lecture_12_ml_algorithms/kmeans/README.md": {
        "name": "K-Means Clustering",
        "problem": "Partitions n data points into k clusters by minimizing within-cluster variance and maximizing between-cluster separation.",
        "intuition": "Place k centroids randomly, assign each point to the nearest centroid, move centroids to cluster centers, repeat until stable.",
        "inputs": "Dataset of n points with d features and desired number of clusters k.",
        "outputs": "k cluster centroids and assignment of each point to a cluster.",
        "steps": [
            "Initialize k centroids randomly or using k-means++.",
            "Assign each point to the nearest centroid (Euclidean distance).",
            "Update each centroid to the mean of points in its cluster.",
            "Repeat assignment and update steps until centroids converge or max iterations.",
            "Return final centroids and cluster assignments."
        ],
        "example": "Points: [(1,1), (1,2), (5,4), (6,5)], k=2 → clusters: {[(1,1),(1,2)], [(5,4),(6,5)]} with centroids (1,1.5) and (5.5,4.5).",
        "time_complexity": "O(n·k·d·i) where i is iterations, typically converges quickly.",
        "space_complexity": "O(n·d + k·d) for points and centroids.",
        "strengths": [
            "Simple and fast for large datasets.",
            "Works well with spherical, well-separated clusters."
        ],
        "weaknesses": [
            "Requires specifying k in advance.",
            "Sensitive to initialization and may converge to local optima."
        ],
        "alternatives": ["Hierarchical Clustering", "DBSCAN", "Gaussian Mixture Models"],
        "explanation": "Iteratively refine cluster centers by assigning points to nearest centroids and updating centroids to cluster means."
    },
    "semester_03/lecture_12_ml_algorithms/knn/README.md": {
        "name": "K-Nearest Neighbors (KNN)",
        "problem": "Classifies or predicts by finding k most similar training examples and using their labels or values.",
        "intuition": "Ask your k closest neighbors what they think; the majority vote or average becomes your answer.",
        "inputs": "Training dataset, query point, and parameter k (number of neighbors).",
        "outputs": "Class label (classification) or predicted value (regression) for the query point.",
        "steps": [
            "Compute distance from query point to all training points.",
            "Select k training points with smallest distances.",
            "For classification: return majority class among k neighbors.",
            "For regression: return mean (or weighted mean) of k neighbors' values.",
            "Optionally use distance-weighted voting for better accuracy."
        ],
        "example": "Classify point (3,4) with k=3: nearest neighbors are [(2,3)→A, (4,5)→A, (1,6)→B] → majority A → predict class A.",
        "time_complexity": "O(n·d) for each query, where n is training size and d is dimensions.",
        "space_complexity": "O(n·d) to store training data.",
        "strengths": [
            "Simple, non-parametric, and effective for non-linear problems.",
            "No training phase; learns from data lazily."
        ],
        "weaknesses": [
            "Slow prediction on large datasets.",
            "Sensitive to irrelevant features and curse of dimensionality."
        ],
        "alternatives": ["Decision Trees", "Support Vector Machines", "Neural Networks"],
        "explanation": "Find the k closest examples in feature space and use their outcomes to make a prediction for the new point."
    },
    "semester_03/lecture_12_ml_algorithms/linear_regression/README.md": {
        "name": "Linear Regression",
        "problem": "Fits a linear relationship between features and a continuous target variable to predict numeric outcomes.",
        "intuition": "Draw the best straight line through data points so predictions are as close as possible to actual values.",
        "inputs": "Training data with features X (n×m matrix) and target values y (n×1 vector).",
        "outputs": "Learned coefficients (weights) and intercept that define the linear model y = X·w + b.",
        "steps": [
            "Initialize weights w and bias b (often to zeros).",
            "Compute predictions: ŷ = X·w + b.",
            "Calculate loss (mean squared error): MSE = (1/n)Σ(y - ŷ)².",
            "Update weights using gradient descent: w = w - α·∇w(MSE), b = b - α·∇b(MSE).",
            "Repeat until convergence or max iterations."
        ],
        "example": "Predict house price from size: price = 50,000 + 200·size. House of 100m² → price = 70,000.",
        "time_complexity": "O(n·m·i) for gradient descent, O(m³) for closed-form solution, where i is iterations.",
        "space_complexity": "O(n·m) for data, O(m) for weights.",
        "strengths": [
            "Simple, interpretable, and fast to train.",
            "Works well when relationship is approximately linear."
        ],
        "weaknesses": [
            "Assumes linear relationship; fails on non-linear patterns.",
            "Sensitive to outliers and multicollinearity."
        ],
        "alternatives": ["Polynomial Regression", "Ridge/Lasso Regression", "Neural Networks"],
        "explanation": "Find the line that minimizes squared prediction errors by adjusting slope and intercept through optimization."
    },
    "semester_03/lecture_12_ml_algorithms/logistic_regression/README.md": {
        "name": "Logistic Regression",
        "problem": "Models probability of binary classification by fitting a sigmoid curve to map features to probabilities between 0 and 1.",
        "intuition": "Instead of a straight line, use an S-shaped curve that squashes predictions into probability values.",
        "inputs": "Training data with features X and binary labels y ∈ {0, 1}.",
        "outputs": "Learned coefficients that define probability P(y=1|x) = 1/(1 + e^(-w·x - b)).",
        "steps": [
            "Initialize weights w and bias b.",
            "Compute logits: z = X·w + b.",
            "Apply sigmoid: p = 1/(1 + e^(-z)) to get probabilities.",
            "Calculate cross-entropy loss: L = -Σ(y·log(p) + (1-y)·log(1-p)).",
            "Update weights via gradient descent on loss function.",
            "Repeat until convergence."
        ],
        "example": "Predict spam: if email contains 'free' and 'money', probability = 0.85 → classify as spam (threshold 0.5).",
        "time_complexity": "O(n·m·i) for gradient descent iterations.",
        "space_complexity": "O(n·m) for data, O(m) for weights.",
        "strengths": [
            "Provides probability estimates, not just classifications.",
            "Fast, interpretable, and works well for linearly separable data."
        ],
        "weaknesses": [
            "Assumes linear decision boundary in log-odds space.",
            "Requires feature scaling for stable convergence."
        ],
        "alternatives": ["Support Vector Machines", "Decision Trees", "Neural Networks"],
        "explanation": "Transform linear combination of features through sigmoid to output probabilities, then optimize to maximize likelihood of observed labels."
    },
    "semester_03/lecture_12_ml_algorithms/naive_bayes/README.md": {
        "name": "Naive Bayes",
        "problem": "Classifies instances using Bayes' theorem with the 'naive' assumption that features are conditionally independent given the class.",
        "intuition": "Calculate probability of each class given the features; pick the class with highest probability, assuming features don't influence each other.",
        "inputs": "Training data with features and class labels.",
        "outputs": "Learned prior probabilities P(class) and likelihoods P(feature|class) for classification.",
        "steps": [
            "Estimate prior probabilities: P(class) = count(class) / total_samples.",
            "For each feature and class, estimate likelihood: P(feature|class) from training data.",
            "For a new instance, compute posterior for each class: P(class|features) ∝ P(class) · Π P(feature_i|class).",
            "Select class with maximum posterior probability.",
            "Use Laplace smoothing to handle unseen feature values."
        ],
        "example": "Classify email: P(spam|'free','money') ∝ P(spam)·P('free'|spam)·P('money'|spam) vs P(ham|'free','money') → choose max.",
        "time_complexity": "O(n·m) for training, O(m·c) for prediction, where c is number of classes.",
        "space_complexity": "O(m·c) to store probability tables.",
        "strengths": [
            "Fast training and prediction, works well with high-dimensional data.",
            "Handles missing values and requires little data to estimate parameters."
        ],
        "weaknesses": [
            "Naive independence assumption is often violated in practice.",
            "Sensitive to irrelevant features."
        ],
        "alternatives": ["Logistic Regression", "Decision Trees", "Support Vector Machines"],
        "explanation": "Use Bayes' rule to flip conditional probabilities, multiply feature likelihoods (assuming independence), and pick the most probable class."
    },
    "semester_03/lecture_12_ml_algorithms/svm/README.md": {
        "name": "Support Vector Machine (SVM)",
        "problem": "Finds the optimal hyperplane that maximally separates classes by maximizing the margin between support vectors.",
        "intuition": "Draw the widest possible 'street' between classes; the boundary is the middle line, and support vectors are the closest points on each side.",
        "inputs": "Training data with features X and class labels y ∈ {-1, +1}.",
        "outputs": "Learned weights w and bias b defining the separating hyperplane w·x + b = 0.",
        "steps": [
            "Formulate optimization: minimize ||w||² subject to y_i(w·x_i + b) ≥ 1 for all points.",
            "Solve using quadratic programming or gradient descent on dual form.",
            "Identify support vectors (points on margin boundaries).",
            "Compute decision boundary from support vectors.",
            "For non-linear data, use kernel trick (RBF, polynomial) to map to higher dimensions."
        ],
        "example": "Separate two classes with maximum margin: hyperplane equidistant from closest points of each class.",
        "time_complexity": "O(n²·m) to O(n³) depending on solver, where n is samples and m is features.",
        "space_complexity": "O(n·m) for data, O(s) for support vectors where s << n typically.",
        "strengths": [
            "Effective in high-dimensional spaces and with clear margin of separation.",
            "Memory efficient (uses only support vectors)."
        ],
        "weaknesses": [
            "Does not perform well on large datasets or with overlapping classes.",
            "Requires careful kernel and parameter selection."
        ],
        "alternatives": ["Logistic Regression", "Neural Networks", "Random Forest"],
        "explanation": "Maximize the gap between classes by finding the hyperplane that is farthest from the nearest points of each class."
    }
}


def main():
    """Update entries with enhanced information."""
    print("Loading existing entries...")
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    entries = data.get("entries", [])
    
    # Create path to entry mapping
    entry_map = {e["path"]: e for e in entries}
    
    # Update entries with enhanced information
    updated_count = 0
    for path, enhanced_info in ENHANCED_ENTRIES.items():
        if path in entry_map:
            entry_map[path].update(enhanced_info)
            updated_count += 1
            print(f"Enhanced: {path}")
    
    # Save updated entries
    data["entries"] = list(entry_map.values())
    DATA_PATH.write_text(
        json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    
    print(f"\nEnhanced {updated_count} entries")
    print(f"Total entries: {len(data['entries'])}")


if __name__ == "__main__":
    main()

