#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
K-Means Clustering implementation.

Unsupervised learning algorithm for clustering data into K groups.
"""

import sys
from pathlib import Path
from typing import List, Tuple
import random
import math

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer


def euclidean_distance(point1: List[float], point2: List[float]) -> float:
    """Calculate Euclidean distance between two points."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(point1, point2)))


class KMeans:
    """
    K-Means Clustering Algorithm.
    
    Groups data into K clusters by minimizing within-cluster variance.
    """
    
    def __init__(self, k: int = 3, max_iters: int = 100, 
                 random_state: int = 42):
        """
        Initialize K-Means.
        
        Args:
            k: Number of clusters
            max_iters: Maximum number of iterations
            random_state: Random seed for initialization
        """
        self.k = k
        self.max_iters = max_iters
        self.random_state = random_state
        self.centroids = []
        self.labels = []
        self.inertia = 0.0  # Sum of squared distances to centroids
        self.history = []
    
    def fit(self, X: List[List[float]]) -> None:
        """
        Fit K-Means to data.
        
        Args:
            X: Training data (n_samples, n_features)
        """
        random.seed(self.random_state)
        n_samples = len(X)
        n_features = len(X[0])
        
        # Initialize centroids randomly from data points
        indices = random.sample(range(n_samples), self.k)
        self.centroids = [X[i][:] for i in indices]
        
        self.labels = [0] * n_samples
        
        for iteration in range(self.max_iters):
            # Assign points to nearest centroid
            new_labels = []
            for point in X:
                distances = [euclidean_distance(point, centroid) 
                           for centroid in self.centroids]
                new_labels.append(distances.index(min(distances)))
            
            # Check for convergence
            if new_labels == self.labels:
                break
            
            self.labels = new_labels
            
            # Update centroids
            new_centroids = []
            for cluster_idx in range(self.k):
                cluster_points = [X[i] for i in range(n_samples) 
                                if self.labels[i] == cluster_idx]
                
                if cluster_points:
                    # Calculate mean of cluster points
                    centroid = [sum(point[j] for point in cluster_points) / 
                              len(cluster_points) 
                              for j in range(n_features)]
                    new_centroids.append(centroid)
                else:
                    # Keep old centroid if cluster is empty
                    new_centroids.append(self.centroids[cluster_idx])
            
            self.centroids = new_centroids
            
            # Calculate inertia (within-cluster sum of squares)
            inertia = sum(euclidean_distance(X[i], 
                                            self.centroids[self.labels[i]])**2 
                         for i in range(n_samples))
            
            self.history.append((iteration, inertia))
        
        # Final inertia
        self.inertia = sum(euclidean_distance(X[i], 
                                             self.centroids[self.labels[i]])**2 
                          for i in range(n_samples))
    
    def predict(self, X: List[List[float]]) -> List[int]:
        """
        Predict cluster labels for new data.
        
        Args:
            X: Data to predict
            
        Returns:
            Cluster labels
        """
        labels = []
        for point in X:
            distances = [euclidean_distance(point, centroid) 
                       for centroid in self.centroids]
            labels.append(distances.index(min(distances)))
        return labels
    
    def fit_predict(self, X: List[List[float]]) -> List[int]:
        """
        Fit and return cluster labels.
        
        Args:
            X: Training data
            
        Returns:
            Cluster labels
        """
        self.fit(X)
        return self.labels


def generate_clusters(n_samples: int, n_clusters: int, 
                     seed: int = 42) -> Tuple[List[List[float]], 
                                              List[int]]:
    """
    Generate synthetic clustered data.
    
    Args:
        n_samples: Samples per cluster
        n_clusters: Number of clusters
        seed: Random seed
        
    Returns:
        (X, true_labels) tuple
    """
    random.seed(seed)
    X = []
    true_labels = []
    
    for cluster in range(n_clusters):
        # Random cluster center
        center = [cluster * 5.0, cluster * 5.0]
        
        for _ in range(n_samples):
            # Add random noise around center
            point = [center[0] + random.gauss(0, 1),
                    center[1] + random.gauss(0, 1)]
            X.append(point)
            true_labels.append(cluster)
    
    return X, true_labels


