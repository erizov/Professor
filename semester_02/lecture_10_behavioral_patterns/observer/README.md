# Observer Pattern

1. **Name of Algorithm**  
   Observer Pattern

2. **What problem does it solve? (1 sentence)**  
   Creates a one-to-many dependency so when one object changes state, all dependents are notified automatically.

3. **Intuition (plain-language explanation)**  
   Subject keeps a list of observers; when state changes, it broadcasts notifications to each observer.

4. **Inputs & Outputs**  
   - Input: Subject with observable state and observers that subscribe to updates.  
   - Output: Observers receive callbacks when the subject changes.

5. **Step-by-step description (5–10 lines max)**  
1. Define Subject interface with attach/detach/notify.
2. Observers implement an update method.
3. Subject maintains list of observers.
4. When state changes, subject iterates observers and calls update.
5. Observers react (e.g., refresh UI, trigger workflows).

6. **Tiny example (hand-simulated)**  
   GUI button (subject) notifies multiple listeners when clicked.

7. **Time & Space Complexity**  
   - Time: O(n) to notify n observers per event.  
   - Space: O(n) to store observers.

8. **Strengths**  
- Promotes loose coupling between subject and observers.
- Supports dynamic number of listeners.

9. **Weaknesses / limitations**  
- Notification order is not guaranteed.
- Observers can cause cascading updates or memory leaks if not detached.

10. **Compare with alternatives**  
    Alternatives: Publish-Subscribe, Mediator Pattern, Event Bus

11. **30-second explanation (your own words)**  
    Subjects expose subscription hooks so observers can register and automatically receive updates when state changes.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
