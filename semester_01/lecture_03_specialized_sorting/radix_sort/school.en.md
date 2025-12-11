# Radix Sort

## Principle of Operation

Radix Sort is a clever sorting algorithm that sorts numbers by looking at them digit by digit, starting from the rightmost digit (ones place) and moving left. It's like sorting a stack of papers by first organizing them by the last digit, then by the second-to-last digit, and so on, until they're completely sorted.

Think of it like sorting phone numbers: you first sort by the last digit, then by the second-to-last digit, continuing until you've sorted by all digits.

### Simple Example

Imagine sorting numbers: [170, 45, 75, 90, 2, 802, 24, 66]

1. **Sort by 1s place (rightmost digit):**
   - Group by last digit: 170(0), 90(0), 2(2), 802(2), 24(4), 45(5), 75(5), 66(6)
   - Result: [170, 90, 2, 802, 24, 45, 75, 66]

2. **Sort by 10s place (middle digit):**
   - Group by middle digit: 2(0), 802(0), 24(2), 45(4), 66(6), 170(7), 75(7), 90(9)
   - Result: [2, 802, 24, 45, 66, 170, 75, 90]

3. **Sort by 100s place (leftmost digit):**
   - Group by first digit: 2(0), 24(0), 45(0), 66(0), 75(0), 90(0), 170(1), 802(8)
   - Final: [2, 24, 45, 66, 75, 90, 170, 802] - sorted!

The key is sorting by each digit position, one at a time, from right to left!

## Algorithm Complexity in O-notation

- **Best Case:** O(d × n) - where d is the number of digits. For numbers with few digits, this is very fast!
- **Average Case:** O(d × n) - always takes the same time, doesn't matter how numbers are arranged.
- **Worst Case:** O(d × n) - same as best case! Very predictable performance.

**Space Complexity:** O(n) - needs space to store the numbers while sorting. Uses a helper method (like Counting Sort) that needs a bit more space, but overall it's efficient!

## Where It Is Used in Practice

Radix Sort is used in special situations:

- **Real Applications:**
  - **Sorting phone numbers** - perfect because they have the same number of digits
  - **Sorting ID numbers** like social security numbers or student IDs
  - **Sorting dates** when written as numbers (like 20231225 for December 25, 2023)
  - **Sorting IP addresses** (when treated as numbers)

- **When It Works Best:**
  - When numbers have the same or similar number of digits
  - When you're sorting many numbers that aren't too large
  - When numbers are integers (whole numbers)

- **Why It's Special:**
  - Can be faster than other sorting methods for certain types of numbers
  - Always takes the same amount of time (predictable)
  - Sorts without comparing whole numbers - just looks at digits!

## What Can the Algorithm Be Compared To

Radix Sort can be compared to:

- **Sorting Cards by Suit Then Rank:** Like organizing playing cards - first by suit, then by number within each suit.

- **Organizing Files by Date:** Like sorting files - first by year, then by month, then by day.

- **Multi-Level Sorting:** Like organizing a library - first by section, then by author, then by title.

## Minimal Code Example (Only Important Parts)

Here's a simple explanation of how it works:

```python
def radix_sort(arr):
    """Sort array using radix sort."""
    if not arr:
        return arr
    
    # Find the maximum number to know how many digits
    max_val = max(arr)
    
    # Sort by each digit, starting from rightmost
    exp = 1  # Start with ones place (1, 10, 100, ...)
    while max_val // exp > 0:
        arr = sort_by_digit(arr, exp)
        exp *= 10  # Move to next digit (tens, hundreds, etc.)
    
    return arr

def sort_by_digit(arr, exp):
    """Sort array by a specific digit position."""
    # Use counting sort to sort by current digit
    # (This is the helper method that does the actual sorting)
    # ... counting sort implementation ...
    return sorted_arr
```

**Key Points:**
- Sort by each digit position, one at a time
- Start with the rightmost digit (ones place)
- Move left through tens, hundreds, thousands, etc.
- Use a helper method (like Counting Sort) to sort by each digit
- Works great for numbers with the same number of digits!

## Common Mistakes

1. **Wrong Digit Extraction:**
   - **Mistake:** Not correctly getting the digit at each position
   - **Why it's bad:** Numbers sorted by wrong digits, final order is wrong
   - **Fix:** Use `(num // exp) % 10` to get the digit at position exp

2. **Not Processing All Digits:**
   - **Mistake:** Stopping too early or missing some digit positions
   - **Why it's bad:** Numbers not fully sorted
   - **Fix:** Continue until `max_val // exp == 0` to process all digits

3. **Wrong Exponent Update:**
   - **Mistake:** Not moving to the next digit correctly
   - **Why it's bad:** Stuck on same digit or skipping digits
   - **Fix:** Always multiply exp by 10: `exp *= 10`

4. **Using on Non-Integers:**
   - **Mistake:** Trying to use Radix Sort on decimal numbers or strings without preparation
   - **Why it's bad:** Algorithm is designed for integers
   - **Fix:** Only use on integers, or convert other types appropriately

5. **Not Handling Different Length Numbers:**
   - **Mistake:** Assuming all numbers have the same number of digits
   - **Why it's bad:** Shorter numbers might be sorted incorrectly
   - **Fix:** Algorithm handles this automatically (shorter numbers have leading zeros)

## Recommended Literature

1. **"Grokking Algorithms" by Aditya Bhargava**
   - Excellent beginner-friendly book that explains Radix Sort with simple examples

2. **"Introduction to Algorithms" (CLRS)**
   - Comprehensive textbook covering Radix Sort with detailed explanations

3. **"Algorithms Unlocked" by Thomas H. Cormen**
   - Accessible introduction that explains when Radix Sort is useful

4. **Online Resources:**
   - Khan Academy's computer science courses
   - Visualgo.net for interactive Radix Sort visualizations
   - GeeksforGeeks for code examples and step-by-step walkthroughs