def main() -> None:
    """Demonstration of K-Means Clustering."""
    print("=" * 70)
    print("K-MEANS CLUSTERING DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Basic clustering
    print("Example 1: Basic Clustering")
    print("-" * 70)
    
    X, true_labels = generate_clusters(30, 3)
    
    print(f"Generated {len(X)} samples in 3 clusters")
    print(f"First few samples: {X[:5]}")
    print()
    
    kmeans = KMeans(k=3, max_iters=100)
    kmeans.fit(X)
    
    print(f"Converged in {len(kmeans.history)} iterations")
    print(f"Final inertia: {kmeans.inertia:.2f}")
    print()
    
    print("Cluster centroids:")
    for i, centroid in enumerate(kmeans.centroids):
        print(f"  Cluster {i}: {[f'{x:.2f}' for x in centroid]}")
    print()
    
    # Example 2: Cluster sizes
    print("Example 2: Cluster Sizes")
    print("-" * 70)
    
    cluster_counts = [0] * kmeans.k
    for label in kmeans.labels:
        cluster_counts[label] += 1
    
    for i, count in enumerate(cluster_counts):
        print(f"  Cluster {i}: {count} samples")
    print()
    
    # Example 3: Predict new points
    print("Example 3: Predicting New Points")
    print("-" * 70)
    
    X_test = [
        [0.0, 0.0],   # Should be cluster 0
        [5.0, 5.0],   # Should be cluster 1
        [10.0, 10.0], # Should be cluster 2
    ]
    
    predictions = kmeans.predict(X_test)
    
    print("Predictions:")
    for point, pred in zip(X_test, predictions):
        print(f"  Point {point} → Cluster {pred}")
    print()
    
    # Example 4: Training progress
    print("Example 4: Training Progress")
    print("-" * 70)
    
    print("Inertia over iterations:")
    for iteration, inertia in kmeans.history[:10]:  # First 10
        print(f"  Iteration {iteration}: Inertia = {inertia:.2f}")
    if len(kmeans.history) > 10:
        print(f"  ... ({len(kmeans.history) - 10} more iterations)")
    print()
    
    # Example 5: Performance measurement
    print("Example 5: Performance Measurement")
    print("-" * 70)
    
    timer = PerformanceTimer("K-Means")
    
    sizes = [100, 500, 1000]
    for size in sizes:
        X_perf, _ = generate_clusters(size // 3, 3)
        model = KMeans(k=3, max_iters=50)
        
        _, metrics = timer.measure(model.fit, X_perf)
        
        print(f"n={size:4d}: {metrics['execution_time_ms']:8.3f} ms, "
              f"{metrics['memory_peak_kb']:8.2f} KB")
    
    print()
    timer.print_summary()
    
    print("\n" + "=" * 70)
    print("\nComplexity Summary:")
    print("  Time:  O(n*k*d*i)")
    print("         n=samples, k=clusters, d=features, i=iterations")
    print("  Space: O(n + k*d)")
    print("\nKey Points:")
    print("  + Simple and fast")
    print("  + Works well for spherical clusters")
    print("  + Scalable to large datasets")
    print("  + Easy to interpret")
    print("  - Requires knowing K in advance")
    print("  - Sensitive to initialization")
    print("  - Assumes spherical clusters")
    print("  - Sensitive to outliers")
    print("\nWhen to use:")
    print("  • Know number of clusters")
    print("  • Spherical, similar-sized clusters")
    print("  • Large datasets")
    print("  • Need fast clustering")
    print("\nWhen NOT to use:")
    print("  • Unknown number of clusters")
    print("  • Non-spherical clusters")
    print("  • Many outliers")
    print("  • Very different cluster sizes")
    print("=" * 70)


if __name__ == "__main__":
    main()
