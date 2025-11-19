# Word2Vec

1. **Name of Algorithm**  
   Word2Vec

2. **What problem does it solve? (1 sentence)**  
   Learns dense word embeddings by predicting context words (CBOW) or predicting target word from context (Skip-gram), capturing semantic and syntactic word relationships.

3. **Intuition (plain-language explanation)**  
   Like learning word meanings from context: 'You shall know a word by the company it keeps' - words that appear in similar contexts should have similar embeddings.

4. **Inputs & Outputs**  
- Input: Large text corpus, context window size, embedding dimension, training algorithm (CBOW or Skip-gram).
   - Output: Dense word embeddings where semantically similar words are close in vector space.

5. **Step-by-step description (5–10 lines max)**  
1. Tokenize corpus and build vocabulary.
2. For CBOW: predict target word from surrounding context words.
3. For Skip-gram: predict context words from target word (more common).
4. Use shallow neural network: input word → hidden layer (embeddings) → output (softmax over vocabulary).
5. Train using negative sampling or hierarchical softmax to avoid expensive full softmax.
6. Extract learned embeddings from hidden layer weights.

6. **Tiny example (hand-simulated)**  
   Skip-gram: sentence 'the cat sat on mat' → target 'sat', context ['the', 'cat', 'on', 'mat'] → predict each context word from 'sat' → embeddings: 'sat' and 'stood' become similar (both verbs with similar contexts).

7. **Time & Space Complexity**  
   - Time: O(n·w·d) where n is corpus size, w is window size, d is embedding dimension (efficient with negative sampling).  
   - Space: O(V·d) for embeddings where V is vocabulary size, d is dimension.

8. **Strengths**  
- Efficient training on large corpora.
- Captures semantic relationships (king - man + woman ≈ queen).

9. **Weaknesses / limitations**  
- Single embedding per word (no context sensitivity).
- Requires large corpus for good performance.

10. **Compare with alternatives**  
    Alternatives: GloVe, FastText, BERT/GPT (contextual), ELMo

11. **30-second explanation (your own words)**  
    Learns word embeddings by predicting words from their context (or vice versa) using shallow neural networks, capturing semantic relationships through distributional similarity.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
