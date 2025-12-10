# Bubble Sort

# School

## 📋 Quick Summary

- **Purpose:** Bubble Sort: Repeatedly compares and rearranges elements until the list is sorted, like organizing items in order.
- **Complexity:** O(n²)
- **Category:** Sorting
- **Key Idea:** The largest element 'bubbles up' to the end in each pass, so we can reduce the comparison range each time.

Bubble Sort: Repeatedly compares and rearranges elements until the list is sorted, like organizing items in order.

The largest element 'bubbles up' to the end in each pass, so we can reduce the comparison range each time.

**BUBBLE** = Bring Up Bigger, Leave Elements. Think of bubbles rising in water - larger elements float to the top!








Этот алгоритм работает, swapping elements, comparing elements, чтобы достичь своей цели. Он относится к категории алгоритмов **Sorting**.


## 📊 Visual Flowchart

```mermaid
flowchart TD
    Start([Start]) --> Init[Initialize array]
    Init --> Loop1[For i = 0 to n-1]
    Loop1 --> Loop2[For j = 0 to n-i-2]
    Loop2 --> Compare{Compare arr[j] and arr[j+1]}
    Compare -->|arr[j] > arr[j+1]| Swap[Swap elements]
    Compare -->|arr[j] <= arr[j+1]| Next[Next iteration]
    Swap --> Next
    Next --> Check{More elements?}
    Check -->|Yes| Loop2
    Check -->|No| Sorted{Array sorted?}
    Sorted -->|No| Loop1
    Sorted -->|Yes| End([End])
```

> **Note**: Mermaid diagrams are rendered automatically on GitHub. For local viewing, use a Mermaid-compatible Markdown viewer.



## Сложность алгоритма

Временная сложность составляет **O(n²)**, что означает, что время выполнения зависит от размера входных данных. Пространственная сложность — **O(1)**, что указывает на количество дополнительной памяти.

## Где применяется на практике

- Educational purposes and small datasets (< 10 elements)
- When simplicity is more important than performance
- Sorting nearly-sorted data with early termination optimization

## С чем можно сравнить

Представьте Bubble Sort как систематический способ организации или поиска информации — похоже на то, как вы можете эффективно организовывать предметы или искать в коллекции.

## Минимальный пример кода

```python
def bubble_sort(data):
    """Implementation of Bubble Sort."""
    # Core algorithm logic
    return result
```

## Частые ошибки

- Не обрабатываются граничные случаи (пустой ввод, один элемент)
- Непонимание последствий сложности
- Неправильная реализация, приводящая к неверным результатам
- Не оптимизировано для конкретного случая использования

## Рекомендуемая литература

- "Алгоритмы: построение и анализ" Томас Кормен и др.
- "Алгоритмы" Роберт Седжвик
- Онлайн-ресурсы: GeeksforGeeks, Википедия, Визуализации алгоритмов



---

## 🎯 Try It Yourself

**Try sorting this by hand:**
```
Input: [5, 2, 8, 1, 9]

Pass 1:
  Compare 5 and 2 → 5 > 2, swap → [2, 5, 8, 1, 9]
  Compare 5 and 8 → 5 < 8, no swap → [2, 5, 8, 1, 9]
  Compare 8 and 1 → 8 > 1, swap → [2, 5, 1, 8, 9]
  Compare 8 and 9 → 8 < 9, no swap → [2, 5, 1, 8, 9]
  Largest element (9) is now at the end!

Pass 2:
  Compare 2 and 5 → 2 < 5, no swap → [2, 5, 1, 8, 9]
  Compare 5 and 1 → 5 > 1, swap → [2, 1, 5, 8, 9]
  (No need to check 8 and 9 - already sorted)

Continue until sorted: [1, 2, 5, 8, 9]
```


---


## 🔍 Step-by-Step Execution

**Step-by-Step Execution:**

