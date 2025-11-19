# Vector Clocks

1. **Name of Algorithm**  
   Vector Clocks

2. **What problem does it solve? (1 sentence)**  
   Tracks causal relationships between events in distributed systems by assigning vector timestamps to events, enabling detection of happened-before relationships and causal ordering without global clocks.

3. **Intuition (plain-language explanation)**  
   Like a timeline with multiple tracks: vector clocks are like a timeline where each person (node) has their own track, and you mark when events happen on each track - when events from different tracks interact (like sending a message), you combine the timelines - this lets you figure out which events happened before others (causality) even though there's no single global clock - it's like having multiple synchronized watches that track not just time, but also who saw what when.

4. **Inputs & Outputs**  
   - Input: Events, node identifiers, messages, vector timestamps, causal relationships.  
   - Output: Vector timestamps, causal ordering, happened-before relationships, event ordering.

5. **Step-by-step description (5–10 lines max)**  
1. Initialize: each node starts with vector clock [0, 0, ..., 0] (one entry per node).
2. Local event: on local event, increment own clock entry.
3. Send message: when sending message, include current vector clock.
4. Receive message: when receiving message, merge with received vector clock.
5. Update: update own clock entry, and take maximum for each other node's entry.
6. Compare: compare vector clocks to determine happened-before relationships.
7. Order: use vector clocks to order events causally.
8. Detect: detect concurrent events (events with incomparable vector clocks).
9. Track: track causal dependencies across distributed system.
10. Use: use for causal consistency, debugging, and event ordering.

6. **Tiny example (hand-simulated)**  
   Vector clocks: 3 nodes (A, B, C) → A: event E1, clock [1,0,0] → A sends to B: message with [1,0,0] → B: receives, updates to [1,1,0] → B: event E2, clock [1,2,0] → B sends to C: [1,2,0] → C: receives, updates to [1,2,1] → compare: [1,0,0] < [1,2,0] → E1 happened before E2 → vector clocks track causality.

7. **Time & Space Complexity**  
   - Time: O(n) for clock operations where n is number of nodes.  
   - Space: O(n) per event where n is number of nodes (vector size).

8. **Strengths**  
- Causality: accurately tracks causal relationships between events.
- No global clock: doesn't require synchronized global clocks.
- Concurrency detection: can detect concurrent events.

9. **Weaknesses / limitations**  
- Space: vector size grows with number of nodes.
- Scalability: may not scale well to very large numbers of nodes.
- Complexity: more complex than scalar timestamps.

10. **Compare with alternatives**  
    Alternatives: Logical Clocks, Lamport Timestamps, Hybrid Logical Clocks, TrueTime

11. **30-second explanation (your own words)**  
    Tracks causal relationships between events in distributed systems by assigning vector timestamps to events, enabling detection of happened-before relationships and causal ordering without global clocks.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
