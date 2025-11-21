# SQL Joins

Name of Algorithm  

## Code Files


## Algorithm Visualization

### Flowchart (ASCII)


```
SQL Joins Flowchart:

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
SQL Joins Step-by-Step Execution:

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
- [Python Implementation](/code/semester_08/lecture_49_sql_fundamentals/joins/algorithm.py)
- [Java Implementation](/code/semester_08/lecture_49_sql_fundamentals/joins/Algorithm.java)
- [Python Tests](/code/semester_08/lecture_49_sql_fundamentals/joins/test_algorithm.py)


   SQL Joins

What problem does it solve? (1 sentence)  
   Combine rows from related tables based on matching keys.

Intuition (plain-language explanation)  
   Treat tables like sets and match rows where keys agree or complement each other.

Inputs & Outputs  
   - Input: Two or more tables plus join condition.  
   - Output: Composite rows containing columns from each source table.

Step-by-step description (5–10 lines max)  
Choose join type (INNER, LEFT, RIGHT, FULL, CROSS).
Identify join keys/conditions.
Relational engine decides join algorithm (nested loop, hash, merge).
Execute join, producing combined tuples.
Apply downstream filters or projections.

Tiny example (hand-simulated)  
   SELECT orders.id, customers.name FROM orders INNER JOIN customers ON orders.customer_id = customers.id;

Time & Space Complexity  
   - Time: Depends on join algorithm; hash join ~O(n + m), nested loop ~O(n·m) without indexes.  
   - Space: May require hash tables or sort buffers.

Strengths  
- Expressive way to relate normalized tables.
- Optimizers pick efficient algorithms automatically.

Weaknesses / limitations  
- Expensive if keys lack indexes.
- Incorrect join types can duplicate or drop rows.

Compare with alternatives  
    Alternatives: Denormalization, Materialized views, Application-level joins

30-second explanation (your own words)  
    Map matching keys across tables so related data can be viewed as a single combined set.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
