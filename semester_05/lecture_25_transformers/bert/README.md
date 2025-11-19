# BERT (Bidirectional Encoder Representations from Transformers)

1. **Name of Algorithm**  
   BERT (Bidirectional Encoder Representations from Transformers)

2. **What problem does it solve? (1 sentence)**  
   Pre-trains deep bidirectional representations by jointly conditioning on both left and right context, enabling state-of-the-art performance on NLP tasks with fine-tuning.

3. **Intuition (plain-language explanation)**  
   Like reading a sentence both forward and backward simultaneously: understand each word by seeing everything around it (left and right context) at once, not just what came before.

4. **Inputs & Outputs**  
   - Input: Text sequences with special tokens ([CLS], [SEP]), token embeddings, position embeddings, segment embeddings.  
   - Output: Contextualized word embeddings that can be fine-tuned for downstream tasks.

5. **Step-by-step description (5–10 lines max)**  
1. Tokenize input and add special tokens: [CLS] at start, [SEP] between sentences.
2. Create embeddings: token + position + segment embeddings.
3. Apply bidirectional Transformer encoder (12-24 layers) with self-attention.
4. Pre-train with two tasks: Masked Language Modeling (MLM) and Next Sentence Prediction (NSP).
5. For downstream tasks: add task-specific head and fine-tune on labeled data.
6. Output contextualized representations for each token position.

6. **Tiny example (hand-simulated)**  
   Input: '[CLS] The cat sat [SEP] on the mat [SEP]' → BERT encodes → '[CLS]' embedding used for classification, 'cat' embedding captures context from entire sentence → fine-tune for sentiment/QA/NER.

7. **Time & Space Complexity**  
   - Time: O(n²·d·l) where n is sequence length, d is dimension, l is number of layers (pre-training is expensive).  
   - Space: O(l·d²) for model parameters (BERT-base: 110M, BERT-large: 340M parameters).

8. **Strengths**  
- Bidirectional context enables better understanding.
- Transfer learning: pre-train once, fine-tune for many tasks.

9. **Weaknesses / limitations**  
- Cannot generate text (encoder-only architecture).
- Pre-training requires massive compute and data.

10. **Compare with alternatives**  
    Alternatives: GPT, RoBERTa, ALBERT, ELECTRA

11. **30-second explanation (your own words)**  
    Pre-trains bidirectional Transformer encoder on large text corpus using masked language modeling, producing contextualized embeddings that excel when fine-tuned on downstream tasks.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
