# Single Responsibility Principle

1. **Name of Algorithm**  
   Single Responsibility Principle

2. **What problem does it solve? (1 sentence)**  
   Ensures each class or module has exactly one reason to change.

3. **Intuition (plain-language explanation)**  
   Treat classes like specialists: one job, done well, so changes in one concern don’t ripple through unrelated code.

4. **Inputs & Outputs**  
   - Input: Object-oriented modules with multiple responsibilities entangled.  
   - Output: Refactored components where each focuses on a single responsibility.

5. **Step-by-step description (5–10 lines max)**  
1. Identify all reasons why the class might change (UI tweaks, business rules, persistence, etc.).
2. Group behaviors by responsibility and highlight unrelated clusters.
3. Extract new classes/functions for secondary responsibilities.
4. Inject dependencies so each class collaborates instead of owning all logic.
5. Add tests per responsibility to prove isolation.

6. **Tiny example (hand-simulated)**  
   A Report class both formats PDFs and queries the database → split into ReportGenerator + ReportRepository.

7. **Time & Space Complexity**  
   - Time: Refactoring effort proportional to responsibilities discovered.  
   - Space: Extra classes/files for separated responsibilities.

8. **Strengths**  
- Improves cohesion and readability.
- Reduces blast radius when business rules evolve.

9. **Weaknesses / limitations**  
- May introduce more classes/interfaces to navigate.
- Requires discipline to maintain separation over time.

10. **Compare with alternatives**  
    Alternatives: Modularization, Functional Decomposition, Componentization

11. **30-second explanation (your own words)**  
    Keep each module focused on one reason to change so maintenance stays local and predictable.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
