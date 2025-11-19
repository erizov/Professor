# Liskov Substitution Principle

1. **Name of Algorithm**  
   Liskov Substitution Principle

2. **What problem does it solve? (1 sentence)**  
   Derived classes must behave like their base class so clients can substitute them without surprises.

3. **Intuition (plain-language explanation)**  
   If a square is a rectangle, any rectangle-using code should still work when given a square; inheritance should not break contracts.

4. **Inputs & Outputs**  
   - Input: Class hierarchies where overrides narrow behavior or violate expectations.  
   - Output: Subclasses that preserve base invariants, preconditions, and postconditions.

5. **Step-by-step description (5–10 lines max)**  
1. Document the base class contract (inputs, outputs, side effects).
2. Ensure subclasses do not strengthen preconditions or weaken postconditions.
3. Avoid throwing new exceptions or changing returned types unexpectedly.
4. Prefer composition when behavior diverges significantly.
5. Add substitution tests to validate behavior parity.

6. **Tiny example (hand-simulated)**  
   Bird base class fly() → Penguin subclass overrides to throw; violates LSP, so extract FlightlessBird behavior instead.

7. **Time & Space Complexity**  
   - Time: Focused on design correctness rather than runtime.  
   - Space: May require extra wrapper classes for composition.

8. **Strengths**  
- Keeps polymorphism reliable for clients.
- Prevents brittle inheritance hierarchies.

9. **Weaknesses / limitations**  
- Hard to enforce without strong contracts/tests.
- Legacy hierarchies may need large refactors.

10. **Compare with alternatives**  
    Alternatives: Composition over Inheritance, Design by Contract, Interface Segregation

11. **30-second explanation (your own words)**  
    Subclasses should honor the promises of their parents so client code can substitute them freely.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
