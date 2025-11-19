# Unit Testing

1. **Name of Algorithm**  
   Unit Testing

2. **What problem does it solve? (1 sentence)**  
   Tests individual units of code (functions, methods, classes) in isolation to verify they behave correctly according to specifications.

3. **Intuition (plain-language explanation)**  
   Like testing each ingredient separately before cooking: verify each function works correctly before testing the whole recipe.

4. **Inputs & Outputs**  
   - Input: Unit of code (function/method), test inputs, expected outputs.  
   - Output: Test results indicating whether unit behaves correctly.

5. **Step-by-step description (5–10 lines max)**  
1. Identify unit to test (function, method, or class).
2. Prepare test inputs and expected outputs.
3. Execute unit with test inputs.
4. Assert actual outputs match expected outputs.
5. Test edge cases and error conditions.
6. Verify unit works in isolation (mock dependencies).

6. **Tiny example (hand-simulated)**  
   Test calculateTotal function: input [1,2,3] → expected output 6 → assert result equals 6. Test with empty list, negative numbers, null input.

7. **Time & Space Complexity**  
   - Time: O(1) to O(n) depending on unit complexity (fast execution).  
   - Space: O(1) for test data (minimal memory usage).

8. **Strengths**  
- Fast execution and quick feedback.
- Isolates bugs to specific units.

9. **Weaknesses / limitations**  
- Doesn't catch integration issues.
- Requires mocking external dependencies.

10. **Compare with alternatives**  
    Alternatives: Integration Testing, System Testing, End-to-End Testing

11. **30-second explanation (your own words)**  
    Tests individual code units in isolation to verify correct behavior, providing fast feedback and early bug detection.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
