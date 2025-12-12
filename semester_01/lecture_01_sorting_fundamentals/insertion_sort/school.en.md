# Insertion Sort

## Principle of Operation (very simple)

- Imagine sorting cards in your hand: take the next card and insert it into
  the correct spot among the cards you already sorted.
- Start with the first element as “sorted”.
- For each next element, shift bigger elements one step to the right until
  you find the spot, then insert.
- Repeat until all elements are placed.

## Algorithm Complexity (O-notation)

- Time: O(n²) in average/worst cases; O(n) when the list is already or almost
  sorted (adaptive).
- Space: O(1) extra space (in-place).
- Stable: equal elements keep their original order.

## Where It Is Used in Practice

- Very small arrays or nearly sorted data.
- Final cleanup step in hybrid sorts (e.g., TimSort, introsort) for tiny
  partitions.
- Educational tools to teach sorting and stability.

## What It Can Be Compared To

- Sorting playing cards in your hand.
- Lining students by height by inserting each newcomer at the right spot.

## Minimal Code Example (only important parts)

```python
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]  # shift right
            j -= 1
        arr[j + 1] = key  # insert
    return arr
```

## Common Mistakes

- Off-by-one errors when shifting and inserting.
- Forgetting the `j >= 0` bound in the while loop (IndexError).
- Copying the key too late or too early, overwriting data.
- Expecting it to be fast on large, unsorted inputs (it is quadratic).

## Recommended Literature

- “Grokking Algorithms” — Aditya Bhargava (great card-sorting analogy).
- “Algorithms” — Sedgewick & Wayne (stability and adaptive behavior).
- CLRS “Introduction to Algorithms” — proofs and loop invariants.

