# Mocking

1. **Name of Algorithm**  
   Mocking

2. **What problem does it solve? (1 sentence)**  
   Replaces real dependencies with fake implementations during testing to isolate the unit under test and control test behavior.

3. **Intuition (plain-language explanation)**  
   Like using a stunt double in movies: replace real actors (dependencies) with stand-ins (mocks) to test scenes (units) in isolation.

4. **Inputs & Outputs**  
   - Input: Unit under test, dependencies to mock, expected behaviors and return values.  
   - Output: Isolated unit tests with controlled dependency behavior.

5. **Step-by-step description (5–10 lines max)**  
1. Identify external dependencies (databases, APIs, services).
2. Create mock objects that implement dependency interfaces.
3. Configure mock behavior (return values, exceptions, call counts).
4. Inject mocks into unit under test.
5. Execute test and verify interactions with mocks.
6. Assert expected calls and behaviors occurred.

6. **Tiny example (hand-simulated)**  
   Test user service: mock database to return fake user data, mock email service to verify email sent, test user creation logic in isolation.

7. **Time & Space Complexity**  
   - Time: O(1) for mock setup and execution (faster than real dependencies).  
   - Space: O(1) for mock objects (minimal memory overhead).

8. **Strengths**  
- Enables fast, isolated unit testing.
- Removes dependency on external systems.

9. **Weaknesses / limitations**  
- Mocks may not reflect real dependency behavior.
- Over-mocking can make tests brittle.

10. **Compare with alternatives**  
    Alternatives: Stubs, Fakes, Test Doubles, Dependency Injection

11. **30-second explanation (your own words)**  
    Uses fake implementations of dependencies to isolate units under test, enabling fast, controlled testing without external systems.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
