# Quantum Entanglement

1. **Name of Algorithm**  
   Quantum Entanglement

2. **What problem does it solve? (1 sentence)**  
   Creates strong correlations between quantum particles where measuring one instantly determines the state of the other, regardless of distance, enabling quantum communication and computation advantages.

3. **Intuition (plain-language explanation)**  
   Like two magic coins: flip them together and they become 'entangled' - if you look at one and see heads, the other instantly becomes tails (even if it's light-years away). Quantum entanglement creates 'spooky action at a distance' where particles share a quantum state and are perfectly correlated.

4. **Inputs & Outputs**  
   - Input: Two or more qubits, quantum gates to create entanglement (CNOT, Hadamard, etc.).  
   - Output: Entangled qubits with correlated states, measurement results showing perfect correlation.

5. **Step-by-step description (5–10 lines max)**  
1. Prepare qubits: initialize qubits in known states (e.g., |00⟩).
2. Create superposition: apply Hadamard gate to first qubit (creates (|0⟩ + |1⟩)/√2).
3. Apply CNOT: entangle qubits using controlled-NOT gate (creates Bell state).
4. Result: qubits now in entangled state (|00⟩ + |11⟩)/√2 (perfectly correlated).
5. Separate (optional): physically separate qubits (entanglement persists).
6. Measure: measure one qubit → instantly know state of other (perfect correlation).
7. Verify: test Bell inequalities to confirm entanglement (violates classical limits).

6. **Tiny example (hand-simulated)**  
   Create Bell pair: |00⟩ → Hadamard on first: (|0⟩ + |1⟩)|0⟩/√2 → CNOT: (|00⟩ + |11⟩)/√2 (entangled) → separate qubits → measure first qubit: if 0, second is 0; if 1, second is 1 (instant correlation, even if separated).

7. **Time & Space Complexity**  
   - Time: O(1) to create entanglement (constant time gate operations).  
   - Space: O(n) qubits for n-partite entanglement (linear in number of particles).

8. **Strengths**  
- Perfect correlation: enables perfect correlation between distant particles.
- Quantum advantage: essential for quantum teleportation, superdense coding.
- Non-locality: demonstrates quantum mechanics beyond classical physics.

9. **Weaknesses / limitations**  
- Fragility: entanglement easily destroyed by decoherence and noise.
- No faster-than-light communication: cannot transmit information faster than light.
- Measurement destroys: measuring one qubit collapses entanglement.

10. **Compare with alternatives**  
    Alternatives: Classical Correlation, Quantum Superposition, Classical Entanglement (simulation), Quantum Discord

11. **30-second explanation (your own words)**  
    Creates strong correlations between quantum particles where measuring one instantly determines the state of the other, regardless of distance, enabling quantum communication and computation advantages.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
