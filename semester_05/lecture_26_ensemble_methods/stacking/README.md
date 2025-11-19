# Stacking (Stacked Generalization)

1. **Name of Algorithm**  
   Stacking (Stacked Generalization)

2. **What problem does it solve? (1 sentence)**  
   Combines predictions from diverse base models using a meta-learner that learns how to best combine their outputs, often achieving better performance than voting or averaging.

3. **Intuition (plain-language explanation)**  
   Like a committee with a smart chairperson: base models (committee members) make predictions, then meta-learner (chairperson) learns the best way to combine their opinions.

4. **Inputs & Outputs**  
   - Input: Training data, diverse base models (level-0), meta-learner (level-1), cross-validation strategy.  
   - Output: Two-level ensemble: base models + meta-learner that combines their predictions.

5. **Step-by-step description (5–10 lines max)**  
1. Split training data into K folds for cross-validation.
2. For each fold: train base models on K-1 folds, generate predictions on held-out fold.
3. Collect out-of-fold predictions from all base models to create meta-features.
4. Train meta-learner on meta-features (predictions) with true labels.
5. Retrain all base models on full training data.
6. Final prediction: base models predict → meta-learner combines predictions.

6. **Tiny example (hand-simulated)**  
   Base models: SVM, Random Forest, Neural Net → 5-fold CV → each generates predictions on held-out fold → meta-features: [SVM_pred, RF_pred, NN_pred] → meta-learner (logistic regression) learns weights → final: weighted combination.

7. **Time & Space Complexity**  
   - Time: O(K·(B·T(n) + M(m))) where K is folds, B is base models, M is meta-learner training (expensive due to CV).  
   - Space: O(B·M_b + M_m) for base models and meta-learner.

8. **Strengths**  
- Can capture complex interactions between base models.
- Often outperforms simple voting/averaging.

9. **Weaknesses / limitations**  
- More complex and computationally expensive.
- Requires careful cross-validation to avoid overfitting.

10. **Compare with alternatives**  
    Alternatives: Bagging, Boosting, Voting, Blending

11. **30-second explanation (your own words)**  
    Uses a meta-learner trained on base model predictions to learn optimal combination strategy, creating a two-level ensemble that leverages model diversity.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
