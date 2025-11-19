# Strategy Pattern

1. **Name of Algorithm**  
   Strategy Pattern

2. **What problem does it solve? (1 sentence)**  
   Defines a family of interchangeable algorithms so behavior can change at runtime without modifying clients.

3. **Intuition (plain-language explanation)**  
   Encapsulate algorithms behind a common interface; clients hold a reference and swap strategies as needed.

4. **Inputs & Outputs**  
   - Input: Context object that uses a Strategy interface implemented by concrete strategies.  
   - Output: Context delegates specific behavior (e.g., sorting, compression) to the selected strategy.

5. **Step-by-step description (5–10 lines max)**  
1. Define Strategy interface with a common operation.
2. Implement concrete strategies for each algorithm variant.
3. Context holds a strategy reference and forwards calls.
4. Allow clients to set or change strategy at runtime.
5. Optional: use dependency injection or configuration to pick strategy.

6. **Tiny example (hand-simulated)**  
   Payment processor selects PayPalStrategy, CreditCardStrategy, or CryptoStrategy based on user choice.

7. **Time & Space Complexity**  
   - Time: Depends on concrete strategy implementation.  
   - Space: Depends on strategies stored; typically O(1) per context.

8. **Strengths**  
- Eliminates conditional logic for algorithm selection.
- Eases extension with new strategies.

9. **Weaknesses / limitations**  
- More classes and objects to manage.
- Clients must understand strategy differences.

10. **Compare with alternatives**  
    Alternatives: State Pattern, Template Method, Policy Injection

11. **30-second explanation (your own words)**  
    Package interchangeable behaviors as strategy objects and let the client choose which one to run.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
