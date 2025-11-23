# Continuous Batching (Iteration-Level Batching)

## Учебные материалы

- [Школьный уровень](school.ru.md)
- [Университетский уровень](univer.ru.md)

## Algorithm Visualization

### Flowchart (ASCII)

```
Continuous Batching (Iteration-Level Batching) Flowchart:

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
Continuous Batching (Iteration-Level Batching) Step-by-Step Execution:

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

- [Python Implementation](/code/semester_10/lecture_66_llm_inference/continuous_batching/algorithm.py)
- [Java Implementation](/code/semester_10/lecture_66_llm_inference/continuous_batching/Algorithm.java)
- [Python Tests](/code/semester_10/lecture_66_llm_inference/continuous_batching/test_algorithm.py)

   Continuous Batching (Iteration-Level Batching)

What problem does it solve? (1 sentence)  
   Dynamically adds and removes requests from an active batch during generation, allowing new requests to join and completed requests to exit without waiting for the entire batch to finish, maximizing GPU utilization.

Intuition (plain-language explanation)  
   Like a revolving door: continuous batching is like a revolving door where people (requests) can enter and exit at any time - instead of waiting for everyone to finish before letting new people in (static batching), new people can join the door (batch) as soon as there's space, and people who finish can leave immediately - the door (GPU) stays busy all the time, maximizing throughput while minimizing wait time for everyone.

Inputs & Outputs  

  - Input: Incoming requests, active batch, generation states, completion status, batch capacity.  
  - Output: Continuous batch processing, high GPU utilization, low latency, improved throughput.

Step-by-step description (5–10 lines max)  
Maintain active batch: maintain active batch of requests being processed.
Add requests: add new requests to batch when they arrive (if capacity allows).
Generate: generate one token for all requests in active batch.
Check completion: check which requests have completed generation.
Remove completed: remove completed requests from active batch.
Add new: add new waiting requests to fill batch capacity.
Continue: continue generation for remaining requests.
Iterate: repeat token generation with dynamic batch membership.
Optimize: optimize batch management for throughput and latency.
Monitor: monitor batch utilization and request wait times.

Tiny example (hand-simulated)  
   Continuous batching: batch capacity 8 → 5 requests generating → 3 new requests arrive → add to batch: now 8 requests → generate token → 2 requests complete → remove: batch now 6 → add 2 new requests: batch 8 again → continue → GPU utilization: 95% (vs 60% static) → latency: low (no waiting for batch) → continuous batching efficient.

Time & Space Complexity  

  - Time: O(b·n) per iteration where b is active batch size, n is sequence length (dynamic batching).  
  - Space: O(b_max·n) where b_max is maximum batch size, n is sequence length (active batch storage).

Strengths  

- Efficiency: maximizes GPU utilization (near 100%).
- Latency: low latency for requests (no waiting for batch completion).
- Throughput: high throughput through continuous processing.

Weaknesses / limitations  

- Complexity: more complex than static batching (dynamic management).
- Memory: requires managing variable batch sizes and generation states.
- Scheduling: requires efficient scheduling of requests.

Compare with alternatives  
    Alternatives: Static Batching, Individual Inference, Dynamic Batching, Request Queuing

30-second explanation (your own words)  
    Dynamically adds and removes requests from an active batch during generation, allowing new requests to join and completed requests to exit without waiting for the entire batch to finish, maximizing GPU utilization.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
