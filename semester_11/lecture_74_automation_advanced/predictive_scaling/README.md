# Predictive Scaling

1. **Name of Algorithm**  
   Predictive Scaling

2. **What problem does it solve? (1 sentence)**  
   Predicts future demand using machine learning and historical patterns, scaling resources proactively before demand increases, reducing latency and improving user experience.

3. **Intuition (plain-language explanation)**  
   Like weather forecasting: Predictive Scaling is like weather forecasting for traffic - you predict when it will be busy (demand spike) and prepare ahead of time (scale up) - just as weather forecasts help you prepare for rain, predictive scaling helps you prepare for traffic spikes, ensuring smooth performance.

4. **Inputs & Outputs**  
   - Input: Historical metrics, time series data, patterns, ML models, scaling policies, prediction horizon.  
   - Output: Demand predictions, proactive scaling, reduced latency, optimized resources, improved performance.

5. **Step-by-step description (5–10 lines max)**  
1. Collect: collect historical metrics and patterns.
2. Train: train ML models on historical data.
3. Predict: predict future demand using models.
4. Analyze: analyze prediction confidence and patterns.
5. Decide: decide when to scale based on predictions.
6. Scale: scale resources proactively before demand spike.
7. Monitor: monitor actual demand vs predictions.
8. Adjust: adjust scaling based on actual demand.
9. Learn: learn from prediction accuracy to improve models.
10. Optimize: optimize predictions and scaling policies.

6. **Tiny example (hand-simulated)**  
   Predictive Scaling: history: traffic spikes at 9 AM daily → predict: spike expected in 15 minutes → scale: preemptively scale up → result: handle spike without latency → actual: spike occurs as predicted → adjust: scale down after spike → Predictive Scaling successful.

7. **Time & Space Complexity**  
   - Time: O(t + p + s) where t is training time, p is prediction time, s is scaling time (continuous).  
   - Space: O(m + d) where m is model storage, d is data storage (historical metrics).

8. **Strengths**  
- Proactive: scales before demand increases, reducing latency.
- Performance: maintains performance during traffic spikes.
- Efficiency: optimizes resource usage through predictions.

9. **Weaknesses / limitations**  
- Accuracy: predictions may not always be accurate.
- Complexity: requires ML models and historical data.
- Overscaling: may scale more than necessary.

10. **Compare with alternatives**  
    Alternatives: Reactive Scaling, Scheduled Scaling, Fixed Capacity, Basic Auto-Scaling

11. **30-second explanation (your own words)**  
    Predicts future demand using machine learning and historical patterns, scaling resources proactively before demand increases, reducing latency and improving user experience.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
