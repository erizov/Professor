# Feature Store

1. **Name of Algorithm**  
   Feature Store

2. **What problem does it solve? (1 sentence)**  
Centralizes storage, versioning, and serving of machine learning features, enabling feature reuse, consistency between training and inference, and efficient feature serving at scale.

3. **Intuition (plain-language explanation)**  
   Like a shared library for features: instead of each team computing the same features differently, store them once in a central place where everyone can access the same version, ensuring training and production use identical features.

4. **Inputs & Outputs**  
   - Input: Raw data, feature definitions, feature computation pipelines, feature metadata (schema, version, lineage).  
   - Output: Stored features accessible via API, feature serving endpoints for real-time and batch inference.

5. **Step-by-step description (5–10 lines max)**  
1. Define feature schema: name, type, description, data source.
2. Implement feature computation pipeline (ETL jobs) to transform raw data into features.
3. Store computed features in feature store (offline storage: data warehouse, online storage: key-value store).
4. Version features: track changes to feature definitions and data over time.
5. Register feature metadata: schema, statistics, data quality metrics, lineage.
6. Expose feature serving API: point-in-time correct features for training, low-latency features for inference.
7. Enable feature discovery: catalog for teams to find and reuse existing features.
8. Monitor feature freshness and data quality.

6. **Tiny example (hand-simulated)**  
   E-commerce: feature 'user_purchase_count_30d' computed from transactions → stored in feature store → training pipeline reads historical features → production API serves current feature value for user_id=123 → both use same feature definition.

7. **Time & Space Complexity**  
   - Time: O(n) for feature computation and retrieval where n is data size (depends on feature complexity).  
   - Space: O(n·d) for storing features where n is number of entities, d is number of features.

8. **Strengths**  
- Ensures feature consistency between training and production.
- Reduces duplicate feature engineering work.
- Enables feature reuse across teams.

9. **Weaknesses / limitations**  
- Requires infrastructure investment and maintenance.
- May introduce latency if not optimized for serving.

10. **Compare with alternatives**  
    Alternatives: Feature Registry, Data Warehouse Features, Custom Feature Pipelines, Feast, Tecton

11. **30-second explanation (your own words)**  
Centralizes feature storage, versioning, and serving to ensure consistency between training and inference while enabling feature reuse and efficient serving at scale.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
