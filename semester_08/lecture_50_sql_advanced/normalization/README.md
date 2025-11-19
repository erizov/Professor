# Database Normalization

1. **Name of Algorithm**  
   Database Normalization

2. **What problem does it solve? (1 sentence)**  
   Organizes database tables to eliminate data redundancy and dependency issues, ensuring data integrity and reducing storage requirements through structured table design.

3. **Intuition (plain-language explanation)**  
   Like organizing a filing cabinet: normalization is like separating documents into different folders (tables) based on what they're about - instead of storing customer address in every order (redundant), you store it once in a customers table and reference it (like a folder reference) - this prevents inconsistencies and saves space.

4. **Inputs & Outputs**  
   - Input: Unnormalized database schema, business requirements, data relationships.  
   - Output: Normalized database schema, reduced redundancy, improved data integrity.

5. **Step-by-step description (5–10 lines max)**  
1. Identify entities: determine main entities (customers, orders, products, etc.).
2. First Normal Form (1NF): eliminate repeating groups, ensure atomic values.
3. Second Normal Form (2NF): remove partial dependencies (non-key attributes depend on full key).
4. Third Normal Form (3NF): remove transitive dependencies (non-key attributes depend on other non-key attributes).
5. Create relationships: establish foreign key relationships between tables.
6. Verify: ensure no data redundancy and all dependencies are properly handled.
7. Optimize: balance normalization with query performance needs.
8. Document: document normalized schema and relationships.

6. **Tiny example (hand-simulated)**  
   Unnormalized: orders table with customer_name, customer_address, product_name, product_price (redundant) → 1NF: separate repeating groups → 2NF: remove partial dependencies → 3NF: remove transitive dependencies → normalized: orders table references customers and products tables → customer data stored once → no redundancy → data integrity maintained.

7. **Time & Space Complexity**  
   - Time: O(n) where n is number of tables and relationships (design phase).  
   - Space: O(d) where d is data size (typically reduces storage due to eliminated redundancy).

8. **Strengths**  
- Data integrity: eliminates redundancy and prevents inconsistencies.
- Storage efficiency: reduces storage requirements.
- Maintainability: easier to update data (change once, affects all references).

9. **Weaknesses / limitations**  
- Query complexity: may require more JOINs to retrieve related data.
- Performance: over-normalization can slow down queries.
- Design complexity: requires careful analysis and design.

10. **Compare with alternatives**  
    Alternatives: Denormalization, Flat Tables, Document Databases, NoSQL

11. **30-second explanation (your own words)**  
    Organizes database tables to eliminate data redundancy and dependency issues, ensuring data integrity and reducing storage requirements through structured table design.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
