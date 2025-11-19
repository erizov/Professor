# Hybrid Search for RAG

1. **Name of Algorithm**  
   Hybrid Search for RAG

2. **What problem does it solve? (1 sentence)**  
   Combines multiple search methods (keyword search, semantic search, dense retrieval) to improve retrieval quality by leveraging strengths of different approaches and compensating for their weaknesses.

3. **Intuition (plain-language explanation)**  
   Like using multiple search tools: hybrid search is like using both a library catalog (keyword search) and asking a librarian (semantic search) - the catalog is great for exact matches (keywords), while the librarian understands meaning (semantics) - by combining both, you get better results: you find documents with exact terms (keyword) and documents that mean the same thing even with different words (semantic) - it's like having multiple ways to find information, making your search more comprehensive and accurate.

4. **Inputs & Outputs**  
   - Input: Query, knowledge base, keyword index, semantic embeddings, search methods, fusion strategy.  
   - Output: Hybrid search results, combined rankings, improved retrieval, diverse document set.

5. **Step-by-step description (5–10 lines max)**  
1. Keyword search: perform keyword/BM25 search on query.
2. Semantic search: perform semantic/dense vector search on query embedding.
3. Score: score documents from each search method.
4. Normalize: normalize scores from different methods to comparable scale.
5. Combine: combine scores using fusion strategy (weighted sum, reciprocal rank fusion).
6. Rank: rank documents by combined scores.
7. Diversify: optionally diversify results to avoid redundancy.
8. Select: select top-k documents from hybrid ranking.
9. Optimize: optimize fusion weights and search methods.
10. Return: return hybrid search results for RAG.

6. **Tiny example (hand-simulated)**  
   Hybrid search: query: 'machine learning algorithms' → keyword: finds docs with exact terms → semantic: finds docs about 'ML methods', 'AI techniques' → combine: weighted sum (0.4 keyword + 0.6 semantic) → rank: hybrid ranking → result: 10 diverse, relevant documents → hybrid search improves retrieval.

7. **Time & Space Complexity**  
   - Time: O(k + s) where k is keyword search time, s is semantic search time (parallel or sequential).  
   - Space: O(i + e) where i is keyword index size, e is embedding index size (both indices needed).

8. **Strengths**  
- Quality: improves retrieval quality by combining methods.
- Robustness: more robust to query variations and document styles.
- Coverage: retrieves both exact matches and semantically similar documents.

9. **Weaknesses / limitations**  
- Complexity: more complex than single-method search.
- Cost: requires maintaining multiple indices.
- Tuning: requires tuning fusion weights and parameters.

10. **Compare with alternatives**  
    Alternatives: Keyword Search, Semantic Search, Dense Retrieval, Sparse Retrieval

11. **30-second explanation (your own words)**  
    Combines multiple search methods (keyword search, semantic search, dense retrieval) to improve retrieval quality by leveraging strengths of different approaches and compensating for their weaknesses.
*Sources: Adapted from standard university textbooks and Wikipedia summaries.*