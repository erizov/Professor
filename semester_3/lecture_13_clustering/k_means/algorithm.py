#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
K-Means Clustering implementation.

Unsupervised learning algorithm that partitions data into K clusters by
minimizing within-cluster variance.
"""

import sys
from pathlib import Path
import numpy as np

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer


class KMeans:
    """
    K-Means Clustering Algorithm.
    
    Iteratively assigns points to nearest centroid and updates centroids.
    """
    
    def __init__(self, n_clusters: int = 3, max_iterations: int = 300,
                 random_state: int = None):
        """
        Initialize K-Means.
        
        Args:
            n_clusters: Number of clusters
            max_iterations: Maximum iterations
            random_state: Random seed
        """
        self.n_clusters = n_clusters
        self.max_iterations = max_iterations
        self.random_state = random_state
        self.centroids = None
        self.labels_ = None
        self.inertia_ = None
        self.n_iter_ = 0
    
    def fit(self, X: np.ndarray) -> 'KMeans':
        """
        Fit K-Means to data.
        
        Args:
            X: Data (n_samples, n_features)
            
        Returns:
            self
        """
        if self.random_state is not None:
            np.random.seed(self.random_state)
        
        n_samples, n_features = X.shape
        
        # Initialize centroids randomly
        indices = np.random.choice(n_samples, self.n_clusters, 
                                  replace=False)
        self.centroids = X[indices].copy()
        
        # Iterate until convergence
        for iteration in range(self.max_iterations):
            # Assign clusters
            labels_old = self.labels_
            self.labels_ = self._assign_clusters(X)
            
            # Update centroids
            centroids_old = self.centroids.copy()
            self._update_centroids(X)
            
            # Check convergence
            if np.array_equal(labels_old, self.labels_):
                self.n_iter_ = iteration + 1
                break
        else:
            self.n_iter_ = self.max_iterations
        
        # Calculate inertia (within-cluster sum of squares)
        self.inertia_ = self._calculate_inertia(X)
        
        return self
    
    def _assign_clusters(self, X: np.ndarray) -> np.ndarray:
        """Assign each point to nearest centroid."""
        distances = np.zeros((X.shape[0], self.n_clusters))
        
        for i, centroid in enumerate(self.centroids):
            distances[:, i] = np.linalg.norm(X - centroid, axis=1)
        
        return np.argmin(distances, axis=1)
    
    def _update_centroids(self, X: np.ndarray) -> None:
        """Update centroids as mean of assigned points."""
        for i in range(self.n_clusters):
            cluster_points = X[self.labels_ == i]
            if len(cluster_points) > 0:
                self.centroids[i] = cluster_points.mean(axis=0)
    
    def _calculate_inertia(self, X: np.ndarray) -> float:
        """Calculate within-cluster sum of squares."""
        inertia = 0
        for i in range(self.n_clusters):
            cluster_points = X[self.labels_ == i]
            if len(cluster_points) > 0:
                inertia += np.sum((cluster_points - 
                                  self.centroids[i]) ** 2)
        return inertia
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict cluster for new data.
        
        Args:
            X: Data (n_samples, n_features)
            
        Returns:
            Cluster labels
        """
        return self._assign_clusters(X)
    
    def fit_predict(self, X: np.ndarray) -> np.ndarray:
        """Fit and return cluster labels."""
        self.fit(X)
        return self.labels_


def elbow_method(X: np.ndarray, max_k: int = 10) -> None:
    """
    Perform elbow method to find optimal K.
    
    Args:
        X: Data
        max_k: Maximum K to test
    """
    inertias = []
    
    for k in range(1, max_k + 1):
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(X)
        inertias.append(kmeans.inertia_)
    
    print("K vs Inertia:")
    for k, inertia in enumerate(inertias, 1):
        print(f"  K={k}: {inertia:.2f}")


