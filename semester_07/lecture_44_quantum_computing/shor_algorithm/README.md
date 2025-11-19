# Shor's Algorithm

1. **Name of Algorithm**  
Shor's Algorithm

2. **What problem does it solve? (1 sentence)**  
   Factors large integers into their prime factors efficiently, breaking RSA encryption and solving problems that are intractable for classical computers.

3. **Intuition (plain-language explanation)**  
Like finding the combination to a safe: classical computers try combinations one by one (exponentially slow) - Shor's algorithm uses quantum Fourier transform to find the 'period' of a function, which reveals the factors (like finding the pattern in the combination) in polynomial time instead of exponential time.

4. **Inputs & Outputs**  
   - Input: Large composite integer N to factor, quantum computer with sufficient qubits (roughly 2·log₂(N) qubits).  
   - Output: Prime factors p and q such that N = p × q, or indication that N is prime.

5. **Step-by-step description (5–10 lines max)**  
1. Classical preprocessing: check if N is even or a perfect power (handle trivial cases).
2. Choose random a: select random integer a where 1 < a < N and gcd(a, N) = 1.
3. Find period: use quantum period finding to find smallest r where a^r ≡ 1 (mod N) (the period).
4. Quantum Fourier transform: apply QFT to extract period r from quantum state.
5. Check period: verify r is even and a^(r/2) ≠ ±1 (mod N).
6. Compute factors: calculate gcd(a^(r/2) ± 1, N) to find factors p and q.
7. Verify: confirm p × q = N and factors are prime.
8. Repeat if needed: if factors not found, try different random a.

6. **Tiny example (hand-simulated)**  
   Factor N = 15: choose a = 7 → find period r where 7^r ≡ 1 (mod 15) → quantum period finding finds r = 4 → check: 4 is even, 7^2 = 49 ≡ 4 (mod 15) ≠ ±1 → compute gcd(7^2 ± 1, 15) = gcd(48, 15) = 3 and gcd(50, 15) = 5 → factors: 3 and 5 → verify: 3 × 5 = 15.

7. **Time & Space Complexity**  
   - Time: O((log N)³) quantum operations vs O(exp((log N)^(1/3))) classical (exponential speedup for large N).  
   - Space: O(log N) qubits (polynomial in input size, exponential advantage over classical).

8. **Strengths**  
- Exponential speedup: factors integers in polynomial time vs exponential classical time.
- Breaks RSA: threatens current RSA encryption if large quantum computers exist.
- Proven: mathematically proven to work for all composite numbers.

9. **Weaknesses / limitations**  
- Hardware requirements: needs large, fault-tolerant quantum computer (not yet available).
- Error sensitivity: requires very low error rates to work correctly.
- Limited to factoring: specific to integer factorization and related problems.

10. **Compare with alternatives**  
Alternatives: Classical Trial Division, Pollard's Rho Algorithm, General Number Field Sieve, Quantum Approximate Optimization

11. **30-second explanation (your own words)**  
    Factors large integers into their prime factors efficiently, breaking RSA encryption and solving problems that are intractable for classical computers.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
