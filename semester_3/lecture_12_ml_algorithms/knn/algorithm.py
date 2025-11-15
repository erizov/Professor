#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
K-Nearest Neighbors (KNN) implementation.

A simple, instance-based learning algorithm for classification
and regression.
"""

import sys
from pathlib import Path
from typing import List, Tuple
from collections import Counter
import math

# Add framework to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from framework.performance_timer import PerformanceTimer


def euclidean_distance(point1: List[float], point2: List[float]) -> float:
    """
    Calculate Euclidean distance between two points.
    
    Args:
        point1: First point coordinates
        point2: Second point coordinates
        
    Returns:
        Euclidean distance
    """
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(point1, point2)))


class KNNClassifier:
    """K-Nearest Neighbors Classifier."""
    
    def __init__(self, k: int = 3):
        """
        Initialize KNN classifier.
        
        Args:
            k: Number of neighbors to consider
        """
        self.k = k
        self.X_train = None
        self.y_train = None
    
    def fit(self, X: List[List[float]], y: List[int]) -> None:
        """
        Train the model (just store the training data).
        
        Args:
            X: Training features
            y: Training labels
        """
        self.X_train = X
        self.y_train = y
    
    def predict_single(self, x: List[float]) -> int:
        """
        Predict class for a single sample.
        
        Args:
            x: Sample features
            
        Returns:
            Predicted class
        """
        # Calculate distances to all training points
        distances = [
            (euclidean_distance(x, x_train), y)
            for x_train, y in zip(self.X_train, self.y_train)
        ]
        
        # Sort by distance and get k nearest
        distances.sort(key=lambda pair: pair[0])
        k_nearest = distances[:self.k]
        
        # Majority vote
        k_nearest_labels = [label for _, label in k_nearest]
        return Counter(k_nearest_labels).most_common(1)[0][0]
    
    def predict(self, X: List[List[float]]) -> List[int]:
        """
        Predict classes for multiple samples.
        
        Args:
            X: Test features
            
        Returns:
            Predicted classes
        """
        return [self.predict_single(x) for x in X]
    
    def score(self, X: List[List[float]], y: List[int]) -> float:
        """
        Calculate accuracy.
        
        Args:
            X: Test features
            y: True labels
            
        Returns:
            Accuracy score
        """
        predictions = self.predict(X)
        correct = sum(pred == true for pred, true in zip(predictions, y))
        return correct / len(y)


def main() -> None:
    """Demonstration of K-Nearest Neighbors."""
    print("=" * 70)
    print("K-NEAREST NEIGHBORS (KNN) DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Simple 2D classification
    print("Example 1: 2D Classification")
    print("-" * 70)
    
    # Training data: [x, y] coordinates with labels (0 or 1)
    X_train = [
        [1.0, 1.0], [1.5, 1.5], [2.0, 2.0],  # Class 0
        [5.0, 5.0], [5.5, 5.5], [6.0, 6.0],  # Class 1
        [1.2, 1.8], [2.1, 1.9],              # Class 0
        [5.2, 5.8], [6.1, 5.9],              # Class 1
    ]
    y_train = [0, 0, 0, 1, 1, 1, 0, 0, 1, 1]
    
    # Test data
    X_test = [
        [1.1, 1.2],  # Should be class 0
        [5.8, 5.9],  # Should be class 1
        [2.5, 2.5],  # Should be class 0
        [5.0, 4.8],  # Should be class 1
    ]
    y_test = [0, 1, 0, 1]
    
    # Train and predict
    knn = KNNClassifier(k=3)
    knn.fit(X_train, y_train)
    
    predictions = knn.predict(X_test)
    accuracy = knn.score(X_test, y_test)
    
    print(f"Training samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")
    print(f"k = {knn.k}")
    print()
    print("Predictions:")
    for i, (x, pred, true) in enumerate(
        zip(X_test, predictions, y_test), 1
    ):
        match = "✓" if pred == true else "✗"
        print(f"  {i}. {x} → Predicted: {pred}, True: {true} {match}")
    print(f"\nAccuracy: {accuracy:.2%}")
    print()
    
    # Example 2: Effect of k
    print("Example 2: Effect of Different k Values")
    print("-" * 70)
    
    for k in [1, 3, 5, 7]:
        knn_k = KNNClassifier(k=k)
        knn_k.fit(X_train, y_train)
        acc = knn_k.score(X_test, y_test)
        print(f"k={k}: Accuracy = {acc:.2%}")
    print()
    
    # Example 3: Performance measurement
    print("Example 3: Performance Measurement")
    print("-" * 70)
    
    timer = PerformanceTimer("KNN Classification")
    
    # Larger dataset
    import random
    random.seed(42)
    
    # Generate synthetic data
    X_large = []
    y_large = []
    for _ in range(100):
        # Class 0: points around (2, 2)
        X_large.append([
            random.gauss(2, 0.5), 
            random.gauss(2, 0.5)
        ])
        y_large.append(0)
        
        # Class 1: points around (6, 6)
        X_large.append([
            random.gauss(6, 0.5), 
            random.gauss(6, 0.5)
        ])
        y_large.append(1)
    
    # Split into train/test
    split = int(0.8 * len(X_large))
    X_train_large = X_large[:split]
    y_train_large = y_large[:split]
    X_test_large = X_large[split:]
    y_test_large = y_large[split:]
    
    knn_large = KNNClassifier(k=5)
    
    # Measure training (just stores data)
    _, train_metrics = timer.measure(
        knn_large.fit, X_train_large, y_train_large
    )
    
    # Measure prediction
    _, test_metrics = timer.measure(
        knn_large.predict, X_test_large
    )
    
    accuracy_large = knn_large.score(X_test_large, y_test_large)
    
    print(f"Dataset size: {len(X_large)} samples")
    print(f"Training time: {train_metrics['execution_time_ms']:.3f} ms")
    print(f"Prediction time: {test_metrics['execution_time_ms']:.3f} ms")
    print(f"Memory used: {test_metrics['memory_peak_kb']:.2f} KB")
    print(f"Accuracy: {accuracy_large:.2%}")
    print()
    
    print("=" * 70)
    print("\nComplexity Summary:")
    print("  Training Time:  O(1) - just stores data")
    print("  Prediction Time: O(n*d) - n samples, d dimensions")
    print("  Space: O(n*d) - stores all training data")
    print("\nKey Points:")
    print("  - No training phase (lazy learning)")
    print("  - Slow prediction for large datasets")
    print("  - Sensitive to feature scaling")
    print("  - Works well for small datasets")
    print("=" * 70)


if __name__ == "__main__":
    main()
