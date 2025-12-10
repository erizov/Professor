# Binary Search

# School

## 📋 Quick Summary

- **Purpose:** Binary Search: Always check the middle element - if it's not what we want, eliminate half the search space.
- **Complexity:** O(log n)
- **Category:** Searching
- **Key Idea:** Always check the middle element - if it's not what we want, eliminate half the search space.

Binary Search: Always check the middle element - if it's not what we want, eliminate half the search space.

Always check the middle element - if it's not what we want, eliminate half the search space.

**BINARY** = Begin In Middle, Always Narrow Your search. Like finding a word in a dictionary - always check the middle!








Этот алгоритм работает, систематически обрабатывая данные, чтобы достичь своей цели. Он относится к категории алгоритмов **Searching**.

## Сложность алгоритма

Временная сложность составляет **O(log n)**, что означает, что время выполнения зависит от размера входных данных. Пространственная сложность — **O(1)**, что указывает на количество дополнительной памяти.

## Где применяется на практике

Binary Search обычно используется в:
- Database query optimization
- Search engines (binary search in sorted indices)
- Autocomplete and suggestion systems
- Образовании по информатике и изучении алгоритмов

## С чем можно сравнить

Представьте Binary Search как систематический способ организации или поиска информации — похоже на то, как вы можете эффективно организовывать предметы или искать в коллекции.

## Минимальный пример кода

```python
def binary_search(arr, target):
    """Implementation."""
    left, right = (0, len(arr) - 1)
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

## ✏️ Practice Exercise

**Exercise 1 (Easy):**
Find the number 42 in this sorted array: [10, 20, 30, 40, 50, 60, 70]
Show each step of your search.

**Exercise 2 (Medium):**
Implement binary search to find the first occurrence of a target value in a sorted array with duplicates.

**Exercise 3 (Hard):**
What happens if you try binary search on an unsorted array? Why doesn't it work?

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