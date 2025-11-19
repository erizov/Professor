# Message Queue

1. **Name of Algorithm**  
   Message Queue

2. **What problem does it solve? (1 sentence)**  
   Decouples producers and consumers of messages, enabling asynchronous communication, load balancing, and reliable message delivery.

3. **Intuition (plain-language explanation)**  
   Like a post office: producers drop messages in a queue, consumers pick them up when ready, allowing independent scaling and fault tolerance.

4. **Inputs & Outputs**  
   - Input: Messages from producers, queue configuration (durability, priority, TTL).  
   - Output: Reliable message delivery to consumers with ordering and persistence guarantees.

5. **Step-by-step description (5–10 lines max)**  
1. Producer sends message to queue (with optional routing key/topic).
2. Queue stores message (optionally persisted to disk).
3. Consumer subscribes to queue and receives messages.
4. Consumer processes message and sends acknowledgment.
5. Queue removes acknowledged message; retries on failure.

6. **Tiny example (hand-simulated)**  
   E-commerce: order service publishes OrderCreated to queue; inventory, payment, shipping services consume and process asynchronously.

7. **Time & Space Complexity**  
   - Time: Enqueue: O(1); Dequeue: O(1) to O(log n) depending on priority.  
   - Space: O(n) for n messages in queue (bounded by queue size limits).

8. **Strengths**  
- Decouples services and enables asynchronous processing.
- Provides reliability through persistence and retries.

9. **Weaknesses / limitations**  
- Message ordering may be lost in distributed systems.
- Requires monitoring and dead letter queue handling.

10. **Compare with alternatives**  
    Alternatives: Direct RPC, Event Streaming (Kafka), Pub/Sub

11. **30-second explanation (your own words)**  
    Buffers messages between producers and consumers, enabling asynchronous, decoupled communication with reliability guarantees.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
