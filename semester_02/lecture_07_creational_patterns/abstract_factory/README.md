# Abstract Factory Pattern

1. **Name of Algorithm**  
   Abstract Factory Pattern

2. **What problem does it solve? (1 sentence)**  
   Creates families of related objects without specifying their concrete classes.

3. **Intuition (plain-language explanation)**  
   Like selecting a furniture style: the abstract factory hands you matching chair/sofa/table sets without exposing exact classes.

4. **Inputs & Outputs**  
   - Input: Client needing themed objects (UI widgets per OS, database drivers per vendor).  
   - Output: Factory interface with methods for each product family plus concrete factories per variant.

5. **Step-by-step description (5–10 lines max)**  
1. Identify product families that must stay consistent together.
2. Define abstract product interfaces for each family member.
3. Declare an AbstractFactory specifying creation methods.
4. Implement concrete factories returning concrete products in the same style.
5. Clients work only with factory and product interfaces; swap factories to change families.

6. **Tiny example (hand-simulated)**  
   GUI library supplies MacFactory and WindowsFactory producing consistent buttons, checkboxes, menus.

7. **Time & Space Complexity**  
   - Time: Object creation remains O(1); pattern adds indirection.  
   - Space: O(n) for concrete factory/product classes.

8. **Strengths**  
- Ensures product consistency across families.
- Encapsulates object creation behind interfaces.

9. **Weaknesses / limitations**  
- Adding a new product type requires touching all factories.
- More abstraction layers to maintain.

10. **Compare with alternatives**  
    Alternatives: Factory Method, Builder Pattern, Prototype

11. **30-second explanation (your own words)**  
    Provide an interface that creates entire families of related objects so clients can change themes by swapping factories.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
