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
    },
    "semester_02/lecture_10_architectural_patterns/clean_architecture/README.md": {
        "name": "Clean Architecture",
        "problem": "Separates enterprise business rules from delivery mechanisms so systems remain testable, maintainable, and technology-agnostic.",
        "intuition": "Organize code in concentric rings where inner layers know nothing about outer layers; dependencies always point inward.",
        "inputs": "Domain entities, use cases, interface adapters, and frameworks/external services.",
        "outputs": "Modular system where core logic can evolve independently from UI, databases, or frameworks.",
        "steps": [
            "Define entities (enterprise rules) at the center.",
            "Create use cases that orchestrate entities.",
            "Add interface adapters (controllers, presenters, gateways) to translate between formats.",
            "Place frameworks and drivers (UI, DB, external APIs) at the outer ring.",
            "Enforce dependency rule: source code dependencies point inward only."
        ],
        "example": "E-commerce app: inner ring handles order validation, middle ring defines place-order use case, outer ring wires HTTP controllers and database gateways.",
        "time_complexity": "Not applicable; architectural pattern.",
        "space_complexity": "Not applicable; organizational structure.",
        "strengths": [
            "Framework-independent core that survives technology churn.",
            "High testability due to isolated business rules."
        ],
        "weaknesses": [
            "Initial setup overhead and learning curve.",
            "Requires discipline to maintain boundary rules."
        ],
        "alternatives": ["Layered Architecture", "Hexagonal Architecture", "Onion Architecture"],
        "explanation": "Keep business logic at the center and surround it with adapters so changing UI or database layers never ripples into the core."
    },
    "semester_02/lecture_10_architectural_patterns/hexagonal/README.md": {
        "name": "Hexagonal (Ports and Adapters)",
        "problem": "Allows applications to run equally in different environments by decoupling the domain from external systems via ports and adapters.",
        "intuition": "Treat the application as a hexagon with ports on each side; adapters plug into ports to talk to the outer world.",
        "inputs": "Domain core, inbound ports for driving actions, outbound ports for driven interactions.",
        "outputs": "Adapters (HTTP, CLI, database, messaging) that plug in without changing core logic.",
        "steps": [
            "Define inbound ports (interfaces) representing use cases.",
            "Implement domain services that realize the ports.",
            "Declare outbound ports for infrastructure dependencies.",
            "Write adapters that implement outbound ports (DB gateways, API clients).",
            "Wire adapters to ports via dependency injection."
        ],
        "example": "Blog service: inbound port publish_post, adapters for REST controller and CLI; outbound port PostRepository with adapters for SQL or NoSQL stores.",
        "time_complexity": "Not applicable.",
        "space_complexity": "Not applicable.",
        "strengths": [
            "Easy to swap infrastructure without touching core.",
            "Supports automated testing by substituting adapters."
        ],
        "weaknesses": [
            "More interfaces and boilerplate.",
            "Requires careful dependency management."
        ],
        "alternatives": ["Clean Architecture", "Onion Architecture", "Layered Architecture"],
        "explanation": "Expose the application through abstract ports while adapters translate between the outside world and the domain core."
    },
    "semester_02/lecture_10_architectural_patterns/mvc/README.md": {
        "name": "Model-View-Controller (MVC)",
        "problem": "Separates domain state (model), user interface (view), and input handling (controller) to build maintainable GUIs and web apps.",
        "intuition": "Controller handles user input, updates the model, and selects a view; view renders model data back to the user.",
        "inputs": "User interactions routed through controllers, domain models storing data, view templates displaying data.",
        "outputs": "Rendered UI plus updated models reflecting user actions.",
        "steps": [
            "Controller receives user action (HTTP request, button click).",
            "Controller validates input and invokes model operations.",
            "Model updates state and notifies observers if needed.",
            "Controller selects a view and provides model data.",
            "View renders output to user."
        ],
        "example": "Todo app: controller handles /add request, model saves task, view renders updated list.",
        "time_complexity": "Depends on model operations; architectural pattern.",
        "space_complexity": "Depends on domain data.",
        "strengths": [
            "Clear separation of concerns improves testability.",
            "Multiple views can reuse the same models."
        ],
        "weaknesses": [
            "Controller and view coupling can grow complex in large apps.",
            "Not ideal for heavily event-driven UIs without additional patterns."
        ],
        "alternatives": ["MVVM", "MVP", "Clean Architecture"],
        "explanation": "Split application logic into model, view, and controller layers so UI changes do not leak into business logic."
    },
    "semester_02/lecture_10_architectural_patterns/mvvm/README.md": {
        "name": "Model-View-ViewModel (MVVM)",
        "problem": "Decouples UI rendering from presentation logic using data binding between views and view-models.",
        "intuition": "ViewModel exposes observable state; the view binds to it and updates automatically when data changes.",
        "inputs": "Model (domain data), ViewModel (presentation state + commands), View (UI components with bindings).",
        "outputs": "Responsive UI that reflects ViewModel changes without manual wiring.",
        "steps": [
            "Wrap models in ViewModel objects exposing observable properties.",
            "Define commands/actions in the ViewModel.",
            "Bind view controls to ViewModel properties and commands.",
            "Update ViewModel in response to user input; binding updates view automatically.",
            "Synchronize ViewModel changes back to models as needed."
        ],
        "example": "WPF app: ViewModel exposes ObservableCollection<Todo>, view binds ListBox.ItemsSource; adding an item updates UI instantly.",
        "time_complexity": "Depends on underlying model operations.",
        "space_complexity": "Depends on number of ViewModels and bindings.",
        "strengths": [
            "Great for data-binding frameworks (WPF, SwiftUI, Android).",
            "Facilitates unit testing of presentation logic."
        ],
        "weaknesses": [
            "Requires binding infrastructure; not ideal for simple UIs.",
            "Two-way binding can obscure data flow."
        ],
        "alternatives": ["MVC", "MVP", "Redux-style state management"],
        "explanation": "Expose presentation logic via observable ViewModels so UI updates automatically when data changes and vice versa."
    },
    "semester_02/lecture_10_behavioral_patterns/observer/README.md": {
        "name": "Observer Pattern",
        "problem": "Creates a one-to-many dependency so when one object changes state, all dependents are notified automatically.",
        "intuition": "Subject keeps a list of observers; when state changes, it broadcasts notifications to each observer.",
        "inputs": "Subject with observable state and observers that subscribe to updates.",
        "outputs": "Observers receive callbacks when the subject changes.",
        "steps": [
            "Define Subject interface with attach/detach/notify.",
            "Observers implement an update method.",
            "Subject maintains list of observers.",
            "When state changes, subject iterates observers and calls update.",
            "Observers react (e.g., refresh UI, trigger workflows)."
        ],
        "example": "GUI button (subject) notifies multiple listeners when clicked.",
        "time_complexity": "O(n) to notify n observers per event.",
        "space_complexity": "O(n) to store observers.",
        "strengths": [
            "Promotes loose coupling between subject and observers.",
            "Supports dynamic number of listeners."
        ],
        "weaknesses": [
            "Notification order is not guaranteed.",
            "Observers can cause cascading updates or memory leaks if not detached."
        ],
        "alternatives": ["Publish-Subscribe", "Mediator Pattern", "Event Bus"],
        "explanation": "Subjects expose subscription hooks so observers can register and automatically receive updates when state changes."
    },
    "semester_02/lecture_10_behavioral_patterns/strategy/README.md": {
        "name": "Strategy Pattern",
        "problem": "Defines a family of interchangeable algorithms so behavior can change at runtime without modifying clients.",
        "intuition": "Encapsulate algorithms behind a common interface; clients hold a reference and swap strategies as needed.",
        "inputs": "Context object that uses a Strategy interface implemented by concrete strategies.",
        "outputs": "Context delegates specific behavior (e.g., sorting, compression) to the selected strategy.",
        "steps": [
            "Define Strategy interface with a common operation.",
            "Implement concrete strategies for each algorithm variant.",
            "Context holds a strategy reference and forwards calls.",
            "Allow clients to set or change strategy at runtime.",
            "Optional: use dependency injection or configuration to pick strategy."
        ],
        "example": "Payment processor selects PayPalStrategy, CreditCardStrategy, or CryptoStrategy based on user choice.",
        "time_complexity": "Depends on concrete strategy implementation.",
        "space_complexity": "Depends on strategies stored; typically O(1) per context.",
        "strengths": [
            "Eliminates conditional logic for algorithm selection.",
            "Eases extension with new strategies."
        ],
        "weaknesses": [
            "More classes and objects to manage.",
            "Clients must understand strategy differences."
        ],
        "alternatives": ["State Pattern", "Template Method", "Policy Injection"],
        "explanation": "Package interchangeable behaviors as strategy objects and let the client choose which one to run."
    },
    "semester_02/lecture_11_repository_patterns/data_mapper/README.md": {
        "name": "Data Mapper",
        "problem": "Separates in-memory domain objects from database schemas by mapping between them, keeping models persistence-agnostic.",
        "intuition": "Mapper translates between domain entities and database rows/columns without letting entities know about SQL.",
        "inputs": "Domain entities, mapper classes, data source connections.",
        "outputs": "Persisted entities and hydrated objects returned from the database.",
        "steps": [
            "Define domain entities with pure business logic.",
            "Create mapper classes with CRUD operations.",
            "Mapper reads/writes using SQL or ORM but returns domain objects.",
            "Unit tests entities without touching the database.",
            "Swap out mappers to change storage technology."
        ],
        "example": "UserMapper inserts/updates rows in users table while returning User entities with behavior.",
        "time_complexity": "Depends on persistence operations (O(1) for indexed queries, etc.).",
        "space_complexity": "O(n) for entity caches or unit of work state.",
        "strengths": [
            "Keeps domain model persistence-agnostic.",
            "Supports richer domain logic than Active Record."
        ],
        "weaknesses": [
            "More boilerplate and mapping code.",
            "Harder to map complex object graphs without tooling."
        ],
        "alternatives": ["Repository Pattern", "Active Record", "Table Data Gateway"],
        "explanation": "Use dedicated mapper classes to translate between domain objects and database rows so business logic stays ignorant of SQL."
    },
    "semester_02/lecture_11_repository_patterns/repository/README.md": {
        "name": "Repository Pattern",
        "problem": "Provides a collection-like abstraction over data sources, hiding persistence details from domain logic.",
        "intuition": "Treat the repository like an in-memory collection; domain code queries repository without knowing about SQL or API calls.",
        "inputs": "Domain aggregates, repository interfaces, concrete implementations for specific data stores.",
        "outputs": "Retrieved aggregates/entities and persisted changes.",
        "steps": [
            "Define repository interface with query/command operations (e.g., find_by_id, save).",
            "Implement repository using ORM, SQL, or external API.",
            "Inject repository into services/use cases.",
            "Use unit of work or transactions to batch changes.",
            "Mock repository in tests to isolate domain logic."
        ],
        "example": "OrderRepository#find_pending returns aggregate root; service manipulates object and calls save.",
        "time_complexity": "Determined by underlying data store queries.",
        "space_complexity": "Depends on caching/unit of work implementation.",
        "strengths": [
            "Decouples domain from persistence technology.",
            "Centralizes data access logic."
        ],
        "weaknesses": [
            "Over-abstraction for simple CRUD apps.",
            "Complex queries may leak storage concepts back into domain."
        ],
        "alternatives": ["Data Mapper", "Active Record", "DAO"],
        "explanation": "Expose persistence operations through repository interfaces so domain code works with aggregates while storage remains hidden."
    },
    "semester_02/lecture_11_repository_patterns/unit_of_work/README.md": {
        "name": "Unit of Work",
        "problem": "Tracks changes to multiple business objects and coordinates a single transaction commit to ensure consistency.",
        "intuition": "Accumulate inserts/updates/deletes in memory, then write them as one atomic unit.",
        "inputs": "Tracked entities, change tracker, transaction boundary.",
        "outputs": "Persisted state or rolled-back transaction if errors occur.",
        "steps": [
            "Start a unit of work and attach entities.",
            "Track changes (new, dirty, removed) as domain logic runs.",
            "On commit, issue database commands in correct order within a transaction.",
            "On rollback, discard pending changes.",
            "Dispose unit of work at end of request."
        ],
        "example": "EF Core DbContext tracks entity states; SaveChanges commits them within a transaction.",
        "time_complexity": "Depends on number of tracked entities; typically O(n) to iterate changes.",
        "space_complexity": "O(n) to store entity state and pending commands.",
        "strengths": [
            "Ensures transactional consistency across repositories.",
            "Reduces database round-trips by batching writes."
        ],
        "weaknesses": [
            "Requires careful lifetime management to avoid stale state.",
            "Can consume memory if many entities are tracked."
        ],
        "alternatives": ["Explicit Transactions", "Command Pattern", "Saga Pattern"],
        "explanation": "Buffer database operations in memory and commit them together so partial failures do not leave inconsistent state."
    },
    "semester_02/lecture_12_concurrency_patterns/producer_consumer/README.md": {
        "name": "Producer-Consumer Pattern",
        "problem": "Coordinates multiple producers generating work items and consumers processing them while preventing race conditions.",
        "intuition": "Use a thread-safe queue or buffer; producers enqueue tasks, consumers dequeue and handle them.",
        "inputs": "Set of producer threads, consumer threads, shared buffer, synchronization primitives.",
        "outputs": "Processed tasks with controlled throughput.",
        "steps": [
            "Create bounded/unbounded thread-safe queue.",
            "Producers acquire lock (or use concurrent queue) and push items.",
            "If queue full, producers block or drop depending on policy.",
            "Consumers wait for items, then dequeue and process.",
            "Use condition variables/semaphores to signal availability."
        ],
        "example": "Web server thread pool: accept requests (producer), worker threads handle responses (consumers).",
        "time_complexity": "Each enqueue/dequeue typically O(1).",
        "space_complexity": "O(capacity) for buffer.",
        "strengths": [
            "Smooths load differences between producers and consumers.",
            "Simplifies synchronization via shared queue."
        ],
        "weaknesses": [
            "Requires careful tuning of buffer size.",
            "Potential for deadlock if signaling is incorrect."
        ],
        "alternatives": ["Actor Model", "Pipeline Pattern", "Reactive Streams"],
        "explanation": "Buffer work items in a synchronized queue so producers and consumers operate independently without data races."
    },
    "semester_02/lecture_12_concurrency_patterns/readers_writers/README.md": {
        "name": "Readers-Writers Problem",
        "problem": "Manages concurrent access to shared resources allowing many readers or one writer at a time.",
        "intuition": "Multiple readers can read simultaneously, but writers require exclusive access.",
        "inputs": "Shared resource, read-write lock or semaphore, reader and writer threads.",
        "outputs": "Safe concurrent operations without stale reads or write conflicts.",
        "steps": [
            "Maintain counters for active readers and waiting writers.",
            "Readers acquire shared lock if no writer active.",
            "Writers wait until readers finish, then acquire exclusive lock.",
            "After operation, release lock and signal waiting threads.",
            "Optionally prioritize writers to prevent starvation."
        ],
        "example": "Database cache accessed by many read queries but occasionally updated by writers.",
        "time_complexity": "Lock acquisition typically O(1); throughput depends on contention.",
        "space_complexity": "O(1) for counters and lock state.",
        "strengths": [
            "Improves read-heavy workloads by allowing parallel reads.",
            "Prevents race conditions on shared resources."
        ],
        "weaknesses": [
            "Complex to implement starvation-free policies.",
            "Still serialized for write-heavy workloads."
        ],
        "alternatives": ["Optimistic Concurrency Control", "Stamped Locks", "Copy-on-Write"],
        "explanation": "Use read-write synchronization primitives so multiple readers can proceed concurrently while writers get exclusive access."
    },
    "semester_02/lecture_12_concurrency_patterns/thread_pool/README.md": {
        "name": "Thread Pool",
        "problem": "Manages a reusable set of worker threads to execute many short-lived tasks without spawning new threads each time.",
        "intuition": "Keep a pool of threads waiting on a work queue; dispatch tasks to idle threads for execution.",
        "inputs": "Task queue, pool size, worker threads, synchronization primitives.",
        "outputs": "Completed tasks with controlled concurrency level.",
        "steps": [
            "Initialize pool with N worker threads.",
            "Workers wait for tasks on a blocking queue.",
            "Clients submit tasks to the queue.",
            "Worker picks up task, executes it, then waits for next task.",
            "Pool manages scaling, timeouts, and graceful shutdown."
        ],
        "example": "Java ExecutorService processes HTTP requests using a fixed thread pool.",
        "time_complexity": "Task dispatch O(1) amortized.",
        "space_complexity": "O(N + queue_size) for threads and pending tasks.",
        "strengths": [
            "Reduces overhead of thread creation/destruction.",
            "Controls resource usage by limiting concurrent threads."
        ],
        "weaknesses": [
            "Improper sizing can cause latency or resource waste.",
            "Tasks must be well-behaved (no blocking forever)."
        ],
        "alternatives": ["Event Loop", "Reactive Streams", "Fork/Join Framework"],
        "explanation": "Pre-create a set of worker threads that repeatedly fetch tasks from a queue, improving throughput and resource control."
    },
    "semester_03/lecture_10_graph_algorithms/bellman_ford/README.md": {
        "name": "Bellman-Ford",
        "problem": "Finds shortest paths from a source to all vertices in a weighted graph, even with negative edge weights (detects negative cycles).",
        "intuition": "Relax all edges repeatedly: after V-1 iterations, shortest paths are found; if another relaxation improves a distance, a negative cycle exists.",
        "inputs": "Weighted directed graph G(V,E), source vertex s, edge weights (may be negative).",
        "outputs": "Shortest distances from s to all vertices; optionally detects negative cycles.",
        "steps": [
            "Initialize distance array: dist[s]=0, others=∞.",
            "Relax all edges V-1 times: for each edge (u,v) with weight w, if dist[u]+w < dist[v], update dist[v]=dist[u]+w.",
            "After V-1 iterations, check for negative cycles: if any edge (u,v) still relaxes, negative cycle exists.",
            "Return distances (or report cycle if detected)."
        ],
        "example": "Graph: A→B(1), B→C(-2), C→A(1). After 3 iterations: dist[A]=0, dist[B]=1, dist[C]=-1. Cycle check: C→A relaxes → negative cycle detected.",
        "time_complexity": "O(V·E) for V-1 iterations over E edges.",
        "space_complexity": "O(V) for distance array.",
        "strengths": [
            "Handles negative edge weights (unlike Dijkstra).",
            "Detects negative cycles in the graph."
        ],
        "weaknesses": [
            "Slower than Dijkstra for positive weights (O(V·E) vs O(E log V)).",
            "Requires V-1 full passes over all edges."
        ],
        "alternatives": ["Dijkstra (positive weights)", "Floyd-Warshall (all pairs)", "SPFA (optimized variant)"],
        "explanation": "Repeatedly relaxes all edges V-1 times; if distances can still improve after that, a negative cycle exists."
    },
    "semester_03/lecture_10_graph_algorithms/bfs/README.md": {
        "name": "Breadth-First Search (BFS)",
        "problem": "Explores a graph level by level, visiting all neighbors before moving to the next depth, finding shortest unweighted paths.",
        "intuition": "Like ripples in water: start from source, visit all immediate neighbors first, then their neighbors, maintaining a queue of vertices to explore.",
        "inputs": "Graph G(V,E) (adjacency list or matrix), source vertex s.",
        "outputs": "Visited vertices in BFS order; distances/parents for shortest path reconstruction.",
        "steps": [
            "Initialize queue with source s, mark s as visited.",
            "While queue not empty: dequeue vertex u.",
            "For each unvisited neighbor v of u: mark v visited, set distance[v]=distance[u]+1, enqueue v.",
            "Continue until queue is empty."
        ],
        "example": "Graph: A-B-C, A-D. BFS from A: visit A (level 0), then B and D (level 1), then C (level 2).",
        "time_complexity": "O(V+E) for adjacency list, O(V²) for adjacency matrix.",
        "space_complexity": "O(V) for queue and visited array.",
        "strengths": [
            "Finds shortest unweighted paths efficiently.",
            "Guarantees level-order traversal."
        ],
        "weaknesses": [
            "Only works for unweighted graphs (use Dijkstra for weighted).",
            "Memory usage grows with graph breadth."
        ],
        "alternatives": ["DFS (depth-first)", "Dijkstra (weighted shortest paths)", "A* (heuristic search)"],
        "explanation": "Uses a queue to explore vertices level by level, ensuring shortest paths in unweighted graphs."
    },
    "semester_03/lecture_10_graph_algorithms/dfs/README.md": {
        "name": "Depth-First Search (DFS)",
        "problem": "Explores a graph by going as deep as possible along each branch before backtracking, useful for connectivity and cycle detection.",
        "intuition": "Like exploring a maze: go down one path as far as possible, mark where you've been, backtrack when stuck, then try another path.",
        "inputs": "Graph G(V,E) (adjacency list or matrix), starting vertex s (optional).",
        "outputs": "Visited vertices in DFS order; discovery/finish times; connected components; cycle detection.",
        "steps": [
            "Mark current vertex as visited.",
            "For each unvisited neighbor: recursively call DFS on that neighbor.",
            "After exploring all neighbors, mark vertex as finished (for timing).",
            "Backtrack to previous vertex."
        ],
        "example": "Graph: A-B-C, A-D. DFS from A: visit A, go to B, go to C (backtrack), backtrack to A, go to D.",
        "time_complexity": "O(V+E) for adjacency list, O(V²) for adjacency matrix.",
        "space_complexity": "O(V) for recursion stack and visited array.",
        "strengths": [
            "Low memory overhead (recursion stack).",
            "Natural for backtracking and tree/graph traversal."
        ],
        "weaknesses": [
            "May not find shortest paths (unlike BFS).",
            "Deep recursion can cause stack overflow for large graphs."
        ],
        "alternatives": ["BFS (level-order)", "Iterative DFS (explicit stack)", "Topological Sort (DAG)"],
        "explanation": "Recursively explores each branch fully before backtracking, useful for connectivity, cycles, and topological ordering."
    },
    "semester_03/lecture_10_graph_algorithms/dijkstra/README.md": {
        "name": "Dijkstra's Algorithm",
        "problem": "Finds shortest paths from a source to all vertices in a weighted graph with non-negative edge weights.",
        "intuition": "Greedily expands the closest unvisited vertex: maintain a priority queue of vertices by distance, always process the nearest one first.",
        "inputs": "Weighted graph G(V,E) with non-negative weights, source vertex s.",
        "outputs": "Shortest distances from s to all vertices; optionally the shortest path tree.",
        "steps": [
            "Initialize: dist[s]=0, others=∞, priority queue Q contains all vertices.",
            "While Q not empty: extract vertex u with minimum distance from Q.",
            "For each neighbor v of u: if dist[u]+weight(u,v) < dist[v], update dist[v] and decrease-key in Q.",
            "Mark u as processed, repeat until Q is empty."
        ],
        "example": "Graph: A→B(4), A→C(2), C→B(1), C→D(5), B→D(1). From A: dist[B]=3 (via C), dist[C]=2, dist[D]=4 (via C and B).",
        "time_complexity": "O((V+E) log V) with binary heap, O(V²) with array.",
        "space_complexity": "O(V) for distance array and priority queue.",
        "strengths": [
            "Efficient for single-source shortest paths with non-negative weights.",
            "Optimal for dense graphs with proper data structures."
        ],
        "weaknesses": [
            "Fails with negative edge weights (use Bellman-Ford).",
            "Requires priority queue for efficiency."
        ],
        "alternatives": ["Bellman-Ford (negative weights)", "Floyd-Warshall (all pairs)", "A* (heuristic)"],
        "explanation": "Greedily processes vertices in order of increasing distance from source, guaranteeing shortest paths when all weights are non-negative."
    },
    "semester_03/lecture_10_graph_algorithms/floyd_warshall/README.md": {
        "name": "Floyd-Warshall",
        "problem": "Finds shortest paths between all pairs of vertices in a weighted graph, handling negative weights (but not negative cycles).",
        "intuition": "Dynamic programming: for each intermediate vertex k, update shortest path between i and j by considering paths through k.",
        "inputs": "Weighted graph G(V,E) with V vertices, edge weights (may be negative, no negative cycles).",
        "outputs": "Matrix of shortest distances between all pairs; optionally the path reconstruction matrix.",
        "steps": [
            "Initialize dist[i][j] = weight(i,j) if edge exists, 0 if i==j, ∞ otherwise.",
            "For k from 1 to V: for each pair (i,j), set dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]).",
            "After all k, dist[i][j] contains shortest path from i to j.",
            "Optionally detect negative cycles: if any dist[i][i] < 0 after algorithm, negative cycle exists."
        ],
        "example": "Graph: A→B(1), B→C(2), A→C(5). After k=A,B,C: dist[A][C]=3 (via B), dist[A][B]=1, dist[B][C]=2.",
        "time_complexity": "O(V³) for three nested loops.",
        "space_complexity": "O(V²) for distance matrix.",
        "strengths": [
            "Finds all-pairs shortest paths in one pass.",
            "Handles negative weights (unlike Dijkstra)."
        ],
        "weaknesses": [
            "Cubic time complexity makes it slow for large graphs.",
            "Memory usage is O(V²) which can be prohibitive."
        ],
        "alternatives": ["Dijkstra (single-source, non-negative)", "Johnson's (all-pairs, sparse graphs)", "Bellman-Ford (single-source, negative)"],
        "explanation": "Uses dynamic programming to consider all possible intermediate vertices, building shortest paths incrementally for all pairs."
    },
    "semester_03/lecture_15_greedy_algorithms/activity_selection/README.md": {
        "name": "Activity Selection",
        "problem": "Selects the maximum number of non-overlapping activities from a set, where each activity has a start and finish time.",
        "intuition": "Greedily choose the activity that finishes earliest: it leaves the most time for remaining activities, maximizing total count.",
        "inputs": "List of activities, each with start_time and finish_time.",
        "outputs": "Maximum-size set of non-overlapping activities.",
        "steps": [
            "Sort activities by finish_time (ascending).",
            "Initialize selected = [first activity].",
            "For each remaining activity: if its start_time >= finish_time of last selected, add it to selected.",
            "Return selected set."
        ],
        "example": "Activities: (1,4), (3,5), (0,6), (5,7), (8,9). Sorted: (1,4), (3,5), (0,6), (5,7), (8,9). Selected: (1,4), (5,7), (8,9) = 3 activities.",
        "time_complexity": "O(n log n) for sorting, O(n) for selection = O(n log n) total.",
        "space_complexity": "O(n) for storing activities and result.",
        "strengths": [
            "Simple greedy approach with optimal solution.",
            "Efficient O(n log n) time complexity."
        ],
        "weaknesses": [
            "Assumes activities are sorted (or requires sorting).",
            "Only maximizes count, not total duration or value."
        ],
        "alternatives": ["Weighted Activity Selection (DP)", "Interval Scheduling (variants)", "Greedy with different criteria"],
        "explanation": "Greedily selects activities that finish earliest, leaving maximum time for future selections and guaranteeing optimal count."
    },
    "semester_03/lecture_15_greedy_algorithms/fractional_knapsack/README.md": {
        "name": "Fractional Knapsack",
        "problem": "Maximizes value in a knapsack of limited capacity by taking fractions of items (unlike 0/1 knapsack where items are indivisible).",
        "intuition": "Greedily take items with highest value-to-weight ratio first: fill knapsack with best items until capacity is exhausted, taking fractions if needed.",
        "inputs": "Items with weights and values, knapsack capacity W.",
        "outputs": "Maximum value achievable; optionally the fraction of each item taken.",
        "steps": [
            "Calculate value-to-weight ratio for each item.",
            "Sort items by ratio (descending).",
            "Initialize total_value = 0, remaining_capacity = W.",
            "For each item in sorted order: take as much as possible (full item or fraction) until capacity is full.",
            "Return total_value."
        ],
        "example": "Items: (weight=10, value=60), (weight=20, value=100), (weight=30, value=120). Ratios: 6, 5, 4. Capacity=50. Take all of item1 (10), all of item2 (20), 2/3 of item3 (20). Value = 60+100+80 = 240.",
        "time_complexity": "O(n log n) for sorting, O(n) for selection = O(n log n) total.",
        "space_complexity": "O(n) for storing items and ratios.",
        "strengths": [
            "Greedy approach yields optimal solution (unlike 0/1 knapsack).",
            "Efficient O(n log n) time complexity."
        ],
        "weaknesses": [
            "Only works when items can be divided (fractional).",
            "Real-world items are often indivisible (0/1 knapsack requires DP)."
        ],
        "alternatives": ["0/1 Knapsack (DP)", "Multiple Knapsack", "Bounded Knapsack"],
        "explanation": "Greedily selects items by value-to-weight ratio, taking full items when possible and fractions when capacity is limited, ensuring optimal value."
    },
    "semester_03/lecture_15_greedy_algorithms/huffman/README.md": {
        "name": "Huffman Coding",
        "problem": "Constructs an optimal prefix-free binary code for compressing data by assigning shorter codes to more frequent symbols.",
        "intuition": "Build a binary tree bottom-up: merge two least frequent symbols into a node, repeat until one tree remains; left edges=0, right edges=1.",
        "inputs": "Symbols with their frequencies (or probabilities).",
        "outputs": "Huffman tree and variable-length binary codes for each symbol.",
        "steps": [
            "Create a leaf node for each symbol with its frequency.",
            "Insert all nodes into a min-priority queue (by frequency).",
            "While queue has >1 node: extract two nodes with lowest frequencies, create internal node with sum frequency, insert back into queue.",
            "Remaining node is root of Huffman tree.",
            "Traverse tree to assign codes: left=0, right=1."
        ],
        "example": "Symbols: A(5), B(2), C(1), D(1). Merge C+D(2), then B+(C+D)(4), then A+(B+C+D)(9). Codes: A=0, B=10, C=110, D=111. Average bits: (5×1+2×2+1×3+1×3)/9 ≈ 1.67.",
        "time_complexity": "O(n log n) where n is number of symbols (priority queue operations).",
        "space_complexity": "O(n) for tree and code table.",
        "strengths": [
            "Optimal prefix-free code (minimizes expected code length).",
            "Widely used in compression (ZIP, JPEG, MP3)."
        ],
        "weaknesses": [
            "Requires frequency table (two-pass encoding).",
            "Not adaptive (fixed codes for entire message)."
        ],
        "alternatives": ["Arithmetic Coding", "Lempel-Ziv (LZ77/LZ78)", "Run-Length Encoding"],
        "explanation": "Builds a binary tree by repeatedly merging least frequent symbols, ensuring frequent symbols get short codes and minimizing total encoded length."
    },
    "semester_03/lecture_11_dynamic_programming/knapsack/README.md": {
        "name": "0/1 Knapsack",
        "problem": "Selects items with maximum total value without exceeding knapsack capacity, where each item can be taken at most once (0 or 1).",
        "intuition": "For each item, decide: take it (if capacity allows) or skip it. Use DP to cache results of subproblems (remaining capacity, remaining items).",
        "inputs": "Items with weights and values, knapsack capacity W, number of items n.",
        "outputs": "Maximum value achievable; optionally the set of items selected.",
        "steps": [
            "Create DP table dp[i][w] = max value using first i items with capacity w.",
            "Base case: dp[0][w] = 0 for all w (no items).",
            "For each item i and capacity w: dp[i][w] = max(dp[i-1][w], value[i] + dp[i-1][w-weight[i]]).",
            "First term: skip item i; second term: take item i (if weight[i] <= w).",
            "Answer is dp[n][W]; backtrack to recover selected items."
        ],
        "example": "Items: (w=1,v=1), (w=3,v=4), (w=4,v=5), (w=5,v=7). Capacity=7. DP yields max value=9 by taking items 2 and 3.",
        "time_complexity": "O(n·W) where n is items, W is capacity.",
        "space_complexity": "O(n·W) for table, or O(W) with space optimization.",
        "strengths": [
            "Optimal solution for 0/1 knapsack problem.",
            "Classic DP problem with many variations."
        ],
        "weaknesses": [
            "Pseudo-polynomial time (depends on W, not just n).",
            "Not efficient for very large capacities."
        ],
        "alternatives": ["Fractional Knapsack (greedy)", "Unbounded Knapsack", "Multiple Knapsack"],
        "explanation": "Dynamic programming builds optimal solution by considering each item and all possible remaining capacities, choosing whether to include the item."
    },
    "semester_03/lecture_13_integration_patterns/cqrs/README.md": {
        "name": "CQRS (Command Query Responsibility Segregation)",
        "problem": "Separates read and write operations into different models to optimize performance, scalability, and maintainability of data access.",
        "intuition": "Split your data model: commands (writes) use one model optimized for updates, queries (reads) use another optimized for fast retrieval.",
        "inputs": "Commands (write operations) and queries (read operations) on domain entities.",
        "outputs": "Separate read and write models with independent optimization strategies.",
        "steps": [
            "Define command model: optimized for validation, business rules, and writes.",
            "Define query model: denormalized, optimized for fast reads and reporting.",
            "Commands update write model and publish events.",
            "Event handlers update read model asynchronously.",
            "Queries read from optimized read model."
        ],
        "example": "E-commerce: Order command model stores normalized data; query model pre-aggregates order history, customer stats for dashboard.",
        "time_complexity": "Write: O(1) to O(log n) depending on model; Read: O(1) to O(log n) for optimized queries.",
        "space_complexity": "O(n) for write model + O(m) for read model (may be larger due to denormalization).",
        "strengths": [
            "Independent scaling of read/write workloads.",
            "Optimized models for each operation type."
        ],
        "weaknesses": [
            "Increased complexity (two models to maintain).",
            "Eventual consistency between read and write models."
        ],
        "alternatives": ["Traditional CRUD", "Event Sourcing", "Read Replicas"],
        "explanation": "Separates command (write) and query (read) responsibilities into distinct models, allowing independent optimization and scaling."
    },
    "semester_03/lecture_13_integration_patterns/event_sourcing/README.md": {
        "name": "Event Sourcing",
        "problem": "Stores all changes to application state as a sequence of events, enabling time travel, audit trails, and rebuilding state from events.",
        "intuition": "Instead of storing current state, store every event that happened: like a bank statement, you can replay events to reconstruct any point in time.",
        "inputs": "Domain events representing state changes (e.g., OrderCreated, PaymentReceived, ItemShipped).",
        "outputs": "Event store (append-only log) and reconstructed current state from events.",
        "steps": [
            "Capture all state changes as immutable events.",
            "Append events to event store (append-only log).",
            "Replay events to rebuild current state (projection).",
            "Optionally create multiple read models from events.",
            "Support event versioning and schema evolution."
        ],
        "example": "Order system: events [OrderCreated, ItemAdded, PaymentReceived, ItemShipped]. Replay to get current order state or historical view at any time.",
        "time_complexity": "Write: O(1) append; Read: O(n) to replay n events for state reconstruction.",
        "space_complexity": "O(n) for n events (grows over time; may need snapshots for performance).",
        "strengths": [
            "Complete audit trail and time travel capabilities.",
            "Natural fit for event-driven architectures."
        ],
        "weaknesses": [
            "Event store grows indefinitely (requires snapshots/archiving).",
            "Complexity in handling schema changes and event versioning."
        ],
        "alternatives": ["Traditional State Storage", "CQRS", "Change Data Capture (CDC)"],
        "explanation": "Stores state changes as immutable events in an append-only log, enabling state reconstruction, auditing, and temporal queries."
    },
    "semester_03/lecture_13_integration_patterns/message_queue/README.md": {
        "name": "Message Queue",
        "problem": "Decouples producers and consumers of messages, enabling asynchronous communication, load balancing, and reliable message delivery.",
        "intuition": "Like a post office: producers drop messages in a queue, consumers pick them up when ready, allowing independent scaling and fault tolerance.",
        "inputs": "Messages from producers, queue configuration (durability, priority, TTL).",
        "outputs": "Reliable message delivery to consumers with ordering and persistence guarantees.",
        "steps": [
            "Producer sends message to queue (with optional routing key/topic).",
            "Queue stores message (optionally persisted to disk).",
            "Consumer subscribes to queue and receives messages.",
            "Consumer processes message and sends acknowledgment.",
            "Queue removes acknowledged message; retries on failure."
        ],
        "example": "E-commerce: order service publishes OrderCreated to queue; inventory, payment, shipping services consume and process asynchronously.",
        "time_complexity": "Enqueue: O(1); Dequeue: O(1) to O(log n) depending on priority.",
        "space_complexity": "O(n) for n messages in queue (bounded by queue size limits).",
        "strengths": [
            "Decouples services and enables asynchronous processing.",
            "Provides reliability through persistence and retries."
        ],
        "weaknesses": [
            "Message ordering may be lost in distributed systems.",
            "Requires monitoring and dead letter queue handling."
        ],
        "alternatives": ["Direct RPC", "Event Streaming (Kafka)", "Pub/Sub"],
        "explanation": "Buffers messages between producers and consumers, enabling asynchronous, decoupled communication with reliability guarantees."
    },
    "semester_03/lecture_13_integration_patterns/publish_subscribe/README.md": {
        "name": "Publish-Subscribe (Pub/Sub)",
        "problem": "Enables one-to-many message distribution where publishers send messages to topics, and multiple subscribers receive copies independently.",
        "intuition": "Like a radio station: broadcaster (publisher) sends to a channel (topic), and all listeners (subscribers) tuned to that channel receive the message.",
        "inputs": "Messages published to topics, subscriber subscriptions to topics.",
        "outputs": "Message delivery to all subscribers of a topic.",
        "steps": [
            "Publisher sends message to a topic (not specific subscribers).",
            "Message broker routes message to all subscribers of that topic.",
            "Each subscriber receives independent copy of message.",
            "Subscribers process messages asynchronously.",
            "Broker handles delivery guarantees (at-least-once, exactly-once)."
        ],
        "example": "News system: publisher sends 'Breaking News' to 'news' topic; email service, SMS service, and push notification service all receive and process.",
        "time_complexity": "Publish: O(1) to O(s) where s is number of subscribers; Subscribe: O(1).",
        "space_complexity": "O(n·s) for n messages and s subscribers (each gets copy).",
        "strengths": [
            "Loose coupling between publishers and subscribers.",
            "Easy to add/remove subscribers without affecting publishers."
        ],
        "weaknesses": [
            "No direct feedback from subscribers to publishers.",
            "Message delivery guarantees vary by implementation."
        ],
        "alternatives": ["Message Queue (point-to-point)", "Event Streaming", "Observer Pattern"],
        "explanation": "Decouples publishers from subscribers through topics, enabling broadcast-style messaging where multiple subscribers receive the same message."
    },
    "semester_04/lecture_14_security_patterns/authentication/README.md": {
        "name": "Authentication",
        "problem": "Verifies the identity of users or systems attempting to access resources, ensuring only authorized entities can proceed.",
        "intuition": "Like showing ID at a checkpoint: prove who you are using credentials (password, token, biometric) before being allowed entry.",
        "inputs": "User credentials (username/password, tokens, certificates, biometrics).",
        "outputs": "Authentication result (success/failure) and session token or identity claim.",
        "steps": [
            "User provides credentials (e.g., username and password).",
            "System validates credentials against stored identity store.",
            "On success: generate session token or JWT, store session (if stateful).",
            "Return token to client for subsequent requests.",
            "On failure: return error, optionally implement rate limiting."
        ],
        "example": "Login flow: user enters username/password → server hashes password, compares with stored hash → if match, issue JWT token → client uses token for API calls.",
        "time_complexity": "O(1) for token validation; O(n) for credential lookup in database.",
        "space_complexity": "O(1) for token storage; O(n) for user credential database.",
        "strengths": [
            "Foundation of security: verifies identity before authorization.",
            "Multiple methods available (password, OAuth, certificates)."
        ],
        "weaknesses": [
            "Password-based auth vulnerable to breaches and phishing.",
            "Session management complexity (tokens, refresh, revocation)."
        ],
        "alternatives": ["OAuth 2.0", "SAML", "Certificate-based Authentication", "Biometric Authentication"],
        "explanation": "Verifies user identity through credentials, establishing trust before allowing access to protected resources."
    },
    "semester_04/lecture_14_security_patterns/authorization/README.md": {
        "name": "Authorization",
        "problem": "Determines what actions an authenticated user or system is permitted to perform on specific resources.",
        "intuition": "After authentication confirms who you are, authorization checks what you're allowed to do: like a bouncer checking if you have VIP access.",
        "inputs": "Authenticated user identity, requested action, target resource, access control policies.",
        "outputs": "Authorization decision (allow/deny) with optional reason.",
        "steps": [
            "Extract user identity and requested action from request.",
            "Retrieve user roles/permissions from identity store.",
            "Evaluate access control policies (RBAC, ABAC, ACL).",
            "Check if user has required permission for action on resource.",
            "Return allow or deny decision."
        ],
        "example": "User requests DELETE /api/users/123. System checks: user is admin? → allow. User is owner of user 123? → allow. Otherwise → deny.",
        "time_complexity": "O(1) to O(r) where r is number of roles/permissions to check.",
        "space_complexity": "O(u·p) for u users with p permissions each.",
        "strengths": [
            "Enforces least privilege principle.",
            "Flexible models: RBAC, ABAC, ACL support different needs."
        ],
        "weaknesses": [
            "Complex policy management in large systems.",
            "Performance overhead of permission checks on every request."
        ],
        "alternatives": ["Role-Based Access Control (RBAC)", "Attribute-Based Access Control (ABAC)", "Access Control Lists (ACL)"],
        "explanation": "Evaluates whether an authenticated user has permission to perform a specific action on a resource based on access control policies."
    },
    "semester_04/lecture_14_security_patterns/encryption/README.md": {
        "name": "Encryption",
        "problem": "Transforms readable data (plaintext) into unreadable form (ciphertext) to protect confidentiality, ensuring only authorized parties can decrypt.",
        "intuition": "Like a secret code: scramble data using a key so only those with the key can unscramble and read it.",
        "inputs": "Plaintext data, encryption key, encryption algorithm (symmetric or asymmetric).",
        "outputs": "Ciphertext (encrypted data) and optionally initialization vector (IV) or nonce.",
        "steps": [
            "Select encryption algorithm (AES, RSA, ChaCha20, etc.).",
            "Generate or use existing encryption key.",
            "For symmetric: use same key for encryption/decryption.",
            "For asymmetric: use public key to encrypt, private key to decrypt.",
            "Apply encryption algorithm to produce ciphertext.",
            "Store/transmit ciphertext; decrypt with corresponding key when needed."
        ],
        "example": "Encrypt 'Hello' with AES-256: plaintext → ciphertext 'a3f9b2c1...' using key. Decrypt with same key → 'Hello'.",
        "time_complexity": "Symmetric: O(n) for n bytes; Asymmetric: O(n·k) where k is key size.",
        "space_complexity": "O(n) for ciphertext (similar to plaintext size, plus IV/nonce overhead).",
        "strengths": [
            "Protects data confidentiality at rest and in transit.",
            "Industry-standard algorithms (AES, RSA) are well-tested."
        ],
        "weaknesses": [
            "Key management complexity (generation, storage, rotation).",
            "Performance overhead, especially for asymmetric encryption."
        ],
        "alternatives": ["Symmetric Encryption (AES)", "Asymmetric Encryption (RSA, ECC)", "Hybrid Encryption"],
        "explanation": "Converts plaintext to ciphertext using cryptographic algorithms and keys, ensuring data remains confidential and can only be read by authorized parties with the decryption key."
    },
    "semester_04/lecture_14_security_patterns/jwt/README.md": {
        "name": "JWT (JSON Web Token)",
        "problem": "Provides a compact, URL-safe token format for securely transmitting claims between parties, commonly used for stateless authentication and authorization.",
        "intuition": "Like a tamper-proof ticket: contains user info and permissions, signed so server can verify it wasn't altered, eliminating need to store sessions.",
        "inputs": "Header (algorithm, type), payload (claims like user ID, roles, expiration), secret key or private key.",
        "outputs": "JWT token string (header.payload.signature) in base64url encoding.",
        "steps": [
            "Create header: algorithm (HS256, RS256) and token type (JWT).",
            "Create payload: claims (iss, sub, exp, iat, custom claims).",
            "Base64url encode header and payload separately.",
            "Create signature: HMAC or RSA signature of encoded header + '.' + encoded payload.",
            "Combine: header.payload.signature.",
            "Client stores token, sends in Authorization header; server validates signature and claims."
        ],
        "example": "Token: eyJhbGc... (header).eyJzdWI... (payload: {sub: 'user123', exp: 1234567890}).SflKxwRJ... (signature). Server validates signature and checks expiration.",
        "time_complexity": "Generate: O(1); Validate: O(1) for signature verification.",
        "space_complexity": "O(1) for token size (typically 100-500 bytes).",
        "strengths": [
            "Stateless: no server-side session storage needed.",
            "Self-contained: includes all necessary claims."
        ],
        "weaknesses": [
            "Cannot revoke tokens before expiration (requires blacklist or short expiry).",
            "Larger than session IDs (sent with every request)."
        ],
        "alternatives": ["Session-based Authentication", "OAuth 2.0 Access Tokens", "SAML Assertions"],
        "explanation": "Encodes authentication/authorization claims as a signed JSON token, enabling stateless, scalable authentication without server-side session storage."
    },
    "semester_03/lecture_16_advanced_ml/gradient_descent/README.md": {
        "name": "Gradient Descent",
        "problem": "Optimizes differentiable objective functions by iteratively moving parameters in the direction of steepest descent to find a local minimum.",
        "intuition": "Imagine descending a foggy hill with only local slope information: step downhill proportional to the slope and step size (learning rate).",
        "inputs": "Objective function J(θ), gradient ∇J(θ), initial parameters θ₀, learning rate α, stopping criteria (iterations or tolerance).",
        "outputs": "Optimized parameter vector θ* approximating a (local) minimum of J.",
        "steps": [
            "Initialize parameters θ₀ (random or heuristic).",
            "Repeat until convergence: compute gradient g = ∇J(θ).",
            "Update parameters θ ← θ − α · g.",
            "Adapt learning rate or use schedules (optional).",
            "Stop when gradient norm < ε or iterations reach limit."
        ],
        "example": "Linear regression cost J(θ) = (1/2m) Σ (hθ(xᵢ) − yᵢ)². Gradient descent updates θ simultaneously until training error plateaus.",
        "time_complexity": "O(k · n · d) for k iterations on dataset of n samples with d features (full-batch).",
        "space_complexity": "O(d) for parameter vector; O(n·d) if full dataset kept in memory.",
        "strengths": [
            "Scales to high-dimensional problems with stochastic/mini-batch variants.",
            "Simple to implement and differentiable-model agnostic."
        ],
        "weaknesses": [
            "Sensitive to learning rate; may diverge or be slow.",
            "Gets trapped in local minima/saddle points on non-convex surfaces."
        ],
        "alternatives": ["Stochastic Gradient Descent", "Momentum/Nesterov", "Adam/Adaptive Optimizers"],
        "explanation": "Iteratively nudges parameters opposite the gradient so the objective decreases each step, converging toward minima when learning rate and convergence criteria are well tuned."
    },
    "semester_03/lecture_16_advanced_ml/neural_network/README.md": {
        "name": "Feedforward Neural Network",
        "problem": "Approximates complex non-linear mappings between inputs and outputs using layered compositions of linear transformations and activation functions.",
        "intuition": "Stack perceptrons: each layer learns increasingly abstract features, enabling the network to model intricate patterns beyond linear decision boundaries.",
        "inputs": "Training data (features X, labels y), network architecture (layers, neurons), activation functions, loss function, optimizer hyperparameters.",
        "outputs": "Trained network weights/biases capable of inference on unseen data; predicted outputs for inputs.",
        "steps": [
            "Define architecture: input layer, one or more hidden layers, output layer.",
            "Initialize weights/biases (Xavier/He random).",
            "Forward pass: compute activations layer by layer.",
            "Compute loss between predictions and targets.",
            "Backpropagate gradients via chain rule and update weights with optimizer."
        ],
        "example": "MNIST digit classifier: 784→128→64→10 network with ReLU activations and softmax output trained via cross-entropy loss.",
        "time_complexity": "O(k · Σ layer_multiplications) roughly O(k · n · Σ (d_{l-1}·d_l)) for k epochs over n samples.",
        "space_complexity": "O(Σ (d_{l-1}·d_l)) for weights plus activations stored during backprop.",
        "strengths": [
            "Universal function approximators with sufficient width/depth.",
            "Can learn hierarchical representations automatically."
        ],
        "weaknesses": [
            "Require large datasets and careful regularization to avoid overfitting.",
            "Training can be unstable (vanishing/exploding gradients)."
        ],
        "alternatives": ["Convolutional Neural Networks", "Recurrent Neural Networks", "Gradient Boosting Machines"],
        "explanation": "Layered neurons perform affine transformations followed by non-linear activations, and training adjusts weights via backpropagation to minimize loss on labeled data."
    },
    "semester_03/lecture_16_advanced_ml/random_forest/README.md": {
        "name": "Random Forest",
        "problem": "Ensemble of decision trees that reduces variance and improves predictive accuracy by averaging many decorrelated trees.",
        "intuition": "Like asking many diverse experts and averaging their answers: each tree sees bootstrap samples and random feature subsets, so their errors cancel out.",
        "inputs": "Training dataset with features/labels, number of trees (n_estimators), maximum depth, feature subsampling rate.",
        "outputs": "Ensemble model producing class probabilities (classification) or average predictions (regression).",
        "steps": [
            "For each tree: draw bootstrap sample of data.",
            "Grow decision tree to max depth or stopping criteria.",
            "At each split, consider random subset of features.",
            "Aggregate predictions of all trees (majority vote or mean).",
            "Evaluate out-of-bag error for validation (optional)."
        ],
        "example": "Predict loan default: train 300 trees with max depth 10, feature subsample √d; aggregate votes for final decision.",
        "time_complexity": "O(n_trees · n_samples · log n_samples) typically, depending on depth and feature count.",
        "space_complexity": "O(n_trees · tree_size) to store all nodes.",
        "strengths": [
            "Handles high-dimensional, mixed-type data with minimal preprocessing.",
            "Robust to overfitting compared to single trees; provides feature importance."
        ],
        "weaknesses": [
            "Large models consume memory and are slower at inference.",
            "Less interpretable than single trees; biased toward features with many levels."
        ],
        "alternatives": ["Gradient Boosted Trees", "Extra Trees", "Bagging with other base learners"],
        "explanation": "Builds many randomized decision trees on bootstrap samples and aggregates their outputs, reducing variance and improving generalization."
    },
    "semester_03/lecture_16_advanced_ml/svm/README.md": {
        "name": "Advanced Support Vector Machine",
        "problem": "Finds a maximum-margin hyperplane separating classes (or regression function) using kernel tricks to operate in high-dimensional feature spaces.",
        "intuition": "Transform data into a space where classes are linearly separable and place the widest possible margin between them while penalizing misclassifications.",
        "inputs": "Training data (features, labels), kernel choice (linear, RBF, polynomial), regularization parameter C, kernel-specific hyperparameters (γ, degree).",
        "outputs": "Support vectors, learned weights/bias (or dual coefficients), decision function for classification or regression.",
        "steps": [
            "Choose kernel and hyperparameters to map data into feature space.",
            "Formulate optimization problem maximizing margin with slack penalties.",
            "Solve quadratic programming problem (dual) to find support vectors.",
            "Compute decision boundary using support vectors and kernel evaluations.",
            "Tune hyperparameters via cross-validation; use model for inference."
        ],
        "example": "RBF-kernel SVM on non-linear spiral dataset: γ controls kernel width, C balances margin width vs. training errors; resulting boundary wraps around spirals.",
        "time_complexity": "Training O(n²) to O(n³) for n samples (QP solver); prediction O(n_sv · d_k) where n_sv is number of support vectors.",
        "space_complexity": "O(n_sv · d) to store support vectors and coefficients.",
        "strengths": [
            "Effective in high-dimensional spaces with clear margins.",
            "Kernel trick enables flexible non-linear boundaries."
        ],
        "weaknesses": [
            "Training scales poorly with large datasets.",
            "Requires careful kernel and hyperparameter tuning."
        ],
        "alternatives": ["Logistic Regression", "Random Forest", "Neural Networks/Deep Learning"],
        "explanation": "Maximizes the separation margin between classes and uses kernel functions to implicitly project data into feature spaces where linear separation is feasible."
    },
    "semester_04/lecture_15_testing_patterns/integration_testing/README.md": {
        "name": "Integration Testing",
        "problem": "Tests interactions between multiple components or systems to ensure they work together correctly as an integrated unit.",
        "intuition": "Like testing a car's engine and transmission together: individual parts may work, but integration testing verifies they function as a cohesive system.",
        "inputs": "Multiple components or services, test data, integration test scenarios.",
        "outputs": "Test results verifying component interactions, data flow, and system behavior.",
        "steps": [
            "Identify integration points between components.",
            "Set up test environment with all required components.",
            "Execute test scenarios that exercise component interactions.",
            "Verify data flows correctly between components.",
            "Check error handling and edge cases at boundaries.",
            "Validate end-to-end workflows."
        ],
        "example": "E-commerce: test order service integrates with payment service and inventory service; verify order creation triggers payment processing and inventory deduction.",
        "time_complexity": "O(n) where n is number of components and interactions tested.",
        "space_complexity": "O(n) for test environment setup and component state.",
        "strengths": [
            "Catches bugs in component interactions early.",
            "Validates real-world system behavior."
        ],
        "weaknesses": [
            "Slower and more complex than unit tests.",
            "Requires full test environment setup."
        ],
        "alternatives": ["Unit Testing", "End-to-End Testing", "Contract Testing"],
        "explanation": "Tests multiple components together to ensure they integrate correctly and work as a unified system."
    },
    "semester_04/lecture_15_testing_patterns/mocking/README.md": {
        "name": "Mocking",
        "problem": "Replaces real dependencies with fake implementations during testing to isolate the unit under test and control test behavior.",
        "intuition": "Like using a stunt double in movies: replace real actors (dependencies) with stand-ins (mocks) to test scenes (units) in isolation.",
        "inputs": "Unit under test, dependencies to mock, expected behaviors and return values.",
        "outputs": "Isolated unit tests with controlled dependency behavior.",
        "steps": [
            "Identify external dependencies (databases, APIs, services).",
            "Create mock objects that implement dependency interfaces.",
            "Configure mock behavior (return values, exceptions, call counts).",
            "Inject mocks into unit under test.",
            "Execute test and verify interactions with mocks.",
            "Assert expected calls and behaviors occurred."
        ],
        "example": "Test user service: mock database to return fake user data, mock email service to verify email sent, test user creation logic in isolation.",
        "time_complexity": "O(1) for mock setup and execution (faster than real dependencies).",
        "space_complexity": "O(1) for mock objects (minimal memory overhead).",
        "strengths": [
            "Enables fast, isolated unit testing.",
            "Removes dependency on external systems."
        ],
        "weaknesses": [
            "Mocks may not reflect real dependency behavior.",
            "Over-mocking can make tests brittle."
        ],
        "alternatives": ["Stubs", "Fakes", "Test Doubles", "Dependency Injection"],
        "explanation": "Uses fake implementations of dependencies to isolate units under test, enabling fast, controlled testing without external systems."
    },
    "semester_04/lecture_15_testing_patterns/tdd/README.md": {
        "name": "TDD (Test-Driven Development)",
        "problem": "Develops software by writing tests before implementation, ensuring code meets requirements and maintains high test coverage.",
        "intuition": "Write the test first (specification), then write code to pass it: like building a house by first drawing blueprints, then constructing to match.",
        "inputs": "Requirements, test cases, implementation code.",
        "outputs": "Working code with comprehensive test coverage and clear specifications.",
        "steps": [
            "Write a failing test for a small feature (Red phase).",
            "Write minimal code to make the test pass (Green phase).",
            "Refactor code while keeping tests green (Refactor phase).",
            "Repeat cycle for next feature.",
            "Maintain test suite as codebase grows."
        ],
        "example": "Feature: calculate discount. Write test expecting 10% discount → test fails → implement discount calculation → test passes → refactor if needed.",
        "time_complexity": "O(n) where n is number of features (each requires test + implementation).",
        "space_complexity": "O(n) for test code and implementation code.",
        "strengths": [
            "High test coverage and confidence in code.",
            "Clear requirements through executable tests."
        ],
        "weaknesses": [
            "Initial development may be slower.",
            "Requires discipline to maintain TDD cycle."
        ],
        "alternatives": ["BDD (Behavior-Driven Development)", "Test-After Development", "Property-Based Testing"],
        "explanation": "Develops code by first writing tests that define desired behavior, then implementing code to satisfy those tests, ensuring requirements are met."
    },
    "semester_04/lecture_15_testing_patterns/unit_testing/README.md": {
        "name": "Unit Testing",
        "problem": "Tests individual units of code (functions, methods, classes) in isolation to verify they behave correctly according to specifications.",
        "intuition": "Like testing each ingredient separately before cooking: verify each function works correctly before testing the whole recipe.",
        "inputs": "Unit of code (function/method), test inputs, expected outputs.",
        "outputs": "Test results indicating whether unit behaves correctly.",
        "steps": [
            "Identify unit to test (function, method, or class).",
            "Prepare test inputs and expected outputs.",
            "Execute unit with test inputs.",
            "Assert actual outputs match expected outputs.",
            "Test edge cases and error conditions.",
            "Verify unit works in isolation (mock dependencies)."
        ],
        "example": "Test calculateTotal function: input [1,2,3] → expected output 6 → assert result equals 6. Test with empty list, negative numbers, null input.",
        "time_complexity": "O(1) to O(n) depending on unit complexity (fast execution).",
        "space_complexity": "O(1) for test data (minimal memory usage).",
        "strengths": [
            "Fast execution and quick feedback.",
            "Isolates bugs to specific units."
        ],
        "weaknesses": [
            "Doesn't catch integration issues.",
            "Requires mocking external dependencies."
        ],
        "alternatives": ["Integration Testing", "System Testing", "End-to-End Testing"],
        "explanation": "Tests individual code units in isolation to verify correct behavior, providing fast feedback and early bug detection."
    },
    "semester_04/lecture_16_deployment_patterns/blue_green/README.md": {
        "name": "Blue-Green Deployment",
        "problem": "Deploys new version alongside current version, then switches traffic to new version, enabling zero-downtime deployments and instant rollback.",
        "intuition": "Like having two identical theaters: run show in blue theater, prepare new show in green theater, then switch audience to green when ready.",
        "inputs": "Current production environment (blue), new application version, traffic routing configuration.",
        "outputs": "Deployed new version with zero downtime and rollback capability.",
        "steps": [
            "Deploy new version to green environment (parallel to blue).",
            "Run smoke tests on green environment.",
            "Switch traffic routing from blue to green.",
            "Monitor green environment for issues.",
            "If problems detected, route traffic back to blue (instant rollback).",
            "Keep blue as backup or decommission after validation period."
        ],
        "example": "Deploy v2.0 to green servers while v1.0 runs on blue. Test green, then update load balancer to route traffic to green. If errors occur, revert to blue.",
        "time_complexity": "O(1) for traffic switch (instantaneous).",
        "space_complexity": "O(2n) for maintaining two full environments simultaneously.",
        "strengths": [
            "Zero-downtime deployments.",
            "Instant rollback capability."
        ],
        "weaknesses": [
            "Requires double infrastructure capacity.",
            "Database migration complexity."
        ],
        "alternatives": ["Canary Deployment", "Rolling Deployment", "Recreate Deployment"],
        "explanation": "Maintains two identical production environments (blue and green), deploying new version to one while the other serves traffic, then switching instantly."
    },
    "semester_04/lecture_16_deployment_patterns/canary/README.md": {
        "name": "Canary Deployment",
        "problem": "Gradually rolls out new version to a small subset of users, monitors for issues, then expands to full deployment if successful.",
        "intuition": "Like canaries in coal mines: test new version on small group first (canary), if safe, expand to everyone; if problems, stop and rollback.",
        "inputs": "New application version, traffic routing rules, monitoring tools, user segmentation.",
        "outputs": "Gradually deployed new version with risk mitigation and monitoring.",
        "steps": [
            "Deploy new version alongside current version.",
            "Route small percentage of traffic (e.g., 5%) to new version.",
            "Monitor metrics (error rates, latency, business metrics).",
            "If metrics acceptable, gradually increase traffic percentage (10%, 25%, 50%, 100%).",
            "If issues detected, route traffic back to old version.",
            "Complete rollout or rollback based on monitoring."
        ],
        "example": "Deploy v2.0, route 5% of users to it. Monitor: if error rate < 1%, increase to 25%, then 50%, then 100%. If errors spike, revert to v1.0.",
        "time_complexity": "O(n) where n is number of rollout stages (gradual process).",
        "space_complexity": "O(n) for maintaining both versions during transition.",
        "strengths": [
            "Low-risk gradual rollout.",
            "Early detection of issues with minimal impact."
        ],
        "weaknesses": [
            "Requires traffic routing infrastructure.",
            "Slower than blue-green deployment."
        ],
        "alternatives": ["Blue-Green Deployment", "Rolling Deployment", "Feature Flags"],
        "explanation": "Gradually exposes new version to increasing traffic percentages while monitoring for issues, enabling safe, risk-mitigated deployments."
    },
    "semester_04/lecture_16_deployment_patterns/circuit_breaker/README.md": {
        "name": "Circuit Breaker",
        "problem": "Prevents cascading failures by detecting service failures and temporarily stopping requests to failing services, allowing recovery time.",
        "intuition": "Like electrical circuit breakers: when a circuit (service) fails repeatedly, trip the breaker to stop current (requests) and prevent damage (cascading failures).",
        "inputs": "Service calls, failure thresholds, timeout configurations.",
        "outputs": "Circuit state (closed, open, half-open) and request handling decisions.",
        "steps": [
            "Monitor service call failures and response times.",
            "If failure count exceeds threshold, open circuit (stop requests).",
            "Return fallback response or error immediately (fast failure).",
            "After timeout period, transition to half-open state.",
            "Allow test request through; if successful, close circuit; if fails, reopen.",
            "Continue monitoring and adjusting circuit state."
        ],
        "example": "Payment service fails 5 times in 10 seconds → circuit opens → subsequent requests fail fast with fallback → after 30s, test request → if succeeds, close circuit.",
        "time_complexity": "O(1) for circuit state check and request handling.",
        "space_complexity": "O(1) for circuit state storage (minimal overhead).",
        "strengths": [
            "Prevents cascading failures and resource exhaustion.",
            "Fast failure improves user experience."
        ],
        "weaknesses": [
            "Requires fallback strategies.",
            "May delay recovery if timeout too long."
        ],
        "alternatives": ["Retry Pattern", "Bulkhead Pattern", "Timeout Pattern"],
        "explanation": "Detects service failures and temporarily stops requests to failing services, preventing cascading failures and allowing time for recovery."
    },
    "semester_04/lecture_16_deployment_patterns/retry_pattern/README.md": {
        "name": "Retry Pattern",
        "problem": "Automatically retries failed operations with exponential backoff to handle transient failures and improve system reliability.",
        "intuition": "Like retrying a phone call: if it fails, wait a bit longer each time before trying again, giving the system time to recover from temporary issues.",
        "inputs": "Operation to retry, retry policy (max attempts, backoff strategy), failure conditions.",
        "outputs": "Successful operation result or final failure after retries exhausted.",
        "steps": [
            "Execute operation (API call, database query, etc.).",
            "If operation fails with retryable error, wait (exponential backoff).",
            "Retry operation up to maximum attempts.",
            "If all retries fail, return error or fallback.",
            "If operation succeeds, return result immediately.",
            "Optionally log retry attempts for monitoring."
        ],
        "example": "API call fails with 503 error → wait 1s → retry → fails → wait 2s → retry → fails → wait 4s → retry → succeeds. Total: 3 retries, 7s elapsed.",
        "time_complexity": "O(k) where k is number of retry attempts (depends on backoff strategy).",
        "space_complexity": "O(1) for retry state (minimal memory).",
        "strengths": [
            "Handles transient failures automatically.",
            "Improves system resilience and user experience."
        ],
        "weaknesses": [
            "May delay failure detection for permanent errors.",
            "Can increase load on failing services."
        ],
        "alternatives": ["Circuit Breaker", "Exponential Backoff", "Jittered Retry"],
        "explanation": "Automatically retries failed operations with increasing delays between attempts, handling transient failures and improving system reliability."
    },
    "semester_04/lecture_17_performance/caching/README.md": {
        "name": "Caching",
        "problem": "Stores frequently accessed data in fast storage to reduce latency and load on primary data sources, improving application performance.",
        "intuition": "Like keeping frequently used items on your desk: instead of going to storage (database) every time, grab from desk (cache) for instant access.",
        "inputs": "Data to cache, cache key, TTL (time-to-live), cache eviction policy.",
        "outputs": "Cached data with fast retrieval and reduced load on primary sources.",
        "steps": [
            "Check cache for requested data using key.",
            "If cache hit: return cached data immediately.",
            "If cache miss: fetch from primary source (database, API).",
            "Store fetched data in cache with TTL.",
            "Return data to caller.",
            "Evict expired or least-recently-used entries when cache full."
        ],
        "example": "User requests product info → check cache for product:123 → miss → fetch from database → store in cache (TTL 1 hour) → return. Next request hits cache instantly.",
        "time_complexity": "O(1) for cache lookup (hash table); O(n) for primary source fetch.",
        "space_complexity": "O(n) for cached data (bounded by cache size limit).",
        "strengths": [
            "Dramatically reduces latency for frequently accessed data.",
            "Reduces load on primary data sources."
        ],
        "weaknesses": [
            "Cache invalidation complexity.",
            "Memory overhead for cached data."
        ],
        "alternatives": ["CDN", "Database Query Optimization", "In-Memory Databases"],
        "explanation": "Stores frequently accessed data in fast storage (memory) to enable instant retrieval and reduce load on slower primary data sources."
    },
    "semester_04/lecture_17_performance/load_balancing/README.md": {
        "name": "Load Balancing",
        "problem": "Distributes incoming requests across multiple servers to optimize resource utilization, maximize throughput, and ensure high availability.",
        "intuition": "Like a restaurant host: when multiple tables (servers) are available, distribute customers (requests) evenly so no table is overloaded while others sit idle.",
        "inputs": "Incoming requests, pool of backend servers, load balancing algorithm.",
        "outputs": "Requests routed to appropriate servers with balanced load distribution.",
        "steps": [
            "Receive incoming request at load balancer.",
            "Select server using algorithm (round-robin, least connections, weighted, etc.).",
            "Route request to selected server.",
            "Monitor server health and response times.",
            "Remove unhealthy servers from pool.",
            "Re-add servers when they recover."
        ],
        "example": "3 servers: A, B, C. Requests 1,2,3 → round-robin routes to A,B,C. Request 4 → routes to A again. If B fails, route only to A and C.",
        "time_complexity": "O(1) to O(log n) for server selection depending on algorithm.",
        "space_complexity": "O(n) for server pool and health status tracking.",
        "strengths": [
            "Improves throughput and resource utilization.",
            "Provides high availability through redundancy."
        ],
        "weaknesses": [
            "Requires session affinity for stateful applications.",
            "Adds latency and complexity."
        ],
        "alternatives": ["DNS Load Balancing", "Client-Side Load Balancing", "Service Mesh"],
        "explanation": "Distributes incoming requests across multiple servers using algorithms to balance load, optimize performance, and ensure high availability."
    },
    "semester_04/lecture_17_performance/rate_limiting/README.md": {
        "name": "Rate Limiting",
        "problem": "Controls the rate of requests from clients to prevent abuse, ensure fair resource usage, and protect services from overload.",
        "intuition": "Like a bouncer at a club: limit how many people (requests) can enter per hour to prevent overcrowding and ensure everyone gets served.",
        "inputs": "Client requests, rate limit rules (requests per time window), client identifier.",
        "outputs": "Allowed requests or rate limit exceeded errors (429).",
        "steps": [
            "Identify client (IP address, API key, user ID).",
            "Check current request count for client in time window.",
            "If under limit: allow request and increment counter.",
            "If at limit: reject request with 429 (Too Many Requests) error.",
            "Reset counters when time window expires.",
            "Optionally implement different limits per client tier."
        ],
        "example": "API limit: 100 requests/hour per API key. Key 'abc123' makes 50 requests → allowed. Makes 60 more → 110 total → 51st request in hour returns 429 error.",
        "time_complexity": "O(1) for limit check (hash table lookup and counter increment).",
        "space_complexity": "O(n) for n unique clients (counter storage per client).",
        "strengths": [
            "Prevents abuse and ensures fair resource allocation.",
            "Protects services from overload and DDoS attacks."
        ],
        "weaknesses": [
            "May block legitimate users during traffic spikes.",
            "Requires distributed state for multi-server deployments."
        ],
        "alternatives": ["Throttling", "Quotas", "Token Bucket Algorithm"],
        "explanation": "Limits the number of requests a client can make within a time window, preventing abuse and ensuring fair resource usage across all clients."
    },
    "semester_04/lecture_18_crypto_algorithms/aes/README.md": {
        "name": "Advanced Encryption Standard (AES)",
        "problem": "Provides fast, secure symmetric-key encryption for protecting data at rest and in transit across modern systems.",
        "intuition": "Encrypt data by repeatedly applying substitution and permutation rounds that mix bytes and columns so ciphertext appears random without the key.",
        "inputs": "Plaintext block (128 bits), secret key (128/192/256 bits), mode of operation (CBC, GCM, CTR), optional IV/nonce.",
        "outputs": "Ciphertext block (128 bits) or full encrypted message with authentication tag for AEAD modes.",
        "steps": [
            "Expand secret key into round keys via key schedule.",
            "Initial AddRoundKey: XOR plaintext with first round key.",
            "For Nr-1 rounds: SubBytes, ShiftRows, MixColumns, AddRoundKey.",
            "Final round omits MixColumns.",
            "For modes like CBC/GCM, combine block cipher with chaining/nonce logic.",
            "Decrypt by applying inverse operations with round keys in reverse."
        ],
        "example": "AES-256-GCM encrypting API payload: generate random 96-bit nonce, encrypt plaintext with key, produce ciphertext and 128-bit auth tag stored alongside nonce.",
        "time_complexity": "O(N · Nr) where N is number of 128-bit blocks and Nr is 10/12/14 rounds depending on key size.",
        "space_complexity": "O(1) beyond key schedule (≈240 bytes for AES-256).",
        "strengths": [
            "NIST-standardized, hardware accelerated (AES-NI).",
            "Supports authenticated encryption (GCM, CCM)."
        ],
        "weaknesses": [
            "Symmetric key distribution required.",
            "Implementation must protect against side-channel leaks."
        ],
        "alternatives": ["ChaCha20-Poly1305", "Camellia", "Twofish"],
        "explanation": "Uses repeated substitution-permutation rounds keyed by a shared secret to scramble data into ciphertext resistant to cryptanalysis."
    },
    "semester_04/lecture_18_crypto_algorithms/bcrypt/README.md": {
        "name": "bcrypt Password Hashing",
        "problem": "Derives computationally expensive password hashes that resist brute-force and rainbow-table attacks for stored credentials.",
        "intuition": "Combine salt with password and run an intentionally slow, memory-hard key setup (EksBlowfish) so attackers must spend significant effort per guess.",
        "inputs": "Password string, cost factor (log2 rounds), 128-bit salt.",
        "outputs": "60-character hash string containing version, cost, salt, and checksum.",
        "steps": [
            "Generate random salt for each password.",
            "Run EksBlowfishSetup with password and salt cost times (2^cost iterations).",
            "Encrypt fixed text \"OrpheanBeholderScryDoubt\" 64 times with derived state.",
            "Format output $2b$<cost>$<22-char-salt><31-char-hash>.",
            "Verification: repeat process with same salt/cost and compare hashes."
        ],
        "example": "Cost=12: hashing password \"Sup3rSecret!\" takes ~300 ms; stored hash includes salt so each account uses unique work factor.",
        "time_complexity": "O(2^cost) per hash; raising cost doubles runtime.",
        "space_complexity": "O(1) (minimal memory aside from small Blowfish state).",
        "strengths": [
            "Salted and adaptive: increase cost as hardware improves.",
            "Widely implemented in language runtimes."
        ],
        "weaknesses": [
            "Limited to passwords ≤72 bytes.",
            "Blowfish-based design lacks modern memory hardness (see Argon2)."
        ],
        "alternatives": ["Argon2id", "scrypt", "PBKDF2"],
        "explanation": "Applies an expensive Blowfish key schedule with per-user salt so each password check consumes significant CPU, deterring offline cracking."
    },
    "semester_04/lecture_18_crypto_algorithms/rsa/README.md": {
        "name": "RSA Public-Key Cryptography",
        "problem": "Enables secure key exchange, encryption, and digital signatures using asymmetric key pairs derived from large primes.",
        "intuition": "Multiplying large primes is easy but factoring their product is hard; leverage modular exponentiation with public/private exponents for encryption/signing.",
        "inputs": "Public modulus n=p·q, public exponent e, private exponent d, message m (properly padded).",
        "outputs": "Ciphertext c = m^e mod n for encryption; signature s = m^d mod n for signing.",
        "steps": [
            "Key generation: choose random primes p,q; compute n=p·q and φ(n).",
            "Select public exponent e (commonly 65537) coprime to φ(n).",
            "Compute private exponent d ≡ e^{-1} mod φ(n).",
            "Encryption: apply modular exponentiation with e; decryption uses d.",
            "Always wrap messages with padding (OAEP for encryption, PSS for signatures).",
            "Validate signatures by raising s^e mod n and comparing to hashed message."
        ],
        "example": "TLS handshake: client verifies server certificate by checking RSA-PSS signature signed with CA's private key.",
        "time_complexity": "Modular exponentiation O(log e · log^2 n) using square-and-multiply; key generation involves probabilistic primality tests.",
        "space_complexity": "O(|n|) to store modulus and exponents (2048+ bits).",
        "strengths": [
            "Mature ecosystem and interoperability.",
            "Enables asymmetric trust models (certificates)."
        ],
        "weaknesses": [
            "Slow compared to symmetric crypto; large key sizes.",
            "Padding/oracle attacks if implemented incorrectly."
        ],
        "alternatives": ["Elliptic Curve Cryptography (ECDSA/ECDH)", "Diffie-Hellman", "Ed25519"],
        "explanation": "Relies on the hardness of factoring a large composite number, using paired exponents for encryption/decryption or signing/verification."
    },
    "semester_04/lecture_18_crypto_algorithms/sha256/README.md": {
        "name": "SHA-256 Hash Function",
        "problem": "Computes fixed-length digests for arbitrary data, enabling integrity checks, digital signatures, and proof-of-work schemes.",
        "intuition": "Process data in 512-bit chunks through nonlinear bit-wise operations (Ch, Maj, Σ) so small input changes avalanche into unrelated 256-bit outputs.",
        "inputs": "Message of arbitrary length, processed as 512-bit blocks after padding.",
        "outputs": "256-bit (32-byte) hash value.",
        "steps": [
            "Pad message with 1-bit, zeros, and 64-bit length to multiple of 512 bits.",
            "Initialize 8 working variables with SHA-256 constants.",
            "For each block: extend 16 words to 64 via schedule; iterate 64 rounds mixing message schedule with constants.",
            "Update hash state by adding working variables modulo 2^32.",
            "Concatenate final 8 words to produce 256-bit digest."
        ],
        "example": "\"hello\" → SHA-256 = 2cf24d...; widely used to verify file downloads and Bitcoin block headers.",
        "time_complexity": "O(n) where n is number of 512-bit blocks.",
        "space_complexity": "O(1) (small state of 8×32-bit words plus schedule).",
        "strengths": [
            "Collision resistant (no known practical attacks).",
            "Deterministic with uniform output distribution."
        ],
        "weaknesses": [
            "Not suitable for password storage (too fast).",
            "Vulnerable to length-extension attacks without proper construction."
        ],
        "alternatives": ["SHA-3", "BLAKE3", "SHA-512/256"],
        "explanation": "Iterative compression function that mixes message words with constants and bitwise operations to produce a 256-bit digest resistant to preimage/collision attacks."
    },
    "semester_04/lecture_19_distributed_patterns/consistent_hashing/README.md": {
        "name": "Consistent Hashing",
        "problem": "Distributes keys across dynamic clusters so adding/removing nodes only remaps a small fraction of keys, enabling scalable caches and storage rings.",
        "intuition": "Hash both nodes and keys onto a ring; each key goes to the next clockwise node, so membership changes affect only neighboring intervals.",
        "inputs": "Set of server nodes, hash function, replication factor, key identifiers.",
        "outputs": "Deterministic mapping from keys to nodes (and replicas).",
        "steps": [
            "Hash each node (optionally multiple virtual nodes) onto 0..2^m ring.",
            "Hash each key onto same ring.",
            "Assign key to first node clockwise from key hash.",
            "Replicate by selecting subsequent clockwise nodes.",
            "When node joins/leaves, reassign only keys in affected ranges.",
            "Rebalance by adjusting virtual node count per server."
        ],
        "example": "Distributed cache (Amazon Dynamo): each cache server owns ring intervals; adding a node only migrates ~1/n of keys.",
        "time_complexity": "Lookup O(log n) using balanced tree of node positions; O(1) with jump hash approximations.",
        "space_complexity": "O(n · v) for n nodes with v virtual replicas stored in ring map.",
        "strengths": [
            "Minimal key reshuffling on node churn.",
            "Supports heterogenous node capacity via virtual nodes."
        ],
        "weaknesses": [
            "Requires uniform hash distribution; hotspots possible.",
            "Rebalancing metadata adds operational complexity."
        ],
        "alternatives": ["Jump Consistent Hash", "Rendezvous Hashing", "Modulo Hashing"],
        "explanation": "Places nodes and keys on the same hash ring so keys map to nearest clockwise node, limiting the amount of data moved during topology changes."
    },
    "semester_04/lecture_19_distributed_patterns/gossip_protocol/README.md": {
        "name": "Gossip Protocol",
        "problem": "Disseminates state information in large-scale distributed systems using epidemic-style message spreading for scalability and fault tolerance.",
        "intuition": "Like rumors spreading: each node periodically contacts random peers to exchange updates, so information eventually reaches everyone without central coordination.",
        "inputs": "Cluster of nodes, heartbeat/state data, gossip interval, fan-out (number of peers per round).",
        "outputs": "Eventual consistency of membership or state across nodes.",
        "steps": [
            "Each node maintains local state (heartbeats, version vectors).",
            "On each tick, select k random peers.",
            "Send local state digests; peers reconcile by merging newer entries.",
            "Update detection timers to suspect failed nodes lacking fresh heartbeats.",
            "Propagate membership changes (join/leave/fail) via subsequent gossip rounds.",
            "Tune fan-out and interval to balance convergence speed and bandwidth."
        ],
        "example": "Amazon Dynamo-style membership: every 1s, node gossips to 3 peers; failure detected after missing N heartbeats across multiple peers.",
        "time_complexity": "Each round O(k) messages per node; convergence typically O(log n) rounds to reach all nodes.",
        "space_complexity": "O(n) per node to track membership metadata.",
        "strengths": [
            "Highly fault-tolerant and decentralized.",
            "Scales to thousands of nodes with bounded load."
        ],
        "weaknesses": [
            "Only eventually consistent; temporary disagreement possible.",
            "Bandwidth usage grows with state size."
        ],
        "alternatives": ["Centralized Membership Service", "Raft/Consensus-based registries", "Multicast/Broadcast protocols"],
        "explanation": "Nodes periodically exchange membership/state updates with random peers, allowing information to percolate through the cluster without a coordinator."
    },
    "semester_04/lecture_19_distributed_patterns/leader_election/README.md": {
        "name": "Leader Election",
        "problem": "Selects a single coordinator among distributed nodes to serialize actions (e.g., lock management, replication control).",
        "intuition": "Nodes compete based on priorities (IDs, timestamps); the \"highest\" remaining alive becomes leader and others defer until failure triggers a new election.",
        "inputs": "Cluster membership, node identifiers/priorities, communication channel (message passing).",
        "outputs": "Identity of the current leader and election status.",
        "steps": [
            "Detect need for election (startup or leader failure).",
            "Each candidate broadcasts election message to higher-priority nodes.",
            "If no higher node responds, candidate declares leadership.",
            "Leader announces victory; others acknowledge and follow.",
            "Monitor leader heartbeats; on timeout, restart election.",
            "Persist leader metadata to avoid split-brain where possible."
        ],
        "example": "Bully algorithm: nodes have unique IDs; highest ID node alive becomes coordinator. ZooKeeper/Etcd use Raft to elect leader for log replication.",
        "time_complexity": "Bully algorithm worst-case O(n^2) messages; consensus-based elections ~O(n).",
        "space_complexity": "O(n) to track membership and leader state.",
        "strengths": [
            "Ensures single coordinator for critical sections.",
            "Detects failures and reconfigures automatically."
        ],
        "weaknesses": [
            "Susceptible to split-brain without quorum/consensus safeguards.",
            "Frequent elections can disrupt system stability."
        ],
        "alternatives": ["Raft Consensus", "Paxos", "Randomized Leader Rotation"],
        "explanation": "Runs a coordination protocol so exactly one node assumes leadership while others remain followers, with re-election triggered on leader failure."
    },
    "semester_04/lecture_19_distributed_patterns/two_phase_commit/README.md": {
        "name": "Two-Phase Commit (2PC)",
        "problem": "Coordinates distributed transactions across multiple participants to achieve atomic commit or abort.",
        "intuition": "Use a coordinator that first collects votes (prepare phase) and then instructs all participants to commit or roll back in unison.",
        "inputs": "Coordinator node, participant nodes, transaction data, persistent logs.",
        "outputs": "Consistent commit/abort decision replicated to all participants.",
        "steps": [
            "Coordinator sends PREPARE to participants asking if they can commit.",
            "Each participant votes YES (and logs intent) or NO, then waits.",
            "If all YES, coordinator logs COMMIT and sends COMMIT messages; otherwise sends ABORT.",
            "Participants apply action (commit/abort), log outcome, and acknowledge.",
            "Coordinator cleans up after receiving acknowledgements.",
            "Recovery: participants replay logs to determine final decision on restart."
        ],
        "example": "Bank transfer across databases: coordinator ensures both debit and credit either commit or abort together to maintain consistency.",
        "time_complexity": "Two rounds of messaging O(n) plus logging.",
        "space_complexity": "O(n) for participants' logs and coordinator state.",
        "strengths": [
            "Provides atomicity across heterogeneous systems.",
            "Simple protocol widely implemented in databases/message brokers."
        ],
        "weaknesses": [
            "Blocking: participants must wait if coordinator crashes.",
            "Does not tolerate coordinator failure without extra protocols (3PC)."
        ],
        "alternatives": ["Three-Phase Commit", "Paxos/Raft Transactions", "Saga Pattern"],
        "explanation": "Uses a coordinator-driven prepare/commit handshake so either all participants commit or all abort, ensuring distributed atomicity at the cost of blocking."
    },
    "semester_04/lecture_14_security_patterns/oauth/README.md": {
        "name": "OAuth 2.0",
        "problem": "Enables third-party applications to obtain limited access to user resources without exposing user credentials, using authorization tokens.",
        "intuition": "Like a hotel key card: instead of giving your master key (password) to every service, issue temporary access cards (tokens) with specific permissions.",
        "inputs": "Client application, resource owner (user), authorization server, resource server, scopes (permissions).",
        "outputs": "Access token and optionally refresh token for accessing protected resources.",
        "steps": [
            "Client redirects user to authorization server with client ID and requested scopes.",
            "User authenticates and grants/denies permission.",
            "Authorization server redirects back to client with authorization code.",
            "Client exchanges authorization code for access token (with client secret).",
            "Client uses access token to access protected resources from resource server.",
            "Optionally refresh token to obtain new access token when expired."
        ],
        "example": "Photo app wants access to user's Google photos: user authorizes → Google issues token → app uses token to fetch photos without user's password.",
        "time_complexity": "O(1) for token validation; O(n) for authorization flow (multiple HTTP requests).",
        "space_complexity": "O(1) for token storage; O(n) for client and user registrations.",
        "strengths": [
            "No password sharing: users don't expose credentials to third parties.",
            "Fine-grained permissions through scopes."
        ],
        "weaknesses": [
            "Complex flow with multiple parties and security considerations.",
            "Token management complexity (expiration, refresh, revocation)."
        ],
        "alternatives": ["SAML", "OpenID Connect", "API Keys", "JWT Bearer Tokens"],
        "explanation": "Delegates authorization to a trusted server that issues tokens to third-party applications, allowing resource access without password sharing."
    },
    "semester_04/lecture_20_monitoring_observability/distributed_tracing/README.md": {
        "name": "Distributed Tracing",
        "problem": "Tracks requests across multiple services in a distributed system to understand request flow, identify bottlenecks, and debug performance issues.",
        "intuition": "Like a package tracking number: follow a request's journey through multiple services, recording each step to see where it goes and how long it takes.",
        "inputs": "Request headers (trace ID, span ID), service calls, instrumentation points.",
        "outputs": "Complete trace showing request path through services with timing and metadata.",
        "steps": [
            "Generate or extract trace ID at request entry point.",
            "Create root span for initial service.",
            "Propagate trace context (trace ID, span ID) in request headers.",
            "Each service creates child spans for operations.",
            "Spans record start time, end time, tags, and logs.",
            "Send spans to tracing backend for aggregation and visualization."
        ],
        "example": "User request → API Gateway (span 1) → Auth Service (span 2) → Order Service (span 3) → Payment Service (span 4). Trace shows full path and 2.3s total latency.",
        "time_complexity": "O(1) for span creation; O(n) for trace collection where n is number of services.",
        "space_complexity": "O(n) for trace data where n is number of spans in trace.",
        "strengths": [
            "End-to-end visibility across distributed systems.",
            "Identifies performance bottlenecks and dependencies."
        ],
        "weaknesses": [
            "Overhead from instrumentation and data collection.",
            "Requires consistent trace context propagation."
        ],
        "alternatives": ["Log Correlation", "APM Tools", "Service Mesh Observability"],
        "explanation": "Instruments services to create spans that form traces, enabling visualization of request flows and performance analysis across distributed systems."
    },
    "semester_04/lecture_20_monitoring_observability/log_aggregation/README.md": {
        "name": "Log Aggregation",
        "problem": "Collects, centralizes, and indexes logs from multiple services to enable search, analysis, and troubleshooting across distributed systems.",
        "intuition": "Like a library catalog: gather all books (logs) from different locations into one central system (aggregator) so you can search and find what you need quickly.",
        "inputs": "Logs from multiple services, log shipping agents, aggregation infrastructure.",
        "outputs": "Centralized, searchable log repository with indexing and query capabilities.",
        "steps": [
            "Services write logs to local files or stdout.",
            "Log shippers (agents) collect logs from each service.",
            "Shippers forward logs to aggregation service (e.g., ELK, Splunk).",
            "Aggregator parses, indexes, and stores logs.",
            "Users query aggregated logs using search interface.",
            "Optionally apply retention policies and archiving."
        ],
        "example": "10 microservices each write logs → Filebeat collects → sends to Elasticsearch → Kibana provides search interface. Query: 'errors in last hour' shows all errors across services.",
        "time_complexity": "O(1) for log ingestion; O(log n) to O(n) for search depending on indexing.",
        "space_complexity": "O(n) for n log entries (requires significant storage for large systems).",
        "strengths": [
            "Centralized view of all system logs.",
            "Enables correlation and analysis across services."
        ],
        "weaknesses": [
            "High storage and processing requirements.",
            "Network overhead from log shipping."
        ],
        "alternatives": ["Structured Logging", "Distributed Tracing", "Centralized Logging Services"],
        "explanation": "Collects logs from distributed services into a central repository, enabling unified search, analysis, and troubleshooting across the entire system."
    },
    "semester_04/lecture_20_monitoring_observability/metrics_collection/README.md": {
        "name": "Metrics Collection",
        "problem": "Collects, aggregates, and stores quantitative measurements about system behavior (CPU, memory, request rates, errors) for monitoring and alerting.",
        "intuition": "Like a car dashboard: continuously measure speed, fuel, temperature (metrics) and display them so you can monitor system health and react to issues.",
        "inputs": "System metrics (CPU, memory, disk), application metrics (request rate, latency, errors), business metrics (revenue, conversions).",
        "outputs": "Time-series database of metrics with visualization and alerting capabilities.",
        "steps": [
            "Instrument application/services to emit metrics (counters, gauges, histograms).",
            "Metrics agents collect metrics at regular intervals.",
            "Forward metrics to time-series database (Prometheus, InfluxDB).",
            "Store metrics with timestamps and labels.",
            "Query metrics for visualization (Grafana) or alerting rules.",
            "Generate alerts when metrics exceed thresholds."
        ],
        "example": "Service emits: request_count=1000, error_count=5, latency_p99=200ms every 10s → Prometheus stores → Grafana dashboard shows trends → Alert fires if error_rate > 1%.",
        "time_complexity": "O(1) for metric emission; O(log n) for time-series queries.",
        "space_complexity": "O(n) for n metric samples (compressed over time).",
        "strengths": [
            "Real-time visibility into system health.",
            "Enables proactive alerting and capacity planning."
        ],
        "weaknesses": [
            "Storage costs grow with metric cardinality.",
            "Requires careful metric design to avoid explosion."
        ],
        "alternatives": ["Log-based Metrics", "Distributed Tracing", "APM Tools"],
        "explanation": "Continuously collects quantitative measurements from systems and applications, storing them as time-series data for monitoring, visualization, and alerting."
    },
    "semester_05/lecture_21_transfer_learning/feature_extraction/README.md": {
        "name": "Feature Extraction",
        "problem": "Uses pre-trained neural network layers to extract meaningful features from new data, leveraging learned representations without retraining the entire model.",
        "intuition": "Like using a professional photographer's camera settings: apply their learned expertise (pre-trained layers) to capture good features from your photos (new data) without learning photography from scratch.",
        "inputs": "Pre-trained model (typically CNN), new dataset, feature extraction layer configuration.",
        "outputs": "Feature vectors representing high-level patterns in the input data.",
        "steps": [
            "Load pre-trained model (e.g., ImageNet-trained ResNet).",
            "Remove final classification layers.",
            "Freeze all layers (set trainable=False).",
            "Pass new data through frozen layers to extract features.",
            "Use extracted features as input to new classifier or downstream task.",
            "Optionally fine-tune some layers if needed."
        ],
        "example": "Pre-trained ResNet on ImageNet → remove last layer → extract 2048-dim features from cat images → train simple classifier on features → achieve good accuracy with little data.",
        "time_complexity": "O(n·d) for n samples with d-dimensional features (faster than training from scratch).",
        "space_complexity": "O(m) for pre-trained model weights plus O(n·d) for extracted features.",
        "strengths": [
            "Leverages powerful pre-trained representations.",
            "Requires less data and training time than training from scratch."
        ],
        "weaknesses": [
            "Features may not be optimal for target task.",
            "Limited to tasks similar to pre-training domain."
        ],
        "alternatives": ["Fine-tuning", "End-to-End Training", "Domain Adaptation"],
        "explanation": "Extracts high-level features using frozen pre-trained model layers, enabling effective learning on new tasks with limited data by leveraging transferable representations."
    },
    "semester_05/lecture_21_transfer_learning/fine_tuning/README.md": {
        "name": "Fine-Tuning",
        "problem": "Adapts a pre-trained model to a new task by training some or all layers on target data, balancing transfer learning with task-specific adaptation.",
        "intuition": "Like adjusting a pre-tuned piano: start with good base tuning (pre-trained weights), then make small adjustments (fine-tune) to match your specific music (target task).",
        "inputs": "Pre-trained model, target dataset, learning rate, layers to fine-tune.",
        "outputs": "Adapted model optimized for target task with improved performance.",
        "steps": [
            "Load pre-trained model weights.",
            "Optionally replace final layers for new task (e.g., different number of classes).",
            "Freeze early layers, unfreeze later layers (or use differential learning rates).",
            "Train on target dataset with lower learning rate than training from scratch.",
            "Optionally unfreeze more layers and continue training.",
            "Validate and adjust hyperparameters."
        ],
        "example": "Pre-trained ResNet on ImageNet → replace last layer for 10 classes → freeze first 100 layers → fine-tune last layers on medical images with lr=0.001 → achieve 95% accuracy.",
        "time_complexity": "O(n·e·l) for n samples, e epochs, l layers (faster than full training).",
        "space_complexity": "O(m) for model weights plus O(b) for batch data during training.",
        "strengths": [
            "Better performance than feature extraction alone.",
            "More efficient than training from scratch."
        ],
        "weaknesses": [
            "Requires more data and computation than feature extraction.",
            "Risk of overfitting with small datasets."
        ],
        "alternatives": ["Feature Extraction", "Full Training from Scratch", "Progressive Unfreezing"],
        "explanation": "Adapts pre-trained models to new tasks by selectively training layers, combining transfer learning benefits with task-specific optimization."
    },
    "semester_05/lecture_21_transfer_learning/transfer_learning/README.md": {
        "name": "Transfer Learning",
        "problem": "Applies knowledge learned from one task (source) to improve learning on a related task (target), reducing data and training requirements.",
        "intuition": "Like learning to drive a car after knowing how to ride a bike: transfer balance and coordination skills (learned features) to the new task (driving) instead of starting from scratch.",
        "inputs": "Pre-trained model on source task, target task dataset, transfer strategy.",
        "outputs": "Model adapted for target task with improved performance and efficiency.",
        "steps": [
            "Train or obtain model on large source dataset (e.g., ImageNet).",
            "Identify transferable knowledge (features, representations).",
            "Choose transfer strategy: feature extraction, fine-tuning, or domain adaptation.",
            "Apply strategy to adapt model for target task.",
            "Train on target dataset (often with less data than needed for from-scratch training).",
            "Evaluate and iterate on transfer approach."
        ],
        "example": "Model trained on ImageNet (1M images, 1000 classes) → transfer to medical diagnosis (1000 images, 5 classes) → fine-tune → achieve 90% accuracy vs 60% from scratch.",
        "time_complexity": "O(n_s + n_t·e) where n_s is source data size, n_t is target data size, e is epochs (much faster than training from scratch).",
        "space_complexity": "O(m) for model weights (same as base model).",
        "strengths": [
            "Reduces data requirements for target task.",
            "Faster training and better performance than from-scratch learning."
        ],
        "weaknesses": [
            "Requires related source and target tasks.",
            "Negative transfer possible if tasks are too different."
        ],
        "alternatives": ["Training from Scratch", "Multi-Task Learning", "Domain Adaptation"],
        "explanation": "Leverages knowledge from a source task to improve learning on a target task, enabling effective learning with limited data by transferring learned representations."
    },
    "semester_05/lecture_22_cnn_architectures/efficientnet/README.md": {
        "name": "EfficientNet",
        "problem": "Scales CNN depth, width, and resolution uniformly using compound scaling to achieve better accuracy and efficiency than scaling dimensions independently.",
        "intuition": "Like adjusting a camera's zoom, aperture, and ISO together: balance all three dimensions (depth, width, resolution) proportionally for optimal performance, rather than just making one bigger.",
        "inputs": "Input images, base EfficientNet architecture, compound scaling coefficient φ.",
        "outputs": "Scaled EfficientNet model with optimized depth, width, and resolution.",
        "steps": [
            "Start with baseline EfficientNet-B0 architecture (found via neural architecture search).",
            "Apply compound scaling: depth^α × width^β × resolution^γ = 2^φ, where α+β+γ=1.",
            "Scale depth (number of layers), width (number of channels), and resolution (input size) together.",
            "Train scaled model on target dataset.",
            "Iterate to find optimal φ for accuracy/efficiency trade-off."
        ],
        "example": "EfficientNet-B0 baseline → scale with φ=1 → EfficientNet-B1 (depth×1.2, width×1.1, resolution×1.15) → achieves better accuracy than ResNet-50 with 8x fewer parameters.",
        "time_complexity": "O(d·w²·r²) where d is depth, w is width, r is resolution (scales polynomially with φ).",
        "space_complexity": "O(d·w²) for model parameters (grows with compound scaling).",
        "strengths": [
            "Achieves state-of-the-art accuracy with fewer parameters.",
            "Systematic scaling approach outperforms ad-hoc scaling."
        ],
        "weaknesses": [
            "Requires careful tuning of compound scaling coefficients.",
            "Higher resolution increases memory requirements."
        ],
        "alternatives": ["ResNet", "MobileNet", "Inception", "Manual Architecture Scaling"],
        "explanation": "Uses compound scaling to uniformly scale depth, width, and resolution, achieving better accuracy-efficiency trade-offs than scaling dimensions independently."
    },
    "semester_05/lecture_22_cnn_architectures/inception/README.md": {
        "name": "Inception (GoogLeNet)",
        "problem": "Uses parallel convolutions of different sizes (1×1, 3×3, 5×5) in the same layer to capture features at multiple scales efficiently.",
        "intuition": "Like using multiple camera lenses simultaneously: capture details at different scales (close-up, medium, wide) in parallel, then combine the best views.",
        "inputs": "Input feature maps, multiple convolution filter sizes (1×1, 3×3, 5×5), max pooling.",
        "outputs": "Feature maps with multi-scale representations concatenated together.",
        "steps": [
            "Apply 1×1 convolution for dimensionality reduction and feature combination.",
            "Apply 3×3 and 5×5 convolutions in parallel to capture different scales.",
            "Apply max pooling for spatial reduction.",
            "Concatenate outputs from all parallel paths.",
            "Use 1×1 convolutions to reduce channel dimensions before expensive operations.",
            "Stack multiple Inception modules to build deep network."
        ],
        "example": "Input 256×256×192 → Inception module: 1×1 conv (64 filters), 3×3 conv (128 filters), 5×5 conv (32 filters), max pool → concatenate → output 256×256×256.",
        "time_complexity": "O(n²·c·k²) where n is spatial size, c is channels, k is kernel size (reduced by 1×1 bottlenecks).",
        "space_complexity": "O(n²·c) for feature maps (1×1 convolutions reduce memory).",
        "strengths": [
            "Captures multi-scale features efficiently.",
            "1×1 convolutions reduce computational cost."
        ],
        "weaknesses": [
            "Complex architecture with many hyperparameters.",
            "Wider layers increase memory usage."
        ],
        "alternatives": ["ResNet", "VGG", "EfficientNet", "Standard Sequential CNNs"],
        "explanation": "Uses parallel convolutions of different sizes in the same layer to capture features at multiple scales, improving representation power while controlling computational cost."
    },
    "semester_05/lecture_22_cnn_architectures/resnet/README.md": {
        "name": "ResNet (Residual Network)",
        "problem": "Enables training of very deep networks by using skip connections (residual blocks) that allow gradients to flow directly, solving the vanishing gradient problem.",
        "intuition": "Like a highway bypass: if the main road (layers) is blocked, use the bypass (skip connection) to get through. This makes it easier to train very deep networks.",
        "inputs": "Input feature maps, residual block configuration, number of layers.",
        "outputs": "Deep network with residual connections enabling effective gradient flow.",
        "steps": [
            "Define residual block: F(x) = activation(conv(x) + x) where x is input (skip connection).",
            "Stack multiple residual blocks to build deep network.",
            "Use identity mapping for skip connection when dimensions match.",
            "Use 1×1 convolution for skip connection when dimensions need adjustment.",
            "Apply batch normalization and ReLU after convolutions.",
            "Train network end-to-end with standard backpropagation."
        ],
        "example": "ResNet-50: input → conv → 16 residual blocks (each with 2-3 conv layers) → global avg pool → classifier. Skip connections allow training 50+ layers vs 20 for plain CNN.",
        "time_complexity": "O(d·n²·c²) where d is depth, n is spatial size, c is channels (similar to plain CNN but enables deeper networks).",
        "space_complexity": "O(d·c²) for parameters (skip connections add minimal overhead).",
        "strengths": [
            "Enables training of very deep networks (100+ layers).",
            "Solves vanishing gradient problem effectively."
        ],
        "weaknesses": [
            "Slightly more memory due to skip connections.",
            "May have redundant representations in very deep networks."
        ],
        "alternatives": ["Plain CNNs", "DenseNet", "Highway Networks", "Inception"],
        "explanation": "Uses skip connections in residual blocks to enable direct gradient flow, allowing training of very deep networks that would otherwise suffer from vanishing gradients."
    },
    "semester_05/lecture_22_cnn_architectures/vgg/README.md": {
        "name": "VGG (Visual Geometry Group)",
        "problem": "Demonstrates that deep networks with small 3×3 convolutions can achieve excellent performance by stacking many layers, establishing depth as a key factor.",
        "intuition": "Like building with small LEGO blocks: use many small 3×3 blocks (convolutions) stacked together instead of a few large blocks, giving more flexibility and depth.",
        "inputs": "Input images, 3×3 convolution filters, max pooling layers.",
        "outputs": "Deep CNN with uniform architecture using small receptive fields.",
        "steps": [
            "Use only 3×3 convolutions (receptive field of larger convolutions can be achieved by stacking).",
            "Stack multiple 3×3 conv layers before pooling (e.g., 2-3 convs per block).",
            "Double number of filters after each max pooling layer.",
            "Use 2×2 max pooling for spatial downsampling.",
            "End with fully connected layers for classification.",
            "Train with data augmentation and dropout."
        ],
        "example": "VGG-16: 224×224×3 → 2×conv64 → pool → 2×conv128 → pool → 3×conv256 → pool → 3×conv512 → pool → 3×conv512 → pool → FC4096 → FC4096 → FC1000 → softmax.",
        "time_complexity": "O(n²·c²·d) where n is spatial size, c is channels, d is depth (many parameters due to FC layers).",
        "space_complexity": "O(c²·d) for parameters (large due to FC layers, ~138M for VGG-16).",
        "strengths": [
            "Simple, uniform architecture easy to understand and implement.",
            "Establishes importance of depth in CNNs."
        ],
        "weaknesses": [
            "Very large number of parameters (especially FC layers).",
            "Slower training and inference than more efficient architectures."
        ],
        "alternatives": ["ResNet", "MobileNet", "EfficientNet", "AlexNet"],
        "explanation": "Uses deep stacks of small 3×3 convolutions to build effective CNNs, demonstrating that depth is crucial for performance while maintaining architectural simplicity."
    },
    "semester_05/lecture_23_object_detection/rcnn/README.md": {
        "name": "R-CNN (Region-based CNN)",
        "problem": "Detects objects by first generating region proposals, then classifying each region with a CNN, combining selective search with deep learning.",
        "intuition": "Like a security guard checking suspicious areas: first identify potential regions (selective search), then examine each region carefully (CNN classification) to confirm if it contains an object.",
        "inputs": "Input image, region proposal algorithm (selective search), pre-trained CNN.",
        "outputs": "Bounding boxes with class labels and confidence scores for detected objects.",
        "steps": [
            "Generate ~2000 region proposals using selective search (bottom-up segmentation).",
            "Warp each region proposal to fixed size (e.g., 227×227).",
            "Extract features from each warped region using pre-trained CNN (e.g., AlexNet).",
            "Train SVM classifiers for each object class on extracted features.",
            "Apply bounding box regression to refine proposal coordinates.",
            "Apply non-maximum suppression to remove duplicate detections."
        ],
        "example": "Image → selective search finds 2000 regions → warp each to 227×227 → CNN extracts 4096-dim features → SVM classifies (person, car, dog) → bounding box regression → NMS → final detections.",
        "time_complexity": "O(n·m) where n is number of proposals (~2000), m is CNN forward pass time (slow: ~47s per image).",
        "space_complexity": "O(n·d) for n proposals with d-dimensional features (high memory usage).",
        "strengths": [
            "First successful application of CNNs to object detection.",
            "Achieves good accuracy on PASCAL VOC dataset."
        ],
        "weaknesses": [
            "Very slow due to processing each proposal separately.",
            "High memory usage and training complexity."
        ],
        "alternatives": ["Fast R-CNN", "Faster R-CNN", "YOLO", "SSD"],
        "explanation": "Uses region proposals with CNN-based classification to detect objects, pioneering deep learning for object detection but suffering from slow inference speed."
    },
    "semester_05/lecture_23_object_detection/ssd/README.md": {
        "name": "SSD (Single Shot Detector)",
        "problem": "Detects objects in a single forward pass by applying multiple default boxes at different scales and aspect ratios to feature maps at various layers.",
        "intuition": "Like a multi-scale fishing net: cast nets of different sizes (default boxes) at different depths (feature map layers) to catch objects of various sizes in one pass.",
        "inputs": "Input image, base CNN (e.g., VGG), multi-scale feature maps, default boxes.",
        "outputs": "Bounding boxes with class predictions and confidence scores in single pass.",
        "steps": [
            "Extract feature maps from multiple CNN layers (different scales).",
            "Generate default boxes (anchor boxes) at each feature map location with different scales and aspect ratios.",
            "For each default box, predict: class scores and bounding box offsets.",
            "Match default boxes to ground truth boxes using IoU threshold.",
            "Train with multi-task loss: classification loss + localization loss.",
            "Apply non-maximum suppression to remove duplicate detections."
        ],
        "example": "Input 300×300 → VGG extracts features at 38×38, 19×19, 10×10, 5×5, 3×3, 1×1 → each location has 4-6 default boxes → predict class+box for each → NMS → final detections.",
        "time_complexity": "O(n·k) where n is number of default boxes (~8732 for 300×300 input), k is prediction time per box (fast: ~58 FPS).",
        "space_complexity": "O(n·(c+4)) for n boxes with c classes and 4 box coordinates.",
        "strengths": [
            "Fast single-shot detection (real-time capable).",
            "Good accuracy-speed trade-off."
        ],
        "weaknesses": [
            "Struggles with small objects.",
            "Requires careful default box design."
        ],
        "alternatives": ["YOLO", "Faster R-CNN", "RetinaNet", "EfficientDet"],
        "explanation": "Performs object detection in a single forward pass using multi-scale feature maps and default boxes, achieving real-time speed with competitive accuracy."
    },
    "semester_05/lecture_23_object_detection/yolo/README.md": {
        "name": "YOLO (You Only Look Once)",
        "problem": "Divides image into grid cells and predicts bounding boxes and class probabilities directly from full images in one evaluation, enabling real-time object detection.",
        "intuition": "Like a single glance at a scene: instead of scanning multiple times, look once and immediately identify what's where, trading some accuracy for speed.",
        "inputs": "Input image, grid division (e.g., 7×7), CNN backbone.",
        "outputs": "Grid of predictions: bounding boxes, confidence scores, and class probabilities.",
        "steps": [
            "Divide input image into S×S grid (e.g., 7×7).",
            "Each grid cell predicts B bounding boxes and class probabilities.",
            "For each bounding box, predict: center coordinates, width, height, confidence score.",
            "Predict class probabilities for each grid cell (shared across boxes in that cell).",
            "Combine predictions: final score = confidence × class probability.",
            "Apply non-maximum suppression to remove overlapping detections."
        ],
        "example": "Input 448×448 → divide into 7×7 grid → each cell predicts 2 boxes (x,y,w,h,confidence) + 20 class probs → 7×7×30 tensor → NMS → final detections. Processes at 45 FPS.",
        "time_complexity": "O(S²·B·C) where S is grid size, B is boxes per cell, C is classes (very fast: real-time).",
        "space_complexity": "O(S²·(B·5+C)) for grid predictions (compact representation).",
        "strengths": [
            "Extremely fast real-time detection.",
            "Sees entire image context, fewer false positives on background."
        ],
        "weaknesses": [
            "Struggles with small objects and objects in groups.",
            "Limited to fixed number of detections per grid cell."
        ],
        "alternatives": ["YOLOv2/v3/v4/v5", "SSD", "Faster R-CNN", "RetinaNet"],
        "explanation": "Performs object detection in a single forward pass by dividing image into grid and predicting boxes and classes directly, achieving real-time speed with end-to-end learning."
    },
    "semester_05/lecture_24_segmentation/fcn/README.md": {
        "name": "FCN (Fully Convolutional Network)",
        "problem": "Performs pixel-level semantic segmentation by replacing fully connected layers with convolutions, enabling dense prediction on arbitrary-sized images.",
        "intuition": "Like a paint-by-numbers map: instead of classifying whole images, classify each pixel to create a detailed segmentation map showing what each pixel belongs to.",
        "inputs": "Input images of arbitrary size, pre-trained CNN (e.g., VGG, ResNet).",
        "outputs": "Dense pixel-wise class predictions (segmentation map) with same spatial dimensions as input.",
        "steps": [
            "Start with pre-trained CNN (e.g., VGG-16) and remove fully connected layers.",
            "Convert FC layers to 1×1 convolutions to maintain spatial information.",
            "Add upsampling layers (transposed convolutions) to restore spatial resolution.",
            "Use skip connections from earlier layers to combine fine and coarse features.",
            "Apply pixel-wise softmax to produce class probabilities for each pixel.",
            "Train end-to-end with pixel-wise cross-entropy loss."
        ],
        "example": "Input 500×500 image → VGG extracts features → remove FC layers → add 1×1 conv + upsampling → skip connections from pool3, pool4 → output 500×500 segmentation map with class per pixel.",
        "time_complexity": "O(n²·c) where n is spatial size, c is number of classes (single forward pass).",
        "space_complexity": "O(n²·c) for output segmentation map plus O(n²·d) for feature maps.",
        "strengths": [
            "First successful end-to-end CNN for semantic segmentation.",
            "Handles arbitrary input sizes and produces dense predictions."
        ],
        "weaknesses": [
            "Coarse predictions due to information loss in downsampling.",
            "Requires skip connections for fine-grained details."
        ],
        "alternatives": ["U-Net", "DeepLab", "PSPNet", "SegNet"],
        "explanation": "Converts classification CNNs to segmentation networks by replacing FC layers with convolutions and adding upsampling, enabling dense pixel-wise predictions."
    },
    "semester_05/lecture_24_segmentation/mask_rcnn/README.md": {
        "name": "Mask R-CNN",
        "problem": "Extends Faster R-CNN to simultaneously perform object detection, bounding box regression, and instance segmentation (pixel-level masks) in a unified framework.",
        "intuition": "Like a multi-tool: not only find objects (detection) and draw boxes (localization), but also precisely outline each object's shape (segmentation mask) in one pass.",
        "inputs": "Input images, region proposals (from RPN), feature maps.",
        "outputs": "Bounding boxes, class labels, confidence scores, and binary segmentation masks for each detected object.",
        "steps": [
            "Use Faster R-CNN backbone to generate region proposals via RPN.",
            "Apply RoIAlign (instead of RoIPool) to extract fixed-size features from proposals.",
            "Branch 1: Classify object and refine bounding box (as in Faster R-CNN).",
            "Branch 2: Predict binary segmentation mask for each RoI using FCN head.",
            "Train with multi-task loss: classification + box regression + mask prediction.",
            "Apply non-maximum suppression and output detections with masks."
        ],
        "example": "Image → RPN finds 1000 proposals → RoIAlign extracts 14×14 features → branch 1: class 'person' + box → branch 2: 28×28 binary mask → final: person at [x,y,w,h] with pixel mask.",
        "time_complexity": "O(n·m) where n is number of proposals, m is mask prediction time (slower than Faster R-CNN due to mask branch).",
        "space_complexity": "O(n·k²) for n proposals with k×k mask predictions (additional memory for masks).",
        "strengths": [
            "Unified framework for detection and segmentation.",
            "High-quality instance segmentation with precise masks."
        ],
        "weaknesses": [
            "Slower than detection-only methods.",
            "Requires instance-level segmentation annotations for training."
        ],
        "alternatives": ["FCN", "U-Net", "YOLACT", "SOLO"],
        "explanation": "Extends Faster R-CNN with a mask prediction branch, enabling simultaneous object detection and instance segmentation in a unified end-to-end framework."
    },
    "semester_05/lecture_24_segmentation/unet/README.md": {
        "name": "U-Net",
        "problem": "Performs biomedical image segmentation using a symmetric encoder-decoder architecture with skip connections to preserve fine-grained spatial details.",
        "intuition": "Like a funnel with a mirror: compress information going down (encoder), then expand it back up (decoder), while keeping shortcuts (skip connections) to preserve details lost during compression.",
        "inputs": "Input images (often biomedical), encoder-decoder architecture, skip connections.",
        "outputs": "Pixel-wise segmentation maps with same spatial dimensions as input.",
        "steps": [
            "Encoder (contracting path): apply 3×3 conv + ReLU, then 2×2 max pooling (repeat 4-5 times).",
            "Bottleneck: two 3×3 convolutions at lowest resolution.",
            "Decoder (expansive path): 2×2 upsampling, concatenate with corresponding encoder feature map (skip connection), then 3×3 conv + ReLU (repeat 4-5 times).",
            "Final layer: 1×1 convolution to map to number of classes.",
            "Train with pixel-wise cross-entropy loss (optionally with dice loss).",
            "Output segmentation map with class prediction for each pixel."
        ],
        "example": "Input 572×572 → encoder: 64→128→256→512→1024 (downsampling) → decoder: 1024→512→256→128→64 (upsampling with skip connections) → output 388×388 segmentation map.",
        "time_complexity": "O(n²·c) where n is spatial size, c is channels (single forward pass, efficient).",
        "space_complexity": "O(n²·c) for feature maps (skip connections require storing encoder features).",
        "strengths": [
            "Excellent for biomedical segmentation with limited data.",
            "Skip connections preserve fine-grained details."
        ],
        "weaknesses": [
            "Symmetric architecture may not be optimal for all tasks.",
            "Memory usage grows with input size due to skip connections."
        ],
        "alternatives": ["FCN", "DeepLab", "SegNet", "Attention U-Net"],
        "explanation": "Uses symmetric encoder-decoder architecture with skip connections to combine high-level semantic features with low-level spatial details, enabling precise segmentation."
    },
    "semester_05/lecture_25_transformers/attention/README.md": {
        "name": "Attention Mechanism",
        "problem": "Allows models to focus on relevant parts of input when making predictions, enabling better handling of long-range dependencies and interpretability.",
        "intuition": "Like reading a long document: when answering a question, focus attention on relevant sentences (high attention weights) rather than reading everything equally.",
        "inputs": "Query vectors Q, key vectors K, value vectors V (all from input sequences).",
        "outputs": "Weighted combination of values, where weights are computed from query-key similarity.",
        "steps": [
            "Compute attention scores: score(q_i, k_j) = similarity between query i and key j.",
            "Apply softmax to scores to get attention weights (sum to 1).",
            "Weighted sum of values: output_i = Σ(attention_weight_ij × v_j).",
            "For self-attention: Q, K, V all come from same input sequence.",
            "For multi-head attention: apply attention in parallel with different learned projections.",
            "Combine multi-head outputs via concatenation and linear transformation."
        ],
        "example": "Translation: 'The cat sat' → attention weights: 'cat' gets high weight when generating 'gato' (Spanish), 'sat' gets high weight for 'se sentó'. Attention matrix shows word alignments.",
        "time_complexity": "O(n²·d) where n is sequence length, d is dimension (quadratic in sequence length).",
        "space_complexity": "O(n²) for attention matrix (grows quadratically with sequence length).",
        "strengths": [
            "Captures long-range dependencies effectively.",
            "Provides interpretability through attention weights."
        ],
        "weaknesses": [
            "Quadratic complexity limits maximum sequence length.",
            "Requires careful initialization and training."
        ],
        "alternatives": ["RNN/LSTM", "CNN", "Sparse Attention", "Linear Attention"],
        "explanation": "Computes weighted combinations of input elements based on query-key similarity, allowing models to dynamically focus on relevant information for each prediction."
    },
    "semester_05/lecture_25_transformers/bert/README.md": {
        "name": "BERT (Bidirectional Encoder Representations from Transformers)",
        "problem": "Pre-trains deep bidirectional representations by jointly conditioning on both left and right context, enabling state-of-the-art performance on NLP tasks with fine-tuning.",
        "intuition": "Like reading a sentence both forward and backward simultaneously: understand each word by seeing everything around it (left and right context) at once, not just what came before.",
        "inputs": "Text sequences with special tokens ([CLS], [SEP]), token embeddings, position embeddings, segment embeddings.",
        "outputs": "Contextualized word embeddings that can be fine-tuned for downstream tasks.",
        "steps": [
            "Tokenize input and add special tokens: [CLS] at start, [SEP] between sentences.",
            "Create embeddings: token + position + segment embeddings.",
            "Apply bidirectional Transformer encoder (12-24 layers) with self-attention.",
            "Pre-train with two tasks: Masked Language Modeling (MLM) and Next Sentence Prediction (NSP).",
            "For downstream tasks: add task-specific head and fine-tune on labeled data.",
            "Output contextualized representations for each token position."
        ],
        "example": "Input: '[CLS] The cat sat [SEP] on the mat [SEP]' → BERT encodes → '[CLS]' embedding used for classification, 'cat' embedding captures context from entire sentence → fine-tune for sentiment/QA/NER.",
        "time_complexity": "O(n²·d·l) where n is sequence length, d is dimension, l is number of layers (pre-training is expensive).",
        "space_complexity": "O(l·d²) for model parameters (BERT-base: 110M, BERT-large: 340M parameters).",
        "strengths": [
            "Bidirectional context enables better understanding.",
            "Transfer learning: pre-train once, fine-tune for many tasks."
        ],
        "weaknesses": [
            "Cannot generate text (encoder-only architecture).",
            "Pre-training requires massive compute and data."
        ],
        "alternatives": ["GPT", "RoBERTa", "ALBERT", "ELECTRA"],
        "explanation": "Pre-trains bidirectional Transformer encoder on large text corpus using masked language modeling, producing contextualized embeddings that excel when fine-tuned on downstream tasks."
    },
    "semester_05/lecture_25_transformers/gpt/README.md": {
        "name": "GPT (Generative Pre-trained Transformer)",
        "problem": "Pre-trains autoregressive language model on large text corpus, then fine-tunes for downstream tasks, enabling strong performance on generation and understanding tasks.",
        "intuition": "Like learning to write by reading millions of books: learn patterns of language (pre-training), then adapt to specific writing tasks (fine-tuning) like essays, code, or stories.",
        "inputs": "Text sequences, token embeddings, position embeddings.",
        "outputs": "Next token predictions or task-specific outputs after fine-tuning.",
        "steps": [
            "Tokenize input text into subword tokens.",
            "Create embeddings: token + position embeddings.",
            "Apply Transformer decoder (masked self-attention + feed-forward).",
            "Pre-train with language modeling objective: predict next token given previous tokens.",
            "For fine-tuning: add task-specific head (classification, generation, etc.).",
            "Train on downstream task with supervised learning."
        ],
        "example": "Pre-training: 'The cat sat' → predict 'on'. Fine-tuning for sentiment: 'Great movie!' → add classification head → predict 'positive'. Generation: 'Once upon a time' → generate story continuation.",
        "time_complexity": "O(n²·d·l) for n tokens, d dimensions, l layers (autoregressive generation is sequential).",
        "space_complexity": "O(l·d²) for parameters (GPT-2: 1.5B, GPT-3: 175B parameters).",
        "strengths": [
            "Strong generative capabilities for text completion and creation.",
            "Transfer learning: one model for many tasks."
        ],
        "weaknesses": [
            "Unidirectional (left-to-right) limits bidirectional understanding.",
            "Large models require significant computational resources."
        ],
        "alternatives": ["BERT", "T5", "GPT-2/GPT-3", "PaLM"],
        "explanation": "Pre-trains autoregressive Transformer decoder on language modeling, learning to predict next tokens, then fine-tunes for downstream tasks or generates text directly."
    },
    "semester_05/lecture_25_transformers/transformer/README.md": {
        "name": "Transformer",
        "problem": "Replaces recurrent and convolutional layers with self-attention mechanisms, enabling parallel processing and better handling of long-range dependencies in sequences.",
        "intuition": "Like a team meeting where everyone can talk to everyone simultaneously: instead of passing messages sequentially (RNN), all positions attend to all others at once, seeing the full context immediately.",
        "inputs": "Input sequences (source and/or target), token embeddings, position encodings.",
        "outputs": "Output sequences (for translation, generation, etc.) or representations (for understanding).",
        "steps": [
            "Create input embeddings and add positional encodings (sinusoidal or learned).",
            "Encoder: apply multi-head self-attention + feed-forward network (repeat N times).",
            "Decoder: apply masked self-attention (causal) + cross-attention to encoder + feed-forward (repeat N times).",
            "Use layer normalization and residual connections around each sub-layer.",
            "Final linear layer and softmax for output predictions.",
            "Train end-to-end with backpropagation."
        ],
        "example": "Translation: 'Hello world' (English) → encoder creates representations → decoder attends to encoder + generates 'Bonjour le monde' (French) token by token, attending to relevant source words.",
        "time_complexity": "O(n²·d) where n is sequence length, d is dimension (parallelizable, but quadratic attention).",
        "space_complexity": "O(n²) for attention matrices plus O(d²) for parameters per layer.",
        "strengths": [
            "Parallel processing enables faster training than RNNs.",
            "Self-attention captures long-range dependencies effectively."
        ],
        "weaknesses": [
            "Quadratic memory and computation in sequence length.",
            "Requires large amounts of data for effective training."
        ],
        "alternatives": ["RNN/LSTM", "CNN", "Sparse Transformers", "Linear Transformers"],
        "explanation": "Uses stacked self-attention and feed-forward layers with residual connections, replacing recurrence with parallel attention mechanisms to process sequences efficiently."
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

