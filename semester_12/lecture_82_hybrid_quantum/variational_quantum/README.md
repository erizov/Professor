# Variational Quantum Algorithms (VQA)

1. **Name of Algorithm**  
   Variational Quantum Algorithms (VQA)

2. **What problem does it solve? (1 sentence)**  
   Solves optimization and machine learning problems by using parameterized quantum circuits (variational circuits) that are optimized classically to minimize a cost function.

3. **Intuition (plain-language explanation)**  
   Like training a quantum neural network: Variational quantum algorithms are like training a neural network, but the network is quantum - you have a quantum circuit with adjustable parameters (like weights), you run it on a quantum computer to get results, then use a classical computer to adjust the parameters to minimize a cost function - repeat until you find the best parameters.

4. **Inputs & Outputs**  
   - Input: Cost function, variational circuit ansatz, initial parameters, quantum device, classical optimizer, convergence criteria.  
   - Output: Optimized parameters, minimum cost value, optimized quantum state, convergence history.

5. **Step-by-step description (5–10 lines max)**  
1. Design: design variational circuit ansatz (parameterized circuit).
2. Initialize: initialize circuit parameters randomly or heuristically.
3. Prepare: prepare quantum state using variational circuit.
4. Measure: measure quantum state to compute cost function.
5. Evaluate: evaluate cost function value.
6. Optimize: use classical optimizer to update parameters.
7. Update: update circuit parameters.
8. Iterate: repeat preparation, measurement, and optimization.
9. Converge: converge to optimal parameters.
10. Extract: extract solution from optimized quantum state.

6. **Tiny example (hand-simulated)**  
   VQE: design ansatz → initialize parameters → prepare |ψ(θ)⟩ → measure energy ⟨H⟩ → evaluate E(θ) = 2.5 → optimize θ → update → repeat → converge → E(θ*) = 1.8 → VQE successful.

7. **Time & Space Complexity**  
   - Time: O(i * (q + c)) where i is optimization iterations, q is quantum evaluation time, c is classical optimization time (variational complexity).  
   - Space: O(n) qubits for n-qubit variational circuit (quantum state space).

8. **Strengths**  
- Near-term: suitable for noisy intermediate-scale quantum (NISQ) devices.
- Flexible: applicable to optimization, ML, and chemistry problems.
- Hybrid: leverages both quantum and classical advantages.

9. **Weaknesses / limitations**  
- Barren plateaus: optimization can get stuck in flat regions.
- Expressibility: ansatz design is crucial and problem-dependent.
- Convergence: may require many iterations to converge.

10. **Compare with alternatives**  
Alternatives: Quantum Approximate Optimization Algorithm, Quantum Machine Learning, Quantum Chemistry Algorithms, Classical Optimization

11. **30-second explanation (your own words)**  
    A class of hybrid quantum-classical algorithms that use parameterized quantum circuits optimized classically to solve optimization and machine learning problems.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
