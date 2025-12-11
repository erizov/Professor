# Edit Distance (Levenshtein Distance)

## Convergence Speed and Complexity Estimate

**Time Complexity:**
- **Dynamic Programming (Bottom-Up):** O(m × n) where m and n are lengths of the two strings. We fill a 2D table of size (m+1) × (n+1), computing each cell in constant time based on three previous cells.
- **Space-Optimized DP:** O(m × n) time, O(min(m, n)) space - using only two rows (current and previous) of the DP table.
- **Recursive with Memoization:** O(m × n) - each unique subproblem (i, j) representing edit distance between first i characters of s1 and first j characters of s2 is solved once.
- **Naive Recursive:** O(3^(m+n)) - exponential time, exploring all possible edit sequences with massive redundancy.

**Space Complexity:**
- **Standard DP:** O(m × n) - 2D table storing edit distance for each (i, j) prefix pair.
- **Space-Optimized DP:** O(min(m, n)) - only storing two rows and updating them.
- **Memoized Recursive:** O(m × n) - memoization table plus recursion stack O(m + n).

**Convergence:** The algorithm converges when the DP table is completely filled. Each cell dp[i][j] represents the minimum edit distance between the first i characters of string s1 and the first j characters of string s2. The final answer is in dp[m][n], computed after processing all characters of both strings.

**Operations:** Edit distance counts three operations: insertion (add character), deletion (remove character), and substitution (replace character). Each operation costs 1. Some variants assign different costs to different operations.

## Where the Algorithm is Used in Real Frameworks and Software

Edit distance (Levenshtein distance) is fundamental in text processing and similarity measurement:

- **Spell Checkers and Autocorrect:**
  - **Microsoft Word, Google Docs** - suggesting corrections for misspelled words
  - **Search engines** - "Did you mean?" suggestions
  - **Mobile keyboards** - autocorrect and word prediction
  - **Text editors** - typo detection and correction

- **Bioinformatics:**
  - **DNA/RNA sequence alignment** - measuring similarity between genetic sequences
  - **Protein sequence comparison** - finding similar protein structures
  - **Phylogenetic analysis** - evolutionary distance between species
  - **Genome assembly** - aligning sequence fragments

- **Natural Language Processing:**
  - **Machine translation** - measuring translation quality
  - **Text similarity** - finding similar documents or sentences
  - **Fuzzy string matching** - matching names, addresses with typos
  - **Plagiarism detection** - detecting similar text passages

- **Database Systems:**
  - **Fuzzy search** - finding records with similar names/values
  - **Record linkage** - matching records from different databases
  - **Data cleaning** - identifying duplicate records with variations
  - **Query suggestions** - suggesting similar search terms

- **Version Control:**
  - **Git, SVN** - computing differences between file versions
  - **Diff algorithms** - showing changes between text files
  - **Merge conflict resolution** - understanding text differences

- **Real-World Applications:**
  - **OCR (Optical Character Recognition)** - correcting recognition errors
  - **Speech recognition** - matching spoken words to dictionary
  - **Password similarity** - checking if new password is too similar to old
  - **Social media** - detecting similar usernames or content

## What It's Similar To in Concept

Edit distance shares conceptual similarities with:

- **Dynamic Programming Pattern:** Classic DP problem with optimal substructure - solution to edit distance between prefixes helps solve edit distance between longer strings. Overlapping subproblems - same prefix pairs computed multiple times in recursive approach.

- **Longest Common Subsequence (LCS):** Both use 2D DP table with similar structure. LCS finds longest matching subsequence, edit distance finds minimum operations to transform one string to another. Related but different objectives.

- **String Alignment:** Edit distance is essentially finding optimal alignment between two strings with minimum cost. Similar to sequence alignment in bioinformatics (Needleman-Wunsch, Smith-Waterman algorithms).

- **Graph Shortest Path:** Can be viewed as finding shortest path in edit graph where nodes are (i, j) positions and edges represent edit operations with cost 1.

- **Hamming Distance:** Hamming distance only allows substitutions (strings must be same length), while edit distance allows insertions and deletions (strings can differ in length). Edit distance is more general.

## Which Algorithms It's Often Used With

Edit distance is frequently combined with:

- **Other String Algorithms:**
  - **Longest Common Subsequence** - similar DP structure, different objective
  - **Longest Common Substring** - finding contiguous matches
  - **String similarity metrics** - Jaro-Winkler, Jaccard similarity

- **Optimization Techniques:**
  - **Space optimization** - reducing O(m×n) to O(min(m,n)) space
  - **Early termination** - stopping when distance exceeds threshold
  - **Approximation algorithms** - for very long strings

