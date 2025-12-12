# Bubble Sort

## Principle of Operation (very simple)

- Walk through the list and compare neighbors.
- If a pair is out of order, swap them.
- After each full pass, the largest item has “bubbled” to the end.
- Repeat passes until no swaps are needed.
- Like shaking a row of numbers so big ones drift to the right.

## Algorithm Complexity (O-notation)

- Time: O(n²) in average and worst cases; O(n) best case if you stop early
  when no swaps happen.
- Space: O(1) extra memory (in-place).

## Where It Is Used in Practice

- Teaching and demos of sorting basics.
- Tiny or nearly sorted lists when simplicity matters more than speed.
- Debugging or visual animations to explain sorting ideas.

## What It Can Be Compared To

- Bubbles rising in water: big bubbles float up each pass.
- Lining up by height: repeatedly swap adjacent students until order is
  correct.

## Minimal Code Example (only important parts)

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:  # already sorted, stop early
            break
    return arr
```

## Common Mistakes

- Forgetting the early-stop check and wasting passes.
- Off-by-one errors in the inner loop bounds.
- Swapping incorrectly or forgetting to swap.
- Expecting it to be fast on large datasets (it is not).

## Recommended Literature

- “Grokking Algorithms” — Aditya Bhargava (visual, beginner-friendly).
- “Algorithms” — Sedgewick & Wayne (clear illustrations).
- CLRS “Introduction to Algorithms” — formal analysis and proofs.

