# Data Mapper

1. **Name of Algorithm**  
   Data Mapper

2. **What problem does it solve? (1 sentence)**  
   Separates in-memory domain objects from database schemas by mapping between them, keeping models persistence-agnostic.

3. **Intuition (plain-language explanation)**  
   Mapper translates between domain entities and database rows/columns without letting entities know about SQL.

4. **Inputs & Outputs**  
   - Input: Domain entities, mapper classes, data source connections.  
   - Output: Persisted entities and hydrated objects returned from the database.

5. **Step-by-step description (5–10 lines max)**  
1. Define domain entities with pure business logic.
2. Create mapper classes with CRUD operations.
3. Mapper reads/writes using SQL or ORM but returns domain objects.
4. Unit tests entities without touching the database.
5. Swap out mappers to change storage technology.

6. **Tiny example (hand-simulated)**  
   UserMapper inserts/updates rows in users table while returning User entities with behavior.

7. **Time & Space Complexity**  
   - Time: Depends on persistence operations (O(1) for indexed queries, etc.).  
   - Space: O(n) for entity caches or unit of work state.

8. **Strengths**  
- Keeps domain model persistence-agnostic.
- Supports richer domain logic than Active Record.

9. **Weaknesses / limitations**  
- More boilerplate and mapping code.
- Harder to map complex object graphs without tooling.

10. **Compare with alternatives**  
    Alternatives: Repository Pattern, Active Record, Table Data Gateway

11. **30-second explanation (your own words)**  
    Use dedicated mapper classes to translate between domain objects and database rows so business logic stays ignorant of SQL.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