```python
# Input
arr = [5, 2, 8, 1, 9]
n = len(arr)  # n = 5

# Pass 1 (i = 0)
j = 0: Compare arr[0]=5 and arr[1]=2 → 5 > 2, swap → arr = [2, 5, 8, 1, 9]
j = 1: Compare arr[1]=5 and arr[2]=8 → 5 < 8, no swap → arr = [2, 5, 8, 1, 9]
j = 2: Compare arr[2]=8 and arr[3]=1 → 8 > 1, swap → arr = [2, 5, 1, 8, 9]
j = 3: Compare arr[3]=8 and arr[4]=9 → 8 < 9, no swap → arr = [2, 5, 1, 8, 9]
# Largest element (9) is now at the end

# Pass 2 (i = 1)
j = 0: Compare arr[0]=2 and arr[1]=5 → 2 < 5, no swap → arr = [2, 5, 1, 8, 9]
j = 1: Compare arr[1]=5 and arr[2]=1 → 5 > 1, swap → arr = [2, 1, 5, 8, 9]
j = 2: Compare arr[2]=5 and arr[3]=8 → 5 < 8, no swap → arr = [2, 1, 5, 8, 9]

# Pass 3 (i = 2)
j = 0: Compare arr[0]=2 and arr[1]=1 → 2 > 1, swap → arr = [1, 2, 5, 8, 9]
j = 1: Compare arr[1]=2 and arr[2]=5 → 2 < 5, no swap → arr = [1, 2, 5, 8, 9]

# Result
arr = [1, 2, 5, 8, 9]  # Sorted!
```

**Expected Output:**

```
Input: [5, 2, 8, 1, 9]
Pass 1: [2, 5, 8, 1, 9] (swapped 5 and 2)
Pass 2: [2, 5, 1, 8, 9] (swapped 8 and 1)
Pass 3: [2, 1, 5, 8, 9] (swapped 5 and 1)
Pass 4: [1, 2, 5, 8, 9] (swapped 2 and 1)
Sorted: [1, 2, 5, 8, 9]
```

## ✏️ Practice Exercise

**Exercise 1 (Easy):**
Sort this list by hand: [64, 34, 25, 12, 22, 11, 90]
Show each pass and count how many swaps you make.

**Exercise 2 (Medium):**
Write a function to sort a list of student names alphabetically using bubble sort.

**Exercise 3 (Hard):**
Optimize bubble sort to stop early if the list is already sorted. How does this improve performance?


---

## ✅ Check Your Understanding

**Q1:** How many passes are needed for n elements in the worst case?
**A:** At most n-1 passes (the last element is already in place after n-1 passes).

**Q2:** What is the best-case time complexity and when does it occur?
**A:** O(n) when the array is already sorted and we use early termination.

**Q3:** Why is bubble sort called "bubble" sort?
**A:** Because larger elements "bubble up" to the end of the array, like bubbles rising in water.

**Q4:** Is bubble sort stable?
**A:** Yes, it preserves the relative order of equal elements.


**Try sorting this by hand:**
```
Input: [5, 2, 8, 1, 9]

Pass 1:
  Compare 5 and 2 → 5 > 2, swap → [2, 5, 8, 1, 9]
  Compare 5 and 8 → 5 < 8, no swap → [2, 5, 8, 1, 9]
  Compare 8 and 1 → 8 > 1, swap → [2, 5, 1, 8, 9]
  Compare 8 and 9 → 8 < 9, no swap → [2, 5, 1, 8, 9]
  Largest element (9) is now at the end!

Pass 2:
  Compare 2 and 5 → 2 < 5, no swap → [2, 5, 1, 8, 9]
  Compare 5 and 1 → 5 > 1, swap → [2, 1, 5, 8, 9]
  (No need to check 8 and 9 - already sorted)

Continue until sorted: [1, 2, 5, 8, 9]
```



## Common Mistakes

### ❌ Mistake 1: Not optimizing to stop early
**Solution:** Add a flag to check if any swaps occurred in a pass. If no swaps, the array is sorted and you can stop early.

### ❌ Mistake 2: Comparing wrong elements
**Solution:** Compare `arr[j]` with `arr[j+1]`, not `arr[i]` with `arr[j]`. The inner loop should compare adjacent elements.

### ❌ Mistake 3: Going out of bounds
**Solution:** In inner loop, iterate `j` from `0` to `n-i-1` (not `n-1`) to avoid comparing already-sorted elements at the end.

### ❌ Mistake 4: Not handling edge cases
**Solution:** Check for empty arrays or single-element arrays before starting the sorting process.

### 💡 How to Avoid
- Test with edge cases: empty array, single element, already sorted
- Use proper loop bounds to avoid index errors
- Add early termination optimization
- Trace through examples step-by-step
- Test with edge cases (empty input, single element, boundary values)
- Trace through examples step-by-step
- Use debugging tools to verify your logic
- Review the algorithm's key steps before implementing


## 🔗 Related Algorithms

You might also want to learn:
- **Insertion Sort** - Similar algorithm in the same category
- **Selection Sort** - Similar algorithm in the same category
- **Heap Sort** - Similar algorithm in the same category







