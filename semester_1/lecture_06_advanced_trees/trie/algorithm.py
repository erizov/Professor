#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trie (Prefix Tree) implementation.

Tree data structure for efficient string operations and prefix matching.
"""

import sys
from pathlib import Path
from typing import Optional, List, Dict
import random

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer


class TrieNode:
    """Node in a Trie."""
    
    def __init__(self):
        self.children: Dict[str, 'TrieNode'] = {}
        self.is_end_of_word: bool = False
        self.word_count: int = 0  # For counting word occurrences


class Trie:
    """
    Trie (Prefix Tree) implementation.
    
    Efficient for:
    - String insertion and search
    - Prefix matching
    - Autocomplete
    - Spell checking
    """
    
    def __init__(self):
        """Initialize empty Trie."""
        self.root = TrieNode()
        self.total_words = 0
    
    def insert(self, word: str) -> None:
        """
        Insert word into Trie.
        
        Time Complexity: O(m) where m is word length
        Space Complexity: O(m) worst case
        
        Args:
            word: Word to insert
        """
        node = self.root
        
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        if not node.is_end_of_word:
            self.total_words += 1
        
        node.is_end_of_word = True
        node.word_count += 1
    
    def search(self, word: str) -> bool:
        """
        Search for exact word in Trie.
        
        Time Complexity: O(m)
        
        Args:
            word: Word to search
            
        Returns:
            True if word exists, False otherwise
        """
        node = self._find_node(word)
        return node is not None and node.is_end_of_word
    
    def starts_with(self, prefix: str) -> bool:
        """
        Check if any word starts with prefix.
        
        Time Complexity: O(m)
        
        Args:
            prefix: Prefix to check
            
        Returns:
            True if prefix exists
        """
        return self._find_node(prefix) is not None
    
    def _find_node(self, prefix: str) -> Optional[TrieNode]:
        """Find node corresponding to prefix."""
        node = self.root
        
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        
        return node
    
    def get_words_with_prefix(self, prefix: str) -> List[str]:
        """
        Get all words with given prefix (autocomplete).
        
        Time Complexity: O(m + n) where n is # results
        
        Args:
            prefix: Prefix to match
            
        Returns:
            List of words with prefix
        """
        node = self._find_node(prefix)
        if not node:
            return []
        
        words = []
        self._collect_words(node, prefix, words)
        return words
    
    def _collect_words(self, node: TrieNode, current: str,
                      words: List[str]) -> None:
        """Recursively collect all words from node."""
        if node.is_end_of_word:
            words.append(current)
        
        for char, child_node in node.children.items():
            self._collect_words(child_node, current + char, words)
    
    def delete(self, word: str) -> bool:
        """
        Delete word from Trie.
        
        Time Complexity: O(m)
        
        Args:
            word: Word to delete
            
        Returns:
            True if word was deleted, False if not found
        """
        def _delete_recursive(node: TrieNode, word: str,
                            index: int) -> bool:
            if index == len(word):
                if not node.is_end_of_word:
                    return False
                
                node.is_end_of_word = False
                self.total_words -= 1
                return len(node.children) == 0
            
            char = word[index]
            if char not in node.children:
                return False
            
            child_node = node.children[char]
            should_delete = _delete_recursive(child_node, word, index + 1)
            
            if should_delete:
                del node.children[char]
                return len(node.children) == 0 and not node.is_end_of_word
            
            return False
        
        return _delete_recursive(self.root, word, 0)
    
    def count_words(self) -> int:
        """Get total number of words in Trie."""
        return self.total_words
    
    def longest_common_prefix(self) -> str:
        """
        Find longest common prefix of all words.
        
        Returns:
            Longest common prefix
        """
        if not self.root.children:
            return ""
        
        prefix = ""
        node = self.root
        
        while len(node.children) == 1 and not node.is_end_of_word:
            char = next(iter(node.children.keys()))
            prefix += char
            node = node.children[char]
        
        return prefix


def main() -> None:
    """Demonstration of Trie."""
    print("=" * 70)
    print("TRIE (PREFIX TREE) DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Basic operations
    print("Example 1: Insert and Search")
    print("-" * 70)
    
    trie = Trie()
    words = ["apple", "app", "apricot", "banana", "band", "bandana"]
    
    print(f"Inserting words: {words}")
    for word in words:
        trie.insert(word)
    
    print(f"\nTotal words: {trie.count_words()}")
    
    search_words = ["app", "apple", "apples", "ban", "banana"]
    print("\nSearching:")
    for word in search_words:
        found = trie.search(word)
        print(f"  '{word}': {'Found' if found else 'Not found'}")
    print()
    
    # Example 2: Prefix matching
    print("Example 2: Prefix Matching")
    print("-" * 70)
    
    prefixes = ["app", "ban", "cat", "b"]
    for prefix in prefixes:
        has_prefix = trie.starts_with(prefix)
        print(f"Starts with '{prefix}': {has_prefix}")
    print()
    
    # Example 3: Autocomplete
    print("Example 3: Autocomplete (Words with Prefix)")
    print("-" * 70)
    
    prefixes_auto = ["app", "ban", "b"]
    for prefix in prefixes_auto:
        matches = trie.get_words_with_prefix(prefix)
        print(f"Words starting with '{prefix}': {matches}")
    print()
    
    # Example 4: Deletion
    print("Example 4: Deletion")
    print("-" * 70)
    
    print(f"Before deletion: {trie.get_words_with_prefix('app')}")
    
    trie.delete("app")
    print(f"After deleting 'app': {trie.get_words_with_prefix('app')}")
    
    trie.delete("apple")
    print(f"After deleting 'apple': {trie.get_words_with_prefix('app')}")
    print()
    
    # Example 5: Longest common prefix
    print("Example 5: Longest Common Prefix")
    print("-" * 70)
    
    trie2 = Trie()
    similar_words = ["flower", "flow", "flight"]
    
    print(f"Words: {similar_words}")
    for word in similar_words:
        trie2.insert(word)
    
    lcp = trie2.longest_common_prefix()
    print(f"Longest common prefix: '{lcp}'")
    print()
    
    # Example 6: Performance measurement
    print("Example 6: Performance Measurement")
    print("-" * 70)
    
    timer = PerformanceTimer("Trie")
    
    # Generate random words
    import string
    
    def generate_words(n: int, length: int = 10) -> List[str]:
        words = []
        for _ in range(n):
            word = ''.join(random.choices(string.ascii_lowercase, k=length))
            words.append(word)
        return words
    
    sizes = [100, 500, 1000]
    for size in sizes:
        trie_perf = Trie()
        words_perf = generate_words(size)
        
        def insert_all():
            for word in words_perf:
                trie_perf.insert(word)
        
        _, metrics = timer.measure(insert_all)
        
        print(f"n={size:4d}: {metrics['execution_time_ms']:8.3f} ms, "
              f"{metrics['memory_peak_kb']:8.2f} KB")
    
    print()
    timer.print_summary()
    
    print("\n" + "=" * 70)
    print("\nComplexity Summary:")
    print("  Insert:  O(m) - m is word length")
    print("  Search:  O(m)")
    print("  Delete:  O(m)")
    print("  Prefix:  O(m)")
    print("  Autocomplete: O(m + n) - n is # results")
    print("  Space:   O(ALPHABET_SIZE * m * n)")
    print("\nKey Points:")
    print("  + Fast string operations")
    print("  + Efficient prefix matching")
    print("  + Space sharing for common prefixes")
    print("  + Great for autocomplete")
    print("  + Dictionary operations")
    print("  - Space intensive")
    print("  - Only efficient for strings")
    print("  - Cache unfriendly")
    print("\nApplications:")
    print("  • Autocomplete systems")
    print("  • Spell checkers")
    print("  • IP routing (longest prefix match)")
    print("  • Dictionary implementation")
    print("  • Word games (Scrabble, Boggle)")
    print("  • String matching")
    print("\nWhen to use:")
    print("  • Prefix matching needed")
    print("  • Many string operations")
    print("  • Autocomplete feature")
    print("  • Large dictionaries")
    print("\nWhen NOT to use:")
    print("  • Space is critical")
    print("  • Few strings")
    print("  • Random access more important")
    print("  • Need approximate matching")
    print("=" * 70)


if __name__ == "__main__":
    main()
