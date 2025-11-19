# Logistic Regression

1. **Name of Algorithm**  
   Logistic Regression

2. **What problem does it solve? (1 sentence)**  
   Models probability of binary classification by fitting a sigmoid curve to map features to probabilities between 0 and 1.

3. **Intuition (plain-language explanation)**  
   Instead of a straight line, use an S-shaped curve that squashes predictions into probability values.

4. **Inputs & Outputs**  
   - Input: Training data with features X and binary labels y ∈ {0, 1}.  
   - Output: Learned coefficients that define probability P(y=1|x) = 1/(1 + e^(-w·x - b)).

5. **Step-by-step description (5–10 lines max)**  
1. Initialize weights w and bias b.
2. Compute logits: z = X·w + b.
3. Apply sigmoid: p = 1/(1 + e^(-z)) to get probabilities.
4. Calculate cross-entropy loss: L = -Σ(y·log(p) + (1-y)·log(1-p)).
5. Update weights via gradient descent on loss function.
6. Repeat until convergence.

6. **Tiny example (hand-simulated)**  
   Predict spam: if email contains 'free' and 'money', probability = 0.85 → classify as spam (threshold 0.5).

7. **Time & Space Complexity**  
   - Time: O(n·m·i) for gradient descent iterations.  
   - Space: O(n·m) for data, O(m) for weights.

8. **Strengths**  
- Provides probability estimates, not just classifications.
- Fast, interpretable, and works well for linearly separable data.

9. **Weaknesses / limitations**  
- Assumes linear decision boundary in log-odds space.
- Requires feature scaling for stable convergence.

10. **Compare with alternatives**  
    Alternatives: Support Vector Machines, Decision Trees, Neural Networks

11. **30-second explanation (your own words)**  
Transform linear combination of features through sigmoid to output probabilities, then optimize to maximize likelihood of observed labels.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
