# GPT (Generative Pre-trained Transformer)

1. **Name of Algorithm**  
   GPT (Generative Pre-trained Transformer)

2. **What problem does it solve? (1 sentence)**  
   Pre-trains autoregressive language model on large text corpus, then fine-tunes for downstream tasks, enabling strong performance on generation and understanding tasks.

3. **Intuition (plain-language explanation)**  
   Like learning to write by reading millions of books: learn patterns of language (pre-training), then adapt to specific writing tasks (fine-tuning) like essays, code, or stories.

4. **Inputs & Outputs**  
   - Input: Text sequences, token embeddings, position embeddings.  
   - Output: Next token predictions or task-specific outputs after fine-tuning.

5. **Step-by-step description (5–10 lines max)**  
1. Tokenize input text into subword tokens.
2. Create embeddings: token + position embeddings.
3. Apply Transformer decoder (masked self-attention + feed-forward).
4. Pre-train with language modeling objective: predict next token given previous tokens.
5. For fine-tuning: add task-specific head (classification, generation, etc.).
6. Train on downstream task with supervised learning.

6. **Tiny example (hand-simulated)**  
   Pre-training: 'The cat sat' → predict 'on'. Fine-tuning for sentiment: 'Great movie!' → add classification head → predict 'positive'. Generation: 'Once upon a time' → generate story continuation.

7. **Time & Space Complexity**  
   - Time: O(n²·d·l) for n tokens, d dimensions, l layers (autoregressive generation is sequential).  
   - Space: O(l·d²) for parameters (GPT-2: 1.5B, GPT-3: 175B parameters).

8. **Strengths**  
- Strong generative capabilities for text completion and creation.
- Transfer learning: one model for many tasks.

9. **Weaknesses / limitations**  
- Unidirectional (left-to-right) limits bidirectional understanding.
- Large models require significant computational resources.

10. **Compare with alternatives**  
    Alternatives: BERT, T5, GPT-2/GPT-3, PaLM

11. **30-second explanation (your own words)**  
    Pre-trains autoregressive Transformer decoder on language modeling, learning to predict next tokens, then fine-tunes for downstream tasks or generates text directly.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
