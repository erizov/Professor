# Bias Mitigation

1. **Name of Algorithm**  
   Bias Mitigation

2. **What problem does it solve? (1 sentence)**  
   Identifies and reduces bias in machine learning models and datasets, ensuring fair and equitable AI systems that don't discriminate against protected groups or perpetuate harmful stereotypes.

3. **Intuition (plain-language explanation)**  
   Like removing bias from decisions: Bias Mitigation is like removing bias from human decisions - you identify where bias exists (in data, models), understand how it affects outcomes (unfair treatment), and fix it (mitigation techniques) - just as we work to remove human bias, we work to remove AI bias to ensure fairness.

4. **Inputs & Outputs**  
   - Input: Training data, models, bias metrics, fairness criteria, demographic data, mitigation techniques.  
   - Output: Debiased models, fair predictions, reduced bias metrics, fairness reports, equitable AI systems.

5. **Step-by-step description (5–10 lines max)**  
1. Detect: detect bias in data and models.
2. Measure: measure bias using fairness metrics.
3. Analyze: analyze sources of bias.
4. Mitigate: apply bias mitigation techniques (pre-processing, in-processing, post-processing).
5. Balance: balance datasets if needed.
6. Train: train models with bias mitigation.
7. Evaluate: evaluate fairness metrics.
8. Validate: validate fairness improvements.
9. Monitor: monitor for bias in production.
10. Iterate: iterate to improve fairness.

6. **Tiny example (hand-simulated)**  
   Bias Mitigation: data: hiring dataset → detect: gender bias detected → measure: 30% gender gap → mitigate: apply fairness constraints → train: train fair model → evaluate: gender gap reduced to 5% → result: fair hiring model → Bias Mitigation successful.

7. **Time & Space Complexity**  
   - Time: O(d + t + e) where d is detection time, t is training time, e is evaluation time (varies by technique).  
   - Space: O(m + d) where m is model storage, d is data storage (training data, demographic data).

8. **Strengths**  
- Fairness: improves fairness and equity in AI systems.
- Compliance: helps meet fairness and anti-discrimination requirements.
- Trust: increases trust in AI systems.

9. **Weaknesses / limitations**  
- Trade-offs: may trade accuracy for fairness.
- Complexity: bias mitigation can be complex.
- Definition: defining fairness can be challenging.

10. **Compare with alternatives**  
    Alternatives: No Mitigation, Data Balancing, Fairness Constraints, Post-Processing

11. **30-second explanation (your own words)**  
    Identifies and reduces bias in machine learning models and datasets, ensuring fair and equitable AI systems that don't discriminate against protected groups or perpetuate harmful stereotypes.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
