# Bridge Pattern

1. **Name of Algorithm**  
   Bridge Pattern

2. **What problem does it solve? (1 sentence)**  
   Decouples abstractions from their implementations so both can vary independently.

3. **Intuition (plain-language explanation)**  
   Think of a remote control talking to different TVs: the remote is the abstraction, the TV electronics are implementations.

4. **Inputs & Outputs**  
   - Input: Hierarchy where multiple dimensions of variation (e.g., shape vs. rendering API) would otherwise explode subclasses.  
   - Output: Two orthogonal class hierarchies linked via composition.

5. **Step-by-step description (5–10 lines max)**  
1. Split the abstraction (high-level operations) from the implementation (platform-specific work).
2. Define an implementation interface with primitive operations.
3. Have the abstraction hold a reference to the implementation and delegate calls.
4. Subclass both sides independently as variation requires.
5. Provide wiring (factories/DI) to pair abstraction with concrete implementation.

6. **Tiny example (hand-simulated)**  
   Shape abstraction (Circle, Square) delegates draw() to Renderer implementation (VectorRenderer, RasterRenderer).

7. **Time & Space Complexity**  
   - Time: Same as underlying implementation plus indirection.  
   - Space: One reference from abstraction to implementation.

8. **Strengths**  
- Prevents class explosion when combining variation axes.
- Allows runtime swapping of implementations.

9. **Weaknesses / limitations**  
- More moving parts compared to simple inheritance.
- Requires careful naming to keep roles clear.

10. **Compare with alternatives**  
    Alternatives: Strategy Pattern, Abstract Factory, Adapter

11. **30-second explanation (your own words)**  
    Compose abstractions with implementations so each can evolve on its own timeline without recompiling the other.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
