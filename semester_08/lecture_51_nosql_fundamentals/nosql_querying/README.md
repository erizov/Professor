# NoSQL Querying

## Учебные материалы

- [Школьный уровень](school.ru.md)
- [Университетский уровень](univer.ru.md)

## Algorithm Visualization

### Flowchart (ASCII)

```
NoSQL Querying Flowchart:

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
NoSQL Querying Step-by-Step Execution:

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

- [Python Implementation](/code/semester_08/lecture_51_nosql_fundamentals/nosql_querying/algorithm.py)
- [Java Implementation](/code/semester_08/lecture_51_nosql_fundamentals/nosql_querying/Algorithm.java)
- [Python Tests](/code/semester_08/lecture_51_nosql_fundamentals/nosql_querying/test_algorithm.py)

   NoSQL Querying

What problem does it solve? (1 sentence)  
   Retrieves and manipulates data from NoSQL databases using query languages and APIs, enabling flexible data access patterns adapted to different NoSQL data models.

Intuition (plain-language explanation)  
   Like different ways to search different types of storage: NoSQL querying is like having different search methods for different storage types - key-value stores use simple key lookups (like looking up a word in a dictionary), document databases use field-based queries (like searching a filing cabinet by document properties), and graph databases use traversal queries (like following connections in a network) - each NoSQL type has query methods suited to its data model.

Inputs & Outputs  

  - Input: Query criteria, data model type, query language/API, database connection.  
  - Output: Query results, retrieved data, filtered documents/rows, aggregated data.

Step-by-step description (5–10 lines max)  
Choose query method: select appropriate query method based on NoSQL type.
Specify criteria: define search criteria (field values, conditions, patterns).
Execute query: send query to NoSQL database using query language or API.
Process: database processes query using indexes, scans, or traversals.
Filter: apply filters to match query criteria.
Return results: retrieve and return matching documents/rows/nodes.
Aggregate (optional): perform aggregations (count, sum, average, etc.).
Format: format results for application use.

Tiny example (hand-simulated)  
   MongoDB: db.users.find({age: {$gt: 25}, city: 'New York'}) → document database query → uses index on age and city → filters documents → returns matching users → flexible: can query nested fields, arrays, and use complex conditions.

Time & Space Complexity  

  - Time: Varies by query type: O(1) for key lookups, O(log n) with indexes, O(n) for full scans, O(d) for graph traversals where d is depth.  
  - Space: O(r) where r is result set size (memory for query results).

Strengths  

- Flexibility: supports various query patterns adapted to data model.
- Performance: can be very fast with proper indexes and data model fit.
- Scalability: queries can be distributed across nodes in distributed systems.

Weaknesses / limitations  

- Limited joins: most NoSQL databases don't support SQL-style joins.
- Query complexity: complex queries may require application-level processing.
- Consistency: eventual consistency may affect query results.

Compare with alternatives  
    Alternatives: SQL Queries, MapReduce, Application-Level Filtering, Search Engines

30-second explanation (your own words)  
    Retrieves and manipulates data from NoSQL databases using query languages and APIs, enabling flexible data access patterns adapted to different NoSQL data models.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
