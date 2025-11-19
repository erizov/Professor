# Open/Closed Principle

1. **Name of Algorithm**  
   Open/Closed Principle

2. **What problem does it solve? (1 sentence)**  
   Code should be open for extension but closed for modification.

3. **Intuition (plain-language explanation)**  
   Once stable, classes become plug-in sockets: add new behavior via extension points instead of editing core logic.

4. **Inputs & Outputs**  
   - Input: Existing class that needs new behavior variations.  
   - Output: Abstractions that allow new features through inheritance, composition, or configuration.

5. **Step-by-step description (5–10 lines max)**  
1. Identify areas where features keep forcing edits to the same class.
2. Extract abstractions (interfaces, base classes, strategy objects).
3. Move variable behavior behind the abstraction boundary.
4. Register new implementations without touching existing code.
5. Cover extension points with tests to guard regressions.

6. **Tiny example (hand-simulated)**  
   ShippingCalculator switches via if/else per region → introduce ShippingStrategy interface and register new strategies.

7. **Time & Space Complexity**  
   - Time: Depends on the breadth of extension points.  
   - Space: Additional classes or configuration objects to host extensions.

8. **Strengths**  
- Limits regression risk when adding features.
- Encourages plugin-style architectures.

9. **Weaknesses / limitations**  
- Requires upfront abstraction design.
- Over-abstraction can make code harder to follow.

10. **Compare with alternatives**  
    Alternatives: Strategy Pattern, Dependency Injection, Feature Toggles

11. **30-second explanation (your own words)**  
    Design modules so you add new behavior by plugging in new classes, not by editing the old ones.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
