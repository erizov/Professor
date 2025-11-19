# Naive Bayes

1. **Name of Algorithm**  
   Naive Bayes

2. **What problem does it solve? (1 sentence)**  
   Classifies instances using Bayes' theorem with the 'naive' assumption that features are conditionally independent given the class.

3. **Intuition (plain-language explanation)**  
   Calculate probability of each class given the features; pick the class with highest probability, assuming features don't influence each other.

4. **Inputs & Outputs**  
   - Input: Training data with features and class labels.  
   - Output: Learned prior probabilities P(class) and likelihoods P(feature|class) for classification.

5. **Step-by-step description (5–10 lines max)**  
1. Estimate prior probabilities: P(class) = count(class) / total_samples.
2. For each feature and class, estimate likelihood: P(feature|class) from training data.
3. For a new instance, compute posterior for each class: P(class|features) ∝ P(class) · Π P(feature_i|class).
4. Select class with maximum posterior probability.
5. Use Laplace smoothing to handle unseen feature values.

6. **Tiny example (hand-simulated)**  
   Classify email: P(spam|'free','money') ∝ P(spam)·P('free'|spam)·P('money'|spam) vs P(ham|'free','money') → choose max.

7. **Time & Space Complexity**  
   - Time: O(n·m) for training, O(m·c) for prediction, where c is number of classes.  
   - Space: O(m·c) to store probability tables.

8. **Strengths**  
- Fast training and prediction, works well with high-dimensional data.
- Handles missing values and requires little data to estimate parameters.

9. **Weaknesses / limitations**  
- Naive independence assumption is often violated in practice.
- Sensitive to irrelevant features.

10. **Compare with alternatives**  
    Alternatives: Logistic Regression, Decision Trees, Support Vector Machines

11. **30-second explanation (your own words)**  
    Use Bayes' rule to flip conditional probabilities, multiply feature likelihoods (assuming independence), and pick the most probable class.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
