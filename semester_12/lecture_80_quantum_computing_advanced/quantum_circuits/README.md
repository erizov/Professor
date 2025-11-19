# Quantum Circuits

1. **Name of Algorithm**  
   Quantum Circuits

2. **What problem does it solve? (1 sentence)**  
   Designs and implements quantum circuits (sequences of quantum gates) to perform quantum computations, algorithms, and operations on qubits.

3. **Intuition (plain-language explanation)**  
   Like circuits for quantum: Quantum Circuits are like electrical circuits but for quantum information - you connect quantum gates (like logic gates) to process qubits - just as circuits process bits, quantum circuits process qubits using quantum gates.

4. **Inputs & Outputs**  
   - Input: Quantum gates, qubits, circuit specifications, algorithm requirements, gate parameters.  
   - Output: Quantum circuits, gate sequences, compiled circuits, optimized circuits, executable quantum programs.

5. **Step-by-step description (5–10 lines max)**  
1. Specify: specify quantum algorithm or operation.
2. Design: design quantum circuit structure.
3. Select: select appropriate quantum gates.
4. Compose: compose gates into circuit.
5. Optimize: optimize circuit (reduce gates, depth).
6. Compile: compile to target quantum hardware.
7. Validate: validate circuit correctness.
8. Execute: execute circuit on quantum computer.
9. Measure: measure quantum state.
10. Analyze: analyze results.

6. **Tiny example (hand-simulated)**  
   Quantum Circuits: algorithm: Grover's search → design: oracle + diffusion → gates: H, X, CNOT, Z → compose: build circuit → optimize: reduce gate count → compile: map to hardware → execute: run on quantum computer → result: search result found → Quantum Circuits successful.

7. **Time & Space Complexity**  
   - Time: O(d) where d is circuit depth (number of gate layers).  
   - Space: O(n) where n is number of qubits (quantum register size).

8. **Strengths**  
- Flexibility: enables implementation of any quantum algorithm.
- Composability: gates compose into complex circuits.
- Standardization: quantum gates provide standard operations.

9. **Weaknesses / limitations**  
- Noise: circuit depth affects error accumulation.
- Compilation: compilation to hardware can be complex.
- Optimization: circuit optimization is challenging.

10. **Compare with alternatives**  
    Alternatives: Ad-Hoc Operations, Fixed Algorithms, High-Level Languages, Quantum Compilers

11. **30-second explanation (your own words)**  
    Designs and implements quantum circuits (sequences of quantum gates) to perform quantum computations, algorithms, and operations on qubits.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
