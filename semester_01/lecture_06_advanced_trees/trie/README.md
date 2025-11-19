# Trie

1. **Name of Algorithm**  
   Trie

2. **What problem does it solve? (1 sentence)**  
   Efficiently stores and searches strings with shared prefixes, enabling fast prefix matching and autocomplete.

3. **Intuition (plain-language explanation)**  
   Like a phone book organized by first letter, then second, then third: each level narrows down the search.

4. **Inputs & Outputs**  
   - Input: Set of strings (words, keys) and query operations (insert, search, prefix match).  
   - Output: Tree structure where each path from root to node represents a string prefix.

5. **Step-by-step description (5–10 lines max)**  
1. Root represents empty string.
2. Each node has children for each possible next character.
3. Insert: traverse/create path for each character, mark end node.
4. Search: follow path character by character, check if end marker exists.
5. Prefix search: traverse to prefix node, collect all descendants.

6. **Tiny example (hand-simulated)**  
   Insert 'cat', 'car': root → 'c' → 'a' → 't' (end) and 'a' → 'r' (end). Search 'car': follow c-a-r, found.

7. **Time & Space Complexity**  
   - Time: O(m) for search/insert where m is string length; O(n*m) to build from n strings.  
   - Space: O(ALPHABET_SIZE * N * M) worst case, but can be compressed.

8. **Strengths**  
- Fast prefix matching and autocomplete queries.
- Efficient for dictionary lookups and spell checkers.

9. **Weaknesses / limitations**  
- High memory usage for sparse tries.
- Slower than hash tables for exact lookups.

10. **Compare with alternatives**  
    Alternatives: Hash Table, Ternary Search Tree, Radix Tree

11. **30-second explanation (your own words)**  
    A tree where each path spells out a string, making prefix searches as fast as following the path.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
