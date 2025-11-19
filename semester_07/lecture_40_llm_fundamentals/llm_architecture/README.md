# LLM Architecture

1. **Name of Algorithm**  
   LLM Architecture

2. **What problem does it solve? (1 sentence)**  
   Defines the structural design of large language models, typically based on Transformer architecture with self-attention, feed-forward networks, and layer normalization, enabling processing of variable-length sequences and learning complex language patterns.

3. **Intuition (plain-language explanation)**  
   Like a factory assembly line: LLM architecture is the blueprint - input text goes through layers (attention, processing, normalization) like products through assembly stations, each layer transforms and refines the representation until you get the final output (predicted text).

4. **Inputs & Outputs**  
   - Input: Token embeddings, positional encodings, architecture hyperparameters (layers, dimensions, heads).  
   - Output: Token predictions, hidden representations, language model probabilities.

5. **Step-by-step description (5–10 lines max)**  
1. Tokenize input: convert text to token IDs using tokenizer (BPE, WordPiece, SentencePiece).
2. Embed tokens: map token IDs to dense vectors (embedding layer).
3. Add positional encoding: inject position information (sinusoidal or learned) to embeddings.
4. Stack transformer blocks: for each of N layers: apply multi-head self-attention, add residual connection, apply layer norm, apply feed-forward network, add residual connection, apply layer norm.
5. Self-attention: compute attention over input sequence (queries, keys, values from same sequence).
6. Feed-forward: apply two linear transformations with activation (ReLU, GELU) in between.
7. Output projection: map final hidden states to vocabulary size for next-token prediction.
8. Generate tokens: sample or greedily select next token, append to sequence, repeat for generation.

6. **Tiny example (hand-simulated)**  
   GPT-3 architecture: input 'The cat' → tokenize → [1234, 5678] → embed → [512-dim vectors] → 96 transformer layers → each layer: self-attention (attends to 'The' and 'cat'), feed-forward → final layer → output projection → predicts 'sat' (next token) with probability 0.3.

7. **Time & Space Complexity**  
   - Time: O(n²·d·L) where n is sequence length, d is dimension, L is number of layers (quadratic in sequence length due to attention).  
   - Space: O(n²·L) for attention matrices across L layers, O(d·L) for model parameters where d is dimension.

8. **Strengths**  
- Scalable: performance improves with model size and data.
- Flexible: handles variable-length sequences naturally.
- Powerful: captures complex language patterns and long-range dependencies.

9. **Weaknesses / limitations**  
- Computational cost: quadratic attention complexity limits sequence length.
- Memory intensive: large models require significant GPU memory.
- Training cost: pre-training requires massive compute and data.

10. **Compare with alternatives**  
    Alternatives: RNN/LSTM, CNN, Hybrid Architectures, Efficient Transformers

11. **30-second explanation (your own words)**  
    Defines structural design of large language models based on Transformer architecture with self-attention and feed-forward networks, enabling processing of variable-length sequences and learning complex language patterns.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
