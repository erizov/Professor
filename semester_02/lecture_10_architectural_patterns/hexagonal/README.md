# Hexagonal (Ports and Adapters)

1. **Name of Algorithm**  
   Hexagonal (Ports and Adapters)

2. **What problem does it solve? (1 sentence)**  
   Allows applications to run equally in different environments by decoupling the domain from external systems via ports and adapters.

3. **Intuition (plain-language explanation)**  
   Treat the application as a hexagon with ports on each side; adapters plug into ports to talk to the outer world.

4. **Inputs & Outputs**  
   - Input: Domain core, inbound ports for driving actions, outbound ports for driven interactions.  
   - Output: Adapters (HTTP, CLI, database, messaging) that plug in without changing core logic.

5. **Step-by-step description (5–10 lines max)**  
1. Define inbound ports (interfaces) representing use cases.
2. Implement domain services that realize the ports.
3. Declare outbound ports for infrastructure dependencies.
4. Write adapters that implement outbound ports (DB gateways, API clients).
5. Wire adapters to ports via dependency injection.

6. **Tiny example (hand-simulated)**  
   Blog service: inbound port publish_post, adapters for REST controller and CLI; outbound port PostRepository with adapters for SQL or NoSQL stores.

7. **Time & Space Complexity**  
   - Time: Not applicable.  
   - Space: Not applicable.

8. **Strengths**  
- Easy to swap infrastructure without touching core.
- Supports automated testing by substituting adapters.

9. **Weaknesses / limitations**  
- More interfaces and boilerplate.
- Requires careful dependency management.

10. **Compare with alternatives**  
    Alternatives: Clean Architecture, Onion Architecture, Layered Architecture

11. **30-second explanation (your own words)**  
    Expose the application through abstract ports while adapters translate between the outside world and the domain core.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
