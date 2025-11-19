# Adapter Pattern

1. **Name of Algorithm**  
   Adapter Pattern

2. **What problem does it solve? (1 sentence)**  
   Allows incompatible interfaces to collaborate without modifying existing code.

3. **Intuition (plain-language explanation)**  
   Like a power plug converter: adapt one shape to another so both sides work together.

4. **Inputs & Outputs**  
   - Input: Client expecting interface A and an existing service implementing interface B.  
   - Output: Adapter class translating client calls to the adaptee’s API.

5. **Step-by-step description (5–10 lines max)**  
1. Identify the target interface the client expects.
2. Wrap the existing class (adaptee) inside an adapter implementing the target interface.
3. Translate each operation: convert parameters, call adaptee, convert results.
4. Inject or instantiate the adapter where the client previously used the adaptee.
5. Write tests ensuring the adapter faithfully forwards behavior.

6. **Tiny example (hand-simulated)**  
   Legacy XmlLogger used by new JsonLogger clients; Adapter implements JsonLogger interface but delegates to XmlLogger.

7. **Time & Space Complexity**  
   - Time: Negligible overhead—method dispatch plus conversions.  
   - Space: O(1) extra state per adapter instance.

8. **Strengths**  
- Enables reuse of existing classes without altering them.
- Supports incremental migrations between APIs.

9. **Weaknesses / limitations**  
- Adds another indirection layer to maintain.
- Complex mappings can become brittle.

10. **Compare with alternatives**  
    Alternatives: Facade Pattern, Decorator Pattern, Wrapper Classes

11. **30-second explanation (your own words)**  
    Introduce a thin wrapper that exposes the interface you need while delegating real work to an incompatible class.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
