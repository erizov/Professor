# Binary Heap

1. **Name of Algorithm**  
   Binary Heap

2. **What problem does it solve? (1 sentence)**  
   Maintains a complete binary tree where parent nodes are always greater (max-heap) or smaller (min-heap) than children.

3. **Intuition (plain-language explanation)**  
Like a family tree where parents always outrank children: the top person is the most important, and you can quickly promote someone up the ranks.

4. **Inputs & Outputs**  
   - Input: Sequence of insert/extract operations on priority values.  
   - Output: Heap structure with O(1) access to max/min element.

5. **Step-by-step description (5–10 lines max)**  
1. Store heap in array: parent at i, children at 2i+1 and 2i+2.
2. Insert: add to end, bubble up by swapping with parent if out of order.
3. Extract: remove root, move last element to root, bubble down by swapping with larger/smaller child.
4. Maintain heap property: parent >= children (max-heap) or parent <= children (min-heap).

6. **Tiny example (hand-simulated)**  
   Max-heap [9,7,5,3,2]: Insert 8 → [9,7,5,3,2,8] → bubble up: [9,8,5,3,2,7] (8 swapped with 7's parent).

7. **Time & Space Complexity**  
   - Time: O(log n) insert/extract, O(1) peek, O(n) build from array.  
   - Space: O(n) array storage.

8. **Strengths**  
- Simple array-based implementation, cache-friendly.
- Efficient for priority queues and heap sort.

9. **Weaknesses / limitations**  
- No efficient search or decrease-key without additional structures.
- Not suitable for merging heaps efficiently.

10. **Compare with alternatives**  
    Alternatives: Fibonacci Heap, Binomial Heap, Pairing Heap

11. **30-second explanation (your own words)**  
    A complete binary tree stored in an array that keeps the highest (or lowest) priority item at the top with O(log n) updates.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
