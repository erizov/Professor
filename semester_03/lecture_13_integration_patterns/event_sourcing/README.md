# Event Sourcing

1. **Name of Algorithm**  
   Event Sourcing

2. **What problem does it solve? (1 sentence)**  
   Stores all changes to application state as a sequence of events, enabling time travel, audit trails, and rebuilding state from events.

3. **Intuition (plain-language explanation)**  
   Instead of storing current state, store every event that happened: like a bank statement, you can replay events to reconstruct any point in time.

4. **Inputs & Outputs**  
   - Input: Domain events representing state changes (e.g., OrderCreated, PaymentReceived, ItemShipped).  
   - Output: Event store (append-only log) and reconstructed current state from events.

5. **Step-by-step description (5–10 lines max)**  
1. Capture all state changes as immutable events.
2. Append events to event store (append-only log).
3. Replay events to rebuild current state (projection).
4. Optionally create multiple read models from events.
5. Support event versioning and schema evolution.

6. **Tiny example (hand-simulated)**  
   Order system: events [OrderCreated, ItemAdded, PaymentReceived, ItemShipped]. Replay to get current order state or historical view at any time.

7. **Time & Space Complexity**  
   - Time: Write: O(1) append; Read: O(n) to replay n events for state reconstruction.  
   - Space: O(n) for n events (grows over time; may need snapshots for performance).

8. **Strengths**  
- Complete audit trail and time travel capabilities.
- Natural fit for event-driven architectures.

9. **Weaknesses / limitations**  
- Event store grows indefinitely (requires snapshots/archiving).
- Complexity in handling schema changes and event versioning.

10. **Compare with alternatives**  
    Alternatives: Traditional State Storage, CQRS, Change Data Capture (CDC)

11. **30-second explanation (your own words)**  
    Stores state changes as immutable events in an append-only log, enabling state reconstruction, auditing, and temporal queries.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
