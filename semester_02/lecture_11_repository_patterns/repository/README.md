# Repository Pattern

1. **Name of Algorithm**  
   Repository Pattern

2. **What problem does it solve? (1 sentence)**  
   Provides a collection-like abstraction over data sources, hiding persistence details from domain logic.

3. **Intuition (plain-language explanation)**  
   Treat the repository like an in-memory collection; domain code queries repository without knowing about SQL or API calls.

4. **Inputs & Outputs**  
   - Input: Domain aggregates, repository interfaces, concrete implementations for specific data stores.  
   - Output: Retrieved aggregates/entities and persisted changes.

5. **Step-by-step description (5–10 lines max)**  
1. Define repository interface with query/command operations (e.g., find_by_id, save).
2. Implement repository using ORM, SQL, or external API.
3. Inject repository into services/use cases.
4. Use unit of work or transactions to batch changes.
5. Mock repository in tests to isolate domain logic.

6. **Tiny example (hand-simulated)**  
   OrderRepository#find_pending returns aggregate root; service manipulates object and calls save.

7. **Time & Space Complexity**  
   - Time: Determined by underlying data store queries.  
   - Space: Depends on caching/unit of work implementation.

8. **Strengths**  
- Decouples domain from persistence technology.
- Centralizes data access logic.

9. **Weaknesses / limitations**  
- Over-abstraction for simple CRUD apps.
- Complex queries may leak storage concepts back into domain.

10. **Compare with alternatives**  
    Alternatives: Data Mapper, Active Record, DAO

11. **30-second explanation (your own words)**  
    Expose persistence operations through repository interfaces so domain code works with aggregates while storage remains hidden.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
