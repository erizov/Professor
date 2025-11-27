# Algorand

## Учебные материалы

- [Школьный уровень](school.ru.md)
- [Университетский уровень](univer.ru.md)

## Algorithm Visualization

### Flowchart (ASCII)

```
Algorand Flowchart:

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
Algorand Step-by-Step Execution:

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

- [Python Implementation](/code/semester_13/lecture_88_consensus_advanced/algorand/algorithm.py)
- [Java Implementation](/code/semester_13/lecture_88_consensus_advanced/algorand/Algorithm.java)
- [Python Tests](/code/semester_13/lecture_88_consensus_advanced/algorand/test_algorithm.py)

What problem does it solve? (1 sentence)  
   Achieves Byzantine fault tolerance and fast finality in a permissionless blockchain using pure proof-of-stake, cryptographic sortition for leader selection, and a two-phase consensus protocol.

Intuition (plain-language explanation)  
   Like a democratic lottery: Algorand is like a democratic lottery system - instead of everyone voting (expensive), you randomly select a small committee (cryptographic sortition) based on stake (like weighted lottery tickets) - the committee reaches consensus quickly, and because selection is random and cryptographic, it's secure and fair - this enables fast, secure consensus without energy waste.

Inputs & Outputs  

  - Input: Stake distribution, transactions, cryptographic sortition, committee selection, consensus messages.  
  - Output: Finalized blocks, consensus certificates, leader selection, network agreement.

Step-by-step description (5–10 lines max)  
Sortition: use cryptographic sortition to select committee members.
Propose: selected proposer creates block proposal.
Broadcast: broadcast proposal to network.
Vote: committee members vote on proposal.
Certify: certify block if sufficient votes received.
Finalize: finalize block (no forks possible).
Next: proceed to next round with new sortition.
Validate: validate sortition and votes cryptographically.
Sync: synchronize network on finalized blocks.
Maintain: maintain liveness and safety properties.

Tiny example (hand-simulated)  
   Algorand: sortition selects 1000 validators → proposer creates block → committee votes → 667+ votes → certify → finalize in <5s → Algorand successful (fast finality).

Time & Space Complexity  

  - Time: O(log n) for sortition, O(1) for consensus with small committee (Algorand complexity).  
  - Space: O(n) for stake distribution, O(c) for committee where c << n (Algorand storage).

Strengths  

- Speed: fast finality (under 5 seconds).
- Security: Byzantine fault tolerant with no forks.
- Efficiency: energy efficient (pure PoS, no mining).

Weaknesses / limitations  

- Complexity: sophisticated cryptographic sortition mechanism.
- Stake: security depends on stake distribution.
- Scalability: committee size affects performance.

Compare with alternatives  
    Alternatives: Proof of Work, Delegated Proof of Stake, Practical Byzantine Fault Tolerance, Tendermint

30-second explanation (your own words)  
    A pure proof-of-stake consensus protocol that uses cryptographic sortition to randomly select small committees for fast, secure, and fork-free consensus.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*


## References

- [Algorand](https://en.wikipedia.org/wiki/Algorand) - Wikipedia
