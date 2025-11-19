# Quantum Teleportation

1. **Name of Algorithm**  
   Quantum Teleportation

2. **What problem does it solve? (1 sentence)**  
   Transfers an unknown quantum state from one location to another using quantum entanglement and classical communication, without physically transporting the quantum particle.

3. **Intuition (plain-language explanation)**  
   Like teleporting quantum information: Quantum Teleportation is like teleporting quantum information - you don't send the qubit itself, you use entanglement (spooky action) and send classical information to recreate the state elsewhere - just as teleportation in sci-fi moves objects instantly, quantum teleportation moves quantum states using entanglement.

4. **Inputs & Outputs**  
   - Input: Unknown quantum state, entangled pair (Bell state), classical communication channel, measurement results.  
   - Output: Teleported quantum state, measurement outcomes, classical bits, reconstructed state.

5. **Step-by-step description (5–10 lines max)**  
1. Prepare: prepare entangled pair (Bell state).
2. Share: share one qubit with sender, one with receiver.
3. Entangle: entangle unknown state with sender's qubit.
4. Measure: measure both qubits at sender.
5. Communicate: send measurement results classically.
6. Apply: receiver applies correction based on results.
7. Reconstruct: receiver reconstructs original state.
8. Verify: verify teleportation was successful.
9. Destroy: original state is destroyed (no-cloning).
10. Complete: teleportation complete.

6. **Tiny example (hand-simulated)**  
   Quantum Teleportation: state: |ψ⟩ unknown → prepare: Bell pair |Φ+⟩ → entangle: |ψ⟩ with Alice's qubit → measure: Alice measures → communicate: send 2 classical bits → apply: Bob applies corrections → result: |ψ⟩ teleported to Bob → Quantum Teleportation successful.

7. **Time & Space Complexity**  
   - Time: O(1) for teleportation protocol (constant time quantum operations).  
   - Space: O(1) for single qubit teleportation (3 qubits: 1 unknown + 2 entangled).

8. **Strengths**  
- Transfer: enables transfer of quantum states.
- Networking: foundation for quantum networks.
- No transport: doesn't require physical transport of qubits.

9. **Weaknesses / limitations**  
- Classical: requires classical communication.
- Entanglement: requires pre-shared entanglement.
- Distance: limited by entanglement distribution.

10. **Compare with alternatives**  
    Alternatives: Physical Transport, Quantum Repeaters, Direct Transmission, Quantum Networks

11. **30-second explanation (your own words)**  
    Transfers an unknown quantum state from one location to another using quantum entanglement and classical communication, without physically transporting the quantum particle.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
