# Random Forest

1. **Name of Algorithm**  
   Random Forest

2. **What problem does it solve? (1 sentence)**  
   Ensemble of decision trees that reduces variance and improves predictive accuracy by averaging many decorrelated trees.

3. **Intuition (plain-language explanation)**  
   Like asking many diverse experts and averaging their answers: each tree sees bootstrap samples and random feature subsets, so their errors cancel out.

4. **Inputs & Outputs**  
   - Input: Training dataset with features/labels, number of trees (n_estimators), maximum depth, feature subsampling rate.  
   - Output: Ensemble model producing class probabilities (classification) or average predictions (regression).

5. **Step-by-step description (5–10 lines max)**  
1. For each tree: draw bootstrap sample of data.
2. Grow decision tree to max depth or stopping criteria.
3. At each split, consider random subset of features.
4. Aggregate predictions of all trees (majority vote or mean).
5. Evaluate out-of-bag error for validation (optional).

6. **Tiny example (hand-simulated)**  
   Predict loan default: train 300 trees with max depth 10, feature subsample √d; aggregate votes for final decision.

7. **Time & Space Complexity**  
   - Time: O(n_trees · n_samples · log n_samples) typically, depending on depth and feature count.  
   - Space: O(n_trees · tree_size) to store all nodes.

8. **Strengths**  
- Handles high-dimensional, mixed-type data with minimal preprocessing.
- Robust to overfitting compared to single trees; provides feature importance.

9. **Weaknesses / limitations**  
- Large models consume memory and are slower at inference.
- Less interpretable than single trees; biased toward features with many levels.

10. **Compare with alternatives**  
    Alternatives: Gradient Boosted Trees, Extra Trees, Bagging with other base learners

11. **30-second explanation (your own words)**  
    Builds many randomized decision trees on bootstrap samples and aggregates their outputs, reducing variance and improving generalization.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
