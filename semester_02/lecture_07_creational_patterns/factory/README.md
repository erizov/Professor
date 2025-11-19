# Factory Method Pattern

1. **Name of Algorithm**  
   Factory Method Pattern

2. **What problem does it solve? (1 sentence)**  
   Defers instantiation to subclasses, letting them decide which concrete class to create.

3. **Intuition (plain-language explanation)**  
   A base class provides a hook for creating collaborators; subclasses override to supply specific types.

4. **Inputs & Outputs**  
   - Input: Superclass defining algorithm that depends on product objects.  
   - Output: factory_method() returning a Product interface implemented by subclasses.

5. **Step-by-step description (5–10 lines max)**  
1. Define Product interface implemented by concrete products.
2. Create Creator base class with factory_method() returning Product.
3. Implement default algorithm in Creator that calls factory_method().
4. Subclass Creator to override factory_method() and return concrete products.
5. Clients use Creator interface; subclass decides actual product.

6. **Tiny example (hand-simulated)**  
   Application::createDocument() overridden by TextApp and SpreadsheetApp to return respective documents.

7. **Time & Space Complexity**  
   - Time: Same as product creation plus virtual call overhead.  
   - Space: O(n) for subclasses implementing factory method.

8. **Strengths**  
- Promotes loose coupling between creators and products.
- Allows new products by subclassing without touching base logic.

9. **Weaknesses / limitations**  
- Requires subclass for each product variant.
- Can lead to parallel class hierarchies.

10. **Compare with alternatives**  
    Alternatives: Abstract Factory, Simple Factory, Builder

11. **30-second explanation (your own words)**  
    Let subclasses decide which product to instantiate by overriding a factory method used by shared creator logic.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
