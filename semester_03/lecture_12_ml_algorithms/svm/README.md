# Support Vector Machine (SVM)

1. **Name of Algorithm**  
   Support Vector Machine (SVM)

2. **What problem does it solve? (1 sentence)**  
   Finds the optimal hyperplane that maximally separates classes by maximizing the margin between support vectors.

3. **Intuition (plain-language explanation)**  
   Draw the widest possible 'street' between classes; the boundary is the middle line, and support vectors are the closest points on each side.

4. **Inputs & Outputs**  
   - Input: Training data with features X and class labels y ∈ {-1, +1}.  
   - Output: Learned weights w and bias b defining the separating hyperplane w·x + b = 0.

5. **Step-by-step description (5–10 lines max)**  
1. Formulate optimization: minimize ||w||² subject to y_i(w·x_i + b) ≥ 1 for all points.
2. Solve using quadratic programming or gradient descent on dual form.
3. Identify support vectors (points on margin boundaries).
4. Compute decision boundary from support vectors.
5. For non-linear data, use kernel trick (RBF, polynomial) to map to higher dimensions.

6. **Tiny example (hand-simulated)**  
   Separate two classes with maximum margin: hyperplane equidistant from closest points of each class.

7. **Time & Space Complexity**  
   - Time: O(n²·m) to O(n³) depending on solver, where n is samples and m is features.  
   - Space: O(n·m) for data, O(s) for support vectors where s << n typically.

8. **Strengths**  
- Effective in high-dimensional spaces and with clear margin of separation.
- Memory efficient (uses only support vectors).

9. **Weaknesses / limitations**  
- Does not perform well on large datasets or with overlapping classes.
- Requires careful kernel and parameter selection.

10. **Compare with alternatives**  
    Alternatives: Logistic Regression, Neural Networks, Random Forest

11. **30-second explanation (your own words)**  
    Maximize the gap between classes by finding the hyperplane that is farthest from the nearest points of each class.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
