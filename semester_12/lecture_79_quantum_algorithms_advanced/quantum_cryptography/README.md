# Quantum Cryptography

1. **Name of Algorithm**  

## Code Files


## Algorithm Visualization

### Flowchart (ASCII)


```
Quantum Cryptography Flowchart:

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
Quantum Cryptography Step-by-Step Execution:

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
- [Python Implementation](semester_12/lecture_79_quantum_algorithms_advanced/quantum_cryptography/algorithm.py)
- [Java Implementation](semester_12/lecture_79_quantum_algorithms_advanced/quantum_cryptography/Algorithm.java)
- [Python Tests](semester_12/lecture_79_quantum_algorithms_advanced/quantum_cryptography/test_algorithm.py)


   Quantum Cryptography

2. **What problem does it solve? (1 sentence)**  
   Uses quantum mechanical properties to provide secure communication protocols that are theoretically unbreakable, even against quantum computers, based on the laws of physics rather than computational complexity.

3. **Intuition (plain-language explanation)**  
   Like unbreakable locks: Quantum Cryptography is like unbreakable locks based on physics - instead of relying on math that might be broken (classical crypto), quantum crypto uses physics (quantum mechanics) - just as you can't break the laws of physics, you can't break quantum cryptography because it's based on fundamental physical principles.

4. **Inputs & Outputs**  
   - Input: Quantum states, quantum channels, measurement bases, encryption keys, quantum protocols.  
   - Output: Secure quantum keys, encrypted quantum communication, quantum key distribution, provably secure protocols.

5. **Step-by-step description (5–10 lines max)**  
1. Prepare: prepare quantum states (qubits) for key distribution.
2. Transmit: transmit qubits over quantum channel.
3. Measure: measure qubits using random bases.
4. Compare: compare measurement bases publicly.
5. Extract: extract secure key from matching bases.
6. Verify: verify key security through error checking.
7. Encrypt: use quantum key for encryption.
8. Decrypt: decrypt using shared quantum key.
9. Detect: detect eavesdropping attempts.
10. Renew: renew keys as needed.

6. **Tiny example (hand-simulated)**  
   Quantum Cryptography: Alice: prepare qubits → transmit: send qubits to Bob → measure: both measure randomly → compare: share bases publicly → extract: key from matching bases → verify: check for errors → result: secure key, eavesdropping detected → Quantum Cryptography successful.

7. **Time & Space Complexity**  
   - Time: O(n) where n is number of qubits (quantum operations are typically O(1) per qubit).  
   - Space: O(n) where n is number of qubits (quantum state storage).

8. **Strengths**  
- Security: theoretically unbreakable based on physics.
- Detection: detects eavesdropping attempts automatically.
- Future-proof: secure against quantum computers.

9. **Weaknesses / limitations**  
- Distance: limited by quantum channel distance.
- Infrastructure: requires quantum communication infrastructure.
- Cost: quantum hardware is expensive.

10. **Compare with alternatives**  
    Alternatives: Classical Cryptography, Post-Quantum Cryptography, Hybrid Approaches, Quantum Key Distribution

11. **30-second explanation (your own words)**  
    Uses quantum mechanical properties to provide secure communication protocols that are theoretically unbreakable, even against quantum computers, based on the laws of physics rather than computational complexity.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
