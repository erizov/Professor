# KMP (Knuth-Morris-Pratt) Algorithm

## Principle of Operation

KMP is a smart way to search for a pattern (like a word) inside a text. Instead of checking every position from the beginning when something doesn't match, it remembers what it already matched and skips ahead intelligently.

**How it works:**
1. First, it builds a "helper table" (LPS array) from the pattern that tells it how much it can skip when a mismatch happens
2. Then it searches through the text, comparing character by character
3. When characters match, it moves forward
4. When characters don't match, instead of going back to the beginning, it uses the helper table to skip ahead to the right position
5. This way, it never goes backwards in the text, only forward

**Simple analogy:** Imagine you're looking for the word "ABC" in text "ABABC". When you find "AB" matches but then "C" doesn't match at position 3, a naive search would start over. KMP is smart - it knows "AB" already matched, so it can skip ahead and continue from where the pattern might match again.

**Key idea:** KMP is like having a "memory" of what you've already matched. When something doesn't match, instead of starting over, you use this memory to jump to the best position to continue.

## Algorithm Complexity

**Time Complexity:** O(n + m)
- n = length of text (where we're searching)
- m = length of pattern (what we're looking for)
- Building the helper table: O(m) - one pass through the pattern
- Searching the text: O(n) - one pass through the text, never going backwards
- Total: O(n + m) - linear time, very efficient!

**Space Complexity:** O(m)
- Need to store the helper table (LPS array) which is the same size as the pattern
- No extra space needed for the text

**Why it's efficient:** Unlike naive search which is O(n × m) (checking every position), KMP only scans the text once and never backtracks. The helper table tells it exactly where to continue when a mismatch occurs.

## Where It's Used in Practice

**Text Editors and Search:**
- **Find/Replace** in text editors - searching for words or patterns
- **Code editors** - finding functions, variables in code
- **Search bars** - finding text in documents or web pages

**Search Engines:**
- **Web search** - finding patterns in web pages
- **Database search** - searching through text in databases
- **Autocomplete** - finding matching words as you type

**Programming:**
- **String matching** in programming languages
- **Pattern recognition** - finding specific patterns in data
- **Text processing** - tools like grep use similar ideas

**Real-World Applications:**
- **Plagiarism detection** - finding matching text in documents
- **DNA analysis** - finding patterns in genetic sequences
- **Virus scanning** - detecting malware patterns in files
- **Log analysis** - searching for specific events in log files

## What It Can Be Compared To

**Like a Smart Reader:**
- Naive search is like reading a book and starting from page 1 every time you lose your place
- KMP is like having bookmarks - when you lose your place, you know where to jump back to

**Like Pattern Matching with Memory:**
- Regular pattern matching checks every position from scratch
- KMP remembers what it already matched and uses that information

**Different from Naive Search:**
- **Naive:** O(n × m) - checks every position, might check same characters many times
- **KMP:** O(n + m) - checks each character in text at most once, much faster

**Like a Smart Sliding Window:**
- Both slide a pattern over text
- But KMP uses the helper table to skip positions that can't possibly match
- This makes it much faster than checking every position

## Minimal Code Example

Here's a simplified explanation of how KMP works:

```python
def build_lps(pattern):
    """Build Longest Proper Prefix which is also Suffix array."""
    m = len(pattern)
    lps = [0] * m
    length = 0  # Length of previous longest prefix suffix
    i = 1
    
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    
    return lps

def kmp_search(text, pattern):
    """Search for pattern in text using KMP algorithm."""
    n, m = len(text), len(pattern)
    lps = build_lps(pattern)
    
    i = 0  # Index for text
    j = 0  # Index for pattern
    
    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
        
        if j == m:
            # Pattern found at position i - j
            print(f"Found at index {i - j}")
            j = lps[j - 1]  # Continue searching
        
        elif i < n and text[i] != pattern[j]:
            if j != 0:
                j = lps[j - 1]  # Don't match lps[0..lps[j-1]] again
            else:
                i += 1

# Example usage:
text = "ABABDABACDABABCABCABAB"
pattern = "ABABCABAB"
kmp_search(text, pattern)
```

**Key parts:**
- `build_lps()` - creates helper table from pattern
- `kmp_search()` - uses helper table to search efficiently
- When mismatch: use LPS to skip, don't go back in text
- Never backtrack in text, only move forward

## Common Mistakes

1. **Not Building LPS Array Correctly:**
   - **Wrong:** Building LPS array incorrectly or skipping this step
   - **Why it's wrong:** LPS array is crucial - it tells algorithm where to continue
   - **Fix:** Carefully implement LPS construction, test with simple patterns

2. **Going Backwards in Text:**
   - **Wrong:** Moving text pointer backwards when mismatch occurs
   - **Why it's wrong:** KMP's key advantage is never backtracking in text
   - **Fix:** Only move text pointer forward, use LPS to adjust pattern position

3. **Incorrect LPS Usage:**
   - **Wrong:** Using wrong LPS value when mismatch occurs
   - **Why it's wrong:** Won't skip to correct position, may miss matches
   - **Fix:** When mismatch at pattern[j], set j = lps[j-1] (not lps[j])

4. **Not Handling Edge Cases:**
   - **Wrong:** Not handling empty pattern or empty text
   - **Why it's wrong:** Will crash or give incorrect results
   - **Fix:** Check if pattern or text is empty before searching

5. **Confusing with Naive Search:**
   - **Wrong:** Implementing naive search (O(n×m)) instead of KMP (O(n+m))
   - **Why it's wrong:** Much slower, defeats the purpose
   - **Fix:** Make sure you're using LPS array and not restarting from beginning

6. **Wrong Pattern Position Reset:**
   - **Wrong:** Resetting pattern position to 0 when mismatch occurs
   - **Why it's wrong:** Loses the benefit of LPS array, becomes like naive search
   - **Fix:** Use LPS value to set new pattern position: j = lps[j-1]

## Recommended Literature

1. **"Grokking Algorithms"** by Aditya Bhargava
   - Simple explanations of string matching algorithms
   - Good visualizations of how KMP works

2. **"Introduction to Algorithms" (CLRS)**
   - Comprehensive coverage of KMP with detailed analysis
   - Explains why KMP is O(n+m) and how LPS array works

3. **"Algorithm Design Manual"** by Steven Skiena
   - Practical approach to string matching
   - Compares KMP with other algorithms like Boyer-Moore

4. **"Algorithms on Strings, Trees, and Sequences"** by Dan Gusfield
   - Comprehensive book on string algorithms
   - Detailed explanation of KMP and its variations

5. **Online Resources:**
   - Visualgo.net - interactive KMP visualization
   - GeeksforGeeks - detailed KMP tutorials with examples
   - Wikipedia - step-by-step KMP explanation with examples
