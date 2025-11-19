# Quantum Algorithms

1. **Name of Algorithm**  
   Quantum Algorithms

2. **What problem does it solve? (1 sentence)**  
   Leverages quantum mechanical properties (superposition, entanglement, interference) to solve computational problems faster than classical algorithms, providing exponential or polynomial speedups for specific problems.

3. **Intuition (plain-language explanation)**  
   Like having a super-powered computer: classical computers process one possibility at a time (like checking rooms one by one) - quantum algorithms use superposition to check all possibilities simultaneously, then use interference to amplify correct answers and cancel wrong ones (like checking all rooms at once and having the right answer 'glow').

4. **Inputs & Outputs**  
   - Input: Problem instance, quantum computer with sufficient qubits, quantum gates and circuits.  
   - Output: Solution to computational problem, potentially with exponential or polynomial speedup over classical methods.

5. **Step-by-step description (5–10 lines max)**  
1. Problem formulation: encode problem into quantum state and operations.
2. Initialize: prepare quantum state (often uniform superposition of all possibilities).
3. Apply quantum operations: use quantum gates to manipulate state (exploit superposition, entanglement).
4. Amplify: use quantum interference to amplify correct answers (constructive interference).
5. Cancel: destructive interference cancels wrong answers.
6. Measure: collapse quantum state to obtain classical result.
7. Post-process: analyze measurement results, may require multiple runs.
8. Verify: check solution correctness (classical verification).

6. **Tiny example (hand-simulated)**  
   Grover's search: initialize superposition of N items → oracle marks target → amplify marked state → repeat √N times → measure → find target in √N steps (vs N classical). Shor's factoring: use quantum Fourier transform to find period → factor large number in polynomial time (vs exponential classical).

7. **Time & Space Complexity**  
   - Time: Varies by algorithm: O(√N) for Grover's, O((log N)³) for Shor's, vs exponential/polynomial classical for same problems.  
   - Space: O(poly(log N)) qubits for many algorithms, enabling exponential state space with polynomial resources.

8. **Strengths**  
- Exponential speedup: some problems show exponential speedup (factoring, simulation).
- Polynomial speedup: many problems show polynomial speedup (search, optimization).
- Fundamental advantage: provable quantum advantage for certain problem classes.

9. **Weaknesses / limitations**  
- Limited applicability: speedups only for specific problem types.
- Hardware requirements: need large, fault-tolerant quantum computers.
- Error sensitivity: algorithms sensitive to noise and decoherence.

10. **Compare with alternatives**  
    Alternatives: Classical Algorithms, Probabilistic Algorithms, Approximate Algorithms, Hybrid Quantum-Classical Algorithms

11. **30-second explanation (your own words)**  
    Leverages quantum mechanical properties (superposition, entanglement, interference) to solve computational problems faster than classical algorithms, providing exponential or polynomial speedups for specific problems.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
