# Metrics Collection

1. **Name of Algorithm**  
   Metrics Collection

2. **What problem does it solve? (1 sentence)**  
   Collects, aggregates, and stores quantitative measurements about system behavior (CPU, memory, request rates, errors) for monitoring and alerting.

3. **Intuition (plain-language explanation)**  
   Like a car dashboard: continuously measure speed, fuel, temperature (metrics) and display them so you can monitor system health and react to issues.

4. **Inputs & Outputs**  
   - Input: System metrics (CPU, memory, disk), application metrics (request rate, latency, errors), business metrics (revenue, conversions).  
   - Output: Time-series database of metrics with visualization and alerting capabilities.

5. **Step-by-step description (5–10 lines max)**  
1. Instrument application/services to emit metrics (counters, gauges, histograms).
2. Metrics agents collect metrics at regular intervals.
3. Forward metrics to time-series database (Prometheus, InfluxDB).
4. Store metrics with timestamps and labels.
5. Query metrics for visualization (Grafana) or alerting rules.
6. Generate alerts when metrics exceed thresholds.

6. **Tiny example (hand-simulated)**  
   Service emits: request_count=1000, error_count=5, latency_p99=200ms every 10s → Prometheus stores → Grafana dashboard shows trends → Alert fires if error_rate > 1%.

7. **Time & Space Complexity**  
   - Time: O(1) for metric emission; O(log n) for time-series queries.  
   - Space: O(n) for n metric samples (compressed over time).

8. **Strengths**  
- Real-time visibility into system health.
- Enables proactive alerting and capacity planning.

9. **Weaknesses / limitations**  
- Storage costs grow with metric cardinality.
- Requires careful metric design to avoid explosion.

10. **Compare with alternatives**  
    Alternatives: Log-based Metrics, Distributed Tracing, APM Tools

11. **30-second explanation (your own words)**  
    Continuously collects quantitative measurements from systems and applications, storing them as time-series data for monitoring, visualization, and alerting.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
