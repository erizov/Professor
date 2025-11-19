#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kmeans implementation.

This file contains the implementation of the Kmeans algorithm.
"""

from typing import List, Optional, Dict, Set


def kmeans(data: List[List[float]], k: int, max_iters: int = 100) -> List[List[float]]:
    """K-means clustering algorithm."""
    import random
    import math

    n = len(data)
    dim = len(data[0]) if data else 0

    # Initialize centroids randomly
    centroids = [data[random.randint(0, n - 1)][:] for _ in range(k)]

    for _ in range(max_iters):
        # Assign points to nearest centroid
        clusters = [[] for _ in range(k)]
        for point in data:
            distances = [
                math.sqrt(sum((point[i] - centroids[j][i]) ** 2 for i in range(dim)))
                for j in range(k)
            ]
            nearest = distances.index(min(distances))
            clusters[nearest].append(point)

        # Update centroids
        new_centroids = []
        for cluster in clusters:
            if cluster:
                new_centroid = [
                    sum(point[i] for point in cluster) / len(cluster)
                    for i in range(dim)
                ]
                new_centroids.append(new_centroid)
            else:
                new_centroids.append(centroids[clusters.index(cluster)])

        if new_centroids == centroids:
            break
        centroids = new_centroids

    return centroids


def main() -> None:
    """Demonstrate Kmeans."""
    print("=" * 70)
    print("KMEANS")
    print("=" * 70)

    # Example usage
    print("Algorithm implementation for Kmeans")
    print("See implementation above for details.")

    print("=" * 70)


if __name__ == "__main__":
    main()
