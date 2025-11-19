# Publish-Subscribe (Pub/Sub)

1. **Name of Algorithm**  
   Publish-Subscribe (Pub/Sub)

2. **What problem does it solve? (1 sentence)**  
   Enables one-to-many message distribution where publishers send messages to topics, and multiple subscribers receive copies independently.

3. **Intuition (plain-language explanation)**  
   Like a radio station: broadcaster (publisher) sends to a channel (topic), and all listeners (subscribers) tuned to that channel receive the message.

4. **Inputs & Outputs**  
   - Input: Messages published to topics, subscriber subscriptions to topics.  
   - Output: Message delivery to all subscribers of a topic.

5. **Step-by-step description (5–10 lines max)**  
1. Publisher sends message to a topic (not specific subscribers).
2. Message broker routes message to all subscribers of that topic.
3. Each subscriber receives independent copy of message.
4. Subscribers process messages asynchronously.
5. Broker handles delivery guarantees (at-least-once, exactly-once).

6. **Tiny example (hand-simulated)**  
   News system: publisher sends 'Breaking News' to 'news' topic; email service, SMS service, and push notification service all receive and process.

7. **Time & Space Complexity**  
   - Time: Publish: O(1) to O(s) where s is number of subscribers; Subscribe: O(1).  
   - Space: O(n·s) for n messages and s subscribers (each gets copy).

8. **Strengths**  
- Loose coupling between publishers and subscribers.
- Easy to add/remove subscribers without affecting publishers.

9. **Weaknesses / limitations**  
- No direct feedback from subscribers to publishers.
- Message delivery guarantees vary by implementation.

10. **Compare with alternatives**  
    Alternatives: Message Queue (point-to-point), Event Streaming, Observer Pattern

11. **30-second explanation (your own words)**  
    Decouples publishers from subscribers through topics, enabling broadcast-style messaging where multiple subscribers receive the same message.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
