# Knapsack Problem (0/1 Knapsack)

## Convergence Speed and Complexity Estimate

**Time Complexity:**
- **Dynamic Programming (Bottom-Up):** O(n × W) where n is number of items and W is knapsack capacity. We fill a 2D table of size (n+1) × (W+1), computing each cell in constant time.
- **Space-Optimized DP:** O(n × W) time, O(W) space - using only one row of the DP table and updating it iteratively.
- **Recursive with Memoization:** O(n × W) - each unique subproblem (item, remaining capacity) is solved once.
- **Brute Force:** O(2ⁿ) - exponential time, checking all 2ⁿ possible subsets of items.

**Space Complexity:**
- **Standard DP:** O(n × W) - 2D table storing maximum value for each (item, capacity) combination.
- **Space-Optimized DP:** O(W) - only storing one row (current capacity values) and updating it.
- **Memoized Recursive:** O(n × W) - memoization table plus recursion stack O(n).

**Convergence:** The algorithm converges when the DP table is completely filled. Each cell dp[i][w] represents the maximum value achievable using first i items with capacity w. The final answer is in dp[n][W], computed after processing all n items and all capacities from 0 to W.

**Pseudopolynomial Complexity:** O(n × W) is pseudopolynomial because W (capacity) is a number, not input size. If W is large (exponential in input size), this becomes exponential. True polynomial would be O(n × log W).

## Where the Algorithm is Used in Real Frameworks and Software

The Knapsack problem is fundamental in optimization and resource allocation:

- **Resource Allocation:**
  - **Cloud computing** - allocating virtual machines with CPU/memory constraints
  - **Budget optimization** - selecting projects within budget constraints
  - **Portfolio optimization** - selecting investments with risk/return trade-offs
  - **Resource scheduling** - allocating tasks with resource limits

- **Cutting Stock Problem:**
  - **Manufacturing** - cutting materials (wood, metal) to minimize waste
  - **Paper industry** - cutting paper rolls to fulfill orders
  - **Textile industry** - cutting fabric with minimum waste

- **Cryptography:**
  - **Merkle-Hellman knapsack cryptosystem** - public-key encryption (though broken)
  - **Subset sum problems** - related cryptographic applications

- **Game Development:**
  - **Inventory systems** - selecting items with weight/value constraints
  - **Loot systems** - optimizing loot selection within capacity
  - **Character equipment** - selecting gear with stat/weight trade-offs

- **Real-World Applications:**
  - **Logistics** - loading trucks/containers with weight/volume constraints
  - **Energy management** - selecting energy sources with cost/capacity limits
  - **Project selection** - choosing projects with budget/time constraints
  - **Advertising** - selecting ad placements with budget/impression constraints

## What It's Similar To in Concept

The Knapsack problem shares conceptual similarities with:

- **Dynamic Programming Pattern:** Classic DP problem - optimal substructure (solution to subproblem helps solve larger problem) and overlapping subproblems (same subproblems computed multiple times). Similar structure to other DP problems like coin change, longest increasing subsequence.

- **Subset Sum Problem:** Knapsack is generalization - instead of just checking if subset sums to target, we maximize value of subset with weight constraint. Both explore all possible subsets.

- **Greedy Algorithms:** Similar to fractional knapsack (greedy works) but 0/1 knapsack requires DP because items can't be split. Greedy would choose highest value/weight ratio, but that's not optimal for 0/1 version.

- **Backtracking:** Brute force solution explores all subsets (2ⁿ possibilities), similar to backtracking. DP optimizes this by storing results of subproblems.

- **Integer Linear Programming:** Knapsack can be formulated as ILP: maximize Σ(vᵢxᵢ) subject to Σ(wᵢxᵢ) ≤ W, xᵢ ∈ {0,1}. DP provides efficient solution for this specific ILP problem.

## Which Algorithms It's Often Used With

The Knapsack algorithm is frequently combined with:

- **Other Dynamic Programming Problems:**
  - **Coin Change** - similar DP structure, different constraints
  - **Longest Common Subsequence** - similar 2D DP table pattern
  - **Edit Distance** - similar DP approach with different recurrence

- **Optimization Techniques:**
  - **Branch and Bound** - for solving large knapsack instances
  - **Approximation algorithms** - for near-optimal solutions when exact solution too slow
  - **Greedy algorithms** - for comparison and understanding trade-offs

