# Radix Sort

## Convergence Speed and Complexity Estimate

**Time Complexity:**
- **Best Case:** O(d × (n + k)) - where d is the number of digits, n is the number of elements, and k is the radix (base, typically 10 for decimal). The algorithm always performs the same operations regardless of input order.
- **Average Case:** O(d × (n + k)) - consistent performance, as Radix Sort processes each digit position exactly once.
- **Worst Case:** O(d × (n + k)) - same as best case, making Radix Sort one of the few algorithms with guaranteed performance independent of input distribution.

**Space Complexity:** O(n + k) - requires space for the output array (n elements) and the count array for each digit position (k elements, where k is the radix, typically 10 for decimal digits).

**Convergence:** The algorithm converges after processing all digit positions from least significant digit (LSD) to most significant digit (MSD), or vice versa. Convergence is deterministic and requires exactly d passes, where d is the maximum number of digits.

## Where the Algorithm is Used in Real Frameworks and Software

Radix Sort is used in specialized applications where its linear-time characteristics provide advantages:

- **Integer Sorting Applications:**
  - **Sorting large integers** where the number of digits is small relative to n
  - **Sorting fixed-width data types** (e.g., 32-bit or 64-bit integers)
  - **Sorting strings** of fixed or bounded length (treating characters as digits)

- **System Software:**
  - **Operating system internals** for sorting process IDs, file handles, or other integer identifiers
  - **Network stack** implementations for sorting packet sequence numbers
  - **Database systems** for sorting integer keys or fixed-width records

- **Real-World Applications:**
  - **Sorting phone numbers** (fixed or bounded length)
  - **Sorting social security numbers** or other ID numbers
  - **Sorting IP addresses** (when treated as integers)
  - **Sorting dates** represented as integers (YYYYMMDD format)

- **As a Building Block:**
  - **String sorting** algorithms use Radix Sort concepts
  - **External sorting** algorithms adapted for integer data
  - **Parallel sorting** algorithms that can process digits in parallel

## What It's Similar To in Concept

Radix Sort shares conceptual similarities with:

- **Counting Sort:** Radix Sort uses Counting Sort as a subroutine for each digit position. Counting Sort is applied d times, once for each digit.

- **Bucket Sort:** Both distribute elements into containers based on some property. Radix Sort uses digit values, while Bucket Sort uses value ranges. Radix Sort can be seen as a multi-pass Bucket Sort.

- **String Sorting:** Radix Sort naturally extends to strings by treating each character as a digit. This makes it efficient for sorting fixed-length strings or strings with bounded length.

- **Trie Data Structures:** The digit-by-digit processing resembles how tries organize data by character/digit position, building the structure incrementally.

## Which Algorithms It's Often Used With

Radix Sort is frequently combined with:

- **Counting Sort:**
  - Radix Sort uses Counting Sort as its core subroutine for sorting by each digit
  - This combination achieves O(d × (n + k)) time complexity

- **Other Distribution-Based Sorts:**
  - **Bucket Sort** - compared for different data characteristics and distribution strategies
  - **Pigeonhole Sort** - another integer sorting algorithm

- **Comparison-Based Sorts (for comparison):**
  - **Quick Sort, Merge Sort** - to demonstrate when non-comparison-based sorting outperforms comparison-based sorting
  - Shows advantages for integer data with limited digit count

## Key Code (Only Important Parts)

Here's a concise implementation highlighting the essential logic:

```python
def radix_sort(arr):
    """Sort array using radix sort (LSD)."""
    if not arr:
        return arr
    
    # Find maximum number to determine number of digits
    max_val = max(arr)
    
    # Do counting sort for every digit
    exp = 1  # Start with least significant digit
    while max_val // exp > 0:
        arr = counting_sort_by_digit(arr, exp)
        exp *= 10  # Move to next digit
    
    return arr

def counting_sort_by_digit(arr, exp):
    """Sort array by specific digit using counting sort."""
    n = len(arr)
    output = [0] * n
    count = [0] * 10  # For digits 0-9
    
    # Count occurrences of current digit
    for i in range(n):
        digit = (arr[i] // exp) % 10
        count[digit] += 1
    
    # Cumulative count
    for i in range(1, 10):
        count[i] += count[i - 1]
    
    # Build output array (stable)
    for i in range(n - 1, -1, -1):
        digit = (arr[i] // exp) % 10
        output[count[digit] - 1] = arr[i]
        count[digit] -= 1
    
    return output
```

**Key Points:**
- Process digits from least significant to most significant (LSD Radix Sort)
- Use Counting Sort as subroutine for each digit position
- Extract digit using: `(num // exp) % 10`
- Process all digits: `exp = 1, 10, 100, ...` until `max_val // exp == 0`
- Stable sorting algorithm

## Common Application Errors

1. **Incorrect Digit Extraction:**
   - **Error:** Wrong formula for extracting the current digit: `(num // exp) % 10`
   - **Impact:** Elements sorted by wrong digit, resulting in incorrect final order
   - **Solution:** Use `(arr[i] // exp) % 10` to extract the digit at position exp

2. **Wrong Exponent Update:**
   - **Error:** Not updating exp correctly (should multiply by radix, typically 10)
   - **Impact:** Stuck in infinite loop or missing digit positions
   - **Solution:** Always multiply exp by the radix: `exp *= 10` for decimal

3. **Not Handling All Digits:**
   - **Error:** Stopping too early or processing wrong number of digits
   - **Impact:** Numbers not fully sorted, especially those with more digits
   - **Solution:** Continue until `max_val // exp == 0` to process all digits

4. **Breaking Stability:**
   - **Error:** Processing array in forward order in Counting Sort subroutine
   - **Impact:** Equal elements may be reordered, breaking stability
   - **Solution:** Process from end to beginning in Counting Sort: `for i in range(n - 1, -1, -1)`

5. **Not Handling Negative Numbers:**
   - **Error:** Assuming all numbers are non-negative
   - **Impact:** Negative numbers sorted incorrectly
   - **Solution:** Separate negatives and positives, sort separately, then combine (negatives reversed)

## Recommended Literature

1. **"Introduction to Algorithms" (CLRS)** - Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein
   - Comprehensive analysis of Radix Sort including correctness proofs, complexity analysis, and comparison with other integer sorting algorithms

2. **"Algorithm Design Manual"** - Steven S. Skiena
   - Practical discussion of Radix Sort, including when its linear-time characteristics make it preferable

3. **"Algorithms"** - Robert Sedgewick, Kevin Wayne
   - Clear explanations with visualizations showing how Radix Sort processes digits incrementally

4. **"The Art of Computer Programming, Volume 3: Sorting and Searching"** - Donald Knuth
   - Authoritative reference on Radix Sort, including analysis of LSD vs. MSD variants and string sorting applications

5. **"Data Structures and Algorithms in Python"** - Michael T. Goodrich, Roberto Tamassia, Michael H. Goldwasser
   - Clear explanation of Radix Sort with Python-specific implementations and discussion of when to use it vs. other sorting algorithms
