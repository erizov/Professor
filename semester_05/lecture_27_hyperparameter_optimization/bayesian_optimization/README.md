# Bayesian Optimization

1. **Name of Algorithm**  
   Bayesian Optimization

2. **What problem does it solve? (1 sentence)**  
   Efficiently finds optimal hyperparameters by building a probabilistic model of the objective function and using it to select the most promising hyperparameters to evaluate next.

3. **Intuition (plain-language explanation)**  
   Like a smart explorer: instead of randomly trying places, build a map (probabilistic model) of where good results might be, then explore the most promising areas based on the map.

4. **Inputs & Outputs**  
   - Input: Hyperparameter search space, objective function to optimize, acquisition function, number of iterations.  
   - Output: Optimal hyperparameter configuration that maximizes/minimizes objective function.

5. **Step-by-step description (5–10 lines max)**  
1. Initialize with a few random hyperparameter evaluations.
2. Build probabilistic model (Gaussian Process) of objective function from observed evaluations.
3. Use acquisition function (e.g., Expected Improvement) to select next hyperparameters to evaluate.
4. Evaluate objective function at selected hyperparameters.
5. Update probabilistic model with new observation.
6. Repeat until budget exhausted; return best hyperparameters found.

6. **Tiny example (hand-simulated)**  
   Optimize learning_rate and batch_size for neural network: evaluate 5 random configs → GP models performance → acquisition suggests lr=0.001, batch=32 → evaluate → update model → suggest next → repeat → find optimal: lr=0.0005, batch=64.

7. **Time & Space Complexity**  
   - Time: O(n³) for GP inference where n is number of evaluations (much fewer evaluations than grid/random search).  
   - Space: O(n²) for GP covariance matrix.

8. **Strengths**  
- Requires fewer evaluations than grid/random search.
- Balances exploration and exploitation intelligently.

9. **Weaknesses / limitations**  
- GP inference becomes expensive with many evaluations.
- Assumes smooth objective function.

10. **Compare with alternatives**  
    Alternatives: Grid Search, Random Search, Tree-structured Parzen Estimators, Optuna

11. **30-second explanation (your own words)**  
    Uses probabilistic modeling and acquisition functions to intelligently select hyperparameters for evaluation, finding optima with fewer function evaluations than exhaustive search.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
