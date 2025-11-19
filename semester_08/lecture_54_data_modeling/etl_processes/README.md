# ETL Processes

1. **Name of Algorithm**  
   ETL Processes

2. **What problem does it solve? (1 sentence)**  
   Extracts data from source systems, transforms it to meet target requirements, and loads it into destination systems, enabling data integration and migration.

3. **Intuition (plain-language explanation)**  
Like a factory assembly line: ETL processes are like a factory assembly line - you extract raw materials (data) from suppliers (source systems), transform them (clean, reshape, calculate) on the assembly line (transformation logic), and load finished products (processed data) into warehouses (destination systems) - the goal is to take data from various sources, make it consistent and useful, and deliver it where it's needed.

4. **Inputs & Outputs**  
   - Input: Source data (databases, files, APIs), transformation rules, target schema, business logic.  
   - Output: Transformed data, loaded destination, data integration, data quality improvements.

5. **Step-by-step description (5–10 lines max)**  
1. Extract: read data from source systems (databases, files, APIs, streams).
2. Validate: check data quality and completeness during extraction.
3. Transform: apply transformations (clean, filter, aggregate, calculate, join).
4. Standardize: standardize formats, codes, and values across sources.
5. Enrich: add derived fields, lookups, and calculated values.
6. Validate: validate transformed data against business rules.
7. Load: insert transformed data into target system (data warehouse, database).
8. Handle errors: manage errors and exceptions during ETL process.
9. Monitor: track ETL execution, performance, and data quality metrics.
10. Schedule: automate ETL processes to run on schedule (daily, hourly, real-time).

6. **Tiny example (hand-simulated)**  
   ETL process: extract: read customer data from CRM (PostgreSQL), sales data from e-commerce (MongoDB) → transform: clean email addresses, standardize date formats, calculate total sales per customer, join customer and sales data → validate: check for duplicates, missing values, data quality → load: insert into data warehouse (star schema) → schedule: run daily at 2 AM → monitor: track records processed, errors, execution time → ETL complete.

7. **Time & Space Complexity**  
   - Time: O(d) where d is data size (extraction, transformation, loading).  
   - Space: O(d) where d is data size (temporary storage during transformation).

8. **Strengths**  
- Data integration: enables integration of data from multiple sources.
- Data quality: improves data quality through cleaning and validation.
- Automation: automates data movement and transformation processes.

9. **Weaknesses / limitations**  
- Complexity: ETL processes can be complex to design and maintain.
- Latency: batch ETL may introduce latency (not real-time).
- Resource intensive: can consume significant compute and storage resources.

10. **Compare with alternatives**  
    Alternatives: ELT Processes, Real-time Streaming, Data Virtualization, API Integration

11. **30-second explanation (your own words)**  

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
