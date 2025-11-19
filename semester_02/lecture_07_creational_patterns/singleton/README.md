# Singleton Pattern

1. **Name of Algorithm**  
   Singleton Pattern

2. **What problem does it solve? (1 sentence)**  
   Ensures a class has only one instance and provides a global access point.

3. **Intuition (plain-language explanation)**  
   System-wide resource manager (e.g., print spooler) that must exist exactly once.

4. **Inputs & Outputs**  
   - Input: Class needing single shared state across application.  
   - Output: Private constructor, static get_instance() method, and stored singleton instance.

5. **Step-by-step description (5–10 lines max)**  
1. Make constructor private/protected to prevent external instantiation.
2. Expose static method that returns the single instance.
3. Instantiate lazily or eagerly inside the static method.
4. Ensure thread safety in multi-threaded environments.
5. Prevent cloning/serialization from creating additional instances.

6. **Tiny example (hand-simulated)**  
   ConfigurationManager loads config once and offers global access to settings.

7. **Time & Space Complexity**  
   - Time: get_instance() typically O(1); synchronization can add contention.  
   - Space: O(1) for stored instance.

8. **Strengths**  
- Ensures single point of coordination.
- Lazy initialization reduces startup cost.

9. **Weaknesses / limitations**  
- Global state hampers testability and introduces hidden dependencies.
- Difficult to scale/distribute.
- Thread-safe implementations can be verbose.

10. **Compare with alternatives**  
    Alternatives: Dependency Injection, Static Classes, Module-level singletons

11. **30-second explanation (your own words)**  
    Control instantiation so exactly one object exists and is accessible globally, but use sparingly due to testability concerns.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
