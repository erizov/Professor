# GloVe (Global Vectors for Word Representation)

1. **Name of Algorithm**  
   GloVe (Global Vectors for Word Representation)

2. **What problem does it solve? (1 sentence)**  
   Learns word embeddings by factorizing a word co-occurrence matrix, combining global statistical information with local context window methods.

3. **Intuition (plain-language explanation)**  
   Like analyzing word relationships in a giant spreadsheet: count how often words appear together across all documents, then find patterns (embeddings) that capture these relationships mathematically.

4. **Inputs & Outputs**  
   - Input: Large text corpus, co-occurrence window size, vocabulary.  
   - Output: Dense word embeddings (vectors) where similar words have similar representations.

5. **Step-by-step description (5–10 lines max)**  
1. Build word co-occurrence matrix: count how often word pairs appear within a window.
2. Apply weighting function to discount distant co-occurrences.
3. Factorize co-occurrence matrix using log-bilinear model: log(X_ij) = w_i^T w_j + b_i + b_j.
4. Minimize weighted least squares objective over all word pairs.
5. Extract word vectors w_i and context vectors w_j (often use sum or average).
6. Output embeddings that capture semantic and syntactic relationships.

6. **Tiny example (hand-simulated)**  
   Corpus: 'cat sits on mat', 'dog sits on floor' → co-occurrence: (cat, sits)=2, (cat, mat)=1, (dog, sits)=2 → GloVe learns: cat and dog have similar embeddings (both animals), mat and floor similar (both surfaces).

7. **Time & Space Complexity**  
   - Time: O(V²) where V is vocabulary size (co-occurrence matrix construction and factorization).  
   - Space: O(V²) for co-occurrence matrix, O(V·d) for embeddings where d is dimension.

8. **Strengths**  
- Captures both global and local word relationships.
- Efficient training on large corpora.

9. **Weaknesses / limitations**  
- Requires storing large co-occurrence matrix.
- Less flexible than neural network-based methods.

10. **Compare with alternatives**  
    Alternatives: Word2Vec, FastText, BERT/GPT (contextual embeddings), ELMo

11. **30-second explanation (your own words)**  
    Learns word embeddings by factorizing word co-occurrence statistics, combining benefits of global matrix factorization with local context window methods.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
