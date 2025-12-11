# Knapsack Problem

## Principle of Operation

The Knapsack problem is like packing a bag for a trip. You have items with different weights and values, and a bag with a weight limit. Your goal is to choose items that give you the most total value without exceeding the weight limit.

**How it works:**
1. You have items, each with a weight and a value
2. You have a knapsack (bag) with a maximum weight capacity
3. For each item, you decide: take it or leave it (0/1 knapsack - can't split items)
4. You want to maximize total value while staying under weight limit
5. Use a table to remember the best value for each combination of items and remaining capacity

**Simple analogy:** Imagine you're a treasure hunter with a backpack that can hold 10 kg. You find items: gold (5 kg, worth $1000), silver (3 kg, worth $500), and gems (4 kg, worth $800). You can't take everything, so you need to choose the best combination. The knapsack algorithm helps you find the optimal choice.

**Key idea:** For each item, you check: "If I include this item, what's the best value I can get with the remaining capacity?" Then you compare that to "If I don't include this item, what's the best value?" You always choose the better option and remember it in a table.

## Algorithm Complexity

**Time Complexity:** O(n × W)
- n = number of items
- W = maximum weight capacity
- We fill a table with n rows and W columns
- Each cell takes constant time to compute

**Space Complexity:** O(n × W)
- Need table to store best value for each (item, capacity) combination
- Can be optimized to O(W) by using only one row

**Why it's efficient:** Instead of trying all 2ⁿ possible combinations (which would be exponential), we use a table to remember solutions to smaller problems. This makes it much faster.

## Where It's Used in Practice

**Resource Allocation:**
- **Budget planning** - choosing projects within budget
- **Cloud computing** - allocating resources with limits
- **Investment** - selecting investments with risk limits

**Everyday Applications:**
- **Packing for trips** - maximizing value within weight limit
- **Shopping** - choosing items within budget
- **Game inventory** - selecting items with weight/value trade-offs

**Real-World Problems:**
- **Manufacturing** - cutting materials to minimize waste
- **Logistics** - loading trucks with weight/volume limits
- **Energy management** - selecting energy sources with cost limits

## What It Can Be Compared To

**Like Making Choices:** At each step, you decide: take this item or skip it? You always choose the option that gives you more value.

**Like Building Up Solutions:** Start with small problems (few items, small capacity) and build up to the full problem. Each step uses answers from previous steps.

**Like a Decision Tree:** For each item, you have two choices: include it or not. The algorithm explores all paths but remembers the best ones to avoid repeating work.

**Different from Greedy:** Greedy would always take the item with best value/weight ratio, but that doesn't always give the best answer. Knapsack needs to consider all combinations, so it uses dynamic programming.

## Minimal Code Example

Here's a simple knapsack implementation:

```python
def knapsack(weights, values, capacity):
    """0/1 Knapsack using dynamic programming."""
    n = len(weights)
    # dp[i][w] = max value using first i items with capacity w
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                # Can include item: take max of including vs. not including
                dp[i][w] = max(
                    values[i - 1] + dp[i - 1][w - weights[i - 1]],  # Include
                    dp[i - 1][w]  # Don't include
                )
            else:
                # Item too heavy, can't include
                dp[i][w] = dp[i - 1][w]
    
    return dp[n][capacity]

# Example:
weights = [2, 3, 4, 5]
values = [3, 4, 5, 6]
capacity = 5
print(knapsack(weights, values, capacity))  # Output: 7
```

**Key parts:**
- Table stores best value for each (item, capacity) combination
- For each item, decide: include it (if fits) or skip it
- Always choose the option with higher value
- Final answer in dp[n][capacity]

## Common Mistakes

1. **Not Using a Table:**
   - **Wrong:** Trying all combinations without remembering results
   - **Why it's wrong:** Very slow, exponential time
   - **Fix:** Use dynamic programming table to remember solutions

2. **Wrong Table Size:**
   - **Wrong:** Using wrong dimensions for the table
   - **Why it's wrong:** Can't store all needed information
   - **Fix:** Table should be (n+1) × (capacity+1)

3. **Not Checking if Item Fits:**
   - **Wrong:** Trying to include items that are too heavy
   - **Why it's wrong:** Accesses invalid positions, wrong results
   - **Fix:** Always check `if weights[i-1] <= w` before including

4. **Confusing with Fractional Knapsack:**
   - **Wrong:** Using greedy approach (sort by value/weight)
   - **Why it's wrong:** Greedy doesn't work for 0/1 knapsack
   - **Fix:** Use dynamic programming for 0/1 knapsack

5. **Array Index Errors:**
   - **Wrong:** Using wrong indices for items and table
   - **Why it's wrong:** Accesses wrong items, incorrect results
   - **Fix:** Remember dp[i][w] uses items[0..i-1], so item i-1 is current

## Recommended Literature

1. **"Grokking Algorithms"** by Aditya Bhargava
   - Simple explanations of dynamic programming
   - Great knapsack examples

2. **"Introduction to Algorithms" (CLRS)**
   - Comprehensive coverage of knapsack problem
   - Explains why dynamic programming works

3. **"Algorithm Design Manual"** by Steven Skiena
   - Practical approach with examples
   - Good for understanding the thinking process

4. **Online Resources:**
   - GeeksforGeeks - knapsack tutorials
   - Khan Academy - dynamic programming course
   - LeetCode - practice problems
