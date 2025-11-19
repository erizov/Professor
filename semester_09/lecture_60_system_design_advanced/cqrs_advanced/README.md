# Advanced CQRS (Command Query Responsibility Segregation)

1. **Name of Algorithm**  
   Advanced CQRS (Command Query Responsibility Segregation)

2. **What problem does it solve? (1 sentence)**  
   Separates read and write operations into different models and data stores, enabling independent scaling, optimization, and evolution of read and write sides for complex domain models.

3. **Intuition (plain-language explanation)**  
   Like separate libraries: Advanced CQRS is like having separate libraries for reading and writing - the reading library (query side) is optimized for fast lookups with indexes and denormalized data, while the writing library (command side) is optimized for data integrity and business rules - they're separate but synchronized, allowing each to be optimized for its purpose without compromising the other.

4. **Inputs & Outputs**  
   - Input: Commands (writes), queries (reads), domain events, read models, write models, synchronization mechanisms.  
   - Output: Separated read/write models, optimized queries, validated commands, synchronized data, scalable architecture.

5. **Step-by-step description (5–10 lines max)**  
1. Separate models: create separate read and write models.
2. Command side: handle commands (writes) through command handlers.
3. Validate: validate commands using business rules.
4. Execute: execute commands and update write model.
5. Publish events: publish domain events after command execution.
6. Query side: handle queries (reads) through query handlers.
7. Project: project events to read models (eventual consistency).
8. Optimize: optimize read models for query performance (denormalization, indexes).
9. Synchronize: synchronize read and write models through events.
10. Scale: scale read and write sides independently.

6. **Tiny example (hand-simulated)**  
   Advanced CQRS: command: CreateOrder → command handler: validate, execute → write model: update order aggregate → event: OrderCreated → query side: project event → read model: update order view (denormalized) → query: GetOrders → query handler: read from optimized read model → result: fast queries, optimized writes → Advanced CQRS operational.

7. **Time & Space Complexity**  
   - Time: O(1) for writes (command), O(log n) or O(1) for reads (optimized query models).  
   - Space: O(w + r) where w is write model size, r is read model size (separate storage).

8. **Strengths**  
- Scalability: enables independent scaling of read and write operations.
- Optimization: allows optimization of each side for its purpose.
- Flexibility: read models can be optimized for specific queries.

9. **Weaknesses / limitations**  
- Complexity: more complex than traditional CRUD architecture.
- Consistency: eventual consistency between read and write models.
- Synchronization: requires event handling and synchronization logic.

10. **Compare with alternatives**  
    Alternatives: Traditional CRUD, Event Sourcing, Read Replicas, CQRS Basic

11. **30-second explanation (your own words)**  
    Separates read and write operations into different models and data stores, enabling independent scaling, optimization, and evolution of read and write sides for complex domain models.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
