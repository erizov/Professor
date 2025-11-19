# Dependency Inversion Principle

1. **Name of Algorithm**  
   Dependency Inversion Principle

2. **What problem does it solve? (1 sentence)**  
   High-level modules should not depend on low-level details; both should rely on abstractions.

3. **Intuition (plain-language explanation)**  
   Make policies depend on interfaces, not concrete wiring—like plugging different chargers into the same standard outlet.

4. **Inputs & Outputs**  
   - Input: Tightly coupled modules where business logic instantiates infrastructure details.  
   - Output: Abstractions (interfaces, ports) with concrete implementations supplied via inversion of control.

5. **Step-by-step description (5–10 lines max)**  
1. Identify high-level policies that currently create or depend on concrete classes.
2. Define abstractions capturing the required behavior.
3. Make high-level code depend on the abstractions instead of concretes.
4. Provide implementations via constructors, factories, or DI containers.
5. Write integration tests that swap implementations to ensure decoupling.

6. **Tiny example (hand-simulated)**  
   OrderService new EmailNotifier() → instead depend on Notifier interface and inject EmailNotifier or SmsNotifier.

7. **Time & Space Complexity**  
   - Time: Adds indirection proportional to number of dependencies.  
   - Space: Requires extra interfaces and binding configuration.

8. **Strengths**  
- Improves testability via mocks/stubs.
- Encourages reusable high-level policies.

9. **Weaknesses / limitations**  
- More abstractions can complicate debugging.
- Needs tooling (DI containers) to stay manageable at scale.

10. **Compare with alternatives**  
    Alternatives: Service Locator, Inversion of Control Containers, Plugin Architecture

11. **30-second explanation (your own words)**  
    Depend on abstractions so high-level logic stays stable while low-level details swap freely.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
