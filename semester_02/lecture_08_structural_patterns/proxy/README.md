# Proxy Pattern

1. **Name of Algorithm**  
   Proxy Pattern

2. **What problem does it solve? (1 sentence)**  
   Provides a surrogate object controlling access to a real subject (lazy loading, security, remote access).

3. **Intuition (plain-language explanation)**  
   Like a personal assistant screening calls before they reach the executive.

4. **Inputs & Outputs**  
   - Input: Original service object that needs access control, caching, or remote indirection.  
   - Output: Proxy implementing the same interface and delegating to the real subject with extra logic.

5. **Step-by-step description (5–10 lines max)**  
1. Define subject interface shared by both real object and proxy.
2. Proxy holds reference to real subject, instantiating it lazily if necessary.
3. Override operations to add pre/post behavior (checks, caching, logging).
4. Ensure client interacts only with the proxy interface.
5. Handle cleanup (connection closing, resource disposal) inside proxy.

6. **Tiny example (hand-simulated)**  
   Virtual proxy delaying image loading until it must be displayed.

7. **Time & Space Complexity**  
   - Time: Varies with added behavior (e.g., caching may improve average time).  
   - Space: Proxy holds pointer to real subject plus any cache state.

8. **Strengths**  
- Adds cross-cutting concerns transparently.
- Supports remote proxies for distributed systems.

9. **Weaknesses / limitations**  
- Another abstraction layer to test and maintain.
- Improper proxies can hide performance issues.

10. **Compare with alternatives**  
    Alternatives: Decorator Pattern, Aspect-Oriented Programming, Mediator

11. **30-second explanation (your own words)**  
    Insert a stand-in object that looks like the real one but adds access control, caching, or remote communication.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
