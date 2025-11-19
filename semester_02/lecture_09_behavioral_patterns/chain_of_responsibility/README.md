# Chain of Responsibility

1. **Name of Algorithm**  
   Chain of Responsibility

2. **What problem does it solve? (1 sentence)**  
   Decouples senders from receivers by giving more than one object a chance to handle a request.

3. **Intuition (plain-language explanation)**  
   Like escalating a customer ticket: each handler decides to process it or pass it along the chain.

4. **Inputs & Outputs**  
   - Input: Request object flowing through ordered handlers.  
   - Output: First handler that can process the request takes action; others remain unaware.

5. **Step-by-step description (5–10 lines max)**  
1. Define a Handler interface with set_next() and handle(request).
2. Implement concrete handlers that either process or forward the request.
3. Link handlers into a chain at runtime.
4. Client sends the request to the first handler only.
5. Optionally report when no handler could process the request.

6. **Tiny example (hand-simulated)**  
   Auth pipeline: BasicAuthHandler → TokenAuthHandler → OAuthHandler, each checking credentials before escalating.

7. **Time & Space Complexity**  
   - Time: O(n) in length of chain in worst case.  
   - Space: O(1) per handler, O(n) to store chain links.

8. **Strengths**  
- Avoids monolithic if/else blocks.
- Supports flexible ordering and additions.

9. **Weaknesses / limitations**  
- May be hard to ensure a request is eventually handled.
- Debugging requires understanding chain order.

10. **Compare with alternatives**  
    Alternatives: Middleware Pipelines, Strategy Pattern, Observer

11. **30-second explanation (your own words)**  
    Pass requests down a linked list of handlers until one handles it, keeping senders unaware of the concrete receiver.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
