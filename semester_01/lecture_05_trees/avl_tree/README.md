# AVL Tree

1. **Name of Algorithm**  
   AVL Tree

2. **What problem does it solve? (1 sentence)**  
   Maintains a self-balancing binary search tree where the heights of left and right subtrees differ by at most one.

3. **Intuition (plain-language explanation)**  
   Like a see-saw that automatically adjusts itself: whenever one side gets too heavy, it rotates to balance out.

4. **Inputs & Outputs**  
   - Input: Sequence of insert/delete/search operations on key-value pairs.  
   - Output: Balanced binary search tree with O(log n) height guarantees.

5. **Step-by-step description (5–10 lines max)**  
1. Insert or delete a node using standard BST rules.
2. Check the balance factor (height difference) of each ancestor.
3. If imbalance detected (|balance| > 1), perform rotations.
4. Single rotation for outside cases (left-left or right-right).
5. Double rotation for inside cases (left-right or right-left).
6. Update heights and continue up the tree until balanced.

6. **Tiny example (hand-simulated)**  
   Insert 3,2,1: After 3 and 2, insert 1 causes left-left imbalance. Rotate right around 3: [2(1,3)].

7. **Time & Space Complexity**  
   - Time: O(log n) for all operations (insert, delete, search).  
   - Space: O(n) to store n nodes.

8. **Strengths**  
- Guaranteed O(log n) height ensures predictable performance.
- Strict balancing prevents worst-case O(n) behavior.

9. **Weaknesses / limitations**  
- More complex than basic BST due to rotation overhead.
- Requires storing balance factors or heights per node.

10. **Compare with alternatives**  
    Alternatives: Red-Black Tree, Splay Tree, B-Tree

11. **30-second explanation (your own words)**  
    A self-adjusting BST that keeps itself balanced by rotating nodes when one subtree becomes too tall.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
