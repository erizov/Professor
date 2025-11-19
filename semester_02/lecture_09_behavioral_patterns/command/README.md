# Command Pattern

1. **Name of Algorithm**  
   Command Pattern

2. **What problem does it solve? (1 sentence)**  
   Encapsulates a request as an object so it can be queued, logged, undone, or replayed.

3. **Intuition (plain-language explanation)**  
   Just like a remote control storing button presses as commands you can redo/undo later.

4. **Inputs & Outputs**  
   - Input: Receiver object performing work and invoker scheduling commands.  
   - Output: Command objects implementing execute() (and optionally undo()).

5. **Step-by-step description (5–10 lines max)**  
1. Define Command interface with execute()/undo().
2. Implement concrete commands wrapping receiver operations.
3. Invoker stores commands and triggers execute at the right time.
4. Maintain history stack if undo/redo is needed.
5. Optionally serialize commands for auditing or retries.

6. **Tiny example (hand-simulated)**  
   Text editor operations (InsertTextCommand, DeleteSelectionCommand) recorded for undo functionality.

7. **Time & Space Complexity**  
   - Time: Exec time equals receiver operation plus bookkeeping.  
   - Space: O(n) to store command history.

8. **Strengths**  
- Decouples senders from receivers.
- Enables undo/redo, macro recording, and asynchronous execution.

9. **Weaknesses / limitations**  
- Lots of small command classes.
- Stateful commands must carefully manage context for undo.

10. **Compare with alternatives**  
    Alternatives: Event Sourcing, Strategy Pattern, Lambda commands

11. **30-second explanation (your own words)**  
    Wrap each action in a command object so invokers can queue, log, or undo requests independently of receivers.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