- **Related Problems:**
  - **Fractional Knapsack** - where items can be split (greedy works)
  - **Multiple Knapsack** - multiple knapsacks to fill
  - **Bounded Knapsack** - each item has limited quantity
  - **Unbounded Knapsack** - unlimited quantity of each item

- **Data Structures:**
  - **2D Arrays** - for DP table storage
  - **Memoization tables** - for recursive DP approach

## Key Code (Only Important Parts)

Here's a concise implementation highlighting the essential logic:

```python
def knapsack(weights: List[int], values: List[int], capacity: int) -> int:
    """0/1 Knapsack using dynamic programming."""
    n = len(weights)
    # dp[i][w] = max value using first i items with capacity w
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            # Can we include item i-1?
            if weights[i - 1] <= w:
                # Take max of: including item vs. not including item
                dp[i][w] = max(
                    values[i - 1] + dp[i - 1][w - weights[i - 1]],  # Include
                    dp[i - 1][w]  # Don't include
                )
            else:
                # Item too heavy, can't include
                dp[i][w] = dp[i - 1][w]
    
    return dp[n][capacity]

# Space-optimized version (O(W) space)
def knapsack_optimized(weights: List[int], values: List[int], capacity: int) -> int:
    """Space-optimized knapsack - only O(W) space."""
    dp = [0] * (capacity + 1)
    
    for i in range(len(weights)):
        # Process backwards to avoid overwriting needed values
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], values[i] + dp[w - weights[i]])
    
    return dp[capacity]
```

**Key Points:**
- DP table: dp[i][w] = max value with first i items, capacity w
- Recurrence: include item (if fits) or skip it
- Time: O(n × W), Space: O(n × W) or O(W) optimized
- Bottom-up approach fills table iteratively
- Final answer: dp[n][capacity]

## Common Application Errors

1. **Wrong DP State Definition:**
   - **Error:** Using dp[i] = max value with i items (missing capacity dimension)
   - **Impact:** Can't track remaining capacity, incorrect results
   - **Solution:** Always use 2D DP: dp[i][w] with both item count and capacity

2. **Incorrect Recurrence Relation:**
   - **Error:** Not checking if item fits before including it
   - **Impact:** Accesses negative indices or incorrect values
   - **Solution:** Always check `if weights[i-1] <= w` before including item

3. **Array Index Off-by-One:**
   - **Error:** Using 0-indexed items with 1-indexed DP table incorrectly
   - **Impact:** Accesses wrong items, incorrect results
   - **Solution:** Be consistent: dp[i][w] uses items[0..i-1], so item i-1 is current item

4. **Not Initializing Base Cases:**
   - **Error:** Not setting dp[0][w] = 0 for all w (no items = 0 value)
   - **Impact:** Incorrect base case, wrong results
   - **Solution:** Initialize dp[0][w] = 0 (0 items always gives 0 value)

5. **Space Optimization Direction Error:**
   - **Error:** Processing capacity forwards instead of backwards in optimized version
   - **Impact:** Overwrites values needed for current iteration
   - **Solution:** Process capacity backwards (W down to weights[i]) to preserve needed values

6. **Confusing with Fractional Knapsack:**
   - **Error:** Using greedy approach (sort by value/weight ratio) for 0/1 knapsack
   - **Impact:** Greedy doesn't work for 0/1 version, gives suboptimal solution
   - **Solution:** Use DP for 0/1 knapsack, greedy only works for fractional version

## Recommended Literature

1. **"Introduction to Algorithms" (CLRS)** - Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein
   - Comprehensive coverage of knapsack problem with detailed DP analysis and proof of correctness

2. **"Algorithm Design Manual"** - Steven S. Skiena
   - Practical approach to knapsack with implementation details, variations, and when to use different approaches

3. **"Dynamic Programming: From Novice to Advanced"** - various online resources
   - Step-by-step explanation of DP thinking process applied to knapsack

4. **"Competitive Programming"** - various authors
   - Knapsack as classic DP problem with optimization techniques and space reduction tricks

5. **Online Resources:**
   - GeeksforGeeks - detailed knapsack tutorials with examples
   - LeetCode - practice problems (Knapsack variations)
   - TopCoder tutorials - advanced DP techniques
