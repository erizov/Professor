# Grafana Dashboards

1. **Name of Algorithm**  
   Grafana Dashboards

2. **What problem does it solve? (1 sentence)**  
   Provides visual dashboards for monitoring and analyzing ML system metrics, enabling real-time visibility into system health, performance trends, and operational insights.

3. **Intuition (plain-language explanation)**  
   Like a car's dashboard with speedometer and fuel gauge: Grafana creates visual dashboards showing all your ML system's 'vital signs' (CPU, memory, latency, errors) in real-time, so you can see at a glance if everything is healthy or if something needs attention.

4. **Inputs & Outputs**  
   - Input: Metrics data sources (Prometheus, InfluxDB, CloudWatch, etc.), dashboard configuration (panels, queries, visualizations), time range filters.  
   - Output: Interactive dashboards with charts, graphs, and tables displaying system metrics and trends.

5. **Step-by-step description (5–10 lines max)**  
1. Connect data sources: configure connections to metrics databases (Prometheus, InfluxDB, etc.).
2. Create dashboard: define dashboard with panels for different metrics (CPU, memory, latency, etc.).
3. Add panels: create panels (graphs, tables, gauges) and write queries to fetch metrics from data sources.
4. Configure visualizations: choose chart types (line, bar, heatmap), set colors, add thresholds and annotations.
5. Set up refresh intervals: configure automatic refresh (e.g., every 30 seconds) to update dashboards in real-time.
6. Add variables: create dashboard variables for filtering (e.g., by service, environment, time range).
7. Organize panels: arrange panels in rows and columns for logical grouping and easy navigation.
8. Share dashboards: export dashboard JSON, share with team, or set up public dashboards for stakeholders.

6. **Tiny example (hand-simulated)**  
   ML inference dashboard: panel 1 shows request rate (line chart, 100 req/s), panel 2 shows latency p95 (200ms), panel 3 shows error rate (0.1%), panel 4 shows CPU usage (60%) → all panels refresh every 30s → engineer sees spike in latency → investigates further.

7. **Time & Space Complexity**  
   - Time: O(Q) for querying Q metrics per panel, O(R) for rendering R panels (typically fast, < 1s for most dashboards).  
   - Space: O(P·D) for storing P panels with D data points, O(M) for metrics data in time-series database.

8. **Strengths**  
- Visual: provides intuitive visual representation of system health.
- Real-time: updates automatically to show current system state.
- Customizable: supports wide variety of visualizations and data sources.

9. **Weaknesses / limitations**  
- Requires setup: needs configuration of data sources and panels.
- Can be overwhelming: too many panels can make dashboards cluttered.

10. **Compare with alternatives**  
    Alternatives: Custom Dashboards, CloudWatch Dashboards, Datadog, New Relic

11. **30-second explanation (your own words)**  
    Provides visual dashboards for monitoring ML system metrics, enabling real-time visibility into system health, performance trends, and operational insights through interactive charts and graphs.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
