# Builder Pattern

1. **Name of Algorithm**  
   Builder Pattern

2. **What problem does it solve? (1 sentence)**  
   Constructs complex objects step-by-step, allowing different representations with the same construction process.

3. **Intuition (plain-language explanation)**  
   Like ordering a custom burger: the builder tracks each ingredient while the director ensures the steps stay consistent.

4. **Inputs & Outputs**  
   - Input: Complex object with many optional parts or configurations.  
   - Output: Builder interface declaring construction steps and a Director orchestrating them.

5. **Step-by-step description (5–10 lines max)**  
1. Define Builder with methods for each part (setEngine, addSeats, etc.).
2. Implement concrete builders producing different representations (e.g., CarBuilder vs. ManualBuilder).
3. Director controls the order of steps for a given recipe.
4. Client retrieves finished object from builder.
5. Optionally let clients bypass Director for custom builds.

6. **Tiny example (hand-simulated)**  
   VehicleBuilder constructs Car objects while ManualBuilder outputs a car manual using the same steps.

7. **Time & Space Complexity**  
   - Time: Linear in number of build steps.  
   - Space: Builder stores interim state until product is assembled.

8. **Strengths**  
- Separates complex construction from representation.
- Supports progressive object creation and validation.

9. **Weaknesses / limitations**  
- Requires multiple builder classes when variants explode.
- Director adds ceremony for simple objects.

10. **Compare with alternatives**  
    Alternatives: Fluent Interfaces, Factory Method, Composite constructors

11. **30-second explanation (your own words)**  
    Encapsulate construction steps in builders so the same process can create different representations of a complex object.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
