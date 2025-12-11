# Edit Distance (Levenshtein Distance)

## Principle of Operation

Edit distance measures how different two strings are by counting the minimum number of operations needed to transform one string into another. The operations are: insert a character, delete a character, or substitute (replace) a character.

**How it works:**
1. Compare two strings character by character
2. If characters match, no operation needed (cost 0)
3. If characters don't match, you can:
   - Delete a character from first string (cost 1)
   - Insert a character into first string (cost 1)
   - Substitute (replace) a character (cost 1)
4. Choose the operation with minimum cost
5. Use a table to remember the minimum cost for transforming each prefix of the strings

**Simple analogy:** Imagine you're editing a document. You want to change "cat" to "bat". You can substitute 'c' with 'b' (1 operation). To change "cat" to "cats", you insert 's' (1 operation). To change "cats" to "cat", you delete 's' (1 operation). Edit distance counts these operations.

**Key idea:** Build a table where each cell represents the minimum cost to transform one prefix of the first string into one prefix of the second string. Start with small prefixes and build up to the full strings.

## Algorithm Complexity

**Time Complexity:** O(m × n)
- m = length of first string
- n = length of second string
- We fill a table with (m+1) rows and (n+1) columns
- Each cell takes constant time to compute

**Space Complexity:** O(m × n)
- Need table to store edit distance for each prefix pair
- Can be optimized to O(min(m, n)) by using only two rows

**Why it's efficient:** Instead of trying all possible edit sequences (exponential), we use a table to remember solutions to smaller problems. This makes it much faster.

## Where It's Used in Practice

**Spell Checkers:**
- **Word processors** - suggesting corrections for misspelled words
- **Search engines** - "Did you mean?" suggestions
- **Mobile keyboards** - autocorrect

**Text Processing:**
- **Plagiarism detection** - finding similar text
- **Document comparison** - measuring how different documents are
- **Fuzzy search** - finding items even with typos

**Real-World Applications:**
- **DNA comparison** - measuring similarity between genetic sequences
- **Version control** - showing differences between file versions
- **Password checking** - ensuring new password isn't too similar to old one

## What It Can Be Compared To

**Like Editing a Document:** You make changes (insert, delete, substitute) to transform one text into another. Edit distance counts these changes.

**Like Building Up Solutions:** Start with transforming empty strings, then add characters one by one, always choosing the cheapest way.

**Like a Grid Path:** Imagine a grid where you move from top-left to bottom-right. Each move represents an operation. Edit distance finds the cheapest path.

**Different from Hamming Distance:** Hamming distance only allows substitutions and requires strings to be same length. Edit distance allows insertions/deletions and works for any string lengths.

## Minimal Code Example

Here's a simple edit distance implementation:

```python
def edit_distance(s1, s2):
    """Edit distance (Levenshtein) using dynamic programming."""
    m, n = len(s1), len(s2)
    # dp[i][j] = edit distance between s1[0:i] and s2[0:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Base cases: distance to empty string
    for i in range(m + 1):
        dp[i][0] = i  # Delete all characters
    for j in range(n + 1):
        dp[0][j] = j  # Insert all characters
    
    # Fill table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                # Characters match, no cost
                dp[i][j] = dp[i - 1][j - 1]
            else:
                # Take minimum of three operations
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # Delete
                    dp[i][j - 1],      # Insert
                    dp[i - 1][j - 1]   # Substitute
                )
    
    return dp[m][n]

# Example:
print(edit_distance("cat", "bat"))    # Output: 1 (substitute)
print(edit_distance("cat", "cats"))    # Output: 1 (insert)
print(edit_distance("kitten", "sitting"))  # Output: 3
```

**Key parts:**
- Table stores edit distance for each prefix pair
- Base cases: distance to empty string = string length
- If characters match, no cost (use diagonal)
- If don't match, take min of delete/insert/substitute (cost 1)

## Common Mistakes

1. **Wrong Base Cases:**
   - **Wrong:** Not initializing distance to empty string
   - **Why it's wrong:** Incorrect starting point, wrong results
   - **Fix:** Initialize dp[i][0] = i and dp[0][j] = j

2. **Not Considering All Operations:**
   - **Wrong:** Only using substitutions
   - **Why it's wrong:** Missing optimal solutions
   - **Fix:** Always consider delete, insert, and substitute

3. **Array Index Errors:**
   - **Wrong:** Using s1[i] instead of s1[i-1]
   - **Why it's wrong:** Accesses wrong characters
   - **Fix:** Remember dp[i][j] uses s1[0:i], so use s1[i-1] for i-th character

4. **Not Handling Empty Strings:**
   - **Wrong:** Not handling case when one string is empty
   - **Why it's wrong:** Incorrect results or errors
   - **Fix:** Base cases handle empty strings correctly

5. **Confusing with Hamming Distance:**
   - **Wrong:** Only allowing substitutions
   - **Why it's wrong:** Only works for strings of same length
   - **Fix:** Edit distance allows insertions and deletions

## Recommended Literature

1. **"Grokking Algorithms"** by Aditya Bhargava
   - Simple explanations of dynamic programming
   - Great edit distance examples

2. **"Introduction to Algorithms" (CLRS)**
   - Comprehensive coverage of edit distance
   - Explains the algorithm in detail

3. **"Algorithm Design Manual"** by Steven Skiena
   - Practical approach with examples
   - Good for understanding applications

4. **Online Resources:**
   - GeeksforGeeks - edit distance tutorials
   - Khan Academy - dynamic programming course
   - LeetCode - practice problems
