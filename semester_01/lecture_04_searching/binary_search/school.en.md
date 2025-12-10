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


> **Note**: Mermaid diagrams are rendered automatically on GitHub. For local viewing, use a Mermaid-compatible Markdown viewer.



## Algorithm Complexity

The time complexity is **O(log n)**, which means the time it takes to run depends on the size of the input data. The space complexity is **O(1)**, indicating how much extra memory is needed.

## Where It's Used in Practice

- Searching in sorted arrays and databases
- Finding elements in phone books, dictionaries
- Range queries in databases
- Game development (finding items in sorted lists)

## What It Can Be Compared To

Think of Binary Search like a systematic way of organizing or finding information - similar to how you might organize items or search through a collection efficiently.

## Minimal Code Example

```python
def binary_search(arr, target):
    """Implementation."""
    left, right = (0, len(arr) - 1)
    return result
```


---

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


---


## 🔍 Step-by-Step Execution

**Step-by-Step Execution:**

```python
# Input
arr = [1, 3, 5, 7, 9, 11, 13]
target = 7
left = 0
right = 6

# Iteration 1
mid = (0 + 6) // 2 = 3
arr[mid] = arr[3] = 7
7 == 7? Yes! Found at index 3

# Result
return 3
```

**Variable States:**
```
Iteration | left | right | mid | arr[mid] | Comparison | Action
----------|------|-------|-----|----------|------------|--------
    1     |  0   |   6   |  3  |    7     | 7 == 7     | Found!
```

**Expected Output:**

```
Searching for 7 in [1, 3, 5, 7, 9, 11, 13]
Checking index 3: value = 7
Found at index 3!
```

## ✏️ Practice Exercise

**Exercise 1 (Easy):**
Find the number 42 in this sorted array: [10, 20, 30, 40, 50, 60, 70]
Show each step of your search.

**Exercise 2 (Medium):**
Implement binary search to find the first occurrence of a target value in a sorted array with duplicates.

**Exercise 3 (Hard):**
What happens if you try binary search on an unsorted array? Why doesn't it work?


---

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



## Common Mistakes

### ❌ Mistake 1: Not handling edge cases
**Solution:** Always check for empty input, single element, or boundary values before processing.

### ❌ Mistake 2: Incorrect initialization
**Solution:** Ensure all variables and data structures are properly initialized before the main algorithm loop.

### ❌ Mistake 3: Off-by-one errors in loops
**Solution:** Carefully verify loop bounds and termination conditions. Test with small examples to catch boundary issues.

### ❌ Mistake 4: Not validating input
**Solution:** Add input validation to ensure data is in expected format and within valid ranges.

### 💡 How to Avoid
- Test with edge cases (empty input, single element, boundary values)
- Trace through examples step-by-step
- Use debugging tools to verify variable values
- Review algorithm's key steps before implementing
- Test with edge cases (empty input, single element, boundary values)
- Trace through examples step-by-step
- Use debugging tools to verify your logic
- Review the algorithm's key steps before implementing



---

## Recommended Literature

- "Introduction to Algorithms" by Cormen, Leiserson, Rivest, and Stein
- "Algorithms" by Robert Sedgewick and Kevin Wayne
- Online resources: GeeksforGeeks, Wikipedia, Algorithm Visualizations



