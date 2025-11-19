# A/B Testing

1. **Name of Algorithm**  
   A/B Testing

2. **What problem does it solve? (1 sentence)**  
   Compares two or more variants (A, B, etc.) of a model, feature, or system to determine which performs better using statistical hypothesis testing, enabling data-driven decision making.

3. **Intuition (plain-language explanation)**  
   Like a scientific experiment: split users into groups, show each group a different version (A or B), measure outcomes, and use statistics to determine which version is truly better, not just due to random chance.

4. **Inputs & Outputs**  
   - Input: User traffic, variant assignments (A/B), success metrics (conversion rate, click-through rate, etc.), sample size, significance level.  
   - Output: Statistical test results (p-value, confidence intervals), recommendation on which variant to deploy.

5. **Step-by-step description (5–10 lines max)**  
1. Randomly assign users to control (A) and treatment (B) groups.
2. Run experiment for sufficient duration to collect statistically significant sample size.
3. Collect metrics: conversion rates, engagement, revenue, etc. for each group.
4. Calculate test statistic (e.g., difference in means, chi-square for proportions).
5. Perform statistical test (t-test, z-test, chi-square) to compute p-value.
6. Compare p-value to significance level (α, typically 0.05): if p < α, reject null hypothesis (variants differ).
7. Calculate confidence intervals for effect size.
8. Make decision: deploy winning variant if statistically significant and practically meaningful.

6. **Tiny example (hand-simulated)**  
   E-commerce: 10,000 users → 5,000 see old checkout (A), 5,000 see new checkout (B) → A: 2% conversion, B: 2.5% conversion → t-test: p=0.01 < 0.05 → B is significantly better → deploy B.

7. **Time & Space Complexity**  
   - Time: O(n) where n is number of users/events (linear in data collection).  
   - Space: O(n) for storing user assignments and metrics.

8. **Strengths**  
- Provides statistical rigor for decision making.
- Reduces risk of deploying changes that hurt performance.

9. **Weaknesses / limitations**  
- Requires sufficient sample size and time.
- May not capture long-term effects or edge cases.

10. **Compare with alternatives**  
    Alternatives: Multi-armed Bandits, Canary Deployments, Shadow Testing, Simulation

11. **30-second explanation (your own words)**  
    Uses controlled experiments with statistical hypothesis testing to compare variants and make data-driven decisions about which version performs better.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
