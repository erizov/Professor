# Log Aggregation

1. **Name of Algorithm**  
   Log Aggregation

2. **What problem does it solve? (1 sentence)**  
   Collects, centralizes, and indexes logs from multiple services to enable search, analysis, and troubleshooting across distributed systems.

3. **Intuition (plain-language explanation)**  
   Like a library catalog: gather all books (logs) from different locations into one central system (aggregator) so you can search and find what you need quickly.

4. **Inputs & Outputs**  
   - Input: Logs from multiple services, log shipping agents, aggregation infrastructure.  
   - Output: Centralized, searchable log repository with indexing and query capabilities.

5. **Step-by-step description (5–10 lines max)**  
1. Services write logs to local files or stdout.
2. Log shippers (agents) collect logs from each service.
3. Shippers forward logs to aggregation service (e.g., ELK, Splunk).
4. Aggregator parses, indexes, and stores logs.
5. Users query aggregated logs using search interface.
6. Optionally apply retention policies and archiving.

6. **Tiny example (hand-simulated)**  
   10 microservices each write logs → Filebeat collects → sends to Elasticsearch → Kibana provides search interface. Query: 'errors in last hour' shows all errors across services.

7. **Time & Space Complexity**  
   - Time: O(1) for log ingestion; O(log n) to O(n) for search depending on indexing.  
   - Space: O(n) for n log entries (requires significant storage for large systems).

8. **Strengths**  
- Centralized view of all system logs.
- Enables correlation and analysis across services.

9. **Weaknesses / limitations**  
- High storage and processing requirements.
- Network overhead from log shipping.

10. **Compare with alternatives**  
    Alternatives: Structured Logging, Distributed Tracing, Centralized Logging Services

11. **30-second explanation (your own words)**  
    Collects logs from distributed services into a central repository, enabling unified search, analysis, and troubleshooting across the entire system.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
