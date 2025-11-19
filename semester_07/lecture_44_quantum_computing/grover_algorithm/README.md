# Grover's Algorithm

1. **Name of Algorithm**  
Grover's Algorithm

2. **What problem does it solve? (1 sentence)**  
   Searches an unsorted database of N items to find a specific target item, providing quadratic speedup over classical search algorithms for unstructured search problems.

3. **Intuition (plain-language explanation)**  
   Like searching a phone book: classical search checks each entry one by one (O(N) time) - Grover's algorithm uses quantum superposition to check all entries simultaneously, then amplifies the correct answer, finding the target in roughly √N steps instead of N steps (quadratic speedup).

4. **Inputs & Outputs**  
   - Input: Unstructured database of N items, oracle function that identifies target item, quantum computer with sufficient qubits.  
   - Output: Index or identifier of target item found in database, with high probability.

5. **Step-by-step description (5–10 lines max)**  
1. Initialize superposition: create uniform superposition of all N possible states (all items equally likely).
2. Apply oracle: mark target item(s) by flipping phase (oracle identifies which state is the target).
3. Apply diffusion operator: amplify amplitude of marked state while reducing others (inversion about mean).
4. Repeat: iterate steps 2-3 approximately √N times to maximize probability of measuring target.
5. Measure: collapse quantum state to obtain result (high probability of finding target).
6. Verify: check if measured result matches target (classical verification).

6. **Tiny example (hand-simulated)**  
   Search unsorted database of 1 million items: classical search checks up to 1M items (worst case) → Grover's: initialize superposition of 1M states → apply oracle (mark target) → amplify → repeat ~1000 times (√1M) → measure → find target in ~1000 steps instead of 1M (1000x speedup).

7. **Time & Space Complexity**  
   - Time: O(√N) quantum queries vs O(N) classical queries, providing quadratic speedup for unstructured search.  
   - Space: O(log N) qubits to represent N items in superposition (exponential advantage in state space).

8. **Strengths**  
- Quadratic speedup: significantly faster than classical search for unstructured data.
- Optimal: provably optimal for unstructured search problems.
- General applicability: works for any search problem with an oracle.

9. **Weaknesses / limitations**  
- Requires oracle: needs quantum oracle function to identify target.
- Limited speedup: only quadratic, not exponential like some other quantum algorithms.
- Hardware requirements: needs fault-tolerant quantum computer.

10. **Compare with alternatives**  
    Alternatives: Classical Linear Search, Classical Binary Search (for sorted data), Quantum Amplitude Amplification, Classical Hashing

11. **30-second explanation (your own words)**  
    Searches an unsorted database of N items to find a specific target item, providing quadratic speedup over classical search algorithms for unstructured search problems.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
