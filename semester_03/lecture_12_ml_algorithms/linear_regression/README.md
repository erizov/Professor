# Linear Regression

1. **Name of Algorithm**  
   Linear Regression

2. **What problem does it solve? (1 sentence)**  
   Fits a linear relationship between features and a continuous target variable to predict numeric outcomes.

3. **Intuition (plain-language explanation)**  
   Draw the best straight line through data points so predictions are as close as possible to actual values.

4. **Inputs & Outputs**  
   - Input: Training data with features X (n×m matrix) and target values y (n×1 vector).  
   - Output: Learned coefficients (weights) and intercept that define the linear model y = X·w + b.

5. **Step-by-step description (5–10 lines max)**  
1. Initialize weights w and bias b (often to zeros).
2. Compute predictions: ŷ = X·w + b.
3. Calculate loss (mean squared error): MSE = (1/n)Σ(y - ŷ)².
4. Update weights using gradient descent: w = w - α·∇w(MSE), b = b - α·∇b(MSE).
5. Repeat until convergence or max iterations.

6. **Tiny example (hand-simulated)**  
   Predict house price from size: price = 50,000 + 200·size. House of 100m² → price = 70,000.

7. **Time & Space Complexity**  
   - Time: O(n·m·i) for gradient descent, O(m³) for closed-form solution, where i is iterations.  
   - Space: O(n·m) for data, O(m) for weights.

8. **Strengths**  
- Simple, interpretable, and fast to train.
- Works well when relationship is approximately linear.

9. **Weaknesses / limitations**  
- Assumes linear relationship; fails on non-linear patterns.
- Sensitive to outliers and multicollinearity.

10. **Compare with alternatives**  
    Alternatives: Polynomial Regression, Ridge/Lasso Regression, Neural Networks

11. **30-second explanation (your own words)**  
    Find the line that minimizes squared prediction errors by adjusting slope and intercept through optimization.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
