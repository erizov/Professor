# Data Governance

1. **Name of Algorithm**  
   Data Governance

2. **What problem does it solve? (1 sentence)**  
   Establishes policies, processes, and standards for managing data assets, ensuring data quality, security, compliance, and proper usage across an organization.

3. **Intuition (plain-language explanation)**  
   Like a library's cataloging system: data governance is like a library's system for organizing, cataloging, and managing books - you have rules for how books are organized (data standards), who can access what (data access policies), how to maintain quality (data quality rules), and how to track usage (data lineage) - it ensures the library (organization) can find, use, and trust its books (data) effectively.

4. **Inputs & Outputs**  
   - Input: Data assets, business requirements, regulatory requirements, organizational policies, data quality standards.  
   - Output: Data governance framework, policies, standards, data catalog, compliance, data quality.

5. **Step-by-step description (5–10 lines max)**  
1. Define framework: establish data governance structure and roles (data stewards, owners).
2. Create policies: develop data policies (access, privacy, retention, quality).
3. Set standards: define data standards (naming, formats, schemas, quality metrics).
4. Catalog data: create data catalog documenting all data assets and metadata.
5. Assign ownership: assign data owners and stewards for each data asset.
6. Implement controls: establish data access controls and security measures.
7. Monitor quality: implement data quality monitoring and validation.
8. Track lineage: document data lineage (where data comes from, how it's used).
9. Ensure compliance: ensure data practices meet regulatory requirements (GDPR, HIPAA).
10. Review: periodically review and update governance policies and practices.

6. **Tiny example (hand-simulated)**  
   Data governance: establish framework → define policies (data retention: 7 years, access: role-based) → create catalog (document all databases, tables, fields) → assign owners (finance data: CFO, customer data: CMO) → implement controls (encryption, access logs) → monitor quality (validate data completeness, accuracy) → track lineage (customer data: CRM → data warehouse → analytics) → compliance: GDPR compliance verified → governance operational.

7. **Time & Space Complexity**  
   - Time: O(a) where a is number of data assets (cataloging and governance setup).  
   - Space: O(m) where m is metadata size (governance documentation and catalogs).

8. **Strengths**  
- Data quality: improves data quality and consistency across organization.
- Compliance: ensures regulatory compliance and reduces risk.
- Trust: builds trust in data through proper management and documentation.

9. **Weaknesses / limitations**  
- Complexity: implementing comprehensive governance can be complex.
- Overhead: governance processes add overhead to data operations.
- Resistance: may face resistance from teams used to less structured approaches.

10. **Compare with alternatives**  
    Alternatives: Ad-hoc Data Management, Data Stewardship, Data Cataloging, Compliance Frameworks

11. **30-second explanation (your own words)**  
    Establishes policies, processes, and standards for managing data assets, ensuring data quality, security, compliance, and proper usage across an organization.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
