# Database Design

1. **Name of Algorithm**  
   Database Design

2. **What problem does it solve? (1 sentence)**  
Creates efficient, normalized database schemas that model real-world entities and relationships, ensuring data integrity, minimizing redundancy, and optimizing for query performance.

3. **Intuition (plain-language explanation)**  
Like designing a building blueprint: database design is like creating an architectural blueprint for data - you identify what entities exist (like rooms in a building), how they relate (like how rooms connect), and design the structure (like floor plan) to be efficient, organized, and easy to navigate - good design makes the database easy to use, maintain, and query.

4. **Inputs & Outputs**  
   - Input: Business requirements, entities, relationships, data constraints, access patterns.  
   - Output: Database schema, entity-relationship model, normalized tables, optimized design.

5. **Step-by-step description (5–10 lines max)**  
1. Gather requirements: understand business needs, data, and access patterns.
2. Identify entities: determine main entities (customers, orders, products, etc.).
3. Define relationships: establish relationships between entities (one-to-many, many-to-many, etc.).
4. Create ER model: build entity-relationship diagram showing entities and relationships.
5. Normalize: apply normalization rules to eliminate redundancy (1NF, 2NF, 3NF).
6. Design tables: create table structures with columns, data types, and constraints.
7. Define keys: establish primary keys, foreign keys, and indexes.
8. Optimize: denormalize selectively for performance if needed.
9. Validate: verify design meets requirements and supports queries efficiently.

6. **Tiny example (hand-simulated)**  
   E-commerce database design: entities: customers, orders, products, order_items → relationships: customer has many orders, order has many order_items, order_item belongs to product → normalize: separate tables for each entity → foreign keys link relationships → indexes on frequently queried fields → efficient, maintainable database design.

7. **Time & Space Complexity**  
   - Time: O(e·r) where e is number of entities, r is number of relationships (design phase).  
   - Space: O(t) where t is number of tables and their schema size.

8. **Strengths**  
- Data integrity: well-designed schema ensures data consistency.
- Efficiency: optimized design supports fast queries.
- Maintainability: clear structure makes database easy to maintain and extend.

9. **Weaknesses / limitations**  
- Complexity: good design requires careful analysis and planning.
- Trade-offs: may need to balance normalization with performance.
- Evolution: schema changes can be complex as requirements evolve.

10. **Compare with alternatives**  
    Alternatives: Ad-hoc Design, Denormalized Design, NoSQL Design, Schema-less Databases

11. **30-second explanation (your own words)**  
Creates efficient, normalized database schemas that model real-world entities and relationships, ensuring data integrity, minimizing redundancy, and optimizing for query performance.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
