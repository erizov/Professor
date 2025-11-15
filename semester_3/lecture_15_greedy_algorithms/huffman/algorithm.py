#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Huffman Coding - Greedy Algorithm.

Lossless data compression algorithm that assigns variable-length codes
to characters based on their frequencies. More frequent characters get
shorter codes.
"""

import sys
from pathlib import Path
from heapq import heappush, heappop
from typing import Dict, Tuple, Optional
from collections import Counter

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer


class HuffmanNode:
    """Node in Huffman tree."""
    
    def __init__(self, char: Optional[str], freq: int, 
                 left: Optional['HuffmanNode'] = None,
                 right: Optional['HuffmanNode'] = None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right
    
    def __lt__(self, other: 'HuffmanNode') -> bool:
        """For priority queue ordering."""
        return self.freq < other.freq
    
    def is_leaf(self) -> bool:
        """Check if node is leaf."""
        return self.left is None and self.right is None


class HuffmanCoding:
    """Huffman coding implementation."""
    
    def __init__(self):
        self.root: Optional[HuffmanNode] = None
        self.codes: Dict[str, str] = {}
        self.reverse_codes: Dict[str, str] = {}
    
    def build_tree(self, text: str) -> None:
        """
        Build Huffman tree from text.
        
        Args:
            text: Input text
        """
        if not text:
            return
        
        # Count character frequencies
        freq = Counter(text)
        
        # Create priority queue (min heap)
        heap = []
        for char, count in freq.items():
            node = HuffmanNode(char, count)
            heappush(heap, node)
        
        # Build tree
        while len(heap) > 1:
            # Extract two nodes with minimum frequency
            left = heappop(heap)
            right = heappop(heap)
            
            # Create internal node
            merged = HuffmanNode(None, left.freq + right.freq, left, right)
            heappush(heap, merged)
        
        self.root = heappop(heap) if heap else None
        self._generate_codes(self.root, "")
    
    def _generate_codes(self, node: Optional[HuffmanNode], code: str) -> None:
        """Generate Huffman codes recursively."""
        if node is None:
            return
        
        if node.is_leaf():
            if code:  # Non-empty code
                self.codes[node.char] = code
                self.reverse_codes[code] = node.char
            else:  # Single character case
                self.codes[node.char] = "0"
                self.reverse_codes["0"] = node.char
        else:
            self._generate_codes(node.left, code + "0")
            self._generate_codes(node.right, code + "1")
    
    def encode(self, text: str) -> str:
        """
        Encode text using Huffman codes.
        
        Args:
            text: Text to encode
            
        Returns:
            Encoded binary string
        """
        if not self.codes:
            self.build_tree(text)
        
        encoded = ""
        for char in text:
            if char in self.codes:
                encoded += self.codes[char]
            else:
                raise ValueError(f"Character '{char}' not in encoding table")
        
        return encoded
    
    def decode(self, encoded: str) -> str:
        """
        Decode binary string using Huffman tree.
        
        Args:
            encoded: Encoded binary string
            
        Returns:
            Decoded text
        """
        if not self.root:
            raise ValueError("Huffman tree not built")
        
        decoded = ""
        current = self.root
        
        for bit in encoded:
            if bit == "0":
                current = current.left
            else:
                current = current.right
            
            if current.is_leaf():
                decoded += current.char
                current = self.root
        
        return decoded
    
    def get_codes(self) -> Dict[str, str]:
        """Get encoding table."""
        return self.codes.copy()
    
    def compression_ratio(self, original: str, encoded: str) -> float:
        """Calculate compression ratio."""
        original_bits = len(original) * 8  # Assuming 8 bits per character
        encoded_bits = len(encoded)
        return encoded_bits / original_bits if original_bits > 0 else 0.0


def main() -> None:
    """Demonstration of Huffman Coding."""
    print("=" * 70)
    print("HUFFMAN CODING DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Basic encoding/decoding
    print("Example 1: Basic Encoding and Decoding")
    print("-" * 70)
    
    text = "hello world"
    huffman = HuffmanCoding()
    huffman.build_tree(text)
    
    print(f"Original text: '{text}'")
    print(f"Character frequencies: {Counter(text)}")
    print()
    
    codes = huffman.get_codes()
    print("Huffman codes:")
    for char, code in sorted(codes.items()):
        print(f"  '{char}': {code}")
    print()
    
    encoded = huffman.encode(text)
    print(f"Encoded: {encoded}")
    print(f"Original size: {len(text) * 8} bits")
    print(f"Encoded size: {len(encoded)} bits")
    print(f"Compression ratio: {huffman.compression_ratio(text, encoded):.2%}")
    print()
    
    decoded = huffman.decode(encoded)
    print(f"Decoded: '{decoded}'")
    print(f"Match: {text == decoded}")
    print()
    
    # Example 2: Different texts
    print("Example 2: Different Text Examples")
    print("-" * 70)
    
    texts = [
        "aabbcc",
        "mississippi",
        "the quick brown fox",
    ]
    
    for text in texts:
        huff = HuffmanCoding()
        huff.build_tree(text)
        encoded = huff.encode(text)
        decoded = huff.decode(encoded)
        
        print(f"Text: '{text}'")
        print(f"  Encoded: {encoded}")
        print(f"  Compression: {huff.compression_ratio(text, encoded):.2%}")
        print(f"  Decoded correctly: {text == decoded}")
        print()
    
    # Example 3: Performance measurement
    print("Example 3: Performance Measurement")
    print("-" * 70)
    
    text = "the quick brown fox jumps over the lazy dog" * 100
    
    timer = PerformanceTimer("Huffman Coding")
    
    def huffman_operations():
        huff = HuffmanCoding()
        huff.build_tree(text)
        encoded = huff.encode(text)
        decoded = huff.decode(encoded)
        return len(encoded)
    
    result, metrics = timer.measure(huffman_operations)
    print(f"Text length: {len(text)} characters")
    print(f"Time: {metrics['execution_time_ms']:.3f} ms")
    print(f"Encoded size: {result} bits")
    print()
    
    # Example 4: Compression efficiency
    print("Example 4: Compression Efficiency")
    print("-" * 70)
    
    test_texts = [
        ("Repeated", "aaaaabbbbbccccc"),
        ("Balanced", "abcdefghijklmnop"),
        ("Real text", "The quick brown fox jumps over the lazy dog. " * 10),
    ]
    
    for name, text in test_texts:
        huff = HuffmanCoding()
        huff.build_tree(text)
        encoded = huff.encode(text)
        ratio = huff.compression_ratio(text, encoded)
        
        print(f"{name}:")
        print(f"  Original: {len(text) * 8} bits")
        print(f"  Encoded: {len(encoded)} bits")
        print(f"  Ratio: {ratio:.2%}")
        print()
    
    print("=" * 70)
    print("\nComplexity Summary:")
    print("  Build Tree: O(n log n) - n is number of unique characters")
    print("  Encode:     O(m) - m is text length")
    print("  Decode:     O(m) - m is encoded length")
    print("  Space:      O(n) - for tree and codes")
    print("\nKey Advantages:")
    print("  - Optimal prefix code")
    print("  - Lossless compression")
    print("  - Efficient for skewed frequencies")
    print("  - Widely used")
    print("\nKey Disadvantages:")
    print("  - Requires frequency analysis")
    print("  - Not optimal for all distributions")
    print("  - Tree overhead")
    print("\nWhen to Use:")
    print("  - Text compression")
    print("  - File compression")
    print("  - Data transmission")
    print("  - Skewed frequency distributions")
    print("\nCommon Use Cases:")
    print("  - ZIP compression")
    print("  - Image compression (JPEG)")
    print("  - Network protocols")
    print("  - Data storage")
    print("=" * 70)


if __name__ == "__main__":
    main()
