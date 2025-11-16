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
from framework.logging_utils import get_logger
logger = get_logger(__name__)


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
    logger.info("=" * 70)
    logger.info("K-NEAREST NEIGHBORS (KNN) DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Simple 2D classification
    logger.info("Example 1: 2D Classification")
    logger.info("-" * 70)
    
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
    
    logger.info(f"Training samples: {len(X_train)}")
    logger.info(f"Test samples: {len(X_test)}")
    logger.info(f"k = {knn.k}")
    logger.info()
    logger.info("Predictions:")
    for i, (x, pred, true) in enumerate(
        zip(X_test, predictions, y_test), 1
    ):
        match = "✓" if pred == true else "✗"
        logger.info(f"  {i}. {x} → Predicted: {pred}, True: {true} {match}")
    logger.info(f"\nAccuracy: {accuracy:.2%}")
    logger.info()
    
    # Example 2: Effect of k
    logger.info("Example 2: Effect of Different k Values")
    logger.info("-" * 70)
    
    for k in [1, 3, 5, 7]:
        knn_k = KNNClassifier(k=k)
        knn_k.fit(X_train, y_train)
        acc = knn_k.score(X_test, y_test)
        logger.info(f"k={k}: Accuracy = {acc:.2%}")
    logger.info()
    
    # Example 3: Performance measurement
    logger.info("Example 3: Performance Measurement")
    logger.info("-" * 70)
    
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
    
    logger.info(f"Dataset size: {len(X_large)} samples")
    logger.info(f"Training time: {train_metrics['execution_time_ms']:.3f} ms")
    logger.info(f"Prediction time: {test_metrics['execution_time_ms']:.3f} ms")
    logger.info(f"Memory used: {test_metrics['memory_peak_kb']:.2f} KB")
    logger.info(f"Accuracy: {accuracy_large:.2%}")
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nComplexity Summary:")
    logger.info("  Training Time:  O(1) - just stores data")
    logger.info("  Prediction Time: O(n*d) - n samples, d dimensions")
    logger.info("  Space: O(n*d) - stores all training data")
    logger.info("\nKey Points:")
    logger.info("  - No training phase (lazy learning)")
    logger.info("  - Slow prediction for large datasets")
    logger.info("  - Sensitive to feature scaling")
    logger.info("  - Works well for small datasets")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()