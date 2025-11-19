# Optuna

1. **Name of Algorithm**  
   Optuna

2. **What problem does it solve? (1 sentence)**  
Automates hyperparameter optimization using state-of-the-art algorithms (TPE, CMA-ES) with efficient pruning and parallelization, making it easy to optimize complex search spaces.

3. **Intuition (plain-language explanation)**  
   Like an intelligent lab assistant: automatically suggests which experiments (hyperparameters) to try next, stops unpromising ones early (pruning), and learns from results to suggest better ones.

4. **Inputs & Outputs**  
- Input: Objective function, hyperparameter search space (define_param), optimization algorithm, pruning strategy.
   - Output: Optimal hyperparameter configuration and optimization history.

5. **Step-by-step description (5–10 lines max)**  
1. Define objective function that takes trial object and returns metric to optimize.
2. Use trial.suggest_* methods to define hyperparameter search space.
3. Create study object and specify optimization direction (minimize/maximize).
4. Run optimization: Optuna suggests hyperparameters, evaluates objective, updates model.
5. Apply pruning to stop unpromising trials early (e.g., MedianPruner).
6. After N trials, return best hyperparameters from study.best_params.

6. **Tiny example (hand-simulated)**  
   Optimize neural network: trial.suggest_float('lr', 1e-5, 1e-1, log=True), trial.suggest_int('layers', 1, 5) → Optuna uses TPE → suggests lr=0.001, layers=3 → evaluate → prune if bad → suggest next → after 100 trials → best: lr=0.0005, layers=4.

7. **Time & Space Complexity**  
   - Time: O(n·T(n)) where n is number of trials, T(n) is objective evaluation time (efficient pruning reduces effective n).  
   - Space: O(n) for storing trial history.

8. **Strengths**  
- Easy-to-use API with automatic algorithm selection.
- Efficient pruning and parallelization support.

9. **Weaknesses / limitations**  
- Requires defining objective function correctly.
- Pruning may stop trials too early in some cases.

10. **Compare with alternatives**  
    Alternatives: Hyperopt, Scikit-optimize, Bayesian Optimization, Grid/Random Search

11. **30-second explanation (your own words)**  
Automates hyperparameter optimization using advanced algorithms like TPE with intelligent trial suggestion, pruning, and parallelization for efficient search.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
