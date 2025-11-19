# Integration Testing

1. **Name of Algorithm**  
   Integration Testing

2. **What problem does it solve? (1 sentence)**  
Tests interactions between multiple components or systems to ensure they work together correctly as an integrated unit.

3. **Intuition (plain-language explanation)**  
   Like testing a car's engine and transmission together: individual parts may work, but integration testing verifies they function as a cohesive system.

4. **Inputs & Outputs**  
   - Input: Multiple components or services, test data, integration test scenarios.  
   - Output: Test results verifying component interactions, data flow, and system behavior.

5. **Step-by-step description (5–10 lines max)**  
1. Identify integration points between components.
2. Set up test environment with all required components.
3. Execute test scenarios that exercise component interactions.
4. Verify data flows correctly between components.
5. Check error handling and edge cases at boundaries.
6. Validate end-to-end workflows.

6. **Tiny example (hand-simulated)**  
   E-commerce: test order service integrates with payment service and inventory service; verify order creation triggers payment processing and inventory deduction.

7. **Time & Space Complexity**  
   - Time: O(n) where n is number of components and interactions tested.  
   - Space: O(n) for test environment setup and component state.

8. **Strengths**  
- Catches bugs in component interactions early.
- Validates real-world system behavior.

9. **Weaknesses / limitations**  
- Slower and more complex than unit tests.
- Requires full test environment setup.

10. **Compare with alternatives**  
    Alternatives: Unit Testing, End-to-End Testing, Contract Testing

11. **30-second explanation (your own words)**  
Tests multiple components together to ensure they integrate correctly and work as a unified system.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
