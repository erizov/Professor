# Conflict-Free Replicated Data Types (CRDTs)

## Учебные материалы

- [Школьный уровень](school.ru.md)
- [Университетский уровень](univer.ru.md)

## Algorithm Visualization

### Flowchart (ASCII)

```
Conflict-Free Replicated Data Types (CRDTs) Flowchart:

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
Conflict-Free Replicated Data Types (CRDTs) Step-by-Step Execution:

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

- [Python Implementation](/code/semester_09/lecture_59_distributed_systems_advanced/crdt/algorithm.py)
- [Java Implementation](/code/semester_09/lecture_59_distributed_systems_advanced/crdt/Algorithm.java)
- [Python Tests](/code/semester_09/lecture_59_distributed_systems_advanced/crdt/test_algorithm.py)

   Conflict-Free Replicated Data Types (CRDTs)

What problem does it solve? (1 sentence)  
   Provides data structures that automatically resolve conflicts in distributed systems without coordination, enabling eventual consistency through mathematical properties (commutativity, associativity, idempotency).

Intuition (plain-language explanation)  
   Like a shared document that auto-merges: CRDTs are like a shared document where multiple people can edit simultaneously, and the system automatically merges changes without conflicts - even if two people edit the same paragraph at the same time, the CRDT ensures both edits are preserved and merged correctly - it's like having a smart merge that always works, no matter what order changes arrive in, because the operations are designed to be commutative (order doesn't matter).

Inputs & Outputs  

  - Input: Operations (add, remove, update), replicas, operation timestamps, vector clocks.  
  - Output: Merged state, conflict-free replication, eventual consistency, convergent data.

Step-by-step description (5–10 lines max)  
Define CRDT: choose appropriate CRDT type (G-Counter, PN-Counter, G-Set, OR-Set, etc.).
Apply locally: apply operation to local replica immediately.
Tag operation: tag operation with metadata (timestamp, vector clock, unique ID).
Replicate: send operation to other replicas asynchronously.
Receive: receive operations from other replicas.
Merge: merge received operations into local state (commutative merge).
Resolve: automatically resolve conflicts using CRDT properties.
Converge: all replicas converge to same state eventually.
Query: query CRDT state (always returns consistent view).
Validate: ensure CRDT properties maintained (commutativity, associativity, idempotency).

Tiny example (hand-simulated)  
   CRDT: G-Counter (grow-only counter) → replica A: increment by 5 → replica B: increment by 3 → merge: A gets +3, B gets +5 → both converge to 8 → commutative: order doesn't matter → conflict-free: no coordination needed → CRDT ensures consistency.

Time & Space Complexity  

  - Time: O(1) for operations, O(n) for merge where n is number of replicas or operations.  
  - Space: O(r) or O(o) depending on CRDT type where r is replicas, o is operations (metadata overhead).

Strengths  

- No coordination: operations don't require coordination between replicas.
- Automatic merge: conflicts resolved automatically without manual intervention.
- Low latency: local operations are immediate (no network wait).

Weaknesses / limitations  

- Limited operations: not all operations can be expressed as CRDTs.
- Metadata overhead: CRDTs may require metadata (timestamps, vector clocks).
- Complexity: some CRDT types are complex to understand and implement.

Compare with alternatives  
    Alternatives: Eventual Consistency, Strong Consistency, Operational Transformation, Last-Write-Wins

30-second explanation (your own words)  
    Provides data structures that automatically resolve conflicts in distributed systems without coordination, enabling eventual consistency through mathematical properties (commutativity, associativity, idempotency).

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*


## References

- [Crdt - Wikipedia](https://en.wikipedia.org/wiki/Crdt)
