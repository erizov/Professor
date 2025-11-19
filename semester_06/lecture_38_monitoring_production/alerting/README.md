# Alerting

1. **Name of Algorithm**  
   Alerting

2. **What problem does it solve? (1 sentence)**  
   Monitors system metrics and automatically triggers notifications when thresholds are exceeded or anomalies are detected, enabling proactive incident response and preventing service degradation.

3. **Intuition (plain-language explanation)**  
   Like a smoke alarm for your ML system: continuously watch metrics (CPU, latency, error rate) - when something goes wrong (CPU spikes, errors increase), immediately send alerts (email, Slack, PagerDuty) so you can fix it before users notice.

4. **Inputs & Outputs**  
   - Input: System metrics (CPU, memory, latency, error rate, prediction accuracy), alert rules (thresholds, conditions), notification channels (email, Slack, PagerDuty).  
   - Output: Alert notifications sent to configured channels when conditions are met, alert history and status.

5. **Step-by-step description (5–10 lines max)**  
1. Define alert rules: specify metrics to monitor, thresholds (e.g., CPU > 80%, error rate > 5%), and conditions (duration, severity).
2. Collect metrics: continuously gather metrics from systems (Prometheus, CloudWatch, custom metrics).
3. Evaluate conditions: compare current metric values to thresholds and check if conditions are met.
4. Trigger alert: when condition is true (e.g., CPU > 80% for 5 minutes), create alert event.
5. Deduplicate alerts: group similar alerts to avoid alert fatigue (same alert multiple times).
6. Route alerts: send notifications to appropriate channels based on severity (critical → PagerDuty, warning → Slack).
7. Escalate alerts: if alert not acknowledged within time window, escalate to higher severity or different team.
8. Resolve alerts: mark alerts as resolved when underlying issue is fixed, track resolution time.

6. **Tiny example (hand-simulated)**  
   ML inference service: monitor latency (p50, p95, p99) → rule: p95 latency > 200ms for 2 minutes → alert triggered → notification sent to on-call engineer via PagerDuty → engineer investigates: high traffic spike → scales up instances → latency returns to normal → alert resolved.

7. **Time & Space Complexity**  
   - Time: O(M) for evaluating M metrics (continuous monitoring), O(1) for alert evaluation per metric.  
   - Space: O(A) for storing active alerts, O(H) for alert history where H is number of historical alerts.

8. **Strengths**  
- Proactive: enables early detection of issues before they impact users.
- Automated: reduces need for manual monitoring.
- Actionable: provides context and severity to guide response.

9. **Weaknesses / limitations**  
- Alert fatigue: too many alerts can desensitize teams.
- False positives: may trigger alerts for non-critical issues.
- Requires tuning: thresholds need careful calibration.

10. **Compare with alternatives**  
    Alternatives: Manual Monitoring, Log-based Alerting, Anomaly Detection, Synthetic Monitoring

11. **30-second explanation (your own words)**  
    Monitors system metrics and automatically triggers notifications when thresholds are exceeded, enabling proactive incident response and preventing service degradation through timely alerts.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
