# Model Versioning

1. **Name of Algorithm**  
   Model Versioning

2. **What problem does it solve? (1 sentence)**  
   Tracks and manages different versions of machine learning models, their code, data, hyperparameters, and artifacts, enabling reproducibility, rollback, and model lineage tracking.

3. **Intuition (plain-language explanation)**  
   Like version control for code, but for models: track which model version was trained with which data and code, so you can reproduce results, compare versions, and roll back if a new version performs worse.

4. **Inputs & Outputs**  
   - Input: Model artifacts (weights, architecture), training code, training data references, hyperparameters, metrics, metadata.  
   - Output: Versioned model registry, model metadata database, APIs for model retrieval and deployment.

5. **Step-by-step description (5–10 lines max)**  
1. Register model: assign unique version identifier (e.g., v1.0.0, git commit hash).
2. Store model artifacts: save model weights, architecture definition, preprocessing code.
3. Record metadata: training data version, hyperparameters, training metrics, timestamp, author.
4. Tag models: mark as 'production', 'staging', 'experimental'.
5. Enable model retrieval: query by version, tag, or metadata to fetch specific model.
6. Track model lineage: link model to training data, code, and parent models (if fine-tuned).
7. Compare versions: side-by-side comparison of metrics, hyperparameters, data.
8. Enable rollback: promote previous version to production if new version fails.

6. **Tiny example (hand-simulated)**  
   Image classifier: v1.0.0 trained on 100K images, accuracy 92% → v1.1.0 trained on 200K images, accuracy 94% → deploy v1.1.0 → performance drops → rollback to v1.0.0 → investigate issue.

7. **Time & Space Complexity**  
   - Time: O(1) for version operations (metadata lookups), O(size) for storing/retrieving model artifacts.  
   - Space: O(V·M) where V is number of versions, M is model size (storage for all versions).

8. **Strengths**  
- Enables reproducibility and model comparison.
- Allows safe experimentation with ability to rollback.

9. **Weaknesses / limitations**  
- Requires storage for multiple model versions.
- May need cleanup policies to manage storage costs.

10. **Compare with alternatives**  
    Alternatives: MLflow, Weights & Biases, DVC, Model Registry, Git LFS

11. **30-second explanation (your own words)**  
    Tracks and manages model versions with associated metadata, code, and data, enabling reproducibility, comparison, and safe deployment with rollback capabilities.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
