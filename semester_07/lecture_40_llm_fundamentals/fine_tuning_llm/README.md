# Fine-Tuning LLM

1. **Name of Algorithm**  
   Fine-Tuning LLM

2. **What problem does it solve? (1 sentence)**  
   Adapts pre-trained large language models to specific tasks or domains by continuing training on task-specific data, enabling high performance on downstream tasks with relatively little data.

3. **Intuition (plain-language explanation)**  
   Like a generalist doctor specializing: start with a doctor who knows medicine broadly (pre-trained LLM), then train them on specific cases (fine-tuning data) - they keep their general knowledge but become expert in your specialty (your task).

4. **Inputs & Outputs**  
   - Input: Pre-trained LLM (GPT, BERT, etc.), task-specific training data, fine-tuning hyperparameters (learning rate, batch size, epochs).  
   - Output: Fine-tuned model adapted to specific task, improved performance on target domain.

5. **Step-by-step description (5–10 lines max)**  
1. Load pre-trained model: initialize model with pre-trained weights (from GPT, BERT, etc.).
2. Prepare task data: format task-specific data (classification, QA, generation) for model input.
3. Add task head (if needed): add task-specific layers (classifier, decoder) on top of base model.
4. Set learning rate: use lower learning rate than pre-training (typically 1e-5 to 1e-4) to avoid catastrophic forgetting.
5. Train on task data: run forward pass, compute loss, backpropagate, update weights (only fine-tune or freeze some layers).
6. Monitor performance: track validation metrics to prevent overfitting on small task datasets.
7. Early stopping: stop training when validation performance plateaus to avoid overfitting.
8. Evaluate: test fine-tuned model on held-out test set to measure task performance.

6. **Tiny example (hand-simulated)**  
   Sentiment analysis: load GPT-3 → add classification head → fine-tune on 10K labeled reviews (positive/negative) → learning rate 2e-5, 3 epochs → model learns to classify sentiment → accuracy: 95% on test set (vs 60% with zero-shot).

7. **Time & Space Complexity**  
   - Time: O(E·D·M) where E is epochs, D is dataset size, M is model size (much faster than pre-training since fewer epochs and smaller dataset).  
   - Space: O(M) for model weights, O(B·S) for batch data where B is batch size, S is sequence length.

8. **Strengths**  
- High performance: achieves strong results with relatively little task-specific data.
- Efficient: much faster and cheaper than training from scratch.
- Transfer learning: leverages knowledge from pre-training.

9. **Weaknesses / limitations**  
- Catastrophic forgetting: may forget general knowledge if fine-tuned too aggressively.
- Data requirements: still needs some task-specific labeled data.
- Overfitting risk: small datasets may cause overfitting.

10. **Compare with alternatives**  
    Alternatives: Zero-shot Learning, Few-shot Learning, Prompt Tuning, Adapter Layers

11. **30-second explanation (your own words)**  
    Adapts pre-trained large language models to specific tasks by continuing training on task-specific data, enabling high performance on downstream tasks with relatively little data through transfer learning.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
