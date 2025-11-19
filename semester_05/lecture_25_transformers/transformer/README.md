# Transformer

1. **Name of Algorithm**  
   Transformer

2. **What problem does it solve? (1 sentence)**  
   Replaces recurrent and convolutional layers with self-attention mechanisms, enabling parallel processing and better handling of long-range dependencies in sequences.

3. **Intuition (plain-language explanation)**  
   Like a team meeting where everyone can talk to everyone simultaneously: instead of passing messages sequentially (RNN), all positions attend to all others at once, seeing the full context immediately.

4. **Inputs & Outputs**  
   - Input: Input sequences (source and/or target), token embeddings, position encodings.  
   - Output: Output sequences (for translation, generation, etc.) or representations (for understanding).

5. **Step-by-step description (5–10 lines max)**  
1. Create input embeddings and add positional encodings (sinusoidal or learned).
2. Encoder: apply multi-head self-attention + feed-forward network (repeat N times).
3. Decoder: apply masked self-attention (causal) + cross-attention to encoder + feed-forward (repeat N times).
4. Use layer normalization and residual connections around each sub-layer.
5. Final linear layer and softmax for output predictions.
6. Train end-to-end with backpropagation.

6. **Tiny example (hand-simulated)**  
   Translation: 'Hello world' (English) → encoder creates representations → decoder attends to encoder + generates 'Bonjour le monde' (French) token by token, attending to relevant source words.

7. **Time & Space Complexity**  
   - Time: O(n²·d) where n is sequence length, d is dimension (parallelizable, but quadratic attention).  
   - Space: O(n²) for attention matrices plus O(d²) for parameters per layer.

8. **Strengths**  
- Parallel processing enables faster training than RNNs.
- Self-attention captures long-range dependencies effectively.

9. **Weaknesses / limitations**  
- Quadratic memory and computation in sequence length.
- Requires large amounts of data for effective training.

10. **Compare with alternatives**  
    Alternatives: RNN/LSTM, CNN, Sparse Transformers, Linear Transformers

11. **30-second explanation (your own words)**  
    Uses stacked self-attention and feed-forward layers with residual connections, replacing recurrence with parallel attention mechanisms to process sequences efficiently.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
