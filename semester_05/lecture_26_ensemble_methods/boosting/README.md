# Boosting

1. **Name of Algorithm**  
   Boosting

2. **What problem does it solve? (1 sentence)**  
   Sequentially trains weak learners, each focusing on examples that previous learners got wrong, combining them into a strong ensemble that reduces both bias and variance.

3. **Intuition (plain-language explanation)**  
   Like a student learning from mistakes: first model makes errors, second model focuses on those mistakes, third focuses on remaining errors, until the ensemble gets it right.

4. **Inputs & Outputs**  
   - Input: Training dataset, weak learning algorithm, number of iterations, loss function.  
   - Output: Weighted ensemble of weak learners that progressively improves performance.

5. **Step-by-step description (5–10 lines max)**  
1. Initialize equal weights for all training examples.
2. For each iteration: train weak learner on weighted data.
3. Calculate error rate and update example weights (increase weights for misclassified examples).
4. Calculate learner weight based on its accuracy.
5. Add weighted learner to ensemble.
6. Final prediction: weighted sum of all learners' predictions.

6. **Tiny example (hand-simulated)**  
   AdaBoost: iteration 1 → tree misclassifies 3 examples → increase their weights → iteration 2 → tree focuses on those 3 → repeat → final: weighted combination of all trees.

7. **Time & Space Complexity**  
   - Time: O(T·M(n)) where T is iterations, M(n) is training time per weak learner (sequential, not parallelizable).  
   - Space: O(T·M) for T models plus O(n) for example weights.

8. **Strengths**  
- Reduces both bias and variance.
- Can achieve high accuracy with weak base learners.

9. **Weaknesses / limitations**  
- Sequential training (cannot parallelize easily).
- Sensitive to noisy data and outliers.

10. **Compare with alternatives**  
    Alternatives: Bagging, Stacking, Gradient Boosting, XGBoost/LightGBM

11. **30-second explanation (your own words)**  
    Sequentially trains weak learners that focus on previously misclassified examples, combining them into a strong ensemble through weighted voting.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
