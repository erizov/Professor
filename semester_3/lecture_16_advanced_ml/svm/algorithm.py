#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Support Vector Machine (SVM) Algorithm.

Supervised learning algorithm used for classification and regression.
Finds optimal hyperplane that separates classes with maximum margin.
"""

import sys
from pathlib import Path
import random
import math
from typing import List, Tuple, Optional

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer
from framework.logging_utils import get_logger
logger = get_logger(__name__)


class SVM:
    """Simple Support Vector Machine implementation."""
    
    def __init__(self, learning_rate: float = 0.01, lambda_param: float = 0.01, 
                 n_iters: int = 1000):
        """
        Initialize SVM.
        
        Args:
            learning_rate: Learning rate for gradient descent
            lambda_param: Regularization parameter
            n_iters: Number of iterations
        """
        self.learning_rate = learning_rate
        self.lambda_param = lambda_param
        self.n_iters = n_iters
        self.w: Optional[List[float]] = None
        self.b: float = 0.0
    
    def fit(self, X: List[List[float]], y: List[int]) -> None:
        """
        Train SVM.
        
        Args:
            X: Feature vectors
            y: Labels (-1 or 1)
        """
        n_samples, n_features = len(X), len(X[0]) if X else 0
        
        # Initialize weights
        self.w = [0.0] * n_features
        self.b = 0.0
        
        # Convert labels to -1 or 1
        y_ = [1 if label > 0 else -1 for label in y]
        
        # Gradient descent
        for _ in range(self.n_iters):
            for idx, x_i in enumerate(X):
                condition = y_[idx] * (self._dot_product(x_i, self.w) - self.b) >= 1
                
                if condition:
                    # Update weights with regularization
                    for j in range(n_features):
                        self.w[j] -= self.learning_rate * (2 * self.lambda_param * self.w[j])
                else:
                    # Update weights with loss
                    for j in range(n_features):
                        self.w[j] -= self.learning_rate * (
                            2 * self.lambda_param * self.w[j] - 
                            y_[idx] * x_i[j]
                        )
                    self.b -= self.learning_rate * y_[idx]
    
    def _dot_product(self, a: List[float], b: List[float]) -> float:
        """Calculate dot product."""
        return sum(a[i] * b[i] for i in range(len(a)))
    
    def predict(self, X: List[List[float]]) -> List[int]:
        """
        Predict labels.
        
        Args:
            X: Feature vectors
            
        Returns:
            Predicted labels
        """
        predictions = []
        for x in X:
            linear_output = self._dot_product(x, self.w) - self.b
            predictions.append(1 if linear_output > 0 else -1)
        return predictions
    
    def decision_function(self, X: List[List[float]]) -> List[float]:
        """Get decision function values."""
        return [self._dot_product(x, self.w) - self.b for x in X]


def main() -> None:
    """Demonstration of SVM Algorithm."""
    logger.info("=" * 70)
    logger.info("SUPPORT VECTOR MACHINE (SVM) DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Simple Binary Classification
    logger.info("Example 1: Binary Classification")
    logger.info("-" * 70)
    
    # Linearly separable data
    X = [
        [1.0, 2.0], [2.0, 1.0], [2.0, 3.0], [3.0, 2.0],  # Class 1
        [6.0, 5.0], [7.0, 6.0], [8.0, 7.0], [7.0, 8.0],  # Class -1
    ]
    y = [1, 1, 1, 1, -1, -1, -1, -1]
    
    # Train SVM
    svm = SVM(learning_rate=0.001, lambda_param=0.01, n_iters=1000)
    svm.fit(X, y)
    
    logger.info(f"Weights: {[f'{w:.3f}' for w in svm.w]}")
    logger.info(f"Bias: {svm.b:.3f}")
    logger.info()
    
    # Predict
    test_X = [[1.5, 2.5], [7.5, 6.5]]
    predictions = svm.predict(test_X)
    
    logger.info("Predictions:")
    for i, (x, pred) in enumerate(zip(test_X, predictions)):
        logger.info(f"  Sample {i+1} {x}: {pred}")
    logger.info()
    
    # Example 2: Decision Function
    logger.info("Example 2: Decision Function Values")
    logger.info("-" * 70)
    
    decision_values = svm.decision_function(test_X)
    for i, (x, dv) in enumerate(zip(test_X, decision_values)):
        margin = abs(dv)
        logger.info(f"Sample {i+1} {x}:")
        logger.info(f"  Decision value: {dv:.3f}")
        logger.info(f"  Margin: {margin:.3f}")
    logger.info()
    
    # Example 3: Performance measurement
    logger.info("Example 3: Performance Measurement")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("SVM")
    
    # Generate larger dataset
    X_large = []
    y_large = []
    for _ in range(50):
        if random.random() < 0.5:
            X_large.append([random.random() * 3, random.random() * 3])
            y_large.append(1)
        else:
            X_large.append([random.random() * 3 + 5, random.random() * 3 + 5])
            y_large.append(-1)
    
    def train_svm():
        svm = SVM(learning_rate=0.001, lambda_param=0.01, n_iters=500)
        svm.fit(X_large, y_large)
        return len(svm.w)
    
    result, metrics = timer.measure(train_svm)
    logger.info(f"Time to train SVM on 50 samples: {metrics['execution_time_ms']:.3f} ms")
    logger.info(f"Features: {result}")
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nAlgorithm Summary:")
    logger.info("\nDescription:")
    logger.info("  Supervised learning algorithm that finds optimal hyperplane")
    logger.info("  separating classes with maximum margin.")
    logger.info("\nTime Complexity:")
    logger.info("  Training: O(n² * m) to O(n³ * m) where:")
    logger.info("    n = number of samples")
    logger.info("    m = number of features")
    logger.info("  Prediction: O(m)")
    logger.info("\nKey Advantages:")
    logger.info("  - Effective in high dimensions")
    logger.info("  - Memory efficient")
    logger.info("  - Versatile (different kernels)")
    logger.info("  - Works well with clear margin")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Poor performance on large datasets")
    logger.info("  - Doesn't work well with noise")
    logger.info("  - No probability estimates")
    logger.info("  - Sensitive to feature scaling")
    logger.info("\nWhen to Use:")
    logger.info("  - Binary classification")
    logger.info("  - High-dimensional data")
    logger.info("  - Clear margin of separation")
    logger.info("  - Text classification")
    logger.info("\nCommon Use Cases:")
    logger.info("  - Text classification")
    logger.info("  - Image classification")
    logger.info("  - Handwriting recognition")
    logger.info("  - Bioinformatics")
    logger.info("\nKernel Types:")
    logger.info("  - Linear: For linearly separable data")
    logger.info("  - Polynomial: For non-linear data")
    logger.info("  - RBF: For complex non-linear patterns")
    logger.info("  - Sigmoid: Neural network-like")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()