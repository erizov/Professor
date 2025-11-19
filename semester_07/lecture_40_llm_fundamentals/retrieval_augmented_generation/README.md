# Retrieval Augmented Generation (RAG)

1. **Name of Algorithm**  
   Retrieval Augmented Generation (RAG)

2. **What problem does it solve? (1 sentence)**  
   Enhances LLM generation by retrieving relevant information from external knowledge base and including it in context, enabling accurate, up-to-date responses without modifying model weights and reducing hallucinations.

3. **Intuition (plain-language explanation)**  
   Like a student with a textbook during an exam: instead of relying only on memory (model's training data), RAG retrieves relevant information from a knowledge base (textbook) and includes it in the prompt (open book) - the model uses this retrieved context to give accurate, factual answers.

4. **Inputs & Outputs**  
   - Input: User query, knowledge base (documents, database), embedding model, retrieval system, LLM.  
   - Output: Generated response augmented with retrieved context, citations to source documents.

5. **Step-by-step description (5–10 lines max)**  
1. Encode query: convert user query to embedding vector using embedding model.
2. Retrieve documents: search knowledge base for documents similar to query (vector similarity search).
3. Rank results: score and rank retrieved documents by relevance to query.
4. Select top-k: choose top k most relevant documents (typically 3-10).
5. Format context: combine retrieved documents into context string for prompt.
6. Construct prompt: create prompt with user query and retrieved context (e.g., 'Context: [retrieved docs]. Question: [query]. Answer:').
7. Generate response: pass prompt to LLM, generate answer using retrieved context.
8. Post-process: format response, add citations to source documents, verify facts.

6. **Tiny example (hand-simulated)**  
   Question: 'What is the capital of France?' → RAG: query embedding → retrieve from knowledge base → find document 'France is a country. Its capital is Paris.' → prompt: 'Context: France is a country. Its capital is Paris. Question: What is the capital of France? Answer:' → LLM: 'The capital of France is Paris.'

7. **Time & Space Complexity**  
   - Time: O(Q + R + G) where Q is query encoding, R is retrieval time (O(log n) for vector search), G is generation time (O(m) where m is output length).  
   - Space: O(D) for knowledge base embeddings where D is number of documents, O(k·S) for retrieved context where k is top-k, S is document size.

8. **Strengths**  
- Up-to-date information: can use recent documents not in training data.
- Reduces hallucinations: grounded in retrieved facts, less likely to make up information.
- Transparent: can cite sources, enabling fact-checking.

9. **Weaknesses / limitations**  
- Retrieval quality: depends on quality of knowledge base and retrieval system.
- Context limits: retrieved documents consume context window.
- Latency: adds retrieval step, increasing response time.

10. **Compare with alternatives**  
    Alternatives: Fine-tuning, In-context Learning, Knowledge Distillation, External Tool Use

11. **30-second explanation (your own words)**  
    Enhances LLM generation by retrieving relevant information from external knowledge base and including it in context, enabling accurate, up-to-date responses without modifying model weights and reducing hallucinations.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
