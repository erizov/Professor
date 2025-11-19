# Multi-Armed Bandit (MAB) for ML

1. **Name of Algorithm**  
   Multi-Armed Bandit (MAB) for ML

2. **What problem does it solve? (1 sentence)**  
   Dynamically allocates traffic between multiple ML model variants using bandit algorithms, automatically favoring better-performing models while continuing to explore alternatives, balancing exploitation and exploration.

3. **Intuition (plain-language explanation)**  
   Like a smart gambler at slot machines: try different machines (models) to see which pays more, but gradually play the winning machine more often while still occasionally trying others - automatically finds the best model and allocates traffic accordingly.

4. **Inputs & Outputs**  
- Input: Multiple model variants (arms), traffic allocation algorithm (ε-greedy, UCB, Thompson Sampling), reward metric (accuracy, revenue, engagement), exploration rate.
   - Output: Dynamic traffic allocation across models, with better models receiving more traffic over time.

5. **Step-by-step description (5–10 lines max)**  
1. Initialize multiple model variants (arms): each model is a different 'arm' to pull.
2. Start with equal traffic allocation: route traffic uniformly across all models.
3. Collect rewards: measure performance metric (e.g., conversion rate, accuracy) for each model.
4. Update arm estimates: track average reward for each model variant.
5. Apply bandit algorithm: ε-greedy (explore ε% of time, exploit best model rest), UCB (upper confidence bound), or Thompson Sampling (probabilistic).
6. Allocate traffic: route more traffic to models with higher estimated rewards.
7. Continue exploration: still allocate some traffic to other models to discover improvements.
8. Converge: over time, best model receives most traffic while maintaining exploration.

6. **Tiny example (hand-simulated)**  
   Recommendation system: 3 models (A, B, C) → start: 33% traffic each → measure: A=2% conversion, B=2.5% conversion, C=2.2% conversion → UCB algorithm → allocate: A=20%, B=50%, C=30% → continue: B performs best → converge: B=80%, A=10%, C=10%.

7. **Time & Space Complexity**  
   - Time: O(N·T) where N is number of arms (models), T is time steps (traffic allocation updates per request or batch).  
   - Space: O(N·M) where N is number of models, M is model size, plus O(N) for tracking arm statistics.

8. **Strengths**  
- Automatic optimization: finds best model without manual A/B testing.
- Adaptive: adjusts allocation as model performance changes.
- Balances exploration and exploitation: continues to try alternatives.

9. **Weaknesses / limitations**  
- Requires sufficient traffic to converge to optimal allocation.
- May take time to identify best model if differences are small.

10. **Compare with alternatives**  
    Alternatives: A/B Testing, Blue-Green Deployment, Canary Deployment, Fixed Traffic Allocation

11. **30-second explanation (your own words)**  
    Dynamically allocates traffic across multiple ML model variants using bandit algorithms, automatically favoring better-performing models while maintaining exploration to discover improvements.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
