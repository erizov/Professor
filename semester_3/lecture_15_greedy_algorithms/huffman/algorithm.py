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
from framework.logging_utils import get_logger
logger = get_logger(__name__)


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
    logger.info("=" * 70)
    logger.info("HUFFMAN CODING DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Basic encoding/decoding
    logger.info("Example 1: Basic Encoding and Decoding")
    logger.info("-" * 70)
    
    text = "hello world"
    huffman = HuffmanCoding()
    huffman.build_tree(text)
    
    logger.info(f"Original text: '{text}'")
    logger.info(f"Character frequencies: {Counter(text)}")
    logger.info()
    
    codes = huffman.get_codes()
    logger.info("Huffman codes:")
    for char, code in sorted(codes.items()):
        logger.info(f"  '{char}': {code}")
    logger.info()
    
    encoded = huffman.encode(text)
    logger.info(f"Encoded: {encoded}")
    logger.info(f"Original size: {len(text) * 8} bits")
    logger.info(f"Encoded size: {len(encoded)} bits")
    logger.info(f"Compression ratio: {huffman.compression_ratio(text, encoded):.2%}")
    logger.info()
    
    decoded = huffman.decode(encoded)
    logger.info(f"Decoded: '{decoded}'")
    logger.info(f"Match: {text == decoded}")
    logger.info()
    
    # Example 2: Different texts
    logger.info("Example 2: Different Text Examples")
    logger.info("-" * 70)
    
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
        
        logger.info(f"Text: '{text}'")
        logger.info(f"  Encoded: {encoded}")
        logger.info(f"  Compression: {huff.compression_ratio(text, encoded):.2%}")
        logger.info(f"  Decoded correctly: {text == decoded}")
        logger.info()
    
    # Example 3: Performance measurement
    logger.info("Example 3: Performance Measurement")
    logger.info("-" * 70)
    
    text = "the quick brown fox jumps over the lazy dog" * 100
    
    timer = PerformanceTimer("Huffman Coding")
    
    def huffman_operations():
        huff = HuffmanCoding()
        huff.build_tree(text)
        encoded = huff.encode(text)
        decoded = huff.decode(encoded)
        return len(encoded)
    
    result, metrics = timer.measure(huffman_operations)
    logger.info(f"Text length: {len(text)} characters")
    logger.info(f"Time: {metrics['execution_time_ms']:.3f} ms")
    logger.info(f"Encoded size: {result} bits")
    logger.info()
    
    # Example 4: Compression efficiency
    logger.info("Example 4: Compression Efficiency")
    logger.info("-" * 70)
    
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
        
        logger.info(f"{name}:")
        logger.info(f"  Original: {len(text) * 8} bits")
        logger.info(f"  Encoded: {len(encoded)} bits")
        logger.info(f"  Ratio: {ratio:.2%}")
        logger.info()
    
    logger.info("=" * 70)
    logger.info("\nComplexity Summary:")
    logger.info("  Build Tree: O(n log n) - n is number of unique characters")
    logger.info("  Encode:     O(m) - m is text length")
    logger.info("  Decode:     O(m) - m is encoded length")
    logger.info("  Space:      O(n) - for tree and codes")
    logger.info("\nKey Advantages:")
    logger.info("  - Optimal prefix code")
    logger.info("  - Lossless compression")
    logger.info("  - Efficient for skewed frequencies")
    logger.info("  - Widely used")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Requires frequency analysis")
    logger.info("  - Not optimal for all distributions")
    logger.info("  - Tree overhead")
    logger.info("\nWhen to Use:")
    logger.info("  - Text compression")
    logger.info("  - File compression")
    logger.info("  - Data transmission")
    logger.info("  - Skewed frequency distributions")
    logger.info("\nCommon Use Cases:")
    logger.info("  - ZIP compression")
    logger.info("  - Image compression (JPEG)")
    logger.info("  - Network protocols")
    logger.info("  - Data storage")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()