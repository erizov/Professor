#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Support Vector Machine (SVM) implementation.

Binary classifier that finds optimal hyperplane to separate classes
with maximum margin.
"""

import sys
from pathlib import Path
import numpy as np

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer
from framework.logging_utils import get_logger
logger = get_logger(__name__)


class SVM:
    """
    Support Vector Machine using gradient descent.
    
    Simplified implementation for educational purposes.
    """
    
    def __init__(self, learning_rate: float = 0.01, 
                 lambda_param: float = 0.01,
                 n_iterations: int = 1000):
        """
        Initialize SVM.
        
        Args:
            learning_rate: Learning rate for gradient descent
            lambda_param: Regularization parameter
            n_iterations: Number of iterations
        """
        self.learning_rate = learning_rate
        self.lambda_param = lambda_param
        self.n_iterations = n_iterations
        self.weights = None
        self.bias = None
    
    def fit(self, X: np.ndarray, y: np.ndarray) -> 'SVM':
        """
        Fit SVM model.
        
        Args:
            X: Training features (n_samples, n_features)
            y: Training labels (n_samples,) - binary -1 or 1
            
        Returns:
            self
        """
        n_samples, n_features = X.shape
        
        # Convert labels to -1 and 1 if needed
        y_ = np.where(y <= 0, -1, 1)
        
        # Initialize weights and bias
        self.weights = np.zeros(n_features)
        self.bias = 0
        
        # Gradient descent
        for _ in range(self.n_iterations):
            for idx, x_i in enumerate(X):
                condition = y_[idx] * (np.dot(x_i, self.weights) - self.bias) >= 1
                
                if condition:
                    # Update weights with regularization
                    self.weights -= self.learning_rate * (2 * self.lambda_param * self.weights)
                else:
                    # Update weights with loss
                    self.weights -= self.learning_rate * (
                        2 * self.lambda_param * self.weights - 
                        np.dot(x_i, y_[idx])
                    )
                    self.bias -= self.learning_rate * y_[idx]
        
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict class labels.
        
        Args:
            X: Features (n_samples, n_features)
            
        Returns:
            Predicted labels (-1 or 1)
        """
        linear_output = np.dot(X, self.weights) - self.bias
        return np.sign(linear_output)
    
    def decision_function(self, X: np.ndarray) -> np.ndarray:
        """
        Compute decision function values.
        
        Args:
            X: Features
            
        Returns:
            Decision function values
        """
        return np.dot(X, self.weights) - self.bias


def main() -> None:
    """Demonstration of SVM."""
    logger.info("=" * 70)
    logger.info("SUPPORT VECTOR MACHINE (SVM) DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Linearly separable data
    logger.info("Example 1: Linearly Separable Data")
    logger.info("-" * 70)
    
    np.random.seed(42)
    
    # Generate linearly separable data
    X_class1 = np.random.randn(20, 2) + np.array([2, 2])
    X_class2 = np.random.randn(20, 2) + np.array([-2, -2])
    X = np.vstack([X_class1, X_class2])
    y = np.array([1] * 20 + [-1] * 20)
    
    # Shuffle
    indices = np.random.permutation(len(y))
    X, y = X[indices], y[indices]
    
    svm = SVM(learning_rate=0.01, lambda_param=0.01, n_iterations=1000)
    svm.fit(X, y)
    
    predictions = svm.predict(X)
    accuracy = np.mean(predictions == y)
    
    logger.info(f"Training accuracy: {accuracy:.4f}")
    logger.info(f"Weights: {svm.weights}")
    logger.info(f"Bias: {svm.bias:.4f}")
    logger.info()
    
    # Example 2: Decision boundary
    logger.info("Example 2: Decision Boundary")
    logger.info("-" * 70)
    
    test_points = np.array([
        [3, 3],    # Should be class 1
        [-3, -3],  # Should be class -1
        [0, 0],    # Near decision boundary
    ])
    
    decisions = svm.decision_function(test_points)
    predictions2 = svm.predict(test_points)
    
    for i, (point, decision, pred) in enumerate(
        zip(test_points, decisions, predictions2)):
        logger.info(f"Point {point}:")
        logger.info(f"  Decision value: {decision:.4f}")
        logger.info(f"  Predicted class: {pred}")
    logger.info()
    
    # Example 3: Performance measurement
    logger.info("Example 3: Performance on Different Dataset Sizes")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("SVM")
    
    for n in [50, 200, 500]:
        X = np.random.randn(n, 5)
        y = (X[:, 0] + X[:, 1] > 0).astype(int)
        y = np.where(y == 0, -1, 1)
        
        def train_svm():
            model = SVM(n_iterations=100)
            model.fit(X, y)
            return model
        
        result, metrics = timer.measure(train_svm)
        accuracy = np.mean(result.predict(X) == y)
        logger.info(f"Dataset size: {n}")
        logger.info(f"  Time: {metrics['execution_time_ms']:.3f} ms")
        logger.info(f"  Accuracy: {accuracy:.4f}")
    
    logger.info()
    logger.info("=" * 70)
    logger.info("\nComplexity Summary:")
    logger.info("  Training: O(n * d * iter) - n samples, d features, iter iterations")
    logger.info("  Prediction: O(d) - per sample")
    logger.info("  Space: O(d) - weights and bias")
    logger.info("\nKey Advantages:")
    logger.info("  - Effective in high-dimensional spaces")
    logger.info("  - Memory efficient (uses support vectors)")
    logger.info("  - Versatile (different kernel functions)")
    logger.info("  - Good generalization")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Doesn't perform well with large datasets")
    logger.info("  - Sensitive to feature scaling")
    logger.info("  - No probabilistic output")
    logger.info("  - Can be slow for very large datasets")
    logger.info("\nWhen to Use:")
    logger.info("  - Text classification")
    logger.info("  - Image classification")
    logger.info("  - Handwriting recognition")
    logger.info("  - Bioinformatics")
    logger.info("  - Small to medium datasets")
    logger.info("\nCommon Use Cases:")
    logger.info("  - Text categorization")
    logger.info("  - Image recognition")
    logger.info("  - Handwriting recognition")
    logger.info("  - Bioinformatics (protein classification)")
    logger.info("  - Face detection")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()