# Quantum Repeaters

1. **Name of Algorithm**  

## Code Files


## Algorithm Visualization

### Flowchart (ASCII)


```
Quantum Repeaters Flowchart:

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
Quantum Repeaters Step-by-Step Execution:

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
- [Python Implementation](semester_12/lecture_85_quantum_networking/quantum_repeaters/algorithm.py)
- [Java Implementation](semester_12/lecture_85_quantum_networking/quantum_repeaters/Algorithm.java)
- [Python Tests](semester_12/lecture_85_quantum_networking/quantum_repeaters/test_algorithm.py)


   Quantum Repeaters

2. **What problem does it solve? (1 sentence)**  
   Extends quantum communication distance by creating entanglement between distant nodes through intermediate nodes, enabling long-distance quantum communication and quantum networks.

3. **Intuition (plain-language explanation)**  
   Like signal repeaters: Quantum Repeaters are like signal repeaters but for quantum information - you use intermediate nodes (repeaters) to extend the range of quantum communication, creating entanglement over long distances - just as repeaters extend radio range, quantum repeaters extend quantum communication range.

4. **Inputs & Outputs**  
   - Input: Quantum channels, intermediate nodes, entanglement sources, quantum memories, protocols.  
   - Output: Extended quantum links, long-distance entanglement, quantum communication, network connectivity.

5. **Step-by-step description (5–10 lines max)**  
1. Deploy: deploy quantum repeaters along path.
2. Create: create local entanglement at each segment.
3. Store: store entanglement in quantum memories.
4. Swap: perform entanglement swapping.
5. Extend: extend entanglement to next segment.
6. Chain: chain entanglement swaps.
7. Establish: establish end-to-end entanglement.
8. Use: use for quantum communication.
9. Maintain: maintain entanglement.
10. Scale: scale to longer distances.

6. **Tiny example (hand-simulated)**  
   Quantum Repeaters: distance: 1000 km → repeaters: deploy 10 repeaters → create: local entanglement → swap: entanglement swapping → chain: chain swaps → result: entanglement over 1000 km → Quantum Repeaters successful.

7. **Time & Space Complexity**  
   - Time: O(r·s) where r is repeaters, s is swap time (repeater operations).  
   - Space: O(r + m) where r is repeater storage, m is memory storage (quantum memories).

8. **Strengths**  
- Distance: extends quantum communication distance.
- Networking: enables long-distance quantum networks.
- Scalability: enables scaling quantum networks.

9. **Weaknesses / limitations**  
- Complexity: quantum repeaters are complex.
- Memory: requires quantum memories.
- Loss: entanglement loss affects performance.

10. **Compare with alternatives**  
    Alternatives: Direct Transmission, Quantum Satellites, Hybrid Approaches, No Repeaters

11. **30-second explanation (your own words)**  
    Extends quantum communication distance by creating entanglement between distant nodes through intermediate nodes, enabling long-distance quantum communication and quantum networks.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
