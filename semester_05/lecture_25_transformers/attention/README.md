# Attention Mechanism

1. **Name of Algorithm**  
   Attention Mechanism

2. **What problem does it solve? (1 sentence)**  
   Allows models to focus on relevant parts of input when making predictions, enabling better handling of long-range dependencies and interpretability.

3. **Intuition (plain-language explanation)**  
   Like reading a long document: when answering a question, focus attention on relevant sentences (high attention weights) rather than reading everything equally.

4. **Inputs & Outputs**  
   - Input: Query vectors Q, key vectors K, value vectors V (all from input sequences).  
   - Output: Weighted combination of values, where weights are computed from query-key similarity.

5. **Step-by-step description (5–10 lines max)**  
1. Compute attention scores: score(q_i, k_j) = similarity between query i and key j.
2. Apply softmax to scores to get attention weights (sum to 1).
3. Weighted sum of values: output_i = Σ(attention_weight_ij × v_j).
4. For self-attention: Q, K, V all come from same input sequence.
5. For multi-head attention: apply attention in parallel with different learned projections.
6. Combine multi-head outputs via concatenation and linear transformation.

6. **Tiny example (hand-simulated)**  
   Translation: 'The cat sat' → attention weights: 'cat' gets high weight when generating 'gato' (Spanish), 'sat' gets high weight for 'se sentó'. Attention matrix shows word alignments.

7. **Time & Space Complexity**  
   - Time: O(n²·d) where n is sequence length, d is dimension (quadratic in sequence length).  
   - Space: O(n²) for attention matrix (grows quadratically with sequence length).

8. **Strengths**  
- Captures long-range dependencies effectively.
- Provides interpretability through attention weights.

9. **Weaknesses / limitations**  
- Quadratic complexity limits maximum sequence length.
- Requires careful initialization and training.

10. **Compare with alternatives**  
    Alternatives: RNN/LSTM, CNN, Sparse Attention, Linear Attention

11. **30-second explanation (your own words)**  
    Computes weighted combinations of input elements based on query-key similarity, allowing models to dynamically focus on relevant information for each prediction.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
