# Agentic RAG

1. **Name of Algorithm**  
   Agentic RAG

2. **What problem does it solve? (1 sentence)**  
   Enhances RAG systems with autonomous agents that can plan, reason, and iteratively retrieve and process information to answer complex queries, enabling multi-step reasoning and dynamic information gathering.

3. **Intuition (plain-language explanation)**  
   Like a research assistant: agentic RAG is like having a research assistant who doesn't just look up one thing - they understand your question, break it down into steps, search for information, read the results, decide if they need more information, search again if needed, and synthesize everything into a complete answer - they're autonomous (make decisions) and iterative (refine their search based on what they find), making them much more capable than simple lookup systems.

4. **Inputs & Outputs**  
   - Input: User query, knowledge base, agent capabilities, reasoning tools, retrieval system.  
   - Output: Comprehensive answer, multi-step reasoning, retrieved information, agent actions, final response.

5. **Step-by-step description (5–10 lines max)**  
1. Understand query: agent analyzes and understands the user query.
2. Plan: agent creates plan for answering query (break into sub-questions).
3. Retrieve: agent retrieves relevant information from knowledge base.
4. Reason: agent reasons about retrieved information.
5. Evaluate: agent evaluates if enough information to answer.
6. Iterate: if needed, agent formulates new queries and retrieves more information.
7. Synthesize: agent synthesizes all retrieved information.
8. Generate: agent generates comprehensive answer using LLM.
9. Verify: agent verifies answer quality and completeness.
10. Return: return final answer to user.

6. **Tiny example (hand-simulated)**  
   Agentic RAG: query: 'What are the main causes of climate change and their economic impacts?' → agent: plans → step 1: retrieve causes → step 2: retrieve economic impacts → step 3: synthesize → retrieves: scientific papers on causes → retrieves: economic studies → reasons: connects causes to impacts → generates: comprehensive answer → agentic RAG provides detailed response.

7. **Time & Space Complexity**  
   - Time: O(s·r) where s is number of steps, r is retrieval time per step (multi-step process).  
   - Space: O(d + m) where d is retrieved documents, m is agent state (planning and reasoning state).

8. **Strengths**  
- Capability: handles complex, multi-step queries.
- Autonomy: agent makes decisions and adapts strategy.
- Quality: produces more comprehensive and accurate answers.

9. **Weaknesses / limitations**  
- Latency: multi-step process increases response time.
- Complexity: more complex than simple RAG systems.
- Cost: multiple LLM calls increase cost.

10. **Compare with alternatives**  
    Alternatives: Simple RAG, Multi-Hop RAG, ReAct, Tool-Using Agents

11. **30-second explanation (your own words)**  
    Enhances RAG systems with autonomous agents that can plan, reason, and iteratively retrieve and process information to answer complex queries, enabling multi-step reasoning and dynamic information gathering.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
