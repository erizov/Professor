# Interface Segregation Principle

1. **Name of Algorithm**  
   Interface Segregation Principle

2. **What problem does it solve? (1 sentence)**  
   Clients should not be forced to depend on methods they do not use.

3. **Intuition (plain-language explanation)**  
   Give each client a tailored remote control; bloated interfaces force consumers to worry about buttons they never press.

4. **Inputs & Outputs**  
   - Input: Large interfaces implemented by many classes with empty or throwing methods.  
   - Output: Smaller, client-specific interfaces implemented by relevant classes.

5. **Step-by-step description (5–10 lines max)**  
1. List interface methods and map them to actual client usage.
2. Identify clusters of methods used together by specific clients.
3. Split the interface into cohesive sub-interfaces.
4. Update classes to implement only the interfaces they need.
5. Refactor clients to depend on the refined contracts.

6. **Tiny example (hand-simulated)**  
IMultiFunctionDevice exposes print/scan/fax; a scanner-only device should not implement fax, so split into IPrinter, IScanner, IFax.

7. **Time & Space Complexity**  
   - Time: Refactor effort grows with number of clients.  
   - Space: More interface definitions to maintain.

8. **Strengths**  
- Reduces stub methods and unused dependencies.
- Improves readability and compile-time safety.

9. **Weaknesses / limitations**  
- Too many interfaces can overwhelm newcomers.
- Requires coordination when clients share overlapping needs.

10. **Compare with alternatives**  
    Alternatives: Adapter Pattern, Role Interfaces, Service Facades

11. **30-second explanation (your own words)**  
    Favor many small interfaces over one large one so consumers only depend on what they actually use.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
