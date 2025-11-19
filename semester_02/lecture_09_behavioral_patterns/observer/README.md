# Observer Pattern

1. **Name of Algorithm**  
   Observer Pattern

2. **What problem does it solve? (1 sentence)**  
   Notifies multiple dependents automatically when a subject’s state changes.

3. **Intuition (plain-language explanation)**  
   Publish/subscribe: when the weather station updates, all registered displays react immediately.

4. **Inputs & Outputs**  
   - Input: Subject maintaining state and observers interested in changes.  
   - Output: Subscription mechanism where observers register for callbacks.

5. **Step-by-step description (5–10 lines max)**  
1. Subject exposes attach(), detach(), and notify() methods.
2. Observers implement an interface (update(subject)).
3. Subject calls notify() after state changes, iterating observers.
4. Observers pull new state from subject or receive it as arguments.
5. Ensure thread-safety and order guarantees if required.

6. **Tiny example (hand-simulated)**  
   Stock ticker pushing price updates to dashboards and alert services.

7. **Time & Space Complexity**  
   - Time: O(n) per notification where n is number of observers.  
   - Space: O(n) to track observer references.

8. **Strengths**  
- Loose coupling between subjects and observers.
- Supports dynamic subscriptions at runtime.

9. **Weaknesses / limitations**  
- Notification storms if observers perform heavy work.
- Difficult to debug notification order and memory leaks from forgotten detach().

10. **Compare with alternatives**  
    Alternatives: Event Bus, Reactive Streams, Mediator Pattern

11. **30-second explanation (your own words)**  
    Let observers subscribe to a subject so they are automatically notified whenever the subject changes state.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
