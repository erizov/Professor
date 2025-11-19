# Attention Mechanisms

1. **Name of Algorithm**  
   Attention Mechanisms

2. **What problem does it solve? (1 sentence)**  
   Enables models to focus on relevant parts of input sequence when generating each output token, allowing capture of long-range dependencies and context-aware representations in sequence-to-sequence tasks.

3. **Intuition (plain-language explanation)**  
   Like reading a long document and highlighting important sentences: when generating each word of a translation, attention mechanism 'looks' at all words in the source sentence and focuses more on the most relevant ones - giving higher 'attention' weights to words that matter most for the current output.

4. **Inputs & Outputs**  
   - Input: Query vectors (Q), key vectors (K), value vectors (V), input sequence, attention mask (optional).  
   - Output: Attention-weighted output vectors, attention scores showing which input tokens are most relevant.

5. **Step-by-step description (5–10 lines max)**  
1. Compute queries, keys, values: project input embeddings to Q, K, V spaces using learned weight matrices.
2. Calculate attention scores: compute similarity between queries and keys (dot product or scaled dot product).
3. Apply scaling: divide scores by sqrt(d_k) where d_k is key dimension (prevents large dot products).
4. Apply mask (optional): mask out padding tokens or future tokens (for causal attention).
5. Apply softmax: normalize scores to probabilities (attention weights sum to 1).
6. Weight values: multiply attention weights by value vectors and sum to get weighted output.
7. Output: return attention-weighted combination of values, representing focused context.
8. Multi-head attention (optional): repeat with different Q, K, V projections and concatenate results.

6. **Tiny example (hand-simulated)**  
   Translation: source 'The cat sat on the mat' → generating 'le' (French 'the') → attention scores: 'The'=0.8 (high), 'cat'=0.1, 'sat'=0.05, 'on'=0.03, 'the'=0.01, 'mat'=0.01 → weighted output focuses on 'The' → model correctly generates 'le'.

7. **Time & Space Complexity**  
   - Time: O(n²·d) where n is sequence length, d is dimension (quadratic in sequence length due to all-pairs attention).  
   - Space: O(n²) for attention matrix storing all query-key scores, O(n·d) for Q, K, V matrices.

8. **Strengths**  
- Captures long-range dependencies: can attend to any position in sequence.
- Interpretable: attention weights show which inputs are most relevant.
- Flexible: works for various sequence tasks (translation, summarization, etc.).

9. **Weaknesses / limitations**  
- Quadratic complexity: O(n²) makes it expensive for very long sequences.
- Memory intensive: requires storing attention matrix for all token pairs.

10. **Compare with alternatives**  
    Alternatives: RNN/LSTM, Convolutional Attention, Sparse Attention, Linear Attention

11. **30-second explanation (your own words)**  
    Enables models to focus on relevant parts of input sequence when generating output, allowing capture of long-range dependencies through attention-weighted combinations of input representations.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
