# Clean Architecture

1. **Name of Algorithm**  
   Clean Architecture

2. **What problem does it solve? (1 sentence)**  
   Separates enterprise business rules from delivery mechanisms so systems remain testable, maintainable, and technology-agnostic.

3. **Intuition (plain-language explanation)**  
   Organize code in concentric rings where inner layers know nothing about outer layers; dependencies always point inward.

4. **Inputs & Outputs**  
   - Input: Domain entities, use cases, interface adapters, and frameworks/external services.  
   - Output: Modular system where core logic can evolve independently from UI, databases, or frameworks.

5. **Step-by-step description (5–10 lines max)**  
1. Define entities (enterprise rules) at the center.
2. Create use cases that orchestrate entities.
3. Add interface adapters (controllers, presenters, gateways) to translate between formats.
4. Place frameworks and drivers (UI, DB, external APIs) at the outer ring.
5. Enforce dependency rule: source code dependencies point inward only.

6. **Tiny example (hand-simulated)**  
   E-commerce app: inner ring handles order validation, middle ring defines place-order use case, outer ring wires HTTP controllers and database gateways.

7. **Time & Space Complexity**  
   - Time: Not applicable; architectural pattern.  
   - Space: Not applicable; organizational structure.

8. **Strengths**  
- Framework-independent core that survives technology churn.
- High testability due to isolated business rules.

9. **Weaknesses / limitations**  
- Initial setup overhead and learning curve.
- Requires discipline to maintain boundary rules.

10. **Compare with alternatives**  
    Alternatives: Layered Architecture, Hexagonal Architecture, Onion Architecture

11. **30-second explanation (your own words)**  
    Keep business logic at the center and surround it with adapters so changing UI or database layers never ripples into the core.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
