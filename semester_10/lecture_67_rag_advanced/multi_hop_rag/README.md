# Multi-Hop RAG

1. **Name of Algorithm**  
   Multi-Hop RAG

2. **What problem does it solve? (1 sentence)**  
   Answers complex queries requiring information from multiple documents through iterative retrieval, where each retrieval step uses information from previous steps to refine the search, enabling reasoning across multiple knowledge sources.

3. **Intuition (plain-language explanation)**  
   Like following a chain of clues: multi-hop RAG is like solving a mystery by following clues - you start with the question (initial query), find the first clue (retrieve first document), which leads you to the next clue (refined query based on first document), you follow that (retrieve second document), and continue until you have enough information to solve the mystery (answer the question) - each step (hop) builds on the previous one, allowing you to reason across multiple sources of information.

4. **Inputs & Outputs**  
   - Input: Complex query, knowledge base, retrieval system, reasoning capability, hop limit.  
   - Output: Multi-hop answer, retrieved document chain, reasoning path, comprehensive response.

5. **Step-by-step description (5–10 lines max)**  
1. Initial retrieval: retrieve initial documents based on original query.
2. Analyze: analyze retrieved documents for relevant information.
3. Reason: reason about what additional information is needed.
4. Refine query: formulate refined query based on initial retrieval.
5. Next hop: retrieve additional documents using refined query.
6. Combine: combine information from all retrieved documents.
7. Check: check if query can be answered with current information.
8. Iterate: if not, perform another hop (refine query, retrieve again).
9. Synthesize: synthesize information from all hops.
10. Generate: generate final answer using all retrieved information.

6. **Tiny example (hand-simulated)**  
   Multi-hop RAG: query: 'What did the CEO say about the company's expansion plans?' → hop 1: retrieve CEO's recent statements → find: mentions 'Asian markets' → hop 2: retrieve company's Asia expansion documents → find: specific plans → hop 3: retrieve financial reports on Asia → combine: CEO statement + expansion plans + financials → answer: comprehensive response → multi-hop RAG successful.

7. **Time & Space Complexity**  
   - Time: O(h·r) where h is number of hops, r is retrieval time per hop (iterative retrieval).  
   - Space: O(h·d) where h is hops, d is documents per hop (accumulated retrieved documents).

8. **Strengths**  
- Complex queries: handles queries requiring information from multiple sources.
- Reasoning: enables reasoning across multiple documents.
- Comprehensiveness: produces more comprehensive answers.

9. **Weaknesses / limitations**  
- Latency: multiple hops increase response time.
- Error propagation: errors in early hops can affect later hops.
- Complexity: more complex than single-hop RAG.

10. **Compare with alternatives**  
    Alternatives: Single-Hop RAG, Agentic RAG, Iterative Retrieval, Query Decomposition

11. **30-second explanation (your own words)**  
    Answers complex queries requiring information from multiple documents through iterative retrieval, where each retrieval step uses information from previous steps to refine the search, enabling reasoning across multiple knowledge sources.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
