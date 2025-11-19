# Decorator Pattern

1. **Name of Algorithm**  
   Decorator Pattern

2. **What problem does it solve? (1 sentence)**  
   Adds responsibilities to objects dynamically without subclass explosion.

3. **Intuition (plain-language explanation)**  
   Like wrapping a gift multiple times: each wrapper adds behavior while still exposing the same interface.

4. **Inputs & Outputs**  
   - Input: Base component with optional features (logging, caching, compression).  
   - Output: Decorator classes implementing the same interface and holding a reference to the wrapped component.

5. **Step-by-step description (5–10 lines max)**  
1. Define a Component interface implemented by the base class.
2. Create Decorator base class implementing Component and storing a Component reference.
3. Implement concrete decorators that augment behavior before/after delegating.
4. Wrap components with decorators at runtime to compose features.
5. Ensure removal/reordering of decorators remains simple.

6. **Tiny example (hand-simulated)**  
   DataSource decorated with CompressionDecorator then EncryptionDecorator before writing to disk.

7. **Time & Space Complexity**  
   - Time: Adds linear overhead proportional to number of decorators.  
   - Space: O(k) extra objects for k decorators.

8. **Strengths**  
- Flexible combination of features at runtime.
- Avoids deep inheritance hierarchies.

9. **Weaknesses / limitations**  
- Debugging stack of decorators can be tricky.
- Many small objects increase complexity.

10. **Compare with alternatives**  
    Alternatives: Proxy Pattern, Aspect-Oriented Programming, Subclassing

11. **30-second explanation (your own words)**  
    Wrap an object with other objects conforming to the same interface to add responsibilities dynamically.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
