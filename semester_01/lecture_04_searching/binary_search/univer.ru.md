# Binary Search

# Univer

## 📋 Quick Summary

- **Purpose:** Binary Search: Always check the middle element - if it's not what we want, eliminate half the search space.
- **Complexity:** O(log n)
- **Category:** Searching
- **Key Idea:** Always check the middle element - if it's not what we want, eliminate half the search space.

Binary Search: Always check the middle element - if it's not what we want, eliminate half the search space.

Always check the middle element - if it's not what we want, eliminate half the search space.

**BINARY** = Begin In Middle, Always Narrow Your search. Like finding a word in a dictionary - always check the middle!








Этот алгоритм относится к категории **Searching** и использует систематическую обработку данных для достижения своих целей.


## 📊 Visual Flowchart

```mermaid
flowchart TD
    Start([Start]) --> Init[Set left=0, right=n-1]
    Init --> Loop{left <= right?}
    Loop -->|No| NotFound[Return -1]
    Loop -->|Yes| Mid[Calculate mid]
    Mid --> Compare{Compare arr[mid] with target}
    Compare -->|Equal| Found[Return mid]
    Compare -->|arr[mid] > target| Left[Set right = mid-1]
    Compare -->|arr[mid] < target| Right[Set left = mid+1]
    Left --> Loop
    Right --> Loop
    Found --> End([End])
    NotFound --> End
```

> **Note**: Mermaid diagrams are rendered automatically on GitHub. For local viewing, use a Mermaid-compatible Markdown viewer.



## Анализ сложности

**Временная сложность:** O(log n)
- Производительность алгоритма масштабируется согласно этому классу сложности
- Лучший, средний и худший случаи могут различаться в зависимости от характеристик входных данных

**Пространственная сложность:** O(1)
- Указывает на количество дополнительной памяти, необходимой во время выполнения

**Ключевые структуры данных:** Стандартные структуры данных

## Применение в реальных системах

Binary Search используется в:
- Database query optimization
- Search engines (binary search in sorted indices)
- Autocomplete and suggestion systems
- Lookup tables and caches

## Концептуальные сходства

Этот алгоритм имеет концептуальное сходство с другими алгоритмами в категории Searching, следуя аналогичным паттернам проектирования и стратегиям оптимизации.

## Связанные алгоритмы

Binary Search часто используется в сочетании с:
- Дополнительными алгоритмами для предобработки или постобработки
- Структурами данных, оптимизирующими его производительность
- Другими алгоритмами того же класса сложности

## Ключевые детали реализации

```python
def binary_search(arr, target):
    """Implementation."""
    left, right = (0, len(arr) - 1)
    return result
```

## Распространённые ошибки применения

- Неправильная обработка граничных случаев (пустой ввод, один элемент, граничные условия)
- Непонимание последствий сложности в крупномасштабных системах
- Субоптимальная реализация, приводящая к деградации производительности
- Неверные предположения о характеристиках входных данных
- Не рассмотрение альтернативных алгоритмов для конкретных случаев использования

## Рекомендуемая литература

- "Алгоритмы: построение и анализ" (CLRS) - Комплексный анализ алгоритмов
- "Руководство по проектированию алгоритмов" Стивена Скиены
- "Алгоритмы" Седжвика и Уэйна
- Научные статьи по оптимизации и анализу алгоритмов
- Документация фреймворков и руководства по реализации



---

## 🎯 Try It Yourself

**Try finding 7 in this sorted array:**
```
Array: [1, 3, 5, 7, 9, 11, 13]
Target: 7

Step 1: Check middle element (index 3, value 5)
  5 < 7, so search right half: [7, 9, 11, 13]

Step 2: Check middle of right half (index 5, value 9)
  9 > 7, so search left half: [7]

Step 3: Found! Element 7 is at index 3
```


---


## 🔍 Step-by-Step Execution

**Step-by-Step Execution:**

```python
# Input
arr = [1, 3, 5, 7, 9, 11, 13]
target = 7
left = 0
right = 6

# Iteration 1
mid = (0 + 6) // 2 = 3
arr[mid] = arr[3] = 7
7 == 7? Yes! Found at index 3

# Result
return 3
```

**Variable States:**
```
Iteration | left | right | mid | arr[mid] | Comparison | Action
----------|------|-------|-----|----------|------------|--------
    1     |  0   |   6   |  3  |    7     | 7 == 7     | Found!
```

**Expected Output:**

```
Searching for 7 in [1, 3, 5, 7, 9, 11, 13]
Checking index 3: value = 7
Found at index 3!
```

## ✏️ Practice Exercise

**Exercise 1 (Easy):**
Find the number 42 in this sorted array: [10, 20, 30, 40, 50, 60, 70]
Show each step of your search.

**Exercise 2 (Medium):**
Implement binary search to find the first occurrence of a target value in a sorted array with duplicates.

**Exercise 3 (Hard):**
What happens if you try binary search on an unsorted array? Why doesn't it work?


---

## ✅ Check Your Understanding

**Q1:** Why must the array be sorted for binary search?
**A:** Because we eliminate half the search space based on comparison - this only works if elements are ordered.

**Q2:** What is the time complexity of binary search?
**A:** O(log n) - we halve the search space each time.

**Q3:** What is the space complexity of iterative binary search?
**A:** O(1) - we only use a few variables, no extra space needed.

**Q4:** When would you use binary search instead of linear search?
**A:** When the array is sorted and you need to search multiple times - the O(log n) vs O(n) advantage is significant.


**Try finding 7 in this sorted array:**
```
Array: [1, 3, 5, 7, 9, 11, 13]
Target: 7

Step 1: Check middle element (index 3, value 5)
  5 < 7, so search right half: [7, 9, 11, 13]

Step 2: Check middle of right half (index 5, value 9)
  9 > 7, so search left half: [7]

Step 3: Found! Element 7 is at index 3
```


**Exercise 1 (Easy):**
Find the number 42 in this sorted array: [10, 20, 30, 40, 50, 60, 70]
Show each step of your search.

**Exercise 2 (Medium):**
Implement binary search to find the first occurrence of a target value in a sorted array with duplicates.

**Exercise 3 (Hard):**
What happens if you try binary search on an unsorted array? Why doesn't it work?


**Q1:** Why must the array be sorted for binary search?
**A:** Because we eliminate half the search space based on comparison - this only works if elements are ordered.

**Q2:** What is the time complexity of binary search?
**A:** O(log n) - we halve the search space each time.

**Q3:** What is the space complexity of iterative binary search?
**A:** O(1) - we only use a few variables, no extra space needed.

**Q4:** When would you use binary search instead of linear search?
**A:** When the array is sorted and you need to search multiple times - the O(log n) vs O(n) advantage is significant.


---

## Common Mistakes

### ❌ Mistake 1: Test with edge cases (empty input, single element, boundary values)
**Solution:** Verify array is sorted: `if data != sorted(data): raise ValueError`

### ❌ Mistake 2: Trace through examples step-by-step
**Solution:** Manually trace through a small example (3-5 elements) to verify each step matches the algorithm logic

### ❌ Mistake 3: Use debugging tools to verify your logic
**Solution:** Use print statements or debugger to check variable values at each step, compare with expected behavior

### ❌ Mistake 4: Review the algorithm's key steps before implementing
**Solution:** Study the algorithm's pseudocode or description, identify the core steps, then implement one step at a time

### 💡 How to Avoid
- Test with edge cases (empty input, single element, boundary values)
- Trace through examples step-by-step
- Use debugging tools to verify your logic
- Review the algorithm's key steps before implementing