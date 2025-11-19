# Model Monitoring

1. **Name of Algorithm**  
   Model Monitoring

2. **What problem does it solve? (1 sentence)**  
   Continuously tracks model performance, data quality, and system health in production to detect degradation, errors, and anomalies, enabling proactive model maintenance.

3. **Intuition (plain-language explanation)**  
   Like a health monitor for your model: continuously check if the model is performing well, if predictions make sense, if data quality is good, and if the system is healthy - alert when something goes wrong.

4. **Inputs & Outputs**  
   - Input: Model predictions, ground truth labels (when available), input data, system metrics (latency, throughput, errors).  
   - Output: Performance dashboards, alerts for anomalies, degradation reports, recommendations for model updates.

5. **Step-by-step description (5–10 lines max)**  
1. Define monitoring metrics: accuracy, precision, recall, latency, prediction distribution, data quality scores.
2. Collect predictions and inputs from production inference.
3. Compare predictions to ground truth (if available) to compute performance metrics.
4. Track prediction distributions: detect if predictions shift (e.g., all predictions become positive).
5. Monitor data quality: missing values, outliers, schema violations.
6. Set thresholds and alerting rules: alert if accuracy drops below threshold, if latency exceeds SLA, if error rate spikes.
7. Visualize metrics in dashboards: time series of performance, distribution plots, error logs.
8. Generate reports and trigger automated responses (e.g., rollback, retrain) when issues detected.

6. **Tiny example (hand-simulated)**  
   Fraud detection model: monitor accuracy (baseline 95%) → drops to 90% → alert triggered → investigate: data drift detected → retrain model with recent data → accuracy returns to 95%.

7. **Time & Space Complexity**  
   - Time: O(n) for processing n predictions/metrics (real-time or batch processing).  
   - Space: O(n) for storing metrics and predictions over time windows.

8. **Strengths**  
- Enables proactive detection of model issues.
- Provides visibility into model behavior in production.

9. **Weaknesses / limitations**  
- Requires ground truth labels for supervised metrics (may be delayed or unavailable).
- May generate noise if thresholds not tuned properly.

10. **Compare with alternatives**  
    Alternatives: Data Drift Detection, Shadow Testing, Canary Deployments, Arize, Fiddler, WhyLabs

11. **30-second explanation (your own words)**  
    Continuously tracks model performance, predictions, and system health in production to detect degradation and anomalies, enabling proactive maintenance and ensuring model reliability.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
