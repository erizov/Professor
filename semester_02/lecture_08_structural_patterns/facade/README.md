# Facade Pattern

1. **Name of Algorithm**  
   Facade Pattern

2. **What problem does it solve? (1 sentence)**  
   Provides a simplified interface to a complex subsystem.

3. **Intuition (plain-language explanation)**  
   Think customer service hotline: one number routes requests to myriad internal departments.

4. **Inputs & Outputs**  
   - Input: Subsystem with many classes and configuration steps overwhelming clients.  
   - Output: Facade class exposing coarse-grained operations that orchestrate underlying components.

5. **Step-by-step description (5–10 lines max)**  
1. Map common client workflows that touch multiple subsystem classes.
2. Create a Facade exposing methods for each workflow.
3. Inside facade methods, coordinate subsystem objects in the right sequence.
4. Keep subsystem classes accessible for advanced clients when needed.
5. Document facade responsibilities clearly.

6. **Tiny example (hand-simulated)**  
   VideoConverter facade hides codecs, bitrates, and file IO from client code.

7. **Time & Space Complexity**  
   - Time: Same as orchestrated workflow; facade adds minimal overhead.  
   - Space: Facade may cache subsystem instances for reuse.

8. **Strengths**  
- Reduces learning curve for complicated APIs.
- Decouples clients from subsystem evolution.

9. **Weaknesses / limitations**  
- Facade can become a god-object if it grows unchecked.
- Still requires subsystem access for edge cases.

10. **Compare with alternatives**  
    Alternatives: Adapter Pattern, Mediator Pattern, Service Layer

11. **30-second explanation (your own words)**  
    Offer a single entry point that bundles complex operations so clients interact with a friendly API.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
