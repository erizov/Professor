# Quantum Approximate Optimization Algorithm (QAOA)

1. **Name of Algorithm**  
Quantum Approximate Optimization Algorithm (QAOA)

2. **What problem does it solve? (1 sentence)**  
   Solves combinatorial optimization problems by using a quantum-classical hybrid approach that alternates between quantum evolution and classical parameter optimization to find approximate solutions.

3. **Intuition (plain-language explanation)**  
Like a quantum-classical dance: QAOA is like a dance between quantum and classical computers - the quantum computer explores the solution space using quantum superposition (trying many solutions at once), while the classical computer fine-tunes the quantum operations (adjusting the dance steps) - together they find good approximate solutions to hard optimization problems.

4. **Inputs & Outputs**  
- Input: Optimization problem (cost function, constraints), number of layers (p), initial parameters, quantum device, classical optimizer.
- Output: Approximate optimal solution, optimized parameters, solution quality, convergence metrics.

5. **Step-by-step description (5–10 lines max)**  
1. Encode: encode optimization problem as quantum Hamiltonian.
2. Initialize: prepare initial quantum state (superposition).
3. Apply: apply alternating unitaries (problem and mixer Hamiltonians).
4. Measure: measure quantum state to get candidate solution.
5. Evaluate: evaluate solution quality using cost function.
6. Optimize: use classical optimizer to adjust parameters.
7. Iterate: repeat quantum evolution and classical optimization.
8. Converge: converge to optimal parameters and solution.
9. Extract: extract best solution from quantum measurements.
10. Validate: validate solution quality and feasibility.

6. **Tiny example (hand-simulated)**  
   QAOA for MaxCut: encode graph as Hamiltonian → initialize superposition → apply 2 layers (p=2) → measure → get cut value 3 → optimize parameters → repeat → converge → best cut value 4 → QAOA successful.

7. **Time & Space Complexity**  
   - Time: O(p * (q + c)) where p is layers, q is quantum evolution time, c is classical optimization time (hybrid complexity).  
   - Space: O(n) qubits for n-variable problem (quantum state space).

8. **Strengths**  
- Hybrid: combines quantum and classical advantages.
- Flexible: works for various optimization problems.
- Near-term: suitable for near-term quantum devices.

9. **Weaknesses / limitations**  
- Approximate: provides approximate solutions, not exact.
- Parameters: requires careful parameter tuning.
- Scaling: performance depends on problem structure.

10. **Compare with alternatives**  
    Alternatives: Quantum Annealing, Classical Optimization, Variational Quantum Eigensolver, Quantum Machine Learning

11. **30-second explanation (your own words)**  
A quantum-classical hybrid algorithm that uses parameterized quantum circuits and classical optimization to solve combinatorial optimization problems approximately.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
