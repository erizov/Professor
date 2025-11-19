# Red-Black Tree

1. **Name of Algorithm**  
   Red-Black Tree

2. **What problem does it solve? (1 sentence)**  
   Maintains a balanced binary search tree with relaxed balancing rules compared to AVL trees.

3. **Intuition (plain-language explanation)**  
   A BST with color coding: red and black nodes follow rules that keep the tree roughly balanced without strict height requirements.

4. **Inputs & Outputs**  
   - Input: Sequence of insert/delete/search operations on key-value pairs.  
   - Output: Balanced binary search tree with O(log n) worst-case height.

5. **Step-by-step description (5–10 lines max)**  
1. Insert node as red (maintains black height property).
2. If parent is black, done; if red, check uncle color.
3. If uncle is red: recolor parent, uncle, and grandparent.
4. If uncle is black: rotate to fix red-red violation.
5. Root is always black; all paths have same black node count.

6. **Tiny example (hand-simulated)**  
   Insert 5,3,7,1: After 1, red-red violation with 3. Uncle 7 is red, so recolor: 3 and 7 become black, 5 becomes red.

7. **Time & Space Complexity**  
   - Time: O(log n) for all operations; slightly faster than AVL due to fewer rotations.  
   - Space: O(n) with one color bit per node.

8. **Strengths**  
- Fewer rotations than AVL trees, better for frequent updates.
- Used in many standard library implementations (Java TreeMap, C++ map).

9. **Weaknesses / limitations**  
- Less strictly balanced than AVL (height can be up to 2*log(n+1)).
- More complex than basic BST.

10. **Compare with alternatives**  
    Alternatives: AVL Tree, Splay Tree, Treap

11. **30-second explanation (your own words)**  
    A self-balancing BST using red/black coloring rules that ensure no path is more than twice as long as any other.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
