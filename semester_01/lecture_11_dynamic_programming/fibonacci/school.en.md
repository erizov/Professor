# Fibonacci

# School

## 📋 Quick Summary

- **Purpose:** Fibonacci: Each number is the sum of the two previous numbers - we can compute this efficiently by storing previous results.
- **Complexity:** O(n²)
- **Category:** Algorithms
- **Key Idea:** Each number is the sum of the two previous numbers - we can compute this efficiently by storing previous results.

Fibonacci: Each number is the sum of the two previous numbers - we can compute this efficiently by storing previous results.

Each number is the sum of the two previous numbers - we can compute this efficiently by storing previous results.

**FIBONACCI** = Find In Both, Add Next, Continue Iteratively. Each number is the sum of the two before it!








This algorithm works by processing data systematically to achieve its goal. It's part of the **Dynamic Programming** category of algorithms.

## Algorithm Complexity

The time complexity is **O(n²)**, which means the time it takes to run depends on the size of the input data. The space complexity is **O(1)**, indicating how much extra memory is needed.

## Where It's Used in Practice

Fibonacci is commonly used in:
- Mathematical sequence generation
- Financial modeling (Fibonacci retracements)
- Algorithm complexity analysis
- Computer science education and algorithm learning

## What It Can Be Compared To

Think of Fibonacci like a systematic way of organizing or finding information - similar to how you might organize items or search through a collection efficiently.

## Minimal Code Example

```python
def fibonacci(n):
    """Implementation."""
    if n <= 1:
    return n
    dp = [0] * (n + 1)
    dp[1] = 1
    return result
```

## 🎯 Try It Yourself

**Try computing Fibonacci(5) by hand:**
F(0) = 0
F(1) = 1
F(2) = F(1) + F(0) = 1 + 0 = 1
F(3) = F(2) + F(1) = 1 + 1 = 2
F(4) = F(3) + F(2) = 2 + 1 = 3
F(5) = F(4) + F(3) = 3 + 2 = 5

Answer: 5
```

## ✏️ Practice Exercise

**Exercise 1 (Easy):**
Calculate the first 10 Fibonacci numbers by hand.

**Exercise 2 (Medium):**
Write a function to compute Fibonacci(n) using dynamic programming (store previous results).

**Exercise 3 (Hard):**
Compare the time complexity of recursive Fibonacci vs dynamic programming Fibonacci. Why is DP faster?

## ✅ Check Your Understanding

**Q1:** What are the base cases for Fibonacci?
**A:** F(0) = 0 and F(1) = 1.

**Q2:** Why is recursive Fibonacci slow?
**A:** It recalculates the same values many times (exponential time complexity).

**Q3:** How does dynamic programming make Fibonacci faster?
**A:** By storing previously computed values, we avoid redundant calculations (linear time complexity).

**Q4:** What is the space complexity of DP Fibonacci?
**A:** O(n) if we store all values, or O(1) if we only keep the last two values.


**Try computing Fibonacci(5) by hand:**
```
F(0) = 0
F(1) = 1
F(2) = F(1) + F(0) = 1 + 0 = 1
F(3) = F(2) + F(1) = 1 + 1 = 2
F(4) = F(3) + F(2) = 2 + 1 = 3
F(5) = F(4) + F(3) = 3 + 2 = 5

Answer: 5


**Exercise 1 (Easy):**
Calculate the first 10 Fibonacci numbers by hand.

**Exercise 2 (Medium):**
Write a function to compute Fibonacci(n) using dynamic programming (store previous results).

**Exercise 3 (Hard):**
Compare the time complexity of recursive Fibonacci vs dynamic programming Fibonacci. Why is DP faster?


**Q1:** What are the base cases for Fibonacci?
**A:** F(0) = 0 and F(1) = 1.

**Q2:** Why is recursive Fibonacci slow?
**A:** It recalculates the same values many times (exponential time complexity).

**Q3:** How does dynamic programming make Fibonacci faster?
**A:** By storing previously computed values, we avoid redundant calculations (linear time complexity).

**Q4:** What is the space complexity of DP Fibonacci?
**A:** O(n) if we store all values, or O(1) if we only keep the last two values.

## Common Mistakes

### ❌ Mistake 1: Test with edge cases (empty input, single element, boundary values)
**Solution:** [How to fix this mistake]

### ❌ Mistake 2: Trace through examples step-by-step

### ❌ Mistake 3: Use debugging tools to verify your logic

### ❌ Mistake 4: Review the algorithm's key steps before implementing

### 💡 How to Avoid
- Test with edge cases (empty input, single element, boundary values)
- Trace through examples step-by-step
- Use debugging tools to verify your logic
- Review the algorithm's key steps before implementing


## Recommended Literature

- "Introduction to Algorithms" by Cormen, Leiserson, Rivest, and Stein
- "Algorithms" by Robert Sedgewick and Kevin Wayne
- Online resources: GeeksforGeeks, Wikipedia, Algorithm Visualizations



