# Composite Pattern

1. **Name of Algorithm**  
   Composite Pattern

2. **What problem does it solve? (1 sentence)**  
   Treats individual objects and compositions uniformly (tree structures).

3. **Intuition (plain-language explanation)**  
   File systems treat files and directories with the same interface; composites hold children, leaves perform real work.

4. **Inputs & Outputs**  
   - Input: Recursive structures needing hierarchical operations (rendering UI trees, calculating totals).  
   - Output: Component interface with Leaf and Composite implementations.

5. **Step-by-step description (5–10 lines max)**  
1. Define a common Component interface with operations clients need.
2. Implement Leaf for atomic objects.
3. Implement Composite storing child components; delegate operations to children.
4. Expose child-management methods (add/remove) on Composite.
5. Ensure clients only depend on the Component interface.

6. **Tiny example (hand-simulated)**  
   Graphic objects: Line, Circle (leaves) and Group (composite) so drawing occurs recursively.

7. **Time & Space Complexity**  
   - Time: Operations typically traverse entire subtree: O(n) where n is number of nodes touched.  
   - Space: O(n) to store tree plus recursion stack.

8. **Strengths**  
- Simplifies client code—treat everything as Component.
- Naturally models hierarchical data.

9. **Weaknesses / limitations**  
- Hard to restrict which composites may contain which components.
- Can complicate operations needing parent references.

10. **Compare with alternatives**  
    Alternatives: Visitor Pattern, Decorator Pattern, Flyweight

11. **30-second explanation (your own words)**  
    Build tree structures where clients operate on components without caring if they’re leaves or composites.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
