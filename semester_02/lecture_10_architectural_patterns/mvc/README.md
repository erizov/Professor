# Model-View-Controller (MVC)

1. **Name of Algorithm**  
   Model-View-Controller (MVC)

2. **What problem does it solve? (1 sentence)**  
   Separates domain state (model), user interface (view), and input handling (controller) to build maintainable GUIs and web apps.

3. **Intuition (plain-language explanation)**  
   Controller handles user input, updates the model, and selects a view; view renders model data back to the user.

4. **Inputs & Outputs**  
   - Input: User interactions routed through controllers, domain models storing data, view templates displaying data.  
   - Output: Rendered UI plus updated models reflecting user actions.

5. **Step-by-step description (5–10 lines max)**  
1. Controller receives user action (HTTP request, button click).
2. Controller validates input and invokes model operations.
3. Model updates state and notifies observers if needed.
4. Controller selects a view and provides model data.
5. View renders output to user.

6. **Tiny example (hand-simulated)**  
   Todo app: controller handles /add request, model saves task, view renders updated list.

7. **Time & Space Complexity**  
   - Time: Depends on model operations; architectural pattern.  
   - Space: Depends on domain data.

8. **Strengths**  
- Clear separation of concerns improves testability.
- Multiple views can reuse the same models.

9. **Weaknesses / limitations**  
- Controller and view coupling can grow complex in large apps.
- Not ideal for heavily event-driven UIs without additional patterns.

10. **Compare with alternatives**  
    Alternatives: MVVM, MVP, Clean Architecture

11. **30-second explanation (your own words)**  
    Split application logic into model, view, and controller layers so UI changes do not leak into business logic.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
