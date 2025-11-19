#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hybrid Search implementation.

This file contains the implementation of the Hybrid Search algorithm.
"""

from typing import List, Optional, Dict, Set


class HybridSearch:
    """Hybrid search combining multiple methods."""

    def __init__(self):
        self.searchers: List[dict] = {}

    def add_searcher(self, name: str, searcher: callable, weight: float) -> None:
        """Add search method."""
        self.searchers[name] = {"searcher": searcher, "weight": weight}

    def search(self, query: str, top_k: int = 10) -> List[tuple]:
        """Hybrid search."""
        all_results = []
        for name, searcher_info in self.searchers.items():
            results = searcher_info["searcher"](query)
            weight = searcher_info["weight"]
            for result, score in results:
                all_results.append((result, score * weight))

        # Sort by weighted score
        all_results.sort(key=lambda x: x[1], reverse=True)
        return all_results[:top_k]


def main() -> None:
    """Demonstrate Hybrid Search."""
    print("=" * 70)
    print("HYBRID SEARCH")
    print("=" * 70)

    # Example usage
    print("Algorithm implementation for Hybrid Search")
    print("See implementation above for details.")

    print("=" * 70)


if __name__ == "__main__":
    main()
