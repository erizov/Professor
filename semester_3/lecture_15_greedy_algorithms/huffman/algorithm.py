#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Huffman implementation.

This file contains the implementation of the Huffman algorithm.
"""

from typing import List, Optional, Dict, Set


class HuffmanNode:
    """Huffman tree node."""
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right
    
    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text: str) -> HuffmanNode:
    """Build Huffman tree."""
    from collections import Counter
    from heapq import heappush, heappop
    
    freq = Counter(text)
    heap = []
    
    for char, count in freq.items():
        heappush(heap, HuffmanNode(char=char, freq=count))
    
    while len(heap) > 1:
        left = heappop(heap)
        right = heappop(heap)
        merged = HuffmanNode(freq=left.freq + right.freq, left=left, right=right)
        heappush(heap, merged)
    
    return heap[0] if heap else None

def build_huffman_codes(root: HuffmanNode, code: str = "", codes: dict = None) -> dict:
    """Build Huffman codes."""
    if codes is None:
        codes = {}
    
    if root.char is not None:
        codes[root.char] = code
    else:
        if root.left:
            build_huffman_codes(root.left, code + "0", codes)
        if root.right:
            build_huffman_codes(root.right, code + "1", codes)
    
    return codes


def main() -> None:
    """Demonstrate Huffman."""
    print("=" * 70)
    print("HUFFMAN")
    print("=" * 70)
    
    # Example usage
    print("Algorithm implementation for Huffman")
    print("See implementation above for details.")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
