# Data Warehousing

1. **Name of Algorithm**  
   Data Warehousing

2. **What problem does it solve? (1 sentence)**  
   Consolidates data from multiple sources into a centralized, structured repository optimized for analytical queries and business intelligence, enabling historical analysis and reporting.

3. **Intuition (plain-language explanation)**  
Like a company's central archive: data warehousing is like a company's central archive where all important documents (data) from different departments (sources) are collected, organized, and stored in a structured way - unlike operational systems (like active filing cabinets) that handle day-to-day transactions, the warehouse (archive) is optimized for finding and analyzing historical information (like 'how did sales change over the past 5 years?') - it's designed for reading and analyzing, not for frequent updates.

4. **Inputs & Outputs**  
   - Input: Source data (operational databases, files, APIs), ETL processes, dimensional model, business requirements.  
   - Output: Data warehouse, integrated data, analytical queries, business intelligence, historical data.

5. **Step-by-step description (5–10 lines max)**  
1. Design schema: create dimensional model (star schema, snowflake schema).
2. Extract: extract data from source systems (databases, files, APIs).
3. Transform: clean, validate, and transform data to match warehouse schema.
4. Load: load transformed data into data warehouse tables.
5. Organize: organize data into facts (measures) and dimensions (descriptors).
6. Index: create indexes for fast analytical queries.
7. Aggregate: pre-compute aggregations for common queries.
8. Update: periodically refresh data from source systems (batch or incremental).
9. Query: enable analytical queries and business intelligence tools.
10. Maintain: monitor performance, optimize queries, and manage data lifecycle.

6. **Tiny example (hand-simulated)**  
   Data warehouse: star schema → fact table: sales (amount, quantity, date_id, product_id, customer_id) → dimensions: date (date_id, year, quarter, month), product (product_id, name, category), customer (customer_id, name, region) → ETL: extract from CRM, ERP, e-commerce → transform: standardize formats, calculate metrics → load: daily batch load → query: 'sales by region and quarter' → fast analytical queries → business intelligence enabled.

7. **Time & Space Complexity**  
   - Time: O(d) for ETL where d is data size, O(log n) for queries with indexes where n is data size.  
   - Space: O(d) where d is data size (stores historical and aggregated data).

8. **Strengths**  
- Performance: optimized for analytical queries and reporting.
- Integration: consolidates data from multiple sources.
- Historical analysis: enables analysis of historical trends and patterns.

9. **Weaknesses / limitations**  
- Complexity: requires careful design and ETL processes.
- Latency: data may not be real-time (batch updates).
- Cost: can be expensive to build and maintain.

10. **Compare with alternatives**  
    Alternatives: Data Lakes, Data Marts, Operational Data Stores, Real-time Analytics

11. **30-second explanation (your own words)**  
    Consolidates data from multiple sources into a centralized, structured repository optimized for analytical queries and business intelligence, enabling historical analysis and reporting.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
