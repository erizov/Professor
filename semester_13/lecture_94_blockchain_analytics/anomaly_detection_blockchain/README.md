# Blockchain Anomaly Detection

1. **Name of Algorithm**  
   Blockchain Anomaly Detection

2. **What problem does it solve? (1 sentence)**  
   Identifies unusual patterns, suspicious activities, and potential security threats in blockchain transactions by analyzing transaction behavior, network patterns, and statistical deviations.

3. **Intuition (plain-language explanation)**  
   Like a security alarm system: Blockchain anomaly detection is like a security alarm system - you monitor normal behavior (typical transaction patterns), and when something unusual happens (anomalies like large transfers, rapid movements, suspicious patterns), the alarm goes off - this helps detect fraud, attacks, or suspicious activities early.

4. **Inputs & Outputs**  
   - Input: Blockchain transactions, historical data, network metrics, behavioral patterns, detection rules, machine learning models.  
   - Output: Anomaly alerts, suspicious transactions, risk scores, detection reports, pattern analysis.

5. **Step-by-step description (5–10 lines max)**  
1. Collect: collect blockchain transaction and network data.
2. Baseline: establish baseline of normal behavior.
3. Analyze: analyze transactions for unusual patterns.
4. Detect: apply detection algorithms (statistical, ML, rule-based).
5. Score: assign risk scores to detected anomalies.
6. Alert: generate alerts for high-risk anomalies.
7. Investigate: investigate flagged transactions.
8. Learn: update models based on investigation results.
9. Refine: refine detection rules and thresholds.
10. Report: generate anomaly detection reports.

6. **Tiny example (hand-simulated)**  
   Anomaly Detection: collect data → baseline → analyze → detect large transfer (1000 ETH) → score high risk → alert → investigate → confirm suspicious → Anomaly Detection successful.

7. **Time & Space Complexity**  
   - Time: O(n * d) where n is transactions, d is detection complexity (anomaly detection complexity).  
   - Space: O(n + m) where n is transaction data, m is model storage (detection storage).

8. **Strengths**  
- Security: helps detect fraud and attacks early.
- Automation: automates threat detection.
- Insights: provides insights into network behavior.

9. **Weaknesses / limitations**  
- False positives: may generate false alarms.
- Complexity: requires sophisticated detection algorithms.
- Privacy: raises privacy concerns.

10. **Compare with alternatives**  
    Alternatives: Manual Monitoring, Rule-Based Detection, Machine Learning Detection, Hybrid Approaches

11. **30-second explanation (your own words)**  
    Techniques for identifying unusual patterns and suspicious activities in blockchain transactions to detect fraud, attacks, and security threats.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
