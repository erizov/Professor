# Advanced Support Vector Machine

1. **Name of Algorithm**  
   Advanced Support Vector Machine

2. **What problem does it solve? (1 sentence)**  
   Finds a maximum-margin hyperplane separating classes (or regression function) using kernel tricks to operate in high-dimensional feature spaces.

3. **Intuition (plain-language explanation)**  
   Transform data into a space where classes are linearly separable and place the widest possible margin between them while penalizing misclassifications.

4. **Inputs & Outputs**  
   - Input: Training data (features, labels), kernel choice (linear, RBF, polynomial), regularization parameter C, kernel-specific hyperparameters (γ, degree).  
   - Output: Support vectors, learned weights/bias (or dual coefficients), decision function for classification or regression.

5. **Step-by-step description (5–10 lines max)**  
1. Choose kernel and hyperparameters to map data into feature space.
2. Formulate optimization problem maximizing margin with slack penalties.
3. Solve quadratic programming problem (dual) to find support vectors.
4. Compute decision boundary using support vectors and kernel evaluations.
5. Tune hyperparameters via cross-validation; use model for inference.

6. **Tiny example (hand-simulated)**  
   RBF-kernel SVM on non-linear spiral dataset: γ controls kernel width, C balances margin width vs. training errors; resulting boundary wraps around spirals.

7. **Time & Space Complexity**  
   - Time: Training O(n²) to O(n³) for n samples (QP solver); prediction O(n_sv · d_k) where n_sv is number of support vectors.  
   - Space: O(n_sv · d) to store support vectors and coefficients.

8. **Strengths**  
- Effective in high-dimensional spaces with clear margins.
- Kernel trick enables flexible non-linear boundaries.

9. **Weaknesses / limitations**  
- Training scales poorly with large datasets.
- Requires careful kernel and hyperparameter tuning.

10. **Compare with alternatives**  
    Alternatives: Logistic Regression, Random Forest, Neural Networks/Deep Learning

11. **30-second explanation (your own words)**  
    Maximizes the separation margin between classes and uses kernel functions to implicitly project data into feature spaces where linear separation is feasible.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
