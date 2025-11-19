# Strategy Pattern

1. **Name of Algorithm**  
   Strategy Pattern

2. **What problem does it solve? (1 sentence)**  
   Defines a family of interchangeable algorithms that can be selected at runtime.

3. **Intuition (plain-language explanation)**  
   Choose the best route on a GPS: driving, walking, cycling strategies share interface but differ internally.

4. **Inputs & Outputs**  
   - Input: Context needing to swap algorithms (sorting, pricing, compression).  
   - Output: Strategy interface with concrete implementations and a context delegating work.

5. **Step-by-step description (5–10 lines max)**  
1. Identify behavior that varies independently from the rest of the class.
2. Extract a Strategy interface declaring the behavior.
3. Implement concrete strategies for each variation.
4. Context holds a reference to a strategy and delegates calls.
5. Provide mechanism to switch strategies dynamically if needed.

6. **Tiny example (hand-simulated)**  
   PaymentProcessor uses CreditCardStrategy, PayPalStrategy, or CryptoStrategy based on user selection.

7. **Time & Space Complexity**  
   - Time: Same as selected strategy; selection overhead is O(1).  
   - Space: O(1) for context reference; additional strategies cost class storage.

8. **Strengths**  
- Eliminates conditionals for algorithm selection.
- Promotes testable, pluggable behaviors.

9. **Weaknesses / limitations**  
- Requires clients to understand and select appropriate strategy.
- Too many tiny classes if not organized carefully.

10. **Compare with alternatives**  
    Alternatives: Policy Objects, Function Pointers/Lambdas, State Pattern

11. **30-second explanation (your own words)**  
    Encapsulate interchangeable behaviors behind a common interface so contexts can switch algorithms without branching.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
