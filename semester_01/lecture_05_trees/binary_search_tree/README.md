# Binary Search Tree

1. **Name of Algorithm**  
   Binary Search Tree

2. **What problem does it solve? (1 sentence)**  
   Stores keys so that lookups, inserts, and deletes can exploit sorted order with O(log n) average time.

3. **Intuition (plain-language explanation)**  
   Think of a game of twenty questions: each comparison decides whether to go left (smaller) or right (larger) until you reach the answer.

4. **Inputs & Outputs**  
   - Input: Comparable keys with optional values; operations like insert, search, delete.  
   - Output: Tree structure where in-order traversal yields sorted keys.

5. **Step-by-step description (5–10 lines max)**  
1. Start at the root node and compare the target key.
2. If key < current node, recurse or iterate into the left child.
3. If key > current node, recurse or iterate into the right child.
4. If key equals the node, update or return the value.
5. During deletion, replace removed nodes with predecessor or successor to preserve ordering.

6. **Tiny example (hand-simulated)**  
   Insert 8,3,10,1,6: 8 is root, 3 goes left, 10 right, 1 left of 3, 6 right of 3.

7. **Time & Space Complexity**  
   - Time: Average O(log n); worst-case O(n) on skewed trees.  
   - Space: O(n) to store n nodes.

8. **Strengths**  
- Maintains sorted order with simple pointer structure.
- Supports inorder traversal to produce sorted output quickly.

9. **Weaknesses / limitations**  
- Unbalanced input degrades operations to O(n).
- Needs balancing variants (AVL, Red-Black) for guaranteed performance.

10. **Compare with alternatives**  
    Alternatives: AVL Tree, Red-Black Tree, Skip List

11. **30-second explanation (your own words)**  
    A search tree where each node’s left subtree holds smaller keys and the right subtree holds larger ones, enabling logarithmic search when balanced.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
