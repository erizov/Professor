# Seq2Seq (Sequence-to-Sequence)

1. **Name of Algorithm**  
   Seq2Seq (Sequence-to-Sequence)

2. **What problem does it solve? (1 sentence)**  
   Maps variable-length input sequences to variable-length output sequences using encoder-decoder architecture, enabling tasks like translation, summarization, and dialogue.

3. **Intuition (plain-language explanation)**  
   Like a translator: encoder reads and understands the source sentence (creates representation), decoder generates the target sentence word by word based on that understanding.

4. **Inputs & Outputs**  
   - Input: Source sequence (e.g., English sentence), encoder RNN/LSTM/Transformer, decoder RNN/LSTM/Transformer.  
   - Output: Target sequence (e.g., French sentence) generated token by token.

5. **Step-by-step description (5–10 lines max)**  
1. Encoder: process source sequence token by token, building hidden states.
2. Final encoder hidden state (or all states) becomes context vector.
3. Decoder: initialize with context vector, generate first target token.
4. Decoder uses previous output token and hidden state to generate next token.
5. Repeat until decoder produces end-of-sequence token.
6. Train with teacher forcing: use ground truth tokens during training, generated tokens during inference.

6. **Tiny example (hand-simulated)**  
   Translation: 'Hello world' (English) → encoder processes → context vector → decoder generates 'Bonjour le monde' (French) token by token: 'Bonjour' → 'le' → 'monde' → <EOS>.

7. **Time & Space Complexity**  
   - Time: O(n·d·l + m·d·l) where n is source length, m is target length, d is dimension, l is layers (sequential processing).  
   - Space: O(n·d + m·d) for encoder and decoder hidden states.

8. **Strengths**  
- Handles variable-length sequences naturally.
- Foundation for many NLP tasks (translation, summarization, dialogue).

9. **Weaknesses / limitations**  
- Bottleneck: single context vector may lose information for long sequences.
- Sequential decoding is slow (cannot parallelize generation).

10. **Compare with alternatives**  
    Alternatives: Transformer (attention-based), Pointer Networks, Copy Mechanisms, Beam Search Decoding

11. **30-second explanation (your own words)**  
    Uses encoder-decoder architecture to map input sequences to output sequences, with encoder creating representation and decoder generating target sequence token by token.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