def main() -> None:
    """Demonstration of K-Means Clustering."""
    print("=" * 70)
    print("K-MEANS CLUSTERING DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Simple clustering
    print("Example 1: Simple 2D Clustering")
    print("-" * 70)
    
    np.random.seed(42)
    
    # Generate 3 clusters
    cluster1 = np.random.randn(30, 2) + np.array([5, 5])
    cluster2 = np.random.randn(30, 2) + np.array([0, 0])
    cluster3 = np.random.randn(30, 2) + np.array([5, 0])
    X = np.vstack([cluster1, cluster2, cluster3])
    
    kmeans = KMeans(n_clusters=3, random_state=42)
    kmeans.fit(X)
    
    print(f"Converged in {kmeans.n_iter_} iterations")
    print(f"Inertia: {kmeans.inertia_:.2f}")
    print(f"\nCentroids:")
    for i, centroid in enumerate(kmeans.centroids):
        print(f"  Cluster {i}: {centroid}")
    print(f"\nCluster sizes:")
    for i in range(3):
        count = np.sum(kmeans.labels_ == i)
        print(f"  Cluster {i}: {count} points")
    print()
    
    # Example 2: Elbow method
    print("Example 2: Elbow Method (Finding Optimal K)")
    print("-" * 70)
    elbow_method(X, max_k=8)
    print("Note: Look for 'elbow' where inertia starts decreasing slowly")
    print()
    
    # Example 3: Prediction on new data
    print("Example 3: Predicting Clusters for New Data")
    print("-" * 70)
    
    new_points = np.array([
        [5.5, 5.5],  # Should be cluster 0
        [0.5, 0.5],  # Should be cluster 1
        [5.5, 0.5],  # Should be cluster 2
    ])
    
    predictions = kmeans.predict(new_points)
    
    for i, (point, label) in enumerate(
        zip(new_points, predictions)):
        print(f"Point {point} → Cluster {label}")
    print()
    
    # Example 4: Different K values
    print("Example 4: Effect of Different K Values")
    print("-" * 70)
    
    for k in [2, 3, 5]:
        kmeans_k = KMeans(n_clusters=k, random_state=42)
        kmeans_k.fit(X)
        print(f"K={k}:")
        print(f"  Iterations: {kmeans_k.n_iter_}")
        print(f"  Inertia: {kmeans_k.inertia_:.2f}")
    print()
    
    # Example 5: Performance measurement
    print("Example 5: Performance on Different Dataset Sizes")
    print("-" * 70)
    
    timer = PerformanceTimer("K-Means")
    
    for n in [100, 1000, 10000]:
        X_large = np.random.randn(n, 10)
        
        def train_model():
            model = KMeans(n_clusters=5, max_iterations=100)
            model.fit(X_large)
            return model
        
        result, metrics = timer.measure(train_model)
        print(f"Dataset size: {n}")
        print(f"  Time: {metrics['execution_time_ms']:.3f} ms")
        print(f"  Iterations: {result.n_iter_}")
        print(f"  Inertia: {result.inertia_:.2f}")
    
    print()
    print("=" * 70)
    print("\nComplexity Summary:")
    print("  Time:  O(n * k * d * iter)")
    print("    n = samples, k = clusters, d = features, iter = iterations")
    print("  Space: O(n + k*d)")
    print("\nKey Advantages:")
    print("  - Simple and easy to implement")
    print("  - Scales well to large datasets")
    print("  - Fast convergence")
    print("  - Works well with spherical clusters")
    print("\nKey Disadvantages:")
    print("  - Must specify K in advance")
    print("  - Sensitive to initial centroids")
    print("  - Assumes spherical clusters")
    print("  - Sensitive to outliers")
    print("  - Only finds local optimum")
    print("\nCommon Use Cases:")
    print("  - Customer segmentation")
    print("  - Image compression")
    print("  - Document clustering")
    print("  - Anomaly detection")
    print("\nTips:")
    print("  - Use elbow method to find optimal K")
    print("  - Run multiple times with different initializations")
    print("  - Scale features before clustering")
    print("  - Consider K-Means++ initialization")
    print("=" * 70)


if __name__ == "__main__":
    main()

