# Insertion Sort

## Convergence Speed and Complexity

- Time: O(n²) comparisons/shifts in average and worst cases; O(n) best case
  when already (or nearly) sorted. Adaptive due to early termination of the
  inner loop.
- Space: O(1) auxiliary (in-place).
- Stable: equal keys keep original order.
- Convergence: After i iterations, the first i elements are sorted; each
  step inserts one element into the sorted prefix.

## Where Used in Real Frameworks and Software

- **Hybrid sorts**: TimSort (Python/Java) and introsort use insertion sort
  for tiny partitions (e.g., size < 32) because it beats n log n sorts on
  very small arrays.
- **Partially sorted inputs**: practical when data is almost sorted.
- **Low-overhead paths**: tiny datasets in embedded or hot loops where branch
  predictability and cache friendliness matter.

## Conceptual Relatives

- **Binary Insertion Sort**: uses binary search for position (same O(n²)
  shifts; fewer comparisons).
- **Shell Sort**: generalizes by inserting with gaps to reduce total shifts.
- **Insertion into linked lists**: analogous operation on a different
  structure.

## Often Used With

- **Merge/Quick hybrids**: cleanup small partitions after divide-and-conquer.
- **TimSort** runs: extend naturally from already-sorted runs.
- **Deduping/aggregation**: stable insertion maintains order while placing
  new items.

## Key Code (only important parts)

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

**Notes**
- Inner loop exits early when the correct spot is found (adaptive).
- Stable because only shifts of larger elements occur to the right.
- Cache-friendly: operates on contiguous memory with simple passes.

## Common Application Errors

- **Off-by-one in while loop**: forgetting `j >= 0` check → IndexError.
- **Missing key save**: overwriting `arr[i]` before storing it.
- **Binary-search variant misuse**: binary search finds position but shifts
  still cost O(n); forgetting that leads to wrong expectations.
- **Using for large random datasets**: quadratic cost dominates; prefer
  O(n log n) sorts.

## Recommended Literature

- CLRS “Introduction to Algorithms” — loop invariants for correctness proof.
- Sedgewick & Wayne “Algorithms” — stable/adaptive characteristics.
- Python’s TimSort notes (PEP 450 references) — real-world hybrid use.
- Knuth, TAOCP Vol. 3 — historical notes on insertion-based methods.

