# TDD (Test-Driven Development)

1. **Name of Algorithm**  
   TDD (Test-Driven Development)

2. **What problem does it solve? (1 sentence)**  
   Develops software by writing tests before implementation, ensuring code meets requirements and maintains high test coverage.

3. **Intuition (plain-language explanation)**  
   Write the test first (specification), then write code to pass it: like building a house by first drawing blueprints, then constructing to match.

4. **Inputs & Outputs**  
   - Input: Requirements, test cases, implementation code.  
   - Output: Working code with comprehensive test coverage and clear specifications.

5. **Step-by-step description (5–10 lines max)**  
1. Write a failing test for a small feature (Red phase).
2. Write minimal code to make the test pass (Green phase).
3. Refactor code while keeping tests green (Refactor phase).
4. Repeat cycle for next feature.
5. Maintain test suite as codebase grows.

6. **Tiny example (hand-simulated)**  
   Feature: calculate discount. Write test expecting 10% discount → test fails → implement discount calculation → test passes → refactor if needed.

7. **Time & Space Complexity**  
   - Time: O(n) where n is number of features (each requires test + implementation).  
   - Space: O(n) for test code and implementation code.

8. **Strengths**  
- High test coverage and confidence in code.
- Clear requirements through executable tests.

9. **Weaknesses / limitations**  
- Initial development may be slower.
- Requires discipline to maintain TDD cycle.

10. **Compare with alternatives**  
    Alternatives: BDD (Behavior-Driven Development), Test-After Development, Property-Based Testing

11. **30-second explanation (your own words)**  
    Develops code by first writing tests that define desired behavior, then implementing code to satisfy those tests, ensuring requirements are met.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
