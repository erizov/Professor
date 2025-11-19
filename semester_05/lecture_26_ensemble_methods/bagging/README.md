# Bagging (Bootstrap Aggregating)

1. **Name of Algorithm**  
   Bagging (Bootstrap Aggregating)

2. **What problem does it solve? (1 sentence)**  
   Reduces variance and overfitting by training multiple models on different bootstrap samples of the training data and averaging their predictions.

3. **Intuition (plain-language explanation)**  
   Like asking multiple experts who saw different parts of a situation: each trains on a different random sample, then combine their opinions (average) for a more stable, reliable answer.

4. **Inputs & Outputs**  
- Input: Training dataset, base learning algorithm, number of models (bootstrap samples).
   - Output: Ensemble model that averages predictions from multiple base models.

5. **Step-by-step description (5–10 lines max)**  
1. Create B bootstrap samples by randomly sampling with replacement from training data.
2. Train a base model on each bootstrap sample independently.
3. For regression: average predictions from all B models.
4. For classification: use majority voting or average class probabilities.
5. Each model sees ~63% of unique training examples (bootstrap sampling).
6. Out-of-bag samples (~37%) can be used for validation.

6. **Tiny example (hand-simulated)**  
   Random Forest: 100 decision trees, each trained on different bootstrap sample → predict class → majority vote → final prediction. Reduces variance compared to single tree.

7. **Time & Space Complexity**  
   - Time: O(B·T(n)) where B is number of models, T(n) is training time per model (parallelizable).  
   - Space: O(B·M) where M is model size (stores B models).

8. **Strengths**  
- Reduces variance and overfitting effectively.
- Models can be trained in parallel.

9. **Weaknesses / limitations**  
- Does not reduce bias (if base model is biased, ensemble is too).
- Requires more memory and computation than single model.

10. **Compare with alternatives**  
    Alternatives: Boosting, Stacking, Random Forest (specialized bagging), Single Model

11. **30-second explanation (your own words)**  
    Trains multiple models on bootstrap samples and averages their predictions, reducing variance and improving generalization through model diversity.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
