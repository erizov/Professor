# Quantum Gates

1. **Name of Algorithm**  
   Quantum Gates

2. **What problem does it solve? (1 sentence)**  
   Provides fundamental operations to manipulate quantum states, enabling construction of quantum algorithms and quantum circuits for computation.

3. **Intuition (plain-language explanation)**  
   Like logic gates in classical computers (AND, OR, NOT) but for quantum states: quantum gates rotate, flip, and combine qubit states in superposition, allowing manipulation of quantum information - like having special tools that can work with 'both 0 and 1 at the same time'.

4. **Inputs & Outputs**  
   - Input: Qubit(s) in initial quantum state, quantum gate operation (unitary matrix).  
   - Output: Qubit(s) in transformed quantum state, ready for next operation or measurement.

5. **Step-by-step description (5–10 lines max)**  
1. Select gate: choose quantum gate based on desired operation (Pauli-X, Hadamard, CNOT, etc.).
2. Apply gate: execute gate operation on qubit(s) (matrix multiplication on quantum state).
3. Transform state: gate transforms input state to output state (e.g., |0⟩ → |1⟩, or superposition).
4. Combine gates: chain multiple gates to build quantum circuits (like classical logic circuits).
5. Verify: check gate operation preserves quantum properties (unitarity, reversibility).
6. Measure (optional): measure qubit state after gate operations to extract classical information.

6. **Tiny example (hand-simulated)**  
   Single qubit: start with |0⟩ → apply Hadamard gate H → get (|0⟩ + |1⟩)/√2 (superposition) → apply Pauli-X gate → get (|1⟩ + |0⟩)/√2 → apply Hadamard again → get |0⟩ (back to original). Two qubits: |00⟩ → CNOT gate → |00⟩ (if control is 0) or |11⟩ (if control is 1).

7. **Time & Space Complexity**  
   - Time: O(1) per gate operation (constant time matrix multiplication).  
   - Space: O(n) qubits for n-qubit gates, O(2^n) classical memory to simulate n-qubit gates.

8. **Strengths**  
- Reversible: all quantum gates are reversible (unitary operations).
- Universal: small set of gates can implement any quantum computation.
- Parallel: gates operate on superposition states simultaneously.

9. **Weaknesses / limitations**  
- No cloning: cannot copy arbitrary quantum states (no-cloning theorem).
- Measurement: gates are probabilistic when measured (quantum uncertainty).
- Error prone: gates are sensitive to noise and decoherence.

10. **Compare with alternatives**  
    Alternatives: Classical Logic Gates, Analog Computation, Reversible Classical Gates, Quantum Error Correction

11. **30-second explanation (your own words)**  
    Provides fundamental operations to manipulate quantum states, enabling construction of quantum algorithms and quantum circuits for computation.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
