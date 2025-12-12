# Selection Sort

## Principle of Operation (very simple)

- Split the list into a sorted part (left) and unsorted part (right).
- Repeatedly find the smallest element in the unsorted part.
- Swap it with the first element of the unsorted part (growing the sorted
  part by one).
- Repeat until all elements are placed.
- Like picking the smallest card from the table and placing it next in your
  sorted hand.

## Algorithm Complexity (O-notation)

- Time: O(n²) comparisons in all cases (same work even if already sorted).
- Space: O(1) extra space (in-place).
- Stability: Not stable in the basic form (swaps can reorder equals).

## Where It Is Used in Practice

- Teaching basic sorting ideas.
- Very small datasets where simplicity matters more than speed.
- Cases where minimal extra memory is required.

## What It Can Be Compared To

- Repeatedly picking the smallest stone from a pile and lining them up.
- Sorting playing cards by always selecting the smallest remaining card.

## Minimal Code Example (only important parts)

```python
def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr
```

## Common Mistakes

- Forgetting to reset `min_idx` each outer loop.
- Off-by-one errors in the inner loop range.
- Assuming it is stable (it is not, unless you modify it to shift instead of
  swap).
- Expecting good performance on large datasets (it is always quadratic).

## Recommended Literature

- “Grokking Algorithms” — Aditya Bhargava (gentle intro with visuals).
- “Algorithms” — Sedgewick & Wayne (good for comparisons of simple sorts).
- CLRS “Introduction to Algorithms” — correctness and complexity proofs.

