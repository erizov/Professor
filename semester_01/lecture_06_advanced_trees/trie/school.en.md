# Trie

## Principle of Operation

A Trie (pronounced "try") is a special tree that's perfect for storing and searching words. Instead of storing whole words, it stores them letter by letter. Each letter is a step down the tree, so words that start the same share the same path!

Think of it like a phone book organized by first letter, then second letter, and so on. Words like "cat" and "car" share the path "c-a" and then branch off.

### Simple Example

Imagine storing words: "cat", "car", "dog", "do"

```
        (root)
       /  |  \
      c   d   ...
     /     \
    a       o
   / \     / \
  t   r   g  (end)
  |   |   |
(end)(end)(end)
```

- "cat" follows path: c → a → t
- "car" follows path: c → a → r
- "dog" follows path: d → o → g
- "do" follows path: d → o (marked as end)
- Words sharing prefixes share paths!

## Algorithm Complexity in O-notation

- **Best Case:** O(m) - where m is the length of the word. To search "cat", you follow 3 steps (c, a, t).
- **Average Case:** O(m) - always takes as many steps as the word has letters.
- **Worst Case:** O(m) - same as best case! Searching doesn't depend on how many words are stored, only on word length.

**Space Complexity:** O(n × m) - where n is number of words and m is average length. Words sharing prefixes use less space!

## Where It Is Used in Practice

Tries are used everywhere words are searched:

- **Real Applications:**
  - **Search engines** - autocomplete suggestions as you type
  - **Phone contacts** - finding names as you type
  - **Spell checkers** - checking if words are spelled correctly
  - **Text editors** - code completion and suggestions

- **When It's Perfect:**
  - When you need to search words quickly
  - When you need to find words that start with certain letters
  - When many words share the same beginning

- **Why It's Special:**
  - Very fast for searching words (O(m) where m is word length)
  - Great for finding words with same prefix
  - Used in autocomplete and search suggestions

## What Can the Algorithm Be Compared To

Tries can be compared to:

- **Phone Book:** Like a phone book organized by first letter, then second, then third - you can quickly find names.

- **Dictionary:** Like a dictionary where you look up words letter by letter.

- **Family Tree for Words:** Like a family tree where words that start the same are related and share a path.

## Minimal Code Example (Only Important Parts)

Here's a simple Python implementation:

```python
class TrieNode:
    def __init__(self):
        self.children = {}  # Map letter to next node
        self.is_word = False  # True if this ends a word

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def add_word(self, word):
        """Add word to trie."""
        node = self.root
        for letter in word:
            if letter not in node.children:
                node.children[letter] = TrieNode()
            node = node.children[letter]
        node.is_word = True  # Mark end of word
    
    def search(self, word):
        """Check if word exists."""
        node = self.root
        for letter in word:
            if letter not in node.children:
                return False
            node = node.children[letter]
        return node.is_word  # Must be end of word
    
    def starts_with(self, prefix):
        """Check if any word starts with prefix."""
        node = self.root
        for letter in prefix:
            if letter not in node.children:
                return False
            node = node.children[letter]
        return True  # Prefix exists
```

**Key Points:**
- Each node represents a letter
- Children map letters to next nodes
- Path from root spells out the word
- `is_word` marks where words end
- Great for prefix matching!

## Common Mistakes

1. **Forgetting to Mark Word End:**
   - **Mistake:** Not marking where words end
   - **Why it's bad:** Can't tell if "do" is a word or just part of "dog"
   - **Fix:** Always set `is_word = True` when you finish adding a word

2. **Confusing Search and Prefix:**
   - **Mistake:** Using search when you want prefix, or vice versa
   - **Why it's bad:** Search needs exact word, prefix just needs beginning
   - **Fix:** Use `search()` for exact words, `starts_with()` for prefixes

3. **Not Sharing Paths:**
   - **Mistake:** Creating separate paths for words that share prefixes
   - **Why it's bad:** Wastes space and defeats the purpose of trie
   - **Fix:** Always reuse existing paths when words share letters

4. **Case Sensitivity:**
   - **Mistake:** "Hello" and "hello" treated as different
   - **Why it's bad:** Can't find words with different capitalization
   - **Fix:** Convert all words to lowercase (or uppercase) before storing

5. **Not Handling Empty:**
   - **Mistake:** Not handling empty string or empty trie
   - **Why it's bad:** Causes errors
   - **Fix:** Check for empty strings and handle empty trie

## Recommended Literature

1. **"Grokking Algorithms" by Aditya Bhargava**
   - Excellent beginner-friendly book that explains Tries simply

2. **"Introduction to Algorithms" (CLRS)**
   - Comprehensive textbook covering Tries

3. **"Algorithms Unlocked" by Thomas H. Cormen**
   - Accessible introduction that explains when Tries are useful

4. **Online Resources:**
   - Khan Academy's computer science courses
   - Visualgo.net for interactive Trie visualizations
   - GeeksforGeeks for code examples and explanations
