# Decision Tree

1. **Name of Algorithm**  
   Decision Tree

2. **What problem does it solve? (1 sentence)**  
   Builds a tree structure that makes decisions by splitting data on feature values to classify or predict outcomes.

3. **Intuition (plain-language explanation)**  
   Like a flowchart: ask yes/no questions about features, branch based on answers, and reach a conclusion at the leaves.

4. **Inputs & Outputs**  
   - Input: Training dataset with features and labels (classification) or target values (regression).  
   - Output: Tree model that can classify new instances or predict continuous values.

5. **Step-by-step description (5–10 lines max)**  
1. Start with root node containing all training data.
2. For each node, find the best feature and threshold to split on (maximize information gain or minimize Gini impurity).
3. Create child nodes for each split outcome.
4. Recursively build subtrees until stopping criteria (max depth, min samples, pure nodes).
5. Assign class label or value to leaf nodes based on majority class or mean value.

6. **Tiny example (hand-simulated)**  
   Classify fruit: if color=red and size>5cm → apple; if color=yellow → banana; else → orange.

7. **Time & Space Complexity**  
   - Time: O(n·m·log n) for training, where n is samples and m is features.  
   - Space: O(n·m) for storing tree structure.

8. **Strengths**  
- Interpretable and easy to visualize.
- Handles non-linear relationships and feature interactions.

9. **Weaknesses / limitations**  
- Prone to overfitting without regularization.
- Sensitive to small data changes (unstable).

10. **Compare with alternatives**  
    Alternatives: Random Forest, Gradient Boosting, Neural Networks

11. **30-second explanation (your own words)**  
    Recursively partition data by asking questions about features until reaching pure groups that can be labeled.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