- **Related Problems:**
  - **Weighted Edit Distance** - different costs for different operations
  - **Edit Distance with Transpositions** - allowing character swaps
  - **Fuzzy string matching** - finding strings within edit distance k

- **Applications:**
  - **Spell checking** - combined with dictionary lookup
  - **Sequence alignment** - in bioinformatics pipelines
  - **Record matching** - in data integration systems

## Key Code (Only Important Parts)

Here's a concise implementation highlighting the essential logic:

```python
def edit_distance(s1: str, s2: str) -> int:
    """Edit distance (Levenshtein) using dynamic programming."""
    m, n = len(s1), len(s2)
    # dp[i][j] = edit distance between s1[0:i] and s2[0:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Base cases: edit distance to empty string
    for i in range(m + 1):
        dp[i][0] = i  # Delete all characters from s1
    for j in range(n + 1):
        dp[0][j] = j  # Insert all characters from s2
    
    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                # Characters match, no operation needed
                dp[i][j] = dp[i - 1][j - 1]
            else:
                # Take minimum of three operations
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # Delete from s1
                    dp[i][j - 1],      # Insert into s1
                    dp[i - 1][j - 1]   # Substitute in s1
                )
    
    return dp[m][n]

# Space-optimized version (O(min(m,n)) space)
def edit_distance_optimized(s1: str, s2: str) -> int:
    """Space-optimized edit distance."""
    if len(s1) < len(s2):
        s1, s2 = s2, s1  # Ensure s1 is longer
    
    m, n = len(s1), len(s2)
    prev = list(range(n + 1))  # Previous row
    
    for i in range(1, m + 1):
        curr = [i]  # Current row starts with i deletions
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                curr.append(prev[j - 1])
            else:
                curr.append(1 + min(prev[j], curr[j - 1], prev[j - 1]))
        prev = curr
    
    return prev[n]
```

**Key Points:**
- DP table: dp[i][j] = edit distance between s1[0:i] and s2[0:j]
- Base cases: distance to empty string = length (all deletions/insertions)
- Recurrence: match (no cost) or min of delete/insert/substitute (cost 1)
- Time: O(m × n), Space: O(m × n) or O(min(m,n)) optimized
- Final answer: dp[m][n]

## Common Application Errors

1. **Wrong Base Case Initialization:**
   - **Error:** Not initializing dp[i][0] = i and dp[0][j] = j
   - **Impact:** Incorrect base cases, wrong results
   - **Solution:** Always initialize: distance to empty string equals string length

2. **Array Index Off-by-One:**
   - **Error:** Using s1[i] instead of s1[i-1] when dp[i][j] represents first i characters
   - **Impact:** Accesses wrong characters, incorrect comparisons
   - **Solution:** Remember dp[i][j] uses s1[0:i] (first i chars), so use s1[i-1] for i-th character

3. **Incorrect Recurrence Relation:**
   - **Error:** Not considering all three operations (delete, insert, substitute)
   - **Impact:** Missing optimal solution, incorrect distance
   - **Solution:** Always take min of all three operations when characters don't match

4. **Not Handling Empty Strings:**
   - **Error:** Not handling case when one or both strings are empty
   - **Impact:** Index errors or incorrect results
   - **Solution:** Base cases handle empty strings: dp[0][j] = j, dp[i][0] = i

5. **Space Optimization Direction Error:**
   - **Error:** Processing in wrong direction in optimized version
   - **Impact:** Overwrites values needed for current iteration
   - **Solution:** Process left to right, maintaining prev and curr rows correctly

6. **Confusing with Hamming Distance:**
   - **Error:** Only allowing substitutions, not insertions/deletions
   - **Impact:** Only works for strings of same length, incorrect for different lengths
   - **Solution:** Edit distance allows all three operations, works for any string lengths

## Recommended Literature

1. **"Introduction to Algorithms" (CLRS)** - Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein
   - Comprehensive coverage of edit distance with detailed DP analysis and space optimization

2. **"Algorithm Design Manual"** - Steven S. Skiena
   - Practical approach to edit distance with implementation details and applications in spell checking

3. **"Algorithms on Strings, Trees, and Sequences"** - Dan Gusfield
   - Comprehensive book on string algorithms including edit distance and variations

4. **"Bioinformatics Algorithms"** - various authors
   - Edit distance in context of sequence alignment and bioinformatics applications

5. **Online Resources:**
   - GeeksforGeeks - detailed edit distance tutorials with examples
   - LeetCode - practice problems (Edit Distance variations)
   - Wikipedia - Levenshtein distance with mathematical analysis
