# Actor Model

1. **Name of Algorithm**  
   Actor Model

2. **What problem does it solve? (1 sentence)**  
   Models concurrent computation using actors (independent computational entities) that communicate through asynchronous message passing, avoiding shared state and locks for better scalability and fault tolerance.

3. **Intuition (plain-language explanation)**  
Like a company with independent departments: the actor model is like a company where each department (actor) works independently and communicates with other departments only through messages (like emails) - departments don't share resources directly (no shared state), they send messages and wait for replies (asynchronous communication) - if one department has a problem (actor crashes), it doesn't affect others (fault isolation), and you can easily add more departments (scale horizontally).

4. **Inputs & Outputs**  
   - Input: Messages, actor definitions, actor system configuration, supervision strategies.  
   - Output: Concurrent computation, message passing, isolated state, fault-tolerant system.

5. **Step-by-step description (5–10 lines max)**  
1. Define actors: create actor types with message handlers and state.
2. Create system: initialize actor system and supervision hierarchy.
3. Spawn actors: create actor instances (mailboxes, state, behavior).
4. Send messages: actors send asynchronous messages to other actors.
5. Receive messages: actors process messages from their mailboxes sequentially.
6. Update state: actors update their internal state based on messages.
7. Reply: actors send reply messages back to senders if needed.
8. Supervise: supervisor actors monitor and restart failed actors.
9. Scale: distribute actors across multiple nodes for scalability.
10. Monitor: track actor behavior, message flow, and system health.

6. **Tiny example (hand-simulated)**  
   Actor model: e-commerce system → actors: UserActor, OrderActor, PaymentActor, InventoryActor → UserActor sends 'place order' message to OrderActor → OrderActor sends 'check inventory' to InventoryActor → InventoryActor replies 'in stock' → OrderActor sends 'process payment' to PaymentActor → PaymentActor replies 'paid' → OrderActor updates state and replies to UserActor → no shared state, no locks → scalable, fault-tolerant → actor model.

7. **Time & Space Complexity**  
   - Time: O(1) for message send, O(m) for message processing where m is message complexity.  
   - Space: O(a + m) where a is number of actors, m is total messages in mailboxes.

8. **Strengths**  
- Scalability: naturally scales to distributed systems.
- Fault tolerance: actor failures are isolated and can be recovered.
- No locks: avoids deadlocks and race conditions through message passing.

9. **Weaknesses / limitations**  
- Message overhead: message passing has overhead compared to shared memory.
- Debugging: debugging distributed actor systems can be challenging.
- Ordering: message ordering guarantees may be complex in distributed systems.

10. **Compare with alternatives**  
    Alternatives: Shared Memory Concurrency, CSP Model, Message Queues, Reactive Streams

11. **30-second explanation (your own words)**  
    Models concurrent computation using actors (independent computational entities) that communicate through asynchronous message passing, avoiding shared state and locks for better scalability and fault tolerance.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
