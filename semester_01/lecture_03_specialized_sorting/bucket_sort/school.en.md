# Bucket Sort

## Principle of Operation

Bucket Sort is a sorting algorithm that works by dividing the array into several "buckets" (like separate containers), putting each number into the right bucket based on its value, sorting each bucket separately, and then putting all the buckets back together in order.

Think of it like organizing toys by size: you have different boxes (buckets) for small, medium, and large toys. You put each toy in the right box, sort the toys within each box, then combine all boxes in order.

### Simple Example

Imagine sorting numbers: [0.42, 0.32, 0.33, 0.52, 0.37, 0.47, 0.51]

1. **Create Buckets:** Make 10 buckets (0.0-0.1, 0.1-0.2, ..., 0.9-1.0)
2. **Distribute:** Put each number in the right bucket
   - 0.42 → bucket 4
   - 0.32 → bucket 3
   - 0.33 → bucket 3
   - 0.52 → bucket 5
   - etc.
3. **Sort Buckets:** Sort numbers within each bucket
   - Bucket 3: [0.32, 0.33, 0.37]
   - Bucket 4: [0.42, 0.47]
   - Bucket 5: [0.51, 0.52]
4. **Combine:** Put all buckets together → [0.32, 0.33, 0.37, 0.42, 0.47, 0.51, 0.52]

The key is that numbers are spread evenly across buckets, so each bucket is small and easy to sort!

## Algorithm Complexity in O-notation

- **Best Case:** O(n) - when numbers are spread evenly and each bucket has very few items (almost like having one item per bucket).
- **Average Case:** O(n + k) - usually very fast when numbers are spread evenly across buckets.
- **Worst Case:** O(n²) - when all numbers end up in the same bucket (like putting all toys in one box), then you have to sort a big bucket which is slow.

**Space Complexity:** O(n + k) - you need space for the original numbers (n) and for the buckets (k). Each bucket can hold multiple numbers.

## Where It Is Used in Practice

Bucket Sort is used in special situations:

- **Real Applications:**
  - **Sorting grades or scores** that are usually spread evenly (like test scores 0-100)
  - **Organizing data by ranges** (like sorting people by age groups)
  - **Data analysis** where you want to see how data is distributed
  - **Sorting decimal numbers** that are evenly spread (like 0.0 to 1.0)

- **When It Works Best:**
  - When you know the numbers will be spread evenly
  - When numbers are in a known range (like 0 to 100)
  - When you have many numbers but they fall into a limited number of ranges

- **Why It's Special:**
  - Can be very fast (almost O(n)) when data is spread evenly
  - Naturally creates groups while sorting
  - Useful for organizing data into categories

## What Can the Algorithm Be Compared To

Bucket Sort can be compared to:

- **Organizing by Categories:** Like sorting library books - you put fiction in one section, non-fiction in another, then organize each section separately.

- **Mail Sorting:** Like a post office that sorts mail by zip code into different bins, then sorts each bin separately.

- **Grouping by Size:** Like organizing clothes - you put small, medium, and large in different piles, then organize each pile.

## Minimal Code Example (Only Important Parts)

Here's a simple Python implementation:

```python
def bucket_sort(arr):
    """Sort array using bucket sort."""
    if not arr:
        return arr
    
    # Find the range of numbers
    min_val, max_val = min(arr), max(arr)
    n = len(arr)
    
    # Create buckets
    buckets = [[] for _ in range(n)]
    
    # Put each number in the right bucket
    for num in arr:
        # Calculate which bucket this number belongs to
        bucket_idx = int(n * (num - min_val) / (max_val - min_val))
        if bucket_idx >= n:
            bucket_idx = n - 1
        buckets[bucket_idx].append(num)
    
    # Sort each bucket
    for bucket in buckets:
        bucket.sort()  # Use any sorting method
    
    # Put all buckets together
    result = []
    for bucket in buckets:
        result.extend(bucket)
    
    return result

# Example usage
numbers = [0.42, 0.32, 0.33, 0.52, 0.37, 0.47, 0.51]
sorted_numbers = bucket_sort(numbers)
print(sorted_numbers)  # [0.32, 0.33, 0.37, 0.42, 0.47, 0.51, 0.52]
```

**Key Points:**
- Create buckets (usually one bucket per item, or a reasonable number)
- Put each number in the right bucket based on its value
- Sort each bucket separately (using a simple sort like Insertion Sort)
- Combine all buckets in order
- Works best when numbers are spread evenly!

## Common Mistakes

1. **Wrong Bucket Calculation:**
   - **Mistake:** Calculating which bucket a number belongs to incorrectly
   - **Why it's bad:** Numbers go into wrong buckets, sorting doesn't work
   - **Fix:** Use the formula: `bucket_idx = int(n * (num - min_val) / (max_val - min_val))`

2. **Not Handling Edge Cases:**
   - **Mistake:** Not checking what happens when all numbers are the same
   - **Why it's bad:** Can cause errors when dividing by zero
   - **Fix:** Check if `min_val == max_val` and return early

3. **Forgetting to Sort Buckets:**
   - **Mistake:** Putting numbers in buckets but not sorting each bucket
   - **Why it's bad:** Numbers within each bucket stay unsorted
   - **Fix:** Always sort each bucket before combining!

4. **Using Too Few or Too Many Buckets:**
   - **Mistake:** Creating too few buckets (all numbers in one bucket) or too many (empty buckets)
   - **Why it's bad:** Too few → slow sorting. Too many → wasted space
   - **Fix:** Usually use n buckets (one per item) for best results

5. **Not Combining Buckets Correctly:**
   - **Mistake:** Combining buckets in wrong order or missing some
   - **Why it's bad:** Final result is not sorted correctly
   - **Fix:** Combine buckets in order from first to last

## Recommended Literature

1. **"Grokking Algorithms" by Aditya Bhargava**
   - Excellent beginner-friendly book with simple explanations of Bucket Sort

2. **"Introduction to Algorithms" (CLRS)**
   - Comprehensive textbook covering Bucket Sort with detailed analysis

3. **"Algorithms Unlocked" by Thomas H. Cormen**
   - Accessible introduction that explains when Bucket Sort is useful

4. **Online Resources:**
   - Khan Academy's computer science courses
   - Visualgo.net for interactive Bucket Sort visualizations
   - GeeksforGeeks for code examples and step-by-step explanations
