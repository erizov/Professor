# Grid Search

1. **Name of Algorithm**  
   Grid Search

2. **What problem does it solve? (1 sentence)**  
   Exhaustively searches hyperparameter space by evaluating all combinations of specified hyperparameter values on a predefined grid.

3. **Intuition (plain-language explanation)**  
   Like checking every intersection on a map: systematically try every combination of hyperparameter values in a grid pattern to find the best one.

4. **Inputs & Outputs**  
   - Input: Hyperparameter search space (discrete values for each hyperparameter), objective function, cross-validation strategy.  
   - Output: Best hyperparameter combination from the grid that optimizes objective function.

5. **Step-by-step description (5–10 lines max)**  
1. Define hyperparameter grid: specify discrete values for each hyperparameter.
2. Generate all combinations of hyperparameter values (Cartesian product).
3. For each combination: train model and evaluate using cross-validation.
4. Record performance metric (e.g., accuracy, F1-score) for each combination.
5. Select combination with best performance metric.
6. Optionally retrain on full data with best hyperparameters.

6. **Tiny example (hand-simulated)**  
   SVM hyperparameters: C ∈ [0.1, 1, 10], gamma ∈ [0.001, 0.01, 0.1] → 3×3 = 9 combinations → evaluate each with 5-fold CV → find best: C=1, gamma=0.01 with 92% accuracy.

7. **Time & Space Complexity**  
   - Time: O(∏(n_i)·T(n)) where n_i is values per hyperparameter, T(n) is training time (exponential in number of hyperparameters).  
   - Space: O(1) for search (only stores best so far).

8. **Strengths**  
- Simple, straightforward, and guaranteed to find best in grid.
- No assumptions about hyperparameter space.

9. **Weaknesses / limitations**  
- Exponential growth with number of hyperparameters (curse of dimensionality).
- May miss optimal values not on the grid.

10. **Compare with alternatives**  
    Alternatives: Random Search, Bayesian Optimization, Optuna, Hyperopt

11. **30-second explanation (your own words)**  
    Exhaustively evaluates all combinations of hyperparameter values on a predefined grid, systematically searching the space to find optimal configuration.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
