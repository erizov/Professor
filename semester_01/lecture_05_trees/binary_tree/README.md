# Binary Tree

1. **Name of Algorithm**  
   Binary Tree

2. **What problem does it solve? (1 sentence)**  
   Represents hierarchical relationships where each node may have up to two children.

3. **Intuition (plain-language explanation)**  
   Picture a family tree where every person can have a left and right child pointer, letting you organize data hierarchically.

4. **Inputs & Outputs**  
   - Input: Nodes containing data plus optional left/right child references.  
   - Output: Tree structure supporting traversals such as preorder, inorder, and postorder.

5. **Step-by-step description (5–10 lines max)**  
1. Create a root node (which may be empty).
2. Attach left/right children as required by the domain problem.
3. Traverse using preorder (node-left-right), inorder (left-node-right), or postorder (left-right-node).
4. Breadth-first traversal visits nodes level by level.
5. Perform application-specific work (search, aggregation) during traversals.

6. **Tiny example (hand-simulated)**  
   Tree with root 1, left child 2, right child 3: inorder traversal yields [2,1,3].

7. **Time & Space Complexity**  
   - Time: Traversals and searches touch each node once: O(n).  
   - Space: O(n) for nodes plus O(h) recursion depth where h is tree height.

8. **Strengths**  
- Flexible backbone for heaps, BSTs, and expression trees.
- Natural fit for recursive definitions and divide-and-conquer algorithms.

9. **Weaknesses / limitations**  
- By itself offers no ordering or balancing guarantees.
- Pointer-heavy representation can hurt cache locality.

10. **Compare with alternatives**  
    Alternatives: General Tree, Binary Search Tree, Heap

11. **30-second explanation (your own words)**  
    A generic two-child-per-node structure that underpins many specialized tree variants and traversals.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
