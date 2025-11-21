# Function as a Service (FaaS)

1. **Name of Algorithm**  

## Code Files


## Algorithm Visualization

### Flowchart (ASCII)


```
Function as a Service (FaaS) Flowchart:

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
Function as a Service (FaaS) Step-by-Step Execution:

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
- [Python Implementation](semester_09/lecture_61_cloud_native/function_as_service/algorithm.py)
- [Java Implementation](semester_09/lecture_61_cloud_native/function_as_service/Algorithm.java)
- [Python Tests](semester_09/lecture_61_cloud_native/function_as_service/test_algorithm.py)


   Function as a Service (FaaS)

2. **What problem does it solve? (1 sentence)**  
   Executes code in stateless functions that are triggered by events, automatically managing infrastructure, scaling, and resource allocation, enabling serverless computing.

3. **Intuition (plain-language explanation)**  
   Like a vending machine for code: Function as a Service is like a vending machine - you put in a request (coin/event), the machine (cloud) automatically prepares and serves your item (executes function), and you don't need to manage the machine (infrastructure) - the machine handles everything: getting the item ready (scaling), serving it (execution), and cleaning up (resource management) - you only pay for what you use (per invocation), not for keeping the machine running.

4. **Inputs & Outputs**  
   - Input: Function code, trigger events, input data, execution context, resource limits.  
   - Output: Function execution results, triggered functions, scaled execution, serverless output.

5. **Step-by-step description (5–10 lines max)**  
1. Write function: write stateless function code (handler function).
2. Deploy: deploy function to FaaS platform (AWS Lambda, Azure Functions, Google Cloud Functions).
3. Configure trigger: configure event triggers (HTTP, queue, database, schedule).
4. Wait: function waits for trigger event (no running infrastructure).
5. Trigger: event triggers function execution.
6. Scale: platform automatically scales to handle concurrent invocations.
7. Execute: platform executes function with provided input.
8. Return: function returns result.
9. Cleanup: platform automatically cleans up resources after execution.
10. Charge: platform charges based on execution time and resources used.

6. **Tiny example (hand-simulated)**  
   FaaS: image processing function → trigger: S3 upload event → S3 uploads image → triggers Lambda function → Lambda: resizes image → stores in S3 → returns URL → automatic scaling: 100 images uploaded → 100 functions execute in parallel → pay: only for execution time → no server management → FaaS operational.

7. **Time & Space Complexity**  
   - Time: O(f) where f is function execution time (varies by function logic).  
   - Space: O(m) where m is memory allocated per function execution (temporary, cleaned after execution).

8. **Strengths**  
- No infrastructure: no need to manage servers or infrastructure.
- Auto-scaling: automatically scales to handle any load.
- Cost-effective: pay only for actual execution time.

9. **Weaknesses / limitations**  
- Cold starts: first invocation may have latency (cold start).
- Time limits: functions have execution time limits.
- Stateless: functions must be stateless (no persistent state).

10. **Compare with alternatives**  
    Alternatives: Traditional Servers, Containers, Virtual Machines, Serverless Containers

11. **30-second explanation (your own words)**  
    Executes code in stateless functions that are triggered by events, automatically managing infrastructure, scaling, and resource allocation, enabling serverless computing.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
