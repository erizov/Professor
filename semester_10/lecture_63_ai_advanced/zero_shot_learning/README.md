# Zero-Shot Learning

1. **Name of Algorithm**  
   Zero-Shot Learning

2. **What problem does it solve? (1 sentence)**  
   Enables models to recognize or classify objects from classes they have never seen during training by leveraging semantic relationships, attribute descriptions, or text descriptions to generalize to unseen classes.

3. **Intuition (plain-language explanation)**  
   Like recognizing something you've never seen: zero-shot learning is like recognizing a new animal you've never seen before by describing it - if someone says 'it's like a cat but bigger with stripes' (semantic description), you can identify it as a tiger even though you've never seen one - zero-shot learning does this for AI: it uses descriptions, attributes, or relationships (like 'tiger is a big cat with stripes') to recognize new classes without training examples.

4. **Inputs & Outputs**  
   - Input: Unseen class descriptions, semantic embeddings, attribute vectors, text descriptions, seen class knowledge.  
   - Output: Predictions for unseen classes, generalized classification, zero-shot recognition.

5. **Step-by-step description (5–10 lines max)**  
1. Train on seen: train model on seen classes with descriptions/attributes.
2. Learn embeddings: learn semantic embeddings for classes and attributes.
3. Build mapping: build mapping between visual features and semantic space.
4. Describe unseen: provide semantic descriptions for unseen classes.
5. Project: project unseen class descriptions into semantic space.
6. Match: match test samples to unseen classes in semantic space.
7. Generalize: generalize from seen to unseen using semantic relationships.
8. Predict: predict unseen class labels based on semantic similarity.
9. Validate: validate zero-shot performance on unseen classes.
10. Refine: refine semantic representations for better generalization.

6. **Tiny example (hand-simulated)**  
   Zero-shot learning: train on: cats, dogs, birds (seen classes) → learn: visual features and semantic attributes (furry, has wings, etc.) → unseen: tiger (never seen) → description: 'big cat with stripes, furry' → match: test image features to semantic description → predict: tiger → zero-shot learning successful.

7. **Time & Space Complexity**  
   - Time: O(n_s) for training on seen classes where n_s is seen class data, O(1) for zero-shot inference.  
   - Space: O(m + a) where m is model size, a is attribute/semantic space size.

8. **Strengths**  
- Generalization: enables recognition of classes without training examples.
- Scalability: can handle many unseen classes without retraining.
- Flexibility: works with various semantic representations (attributes, text, embeddings).

9. **Weaknesses / limitations**  
- Semantic gap: semantic descriptions may not capture all visual characteristics.
- Performance: typically lower accuracy than supervised learning.
- Dependency: requires good semantic representations for unseen classes.

10. **Compare with alternatives**  
    Alternatives: Few-Shot Learning, Transfer Learning, Open-Set Recognition, Attribute-Based Classification

11. **30-second explanation (your own words)**  
    Enables models to recognize or classify objects from classes they have never seen during training by leveraging semantic relationships, attribute descriptions, or text descriptions to generalize to unseen classes.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
