# Database Monitoring

1. **Name of Algorithm**  
   Database Monitoring

2. **What problem does it solve? (1 sentence)**  
   Continuously tracks database performance, health, and resource usage through metrics, logs, and alerts, enabling proactive issue detection and performance optimization.

3. **Intuition (plain-language explanation)**  
   Like a health monitor for databases: database monitoring is like a fitness tracker for your database - it continuously measures vital signs (CPU, memory, disk, queries) and alerts you when something's wrong (like a heart rate monitor alerting if heart rate is too high) - you can see trends over time (like fitness progress) and catch problems early before they become critical.

4. **Inputs & Outputs**  
   - Input: Database metrics, performance counters, logs, monitoring tools, alert thresholds.  
   - Output: Performance metrics, health status, alerts, dashboards, optimization insights.

5. **Step-by-step description (5–10 lines max)**  
1. Define metrics: identify key metrics to monitor (CPU, memory, disk I/O, query performance, connections).
2. Set up monitoring: configure monitoring tools to collect metrics.
3. Collect data: continuously gather metrics from database and system.
4. Store metrics: save metrics in time-series database for historical analysis.
5. Create dashboards: build dashboards to visualize metrics and trends.
6. Set alerts: configure alert thresholds for critical metrics.
7. Analyze: identify performance bottlenecks, anomalies, and trends.
8. Alert: notify administrators when metrics exceed thresholds.
9. Optimize: use insights to optimize database performance and configuration.

6. **Tiny example (hand-simulated)**  
   Database monitoring: track CPU (currently 45%), memory (60%), disk I/O (high), slow queries (5 queries > 1s) → alert: disk I/O > 90% → investigate: find I/O-intensive query → optimize: add index → disk I/O drops to 30% → proactive monitoring → prevented performance degradation.

7. **Time & Space Complexity**  
   - Time: O(1) per metric collection, O(m) for analysis where m is number of metrics.  
   - Space: O(m·t) where m is metrics count, t is time period (time-series data storage).

8. **Strengths**  
- Proactive: detects issues before they impact users.
- Visibility: provides clear view of database health and performance.
- Optimization: enables data-driven performance optimization.

9. **Weaknesses / limitations**  
- Overhead: monitoring adds some overhead to database operations.
- Alert fatigue: too many alerts can desensitize administrators.
- Tool dependency: requires monitoring tools and infrastructure.

10. **Compare with alternatives**  
    Alternatives: Manual Monitoring, Log Analysis, Performance Testing, APM Tools

11. **30-second explanation (your own words)**  
    Continuously tracks database performance, health, and resource usage through metrics, logs, and alerts, enabling proactive issue detection and performance optimization.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
