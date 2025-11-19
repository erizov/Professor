# CQRS (Command Query Responsibility Segregation)

1. **Name of Algorithm**  
   CQRS (Command Query Responsibility Segregation)

2. **What problem does it solve? (1 sentence)**  
Separates read and write operations into different models to optimize performance, scalability, and maintainability of data access.

3. **Intuition (plain-language explanation)**  
   Split your data model: commands (writes) use one model optimized for updates, queries (reads) use another optimized for fast retrieval.

4. **Inputs & Outputs**  
   - Input: Commands (write operations) and queries (read operations) on domain entities.  
   - Output: Separate read and write models with independent optimization strategies.

5. **Step-by-step description (5–10 lines max)**  
1. Define command model: optimized for validation, business rules, and writes.
2. Define query model: denormalized, optimized for fast reads and reporting.
3. Commands update write model and publish events.
4. Event handlers update read model asynchronously.
5. Queries read from optimized read model.

6. **Tiny example (hand-simulated)**  
   E-commerce: Order command model stores normalized data; query model pre-aggregates order history, customer stats for dashboard.

7. **Time & Space Complexity**  
   - Time: Write: O(1) to O(log n) depending on model; Read: O(1) to O(log n) for optimized queries.  
   - Space: O(n) for write model + O(m) for read model (may be larger due to denormalization).

8. **Strengths**  
- Independent scaling of read/write workloads.
- Optimized models for each operation type.

9. **Weaknesses / limitations**  
- Increased complexity (two models to maintain).
- Eventual consistency between read and write models.

10. **Compare with alternatives**  
    Alternatives: Traditional CRUD, Event Sourcing, Read Replicas

11. **30-second explanation (your own words)**  
    Separates command (write) and query (read) responsibilities into distinct models, allowing independent optimization and scaling.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
