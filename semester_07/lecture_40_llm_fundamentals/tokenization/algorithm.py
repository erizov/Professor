#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tokenization implementation.

This file contains the implementation of the Tokenization algorithm.
"""

from typing import List, Optional, Dict, Set


class Tokenization:
    """Text tokenization."""

    def __init__(self):
        self.vocab: Dict[str, int] = {}
        self.token_to_id: Dict[str, int] = {}
        self.id_to_token: Dict[int, str] = {}

    def tokenize(self, text: str) -> List[int]:
        """Tokenize text."""
        tokens = text.split()
        token_ids = []
        for token in tokens:
            if token not in self.token_to_id:
                token_id = len(self.token_to_id)
                self.token_to_id[token] = token_id
                self.id_to_token[token_id] = token
            token_ids.append(self.token_to_id[token])
        return token_ids

    def detokenize(self, token_ids: List[int]) -> str:
        """Detokenize."""
        tokens = [self.id_to_token.get(tid, "<UNK>") for tid in token_ids]
        return " ".join(tokens)


def main() -> None:
    """Demonstrate Tokenization."""
    print("=" * 70)
    print("TOKENIZATION")
    print("=" * 70)

    # Example usage
    print("Algorithm implementation for Tokenization")
    print("See implementation above for details.")

    print("=" * 70)


if __name__ == "__main__":
    main()
