# Graph Databases

1. **Name of Algorithm**  

## Code Files


## Algorithm Visualization

### Flowchart (ASCII)


```
Graph Databases Flowchart:

┌─────────────┐
│   Start     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Initialize │
│   data      │
└──────┬──────┘
       │
       ▼
┌─────────────┐      Yes
│  Process   ├──────┐
│  condition?│      │
└──────┬──────┘      │
       │ No          │
       ▼             │
┌─────────────┐      │
│  Execute   │      │
│  operation │      │
└──────┬──────┘      │
       │             │
       └─────────────┘
       │
       ▼
┌─────────────┐
│    End      │
└─────────────┘
```


### Step-by-Step Execution


```
Graph Databases Step-by-Step Execution:

Input: [example data]

Step 1: Initialize
State: [initial state]

Step 2: Process
State: [intermediate state]

Step 3: Finalize
State: [final state]

Result: [output]
```


### Interactive Flowchart (Mermaid)


```mermaid
flowchart TD
    Start([Start]) --> Init[Initialize data]
    Init --> Process{Process condition}
    Process -->|True| Execute[Execute operation]
    Execute --> Done{Complete?}
    Done -->|No| Process
    Done -->|Yes| End([End])
    Process -->|False| End
```


> **Note**: Mermaid diagrams are rendered automatically on GitHub. For local viewing, use a Mermaid-compatible Markdown viewer.
- [Python Implementation](semester_08/lecture_51_nosql_fundamentals/graph_databases/algorithm.py)
- [Java Implementation](semester_08/lecture_51_nosql_fundamentals/graph_databases/Algorithm.java)
- [Python Tests](semester_08/lecture_51_nosql_fundamentals/graph_databases/test_algorithm.py)


   Graph Databases

2. **What problem does it solve? (1 sentence)**  
Stores data as nodes (entities) and edges (relationships), enabling efficient traversal and querying of complex relationships and network structures.

3. **Intuition (plain-language explanation)**  
   Like a social network: graph databases store data like a social network where people are nodes (entities) and friendships are edges (relationships) - you can easily find 'friends of friends' by following edges (relationships), making it perfect for modeling and querying complex relationships like social networks, recommendation systems, or knowledge graphs.

4. **Inputs & Outputs**  
   - Input: Nodes (entities), edges (relationships), properties, graph queries.  
   - Output: Graph structure, traversed paths, relationship queries, network analysis.

5. **Step-by-step description (5–10 lines max)**  
1. Create nodes: define entities as nodes with properties (e.g., Person, Product).
2. Create edges: define relationships as edges with properties (e.g., FRIENDS_WITH, PURCHASED).
3. Store graph: save nodes and edges in graph database.
4. Index: create indexes on node properties and edge types.
5. Traverse: navigate graph by following edges from node to node.
6. Query: use graph query language (Cypher, Gremlin) to find paths, patterns, or relationships.
7. Analyze: perform graph algorithms (shortest path, centrality, community detection).
8. Update: add/remove nodes and edges as relationships change.

6. **Tiny example (hand-simulated)**  
   Nodes: Person(id=1, name='Alice'), Person(id=2, name='Bob') → Edge: FRIENDS_WITH(from=1, to=2) → query: find friends of Alice → traverse: start at Alice → follow FRIENDS_WITH edges → return Bob → efficient relationship traversal.

7. **Time & Space Complexity**  
   - Time: O(1) for node/edge lookup, O(d) for traversal where d is depth, O(n+m) for graph algorithms where n is nodes, m is edges.  
   - Space: O(n+m) where n is number of nodes, m is number of edges.

8. **Strengths**  
- Relationship queries: excels at querying complex relationships.
- Traversal performance: fast graph traversal and path finding.
- Flexible schema: easily add new node types and relationship types.

9. **Weaknesses / limitations**  
- Scalability: may face challenges scaling to very large graphs.
- Query complexity: graph queries can be complex to write.
- Use case specific: best suited for relationship-heavy data.

10. **Compare with alternatives**  
    Alternatives: Relational Databases, Document Databases, Triple Stores, Network Databases

11. **30-second explanation (your own words)**  

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
