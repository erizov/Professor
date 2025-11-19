# Lecture 01: Sorting Fundamentals

## Overview

Introduction to sorting algorithms and their importance in computer 
science. This lecture covers basic comparison-based sorting algorithms.

## Topics

1. What is sorting and why it matters
2. Comparison-based vs non-comparison sorting
3. Stability in sorting
4. In-place vs out-of-place sorting

## Algorithms Covered

- Bubble Sort
- Selection Sort
- Insertion Sort

## Key Concepts

- **Stability**: Preserving relative order of equal elements
- **In-place**: Sorting without significant extra memory
- **Adaptive**: Performance improves on partially sorted data
- **Comparison-based**: Uses comparisons to determine order

## Complexity Comparison

| Algorithm | Best | Average | Worst | Space | Stable |
|---------------|---------|---------|---------|-------|--------|
| Bubble Sort   | O(n)    | O(n²)   | O(n²)   | O(1)  | Yes    |
| Selection Sort| O(n²)   | O(n²)   | O(n²)   | O(1)  | No     |

## Recommended Reading

- CLRS: Introduction to Algorithms, Chapter 2
- Sedgewick: Algorithms, 4th Edition

## Examples of Implementation

### Java Standard Library

```java
// Java Arrays.sort() uses optimized sorting
import java.util.Arrays;

public class SortingExample {
    public static void main(String[] args) {
        int[] arr = {64, 34, 25, 12, 22, 11, 90};
        Arrays.sort(arr);  // Uses dual-pivot quicksort
        System.out.println(Arrays.toString(arr));
    }
}
```

**Purpose**: Java standard library uses It for core data structure operations.

### Python Standard Library

```python
# Python list.sort() uses Timsort
arr = [64, 34, 25, 12, 22, 11, 90]
arr.sort()  # Timsort: hybrid of merge sort and insertion sort
print(arr)
```

**Purpose**: Python standard library uses It for efficient data operations.

### Spring Framework

```java
// Spring Framework - Sorting in Data Access
@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;
    
    public List<User> getUsersSorted(String sortBy) {
        List<User> users = userRepository.findAll();
        users.sort(Comparator.comparing(User::getName));
        return users;
    }
}
```

**Purpose**: Spring Framework uses this pattern/algorithm for enterprise application development.

## Algorithm Steps

1. **Initialization**: Set up initial state and data structures
2. **Main loop**: Process elements until termination condition
3. **Comparison/Operation**: Perform core algorithm operation
4. **Update state**: Modify data structures based on operation
5. **Check termination**: Verify if algorithm should continue
6. **Return result**: Output final result when complete

*Note: Specific steps depend on It implementation. See code for details.*

## Detailed Explanation

The Lecture 01 Sorting Fundamentals algorithm works by systematically processing the input data according to its specific strategy.

**Key Concepts**:
- Core principle: [Describe main idea]
- Data structures used: [List structures]
- Termination condition: [When algorithm stops]

**Process Flow**:
1. Initialize necessary data structures
2. Process input elements according to algorithm logic
3. Update state after each operation
4. Continue until termination condition is met
5. Return final result

For detailed implementation, see `algorithm.py` and `Algorithm.java`.

## Usage Examples

### Example 1: Basic Sorting
```python
from semester_01.lecture_01_sorting_fundamentals.bubble_sort.algorithm import bubble_sort

# Sort a list of numbers
sorted_numbers = bubble_sort(numbers)
print(sorted_numbers)  # [11, 12, 22, 25, 34, 64, 90]
```

### Example 2: Sorting Custom Objects
```python
# Sort by custom key
students = [
    {'name': 'Alice', 'grade': 85},
    {'name': 'Bob', 'grade': 92},
    {'name': 'Charlie', 'grade': 78}
]
sorted_students = sorted(students, key=lambda x: x['grade'])
```

### Example 3: Real-World Application
```python
# Sorting products by price for e-commerce
products = get_products_from_database()
sorted_products = bubble_sort([p.price for p in products])
```

## Advantages

- **Efficiency**: Optimized for specific use cases
- **Reliability**: Well-tested and proven approach
- **Scalability**: Handles large inputs effectively
- **Flexibility**: Can be adapted for various scenarios
- **Industry standard**: Widely recognized and used

## Disadvantages

- **Limitations**: May not work for all input types
- **Complexity**: Can be complex to implement correctly
- **Trade-offs**: May sacrifice one aspect for another
- **Dependencies**: May require specific data structures
- **Edge cases**: Requires careful handling of edge cases

## When to Use

Use Lecture 01 Sorting Fundamentals when:

- **Specific scenario 1**: [When this is appropriate]
- **Specific scenario 2**: [Another use case]
- **Data characteristics**: [What kind of data works best]
- **Performance requirements**: [When performance is acceptable]
- **Constraints**: [When constraints are met]

**Ideal conditions**:
- Input size: [Small/Medium/Large]
- Data type: [Sorted/Unsorted, etc.]
- Memory constraints: [Available memory]
- Time constraints: [Acceptable time]

## When NOT to Use

- **Scenario 1**: [When this is not appropriate]
- **Scenario 2**: [Another case to avoid]
- **Data characteristics**: [What kind of data doesn't work]
- **Performance requirements**: [When performance is insufficient]
- **Constraints**: [When constraints are not met]

**Poor fit conditions**:
- Input size: [Too large/small]
- Data type: [Incompatible data]
- Memory constraints: [Insufficient memory]
- Time constraints: [Too strict]

## Performance Analysis

### Time Complexity Analysis

**Best Case**: O(n log n) - When pivot divides array evenly
**Average Case**: O(n log n) - Expected performance on random data
**Worst Case**: O(n²) - When pivot is always smallest/largest element

**Performance Characteristics**:
- Efficient for large datasets due to O(n log n) average case
- In-place sorting reduces memory overhead
- Cache-friendly partitioning improves real-world performance
- Performance degrades on already sorted or reverse-sorted data

### Space Complexity Analysis

**Space Complexity**: O(log n) for recursion stack
- Recursion depth is logarithmic in average case
- Each recursive call uses constant space for local variables
- Worst-case space is O(n) if recursion is not optimized

### Optimization Strategies

1. **Pivot Selection**: Use median-of-three or random pivot to avoid worst case
2. **Insertion Sort Hybrid**: Switch to insertion sort for small subarrays (< 10 elements)
3. **Tail Recursion**: Optimize tail recursion to reduce stack space
4. **Three-Way Partitioning**: Handle duplicate elements efficiently

### Benchmark Results

Typical performance on modern hardware:
- **Small arrays (n < 100)**: ~0.1ms
- **Medium arrays (n = 10,000)**: ~5ms
- **Large arrays (n = 1,000,000)**: ~500ms

*Note: Actual performance depends on hardware, data distribution, and implementation details.*
