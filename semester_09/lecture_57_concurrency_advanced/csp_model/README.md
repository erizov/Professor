# Communicating Sequential Processes (CSP)

1. **Name of Algorithm**  

## Code Files


## Algorithm Visualization

### Flowchart (ASCII)


```
Communicating Sequential Processes (CSP) Flowchart:

┌─────────────┐
│   Start     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Initialize │
│   data      │
└──────┬──────┘
       │
       ▼
┌─────────────┐      Yes
│  Process   ├──────┐
│  condition?│      │
└──────┬──────┘      │
       │ No          │
       ▼             │
┌─────────────┐      │
│  Execute   │      │
│  operation │      │
└──────┬──────┘      │
       │             │
       └─────────────┘
       │
       ▼
┌─────────────┐
│    End      │
└─────────────┘
```


### Step-by-Step Execution


```
Communicating Sequential Processes (CSP) Step-by-Step Execution:

Input: [example data]

Step 1: Initialize
State: [initial state]

Step 2: Process
State: [intermediate state]

Step 3: Finalize
State: [final state]

Result: [output]
```


### Interactive Flowchart (Mermaid)


```mermaid
flowchart TD
    Start([Start]) --> Init[Initialize data]
    Init --> Process{Process condition}
    Process -->|True| Execute[Execute operation]
    Execute --> Done{Complete?}
    Done -->|No| Process
    Done -->|Yes| End([End])
    Process -->|False| End
```


> **Note**: Mermaid diagrams are rendered automatically on GitHub. For local viewing, use a Mermaid-compatible Markdown viewer.
- [Python Implementation](semester_09/lecture_57_concurrency_advanced/csp_model/algorithm.py)
- [Java Implementation](semester_09/lecture_57_concurrency_advanced/csp_model/Algorithm.java)
- [Python Tests](semester_09/lecture_57_concurrency_advanced/csp_model/test_algorithm.py)


   Communicating Sequential Processes (CSP)

2. **What problem does it solve? (1 sentence)**  
   Models concurrent systems using independent sequential processes that communicate through synchronous message passing over channels, providing deterministic concurrency and avoiding shared state.

3. **Intuition (plain-language explanation)**  
   Like a phone call system: CSP is like a phone call where both parties must be ready to talk (synchronous) - when you call someone (send message), you wait until they answer (receive), then you exchange information (communicate), and both hang up (synchronization complete) - unlike email (asynchronous), phone calls require both parties to be ready at the same time, ensuring messages are delivered and received in a coordinated way.

4. **Inputs & Outputs**  
   - Input: Processes, channels, messages, synchronization points, communication patterns.  
   - Output: Synchronized communication, deterministic behavior, coordinated processes, no shared state.

5. **Step-by-step description (5–10 lines max)**  
1. Define processes: create independent sequential processes.
2. Create channels: establish communication channels between processes.
3. Send: process sends message on channel (blocks until receiver ready).
4. Receive: process receives message from channel (blocks until sender ready).
5. Synchronize: send and receive operations synchronize (rendezvous).
6. Select: use select statement to wait on multiple channels.
7. Compose: compose processes to build larger concurrent systems.
8. Verify: use formal methods to verify system properties.
9. Execute: run processes concurrently with synchronized communication.
10. Monitor: observe communication patterns and system behavior.

6. **Tiny example (hand-simulated)**  
   CSP: producer-consumer → producer process: produce item → send on channel → wait for consumer → consumer process: receive from channel → process item → send acknowledgment → producer receives ack → continue → synchronization: both processes coordinate → no shared buffer needed → deterministic behavior → CSP model.

7. **Time & Space Complexity**  
   - Time: O(1) for channel operations, O(n) for process execution where n is computation size.  
   - Space: O(p + c) where p is number of processes, c is channel buffer size (often 0 for synchronous).

8. **Strengths**  
- Determinism: synchronous communication provides deterministic behavior.
- Formal verification: amenable to formal methods and verification.
- No shared state: avoids race conditions and data races.

9. **Weaknesses / limitations**  
- Blocking: synchronous communication can cause blocking and deadlocks.
- Performance: may have lower throughput than asynchronous models.
- Complexity: managing many channels and processes can be complex.

10. **Compare with alternatives**  
    Alternatives: Actor Model, Shared Memory, Message Queues, Asynchronous Communication

11. **30-second explanation (your own words)**  
    Models concurrent systems using independent sequential processes that communicate through synchronous message passing over channels, providing deterministic concurrency and avoiding shared state.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
