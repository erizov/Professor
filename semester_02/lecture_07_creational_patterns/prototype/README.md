# Prototype Pattern

1. **Name of Algorithm**  
   Prototype Pattern

2. **What problem does it solve? (1 sentence)**  
   Creates new objects by cloning existing ones when instantiation cost is high or classes are dynamic.

3. **Intuition (plain-language explanation)**  
   Make copies from a mold: keep prototypes and clone them instead of constructing from scratch.

4. **Inputs & Outputs**  
   - Input: Prototype registry storing exemplar objects capable of deep/shallow cloning.  
   - Output: clone() operations returning duplicated objects with optional tweaks.

5. **Step-by-step description (5–10 lines max)**  
1. Implement prototype interface with clone() method.
2. Store registered prototypes in a lookup table.
3. To create a new object, retrieve prototype and clone it.
4. Customize cloned instance (e.g., set new IDs).
5. Ensure deep copies for mutable nested objects to avoid shared state.

6. **Tiny example (hand-simulated)**  
   Graphics editor clones shapes (circles, arrows) to duplicate user-drawn elements quickly.

7. **Time & Space Complexity**  
   - Time: Depends on clone depth; typically O(size of object graph).  
   - Space: O(size) to duplicate object graph per clone.

8. **Strengths**  
- Avoids complex constructor logic for each new instance.
- Supports runtime addition of new prototype types.

9. **Weaknesses / limitations**  
- Implementing deep cloning can be tricky.
- Hidden coupling when prototypes share mutable state.

10. **Compare with alternatives**  
    Alternatives: Builder Pattern, Abstract Factory, Serialization copy

11. **30-second explanation (your own words)**  
    Register exemplar objects and copy them to produce new instances whenever direct construction is expensive or dynamic.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
