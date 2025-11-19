#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Knn implementation.

This file contains the implementation of the Knn algorithm.
"""

from typing import List, Optional, Dict, Set


def knn(
    X_train: List[List[float]], y_train: List[any], X_test: List[float], k: int = 3
) -> any:
    """K-Nearest Neighbors classification."""
    import math

    distances = []
    for i, x_train in enumerate(X_train):
        dist = math.sqrt(sum((X_test[j] - x_train[j]) ** 2 for j in range(len(X_test))))
        distances.append((dist, y_train[i]))

    distances.sort(key=lambda x: x[0])
    k_nearest = [label for _, label in distances[:k]]

    # Return most common label
    return max(set(k_nearest), key=k_nearest.count)


def main() -> None:
    """Demonstrate Knn."""
    print("=" * 70)
    print("KNN")
    print("=" * 70)

    # Example usage
    print("Algorithm implementation for Knn")
    print("See implementation above for details.")

    print("=" * 70)


if __name__ == "__main__":
    main()
