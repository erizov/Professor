# Dynamic Programming Fibonacci

1. **Name of Algorithm**  
   Dynamic Programming Fibonacci

2. **What problem does it solve? (1 sentence)**  
   Computes nth Fibonacci number efficiently by caching results instead of using exponential recursion.

3. **Intuition (plain-language explanation)**  
   Store results of smaller fib values so each number is computed once; akin to filling a table bottom-up.

4. **Inputs & Outputs**  
   - Input: Integer n ≥ 0.  
   - Output: Fibonacci number F(n) where F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2).

5. **Step-by-step description (5–10 lines max)**  
1. Initialize dp[0]=0, dp[1]=1.
2. For i=2 to n: dp[i] = dp[i-1] + dp[i-2].
3. Optionally reduce to two variables for constant space.
4. Return dp[n].

6. **Tiny example (hand-simulated)**  
   n=6 → sequence 0,1,1,2,3,5,8 → fib(6)=8.

7. **Time & Space Complexity**  
   - Time: O(n).  
   - Space: O(n) for table or O(1) with rolling values.

8. **Strengths**  
- Demonstrates memoization/bottom-up DP basics.
- Linear time versus exponential recursive approach.

9. **Weaknesses / limitations**  
- Simple example; real problems may require more intricate states.
- Large n requires big integers or modulo arithmetic.

10. **Compare with alternatives**  
    Alternatives: Matrix Exponentiation, Closed-form (Binet) Formula, Fast Doubling Method

11. **30-second explanation (your own words)**  
    Replace naive recursion with iterative accumulation while caching prior values so each Fibonacci number is computed exactly once.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
