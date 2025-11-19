# Quantum Superposition

1. **Name of Algorithm**  
   Quantum Superposition

2. **What problem does it solve? (1 sentence)**  
   Enables quantum bits (qubits) to exist in multiple states simultaneously, allowing quantum computers to process exponentially many possibilities in parallel.

3. **Intuition (plain-language explanation)**  
   Like a spinning coin: while it's spinning, it's both heads and tails simultaneously (superposition) - only when you look (measure) does it 'collapse' to one state. Quantum superposition lets a qubit be 0 and 1 at the same time, enabling parallel computation on all possible states.

4. **Inputs & Outputs**  
   - Input: Qubit(s) in initial state, quantum gates to create and manipulate superposition.  
   - Output: Qubit(s) in superposition state (linear combination of |0⟩ and |1⟩), measurement result after collapse.

5. **Step-by-step description (5–10 lines max)**  
1. Initialize qubit: prepare qubit in basis state |0⟩ (classical 0).
2. Apply Hadamard gate: create equal superposition (|0⟩ + |1⟩)/√2 (50% chance of 0, 50% chance of 1).
3. Apply operations: perform quantum gates on superposition (operations affect all states simultaneously).
4. Interference: quantum states interfere constructively or destructively (amplify correct answers, cancel wrong ones).
5. Measure: collapse superposition to definite state (0 or 1) with probabilities determined by amplitudes.
6. Repeat: run algorithm multiple times to sample from probability distribution.
7. Post-process: analyze measurement results to extract answer.

6. **Tiny example (hand-simulated)**  
   2-qubit system: initialize |00⟩ → apply Hadamard to both qubits → create superposition of all 4 states: (|00⟩ + |01⟩ + |10⟩ + |11⟩)/2 → apply quantum operations → all 4 states processed in parallel → measure → get one of 4 states → repeat to sample distribution.

7. **Time & Space Complexity**  
   - Time: O(1) to create superposition, but measurement and post-processing may require multiple runs.  
   - Space: O(n) qubits to represent 2^n classical states in superposition (exponential state space).

8. **Strengths**  
- Parallelism: enables exponential parallelism (n qubits = 2^n states simultaneously).
- Fundamental: core principle enabling quantum speedups.
- Interference: allows constructive/destructive interference to amplify correct answers.

9. **Weaknesses / limitations**  
- Measurement collapse: superposition destroyed upon measurement (only one outcome).
- Decoherence: superposition fragile, easily destroyed by noise.
- No direct access: cannot directly read all superposition states (only measure one).

10. **Compare with alternatives**  
    Alternatives: Classical Parallel Processing, Probabilistic Algorithms, Quantum Entanglement, Classical Superposition (simulation)

11. **30-second explanation (your own words)**  

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
