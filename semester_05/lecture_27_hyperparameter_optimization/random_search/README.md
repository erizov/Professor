# Random Search

1. **Name of Algorithm**  
   Random Search

2. **What problem does it solve? (1 sentence)**  
   Searches hyperparameter space by randomly sampling configurations, often finding good solutions faster than grid search, especially when some hyperparameters are more important than others.

3. **Intuition (plain-language explanation)**  
   Like throwing darts randomly: instead of checking every spot on a grid, randomly sample hyperparameter combinations. Often finds good solutions faster, especially if only a few hyperparameters matter.

4. **Inputs & Outputs**  
   - Input: Hyperparameter search space (distributions for each hyperparameter), objective function, number of random samples.  
   - Output: Best hyperparameter configuration from random samples.

5. **Step-by-step description (5–10 lines max)**  
1. Define probability distributions for each hyperparameter (uniform, log-uniform, etc.).
2. Randomly sample N hyperparameter configurations from these distributions.
3. For each sampled configuration: train model and evaluate using cross-validation.
4. Record performance metric for each configuration.
5. Select configuration with best performance metric.
6. Optionally retrain on full data with best hyperparameters.

6. **Tiny example (hand-simulated)**  
   SVM: sample C from log-uniform(0.001, 100), gamma from log-uniform(0.0001, 1) → randomly sample 50 configurations → evaluate each → find best: C=2.3, gamma=0.05 with 91% accuracy (faster than 9×9=81 grid points).

7. **Time & Space Complexity**  
   - Time: O(N·T(n)) where N is number of random samples, T(n) is training time (linear in samples, parallelizable).  
   - Space: O(1) for search (only stores best so far).

8. **Strengths**  
- Faster than grid search for high-dimensional spaces.
- Can explore continuous spaces more effectively.
- Easy to parallelize.

9. **Weaknesses / limitations**  
- No guarantee of finding optimal solution.
- May waste evaluations on poor regions.

10. **Compare with alternatives**  
    Alternatives: Grid Search, Bayesian Optimization, Optuna, Hyperopt

11. **30-second explanation (your own words)**  
    Randomly samples hyperparameter configurations from defined distributions, often finding good solutions more efficiently than exhaustive grid search, especially in high-dimensional spaces.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
