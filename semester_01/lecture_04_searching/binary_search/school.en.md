# Binary Search

# School

## 📋 Quick Summary

- **Purpose:** Binary Search: Always check the middle element - if it's not what we want, eliminate half the search space.
- **Complexity:** O(log n)
- **Category:** Searching
- **Key Idea:** Always check the middle element - if it's not what we want, eliminate half the search space.

Binary Search: Always check the middle element - if it's not what we want, eliminate half the search space.

Always check the middle element - if it's not what we want, eliminate half the search space.

**BINARY** = Begin In Middle, Always Narrow Your search. Like finding a word in a dictionary - always check the middle!








This algorithm works by processing data systematically to achieve its goal. It's part of the **Searching** category of algorithms.

## Algorithm Complexity

The time complexity is **O(log n)**, which means the time it takes to run depends on the size of the input data. The space complexity is **O(1)**, indicating how much extra memory is needed.

## Where It's Used in Practice

Binary Search is commonly used in:
- Database query optimization
- Search engines (binary search in sorted indices)
- Autocomplete and suggestion systems
- Computer science education and algorithm learning

## What It Can Be Compared To

Think of Binary Search like a systematic way of organizing or finding information - similar to how you might organize items or search through a collection efficiently.

## Minimal Code Example

```python
def binary_search(arr, target):
    """Implementation."""
    left, right = (0, len(arr) - 1)
    return result
```

## 🎯 Try It Yourself

**Try finding 7 in this sorted array:**
Array: [1, 3, 5, 7, 9, 11, 13]
Target: 7

Step 1: Check middle element (index 3, value 5)
  5 < 7, so search right half: [7, 9, 11, 13]

Step 2: Check middle of right half (index 5, value 9)
  9 > 7, so search left half: [7]

Step 3: Found! Element 7 is at index 3
```

## ✏️ Practice Exercise

**Exercise 1 (Easy):**
Find the number 42 in this sorted array: [10, 20, 30, 40, 50, 60, 70]
Show each step of your search.

**Exercise 2 (Medium):**
Implement binary search to find the first occurrence of a target value in a sorted array with duplicates.

**Exercise 3 (Hard):**
What happens if you try binary search on an unsorted array? Why doesn't it work?

## ✅ Check Your Understanding

**Q1:** Why must the array be sorted for binary search?
**A:** Because we eliminate half the search space based on comparison - this only works if elements are ordered.

**Q2:** What is the time complexity of binary search?
**A:** O(log n) - we halve the search space each time.

**Q3:** What is the space complexity of iterative binary search?
**A:** O(1) - we only use a few variables, no extra space needed.

**Q4:** When would you use binary search instead of linear search?
**A:** When the array is sorted and you need to search multiple times - the O(log n) vs O(n) advantage is significant.


**Try finding 7 in this sorted array:**
```
Array: [1, 3, 5, 7, 9, 11, 13]
Target: 7

Step 1: Check middle element (index 3, value 5)
  5 < 7, so search right half: [7, 9, 11, 13]

Step 2: Check middle of right half (index 5, value 9)
  9 > 7, so search left half: [7]

Step 3: Found! Element 7 is at index 3
```


**Exercise 1 (Easy):**
Find the number 42 in this sorted array: [10, 20, 30, 40, 50, 60, 70]
Show each step of your search.

**Exercise 2 (Medium):**
Implement binary search to find the first occurrence of a target value in a sorted array with duplicates.

**Exercise 3 (Hard):**
What happens if you try binary search on an unsorted array? Why doesn't it work?


**Q1:** Why must the array be sorted for binary search?
**A:** Because we eliminate half the search space based on comparison - this only works if elements are ordered.

**Q2:** What is the time complexity of binary search?
**A:** O(log n) - we halve the search space each time.

**Q3:** What is the space complexity of iterative binary search?
**A:** O(1) - we only use a few variables, no extra space needed.

**Q4:** When would you use binary search instead of linear search?
**A:** When the array is sorted and you need to search multiple times - the O(log n) vs O(n) advantage is significant.

## Common Mistakes

### ❌ Mistake 1: Test with edge cases (empty input, single element, boundary values)
**Solution:** Verify array is sorted: `if data != sorted(data): raise ValueError`

### ❌ Mistake 2: Trace through examples step-by-step
**Solution:** Manually trace through a small example (3-5 elements) to verify each step matches the algorithm logic

### ❌ Mistake 3: Use debugging tools to verify your logic
**Solution:** Use print statements or debugger to check variable values at each step, compare with expected behavior

### ❌ Mistake 4: Review the algorithm's key steps before implementing
**Solution:** Study the algorithm's pseudocode or description, identify the core steps, then implement one step at a time

### 💡 How to Avoid
- Test with edge cases (empty input, single element, boundary values)
- Trace through examples step-by-step
- Use debugging tools to verify your logic
- Review the algorithm's key steps before implementing


## Recommended Literature

- "Introduction to Algorithms" by Cormen, Leiserson, Rivest, and Stein
- "Algorithms" by Robert Sedgewick and Kevin Wayne
- Online resources: GeeksforGeeks, Wikipedia, Algorithm Visualizations



