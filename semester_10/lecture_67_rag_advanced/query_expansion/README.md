# Query Expansion for RAG

1. **Name of Algorithm**  
   Query Expansion for RAG

2. **What problem does it solve? (1 sentence)**  
   Enhances user queries by adding related terms, synonyms, or reformulations to improve retrieval quality, helping RAG systems find relevant documents even when query terms don't exactly match document vocabulary.

3. **Intuition (plain-language explanation)**  
   Like adding synonyms to your search: query expansion is like searching for 'car' and also searching for 'automobile', 'vehicle', 'auto' - you expand your search terms to include related words, making it more likely to find what you're looking for even if the documents use different words - it's like speaking the same language as the documents, increasing the chances of finding relevant information.

4. **Inputs & Outputs**  
   - Input: Original query, synonym dictionaries, related terms, expansion methods, expansion parameters.  
   - Output: Expanded query, improved retrieval, diverse search terms, better document matching.

5. **Step-by-step description (5–10 lines max)**  
1. Analyze query: analyze original query to identify key terms.
2. Generate synonyms: generate synonyms for key terms (thesaurus, word embeddings).
3. Add related terms: add related terms using word embeddings or knowledge graphs.
4. Reformulate: create query reformulations (paraphrases, alternative phrasings).
5. Combine: combine original query with expanded terms.
6. Weight: assign weights to original vs expanded terms.
7. Retrieve: perform retrieval using expanded query.
8. Rank: rank documents based on expanded query matching.
9. Validate: validate that expansion improves retrieval quality.
10. Optimize: optimize expansion strategy and parameters.

6. **Tiny example (hand-simulated)**  
   Query expansion: query: 'machine learning' → expand: add 'ML', 'artificial intelligence', 'AI algorithms', 'deep learning' → retrieve: finds documents with any of these terms → result: 50% more relevant documents → query expansion improves retrieval.

7. **Time & Space Complexity**  
   - Time: O(t·e) where t is number of terms, e is expansion time per term (synonym lookup, embedding search).  
   - Space: O(s) where s is synonym/embedding dictionary size (expansion resources).

8. **Strengths**  
- Coverage: improves retrieval coverage by matching more document variations.
- Robustness: more robust to vocabulary mismatches between query and documents.
- Quality: can improve retrieval quality for ambiguous or short queries.

9. **Weaknesses / limitations**  
- Noise: may introduce irrelevant terms and noise.
- Precision: may reduce precision if expansion is too broad.
- Tuning: requires careful tuning of expansion parameters.

10. **Compare with alternatives**  
    Alternatives: Original Query, Query Reformulation, Pseudo-Relevance Feedback, Query Understanding

11. **30-second explanation (your own words)**  
    Enhances user queries by adding related terms, synonyms, or reformulations to improve retrieval quality, helping RAG systems find relevant documents even when query terms don't exactly match document vocabulary.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
