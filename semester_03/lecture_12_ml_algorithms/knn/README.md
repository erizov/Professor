# K-Nearest Neighbors (KNN)

1. **Name of Algorithm**  
   K-Nearest Neighbors (KNN)

2. **What problem does it solve? (1 sentence)**  
   Classifies or predicts by finding k most similar training examples and using their labels or values.

3. **Intuition (plain-language explanation)**  
   Ask your k closest neighbors what they think; the majority vote or average becomes your answer.

4. **Inputs & Outputs**  
   - Input: Training dataset, query point, and parameter k (number of neighbors).  
   - Output: Class label (classification) or predicted value (regression) for the query point.

5. **Step-by-step description (5–10 lines max)**  
1. Compute distance from query point to all training points.
2. Select k training points with smallest distances.
3. For classification: return majority class among k neighbors.
4. For regression: return mean (or weighted mean) of k neighbors' values.
5. Optionally use distance-weighted voting for better accuracy.

6. **Tiny example (hand-simulated)**  
   Classify point (3,4) with k=3: nearest neighbors are [(2,3)→A, (4,5)→A, (1,6)→B] → majority A → predict class A.

7. **Time & Space Complexity**  
   - Time: O(n·d) for each query, where n is training size and d is dimensions.  
   - Space: O(n·d) to store training data.

8. **Strengths**  
- Simple, non-parametric, and effective for non-linear problems.
- No training phase; learns from data lazily.

9. **Weaknesses / limitations**  
- Slow prediction on large datasets.
- Sensitive to irrelevant features and curse of dimensionality.

10. **Compare with alternatives**  
    Alternatives: Decision Trees, Support Vector Machines, Neural Networks

11. **30-second explanation (your own words)**  
    Find the k closest examples in feature space and use their outcomes to make a prediction for the new point.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
