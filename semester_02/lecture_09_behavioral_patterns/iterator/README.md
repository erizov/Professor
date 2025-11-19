# Iterator Pattern

1. **Name of Algorithm**  
   Iterator Pattern

2. **What problem does it solve? (1 sentence)**  
   Provides a standard way to traverse elements of a collection without exposing its internals.

3. **Intuition (plain-language explanation)**  
   Like flipping through a photo album with an index finger that remembers your current spot.

4. **Inputs & Outputs**  
   - Input: Collection with potentially complex storage (trees, graphs, aggregates).  
   - Output: Iterator objects supporting next(), has_next(), and optional remove().

5. **Step-by-step description (5–10 lines max)**  
1. Define Iterator interface with traversal methods.
2. Have collection expose factory method returning new iterator.
3. Iterator maintains traversal state (current index/node).
4. Clients use iterator to loop without knowing collection structure.
5. Provide specialized iterators (reverse, breadth-first) as needed.

6. **Tiny example (hand-simulated)**  
   Composite pattern provides a depth-first iterator to traverse nested components.

7. **Time & Space Complexity**  
   - Time: O(n) to traverse n elements.  
   - Space: O(1) to O(h) depending on iteration strategy (h = height for tree traversals).

8. **Strengths**  
- Supports multiple concurrent traversals.
- Keeps collection encapsulation intact.

9. **Weaknesses / limitations**  
- Custom iterators can be verbose to implement.
- Modifications during iteration need careful coordination.

10. **Compare with alternatives**  
    Alternatives: Generator Functions, Visitor Pattern, Indexed loops

11. **30-second explanation (your own words)**  
    Expose a traversal object so clients iterate over aggregates without coupling to internal representation.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
