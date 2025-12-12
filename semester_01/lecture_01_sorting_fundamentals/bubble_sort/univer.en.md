# Bubble Sort

## Convergence Speed and Complexity

- Time: O(n²) comparisons/swaps in average and worst cases; O(n) best case
  with early-exit when the array is already sorted.
- Space: O(1) auxiliary space (in-place).
- Stability: Stable when implemented with adjacent swaps.
- Convergence: Each pass places the next-largest element at its final
  position; after k passes, the k largest elements are fixed.

## Where It Is Used in Real Frameworks and Software

Rare in production due to poor asymptotic performance, but appears in:
- **Educational tooling/visualizers** (e.g., CS teaching platforms).
- **Sanity checks** for very small collections inside scripts/tests.
- **Nearly sorted micro-batches** where early-exit makes it effectively O(n).
- **Debugging utilities** when simplicity and readability trump speed.

## Conceptual Relatives

- **Adjacent transposition sorting**: repeatedly fixes local inversions.
- **Insertion Sort**: also quadratic but adaptive; often preferred for small
  inputs.
- **Shaker/Cocktail Sort**: bidirectional variant reducing passes slightly.
- **Odd–Even Sort**: parallel-friendly variant for specific hardware models.

## Often Used With

- **Teaching comparisons** vs. Insertion, Selection, Merge, Quick.
- **Hybrid pipelines**: occasionally as a cleanup pass after another sort for
  very small tail segments (though Insertion is more common).
- **Algorithm demos**: baseline to show why n² sorts are superseded.

## Key Code (only important parts)

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:  # converged early
            break
    return arr
```

**Highlights**
- Early-exit cuts best case to O(n).
- Inner loop shrinks by `i` because last `i` elements are already placed.
- Only adjacent comparisons preserve stability.

## Common Application Errors

- **Forgetting early-exit**: wastes passes on sorted inputs.
- **Wrong bounds**: off-by-one in `n - i - 1` causes IndexError or misses
  comparisons.
- **Unstable swaps**: replacing adjacent swap with distant swap breaks
  stability.
- **Using on large datasets**: quadratic cost dominates; prefer O(n log n)
  algorithms (TimSort, Merge, Quick).
- **No guard for already-sorted runs**: use `swapped` to short-circuit.

## Recommended Literature

- CLRS “Introduction to Algorithms” — Section on elementary sorting.
- Sedgewick & Wayne “Algorithms” — visual intuition and comparisons.
- Knuth “The Art of Computer Programming”, Vol. 3 — historical context and
  analysis of simple sorts.
- Online: Visualgo, CS50 visualizers for step-by-step animations.

