**Brief about Insertion Sort Algorithm for School Students**

**Principle of Operation:**
- Insertion Sort is a simple sorting algorithm that builds the final sorted array one item at a time.
- It takes each element from an unsorted portion and inserts it into its correct position in the sorted portion.

**Algorithm Complexity:** 
- The time complexity of Insertion Sort is O(n^2) in the worst case scenario, where n is the number of elements in the array.

**Usage in Practice:**
- Insertion Sort is commonly used for sorting small arrays or as a building block in more advanced sorting algorithms.

**Comparison:**
- Insertion Sort can be compared to sorting a hand of cards in your hand, where you pick one card at a time and insert it in the correct position.

**Minimal Code Example:**
```
void insertionSort(int arr[], int n) {
    int i, key, j;
    for (i = 1; i < n; i++) {
        key = arr[i];
        j = i - 1;

        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j = j - 1;
        }
        arr[j + 1] = key;
    }
}
```

**Common Mistakes:**
- Forgetting to update the index correctly in the inner while loop can lead to incorrect sorting.
- Not understanding the concept of shifting elements can also result in errors.

**Recommended Literature:**
- "Introduction to Algorithms" by Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein
- "Algorithms" by Robert Sedgewick and Kevin Wayne