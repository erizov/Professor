# Model-View-ViewModel (MVVM)

1. **Name of Algorithm**  
   Model-View-ViewModel (MVVM)

2. **What problem does it solve? (1 sentence)**  
   Decouples UI rendering from presentation logic using data binding between views and view-models.

3. **Intuition (plain-language explanation)**  
   ViewModel exposes observable state; the view binds to it and updates automatically when data changes.

4. **Inputs & Outputs**  
   - Input: Model (domain data), ViewModel (presentation state + commands), View (UI components with bindings).  
   - Output: Responsive UI that reflects ViewModel changes without manual wiring.

5. **Step-by-step description (5–10 lines max)**  
1. Wrap models in ViewModel objects exposing observable properties.
2. Define commands/actions in the ViewModel.
3. Bind view controls to ViewModel properties and commands.
4. Update ViewModel in response to user input; binding updates view automatically.
5. Synchronize ViewModel changes back to models as needed.

6. **Tiny example (hand-simulated)**  
   WPF app: ViewModel exposes ObservableCollection<Todo>, view binds ListBox.ItemsSource; adding an item updates UI instantly.

7. **Time & Space Complexity**  
   - Time: Depends on underlying model operations.  
   - Space: Depends on number of ViewModels and bindings.

8. **Strengths**  
- Great for data-binding frameworks (WPF, SwiftUI, Android).
- Facilitates unit testing of presentation logic.

9. **Weaknesses / limitations**  
- Requires binding infrastructure; not ideal for simple UIs.
- Two-way binding can obscure data flow.

10. **Compare with alternatives**  
    Alternatives: MVC, MVP, Redux-style state management

11. **30-second explanation (your own words)**  
    Expose presentation logic via observable ViewModels so UI updates automatically when data changes and vice versa.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
