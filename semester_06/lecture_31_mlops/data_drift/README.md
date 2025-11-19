# Data Drift Detection

1. **Name of Algorithm**  
   Data Drift Detection

2. **What problem does it solve? (1 sentence)**  
   Monitors and detects when the distribution of production data deviates from training data distribution, indicating model performance degradation and need for retraining.

3. **Intuition (plain-language explanation)**  
   Like a quality control inspector: continuously check if incoming data looks like the data the model was trained on - if it changes significantly (drifts), the model may no longer work well and needs updating.

4. **Inputs & Outputs**  
   - Input: Training data distribution, production data stream, drift detection method (statistical tests, distance metrics).  
   - Output: Drift alerts, drift scores, feature-level drift indicators, recommendations for model retraining.

5. **Step-by-step description (5–10 lines max)**  
1. Establish baseline: compute statistics (mean, std, distribution) of training data.
2. Collect production data samples over time windows (e.g., daily batches).
3. Compute same statistics for production data.
4. Apply drift detection method: Kolmogorov-Smirnov test, Population Stability Index (PSI), Maximum Mean Discrepancy (MMD), or Wasserstein distance.
5. Compare distributions: if test statistic exceeds threshold, flag drift.
6. Identify which features have drifted (feature-level analysis).
7. Trigger alert if drift detected, optionally trigger automatic retraining pipeline.
8. Track drift over time to understand trends.

6. **Tiny example (hand-simulated)**  
   Fraud detection: training data has 1% fraud rate, production data shows 5% fraud rate → PSI > 0.25 (high drift) → alert: model may be outdated → retrain with recent data.

7. **Time & Space Complexity**  
   - Time: O(n·d) where n is sample size, d is number of features (statistical tests per feature).  
   - Space: O(d) for storing baseline statistics and O(n·d) for production samples.

8. **Strengths**  
- Early warning system for model degradation.
- Enables proactive model maintenance.

9. **Weaknesses / limitations**  
- May produce false positives (noise vs. real drift).
- Requires defining appropriate thresholds and detection methods.

10. **Compare with alternatives**  
    Alternatives: Concept Drift Detection, Model Performance Monitoring, Feature Monitoring, Evidently AI

11. **30-second explanation (your own words)**  
    Monitors production data distribution against training baseline using statistical tests to detect when data changes significantly, indicating potential need for model retraining.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
