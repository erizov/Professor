# Event-Driven Architecture

1. **Name of Algorithm**  
   Event-Driven Architecture

2. **What problem does it solve? (1 sentence)**  
   Designs systems where components communicate through events, enabling loose coupling, scalability, and responsiveness to changes, making systems more flexible and resilient.

3. **Intuition (plain-language explanation)**  
   Like a news broadcast: Event-Driven Architecture is like a news broadcast system - when something happens (event occurs), it's broadcast to everyone who's interested (subscribers) - they can react independently without knowing about each other - just as news stations broadcast events and listeners tune in to what they care about, event-driven systems broadcast events and services react to what they're interested in, creating a loosely coupled, responsive system.

4. **Inputs & Outputs**  
   - Input: Events, event producers, event consumers, event bus/broker, event schemas, routing rules.  
   - Output: Published events, consumed events, reactive behaviors, decoupled services, scalable system.

5. **Step-by-step description (5–10 lines max)**  
1. Define events: define event types and schemas.
2. Publish: producers publish events to event bus.
3. Route: event bus routes events to interested consumers.
4. Subscribe: consumers subscribe to event types they care about.
5. Receive: consumers receive events from event bus.
6. Process: consumers process events and perform actions.
7. React: consumers react to events independently.
8. Scale: scale producers and consumers independently.
9. Monitor: monitor event flow and processing.
10. Handle failures: handle event processing failures (retry, dead letter queue).

6. **Tiny example (hand-simulated)**  
   Event-Driven Architecture: user registers → producer: publish UserRegistered event → event bus: route to subscribers → email service: subscribe, send welcome email → analytics service: subscribe, track registration → notification service: subscribe, send notification → services react independently → Event-Driven Architecture operational.

7. **Time & Space Complexity**  
   - Time: O(1) for event publishing, O(n) for routing where n is number of subscribers.  
   - Space: O(e + s) where e is event storage, s is subscriber state (event queue per subscriber).

8. **Strengths**  
- Decoupling: loose coupling between producers and consumers.
- Scalability: enables horizontal scaling of consumers.
- Responsiveness: systems react to events in real-time.

9. **Weaknesses / limitations**  
- Complexity: event flow can be complex to understand and debug.
- Consistency: eventual consistency challenges.
- Event ordering: maintaining event order can be challenging.

10. **Compare with alternatives**  
    Alternatives: Request-Response, Message Queue, Publish-Subscribe, Synchronous Communication

11. **30-second explanation (your own words)**  
    Designs systems where components communicate through events, enabling loose coupling, scalability, and responsiveness to changes, making systems more flexible and resilient.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
