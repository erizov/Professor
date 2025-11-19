# Template Method Pattern

1. **Name of Algorithm**  
   Template Method Pattern

2. **What problem does it solve? (1 sentence)**  
Defines the skeleton of an algorithm in a base class while letting subclasses override specific steps.

3. **Intuition (plain-language explanation)**  
   Recipe template: the base class outlines the process, subclasses supply the ingredient variations.

4. **Inputs & Outputs**  
- Input: Algorithm with invariant structure but customizable steps.
   - Output: Abstract class with template method calling primitive operations that subclasses override.

5. **Step-by-step description (5–10 lines max)**  
1. Identify invariant workflow steps and variable steps.
2. Implement template_method() in base class orchestrating the workflow.
3. Mark variable steps as abstract or provide default hooks.
4. Subclasses override the hook methods to customize behavior.
5. Optional hooks allow subclasses to insert logic before/after key steps.

6. **Tiny example (hand-simulated)**  
   DocumentExporter defines export(): open → format → save; subclasses override format().

7. **Time & Space Complexity**  
   - Time: Equals sum of step complexities; overhead is minimal virtual dispatch.  
   - Space: O(1) additional space.

8. **Strengths**  
- Promotes code reuse for algorithm skeletons.
- Enforces consistent workflow across subclasses.

9. **Weaknesses / limitations**  
- Inheritance-based, so variations require subclassing.
- Difficult to change algorithm order without altering base class.

10. **Compare with alternatives**  
    Alternatives: Strategy Pattern, Hooks/Callbacks, Pipeline Pattern

11. **30-second explanation (your own words)**  
Put the invariant algorithm flow in a base class and let subclasses override specific steps via hook methods.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
