# Binary Search

**Category**: Searching

**Time Complexity**: O(log n)

**Space Complexity**: O(1)

## Implementation

## Introduction

Binary Search is a fundamental algorithm.

This algorithm is widely used in computer science and software engineering for solving a specific class of problems efficiently. Understanding Binary Search is essential for building performant and scalable applications.

## TL;DR (Too Long; Didn't Read)

**One Sentence**: An efficient search algorithm that finds the position of a target value within a sorted array by repeatedly dividing the search interval in half.

**Time Complexity**: See complexity analysis below
**Space Complexity**: See complexity analysis below
**When to Use**: See 'Best Use Case' section
**When NOT to Use**: See 'Do Not Confuse With' section

## Learning Objectives
## Prerequisites

- Basic programming knowledge in Python or Java
- Understanding of arrays, lists, and basic data structures
- Familiarity with loops, conditionals, and functions
- Knowledge of array indexing and iteration



By the end of this lecture, students will be able to:

1. Implement Binary Search from scratch
2. Analyze time and space complexity using Big O notation
3. Identify when to use this algorithm vs. alternative approaches
4. Recognize common implementation pitfalls and how to avoid them
5. Apply this algorithm to solve real-world problems

### Short Description

An efficient search algorithm that finds the position of a target value within a sorted array by repeatedly dividing the search interval in half.

**Key Characteristics:**
- **Time Complexity**: Varies
- **Space Complexity**: Varies
- **Stability**: N/A
- **Best Use Case**: General purpose


See algorithm.py and Algorithm.java


## Often Used Together With

Binary Search is commonly used in combination with:

- **Linear Search**: Often combined for comprehensive solutions
- **Hash Table**: Often combined for comprehensive solutions

**Common Combinations:**
- Used together in production systems for optimal performance
- Complementary algorithms that solve related problems
- Often part of larger algorithmic frameworks


## Do Not Confuse With

- **Linear Search**: Binary search requires sorted data O(log n), linear search works on any data O(n)
- **Interpolation Search**: Both require sorted data but interpolation assumes uniform distribution for better average case
- **Ternary Search**: Divides into three parts instead of two, similar concept but different implementation


## Self-Assessment Questions

Test your understanding with these questions:

### Comprehension
1. Can you explain how Binary Search works in your own words?
2. What is the key insight or technique that makes Binary Search efficient?

### Analysis
3. What are the best-case, average-case, and worst-case time complexities?
4. When would you choose Binary Search over alternative algorithms?

### Application
5. Can you implement Binary Search from memory without looking at the code?
6. What real-world problem could you solve using Binary Search?

### Debugging
7. What are the most common mistakes when implementing Binary Search?
8. How would you test your Binary Search implementation?

**Scoring**: If you can answer 6+ questions confidently, you've mastered this algorithm!


## Algorithm Visualization


```
Binary Search: Find 7 in [1, 3, 5, 7, 9, 11]

Step 1: Check middle (index 2, value 5)
[1, 3, 5, 7, 9, 11]
         ↑
        5 < 7, search right

Step 2: Check middle of right half (index 4, value 9)
[7, 9, 11]
    ↑
    9 > 7, search left

Step 3: Check remaining (index 3, value 7)
[7]
 ↑
 Found! Index 3
```


## Practice Exercises

### Level 1: Understanding (Beginner)
1. Trace through Binary Search step-by-step with input: [5, 2, 8, 1, 9]
2. Identify the base case(s) in Binary Search
3. Explain why Binary Search has its time complexity

### Level 2: Implementation (Intermediate)
4. Implement Binary Search from scratch using only the function signature
5. Modify Binary Search to handle edge cases (empty input, single element, etc.)
6. Add logging to track the algorithm's execution steps

### Level 3: Optimization (Advanced)
7. Optimize Binary Search for a specific use case (e.g., nearly sorted data)
8. Implement a parallel or distributed version of Binary Search
9. Compare Binary Search performance with alternative algorithms on large datasets

### Level 4: Real-World Application (Expert)
10. Design a system that uses Binary Search to solve a production problem
11. Create unit tests with 100% code coverage for Binary Search
12. Write a technical blog post explaining Binary Search to beginners


## Real-World Applications

- **Search Engines**: Finding documents in sorted indexes
- **Databases**: Index lookups in B-trees
- **Debugging**: Binary search for finding bugs (git bisect)


## Common Misconceptions

❌ **WRONG**: "Binary Search works on any array"
✓ **CORRECT**: Binary Search requires the array to be sorted

❌ **WRONG**: "Binary Search is always faster than Linear Search"
✓ **CORRECT**: For small arrays, linear search may be faster due to overhead


## Examples of Implementation



This algorithm/pattern is implemented in the following frameworks and technologies:

### Spring Framework

```java
// Spring Data JPA - Binary search on indexed fields
public interface UserRepository extends JpaRepository<User, Long> {
    // Uses binary search on indexed email field
    Optional<User> findByEmail(String email);
    
    // Binary search for range queries
    List<User> findByIdBetween(Long start, Long end);
}
```

**Purpose**: Spring Framework uses this pattern for dependency injection, bean management, and enterprise application development.

### .NET Framework

```csharp
// .NET Array.BinarySearch for sorted collections
int[] sortedIds = GetSortedUserIds();
int index = Array.BinarySearch(sortedIds, userId);
if (index >= 0) {
    return users[index];
}
```

**Purpose**: .NET Framework uses this pattern for dependency injection, ASP.NET Core, and enterprise application development.


