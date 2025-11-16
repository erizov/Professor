#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Logistic Regression implementation.

Binary classification algorithm that uses sigmoid function to predict
probability of binary outcomes.
"""

import sys
from pathlib import Path
import numpy as np

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer
from framework.logging_utils import get_logger
logger = get_logger(__name__)


class LogisticRegression:
    """
    Logistic Regression for binary classification.
    
    Uses sigmoid function: σ(z) = 1 / (1 + e^(-z))
    """
    
    def __init__(self, learning_rate: float = 0.01,
                 n_iterations: int = 1000,
                 regularization: float = 0.0):
        """
        Initialize Logistic Regression.
        
        Args:
            learning_rate: Learning rate for gradient descent
            n_iterations: Number of iterations
            regularization: L2 regularization parameter
        """
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
        self.regularization = regularization
        self.weights = None
        self.bias = None
        self.losses = []
    
    def _sigmoid(self, z: np.ndarray) -> np.ndarray:
        """Sigmoid activation function."""
        return 1 / (1 + np.exp(-np.clip(z, -500, 500)))
    
    def fit(self, X: np.ndarray, y: np.ndarray) -> 'LogisticRegression':
        """
        Fit logistic regression model.
        
        Args:
            X: Training features (n_samples, n_features)
            y: Training labels (n_samples,) - binary 0/1
            
        Returns:
            self
        """
        n_samples, n_features = X.shape
        
        # Initialize parameters
        self.weights = np.zeros(n_features)
        self.bias = 0
        self.losses = []
        
        # Gradient descent
        for i in range(self.n_iterations):
            # Linear combination
            z = np.dot(X, self.weights) + self.bias
            
            # Apply sigmoid
            y_pred = self._sigmoid(z)
            
            # Calculate loss (binary cross-entropy)
            loss = -(1 / n_samples) * np.sum(
                y * np.log(y_pred + 1e-15) +
                (1 - y) * np.log(1 - y_pred + 1e-15)
            )
            
            # Add regularization
            if self.regularization > 0:
                loss += (self.regularization / (2 * n_samples)) * \
                       np.sum(self.weights ** 2)
            
            self.losses.append(loss)
            
            # Calculate gradients
            dw = (1 / n_samples) * np.dot(X.T, (y_pred - y))
            db = (1 / n_samples) * np.sum(y_pred - y)
            
            # Add regularization gradient
            if self.regularization > 0:
                dw += (self.regularization / n_samples) * self.weights
            
            # Update parameters
            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db
        
        return self
    
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Predict probabilities.
        
        Args:
            X: Features (n_samples, n_features)
            
        Returns:
            Probabilities (n_samples,)
        """
        z = np.dot(X, self.weights) + self.bias
        return self._sigmoid(z)
    
    def predict(self, X: np.ndarray, 
                threshold: float = 0.5) -> np.ndarray:
        """
        Predict class labels.
        
        Args:
            X: Features
            threshold: Classification threshold
            
        Returns:
            Class labels (0 or 1)
        """
        return (self.predict_proba(X) >= threshold).astype(int)
    
    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """
        Calculate accuracy score.
        
        Args:
            X: Features
            y: True labels
            
        Returns:
            Accuracy
        """
        y_pred = self.predict(X)
        return np.mean(y_pred == y)


def main() -> None:
    """Demonstration of Logistic Regression."""
    logger.info("=" * 70)
    logger.info("LOGISTIC REGRESSION DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Simple binary classification
    logger.info("Example 1: Simple Binary Classification")
    logger.info("-" * 70)
    
    np.random.seed(42)
    
    # Generate linearly separable data
    X_class0 = np.random.randn(50, 2) + np.array([2, 2])
    X_class1 = np.random.randn(50, 2) + np.array([-2, -2])
    X = np.vstack([X_class0, X_class1])
    y = np.array([0] * 50 + [1] * 50)
    
    # Shuffle
    indices = np.random.permutation(len(y))
    X, y = X[indices], y[indices]
    
    model = LogisticRegression(learning_rate=0.1, n_iterations=1000)
    model.fit(X, y)
    
    logger.info(f"Accuracy: {model.score(X, y):.4f}")
    logger.info(f"Final loss: {model.losses[-1]:.4f}")
    logger.info(f"Weights: {model.weights}")
    logger.info(f"Bias: {model.bias:.4f}")
    logger.info()
    
    # Example 2: With regularization
    logger.info("Example 2: L2 Regularization")
    logger.info("-" * 70)
    
    # Add some noise to make it harder
    X_noise = np.hstack([X, np.random.randn(100, 3)])
    
    model_no_reg = LogisticRegression(learning_rate=0.1, 
                                      n_iterations=1000,
                                      regularization=0.0)
    model_no_reg.fit(X_noise, y)
    
    model_reg = LogisticRegression(learning_rate=0.1,
                                   n_iterations=1000,
                                   regularization=0.1)
    model_reg.fit(X_noise, y)
    
    logger.info("Without regularization:")
    logger.info(f"  Accuracy: {model_no_reg.score(X_noise, y):.4f}")
    logger.info(f"  Weight magnitude: {np.linalg.norm(model_no_reg.weights):.4f}")
    
    logger.info("\nWith regularization:")
    logger.info(f"  Accuracy: {model_reg.score(X_noise, y):.4f}")
    logger.info(f"  Weight magnitude: {np.linalg.norm(model_reg.weights):.4f}")
    logger.info()
    
    # Example 3: Probability predictions
    logger.info("Example 3: Probability Predictions")
    logger.info("-" * 70)
    
    test_samples = np.array([
        [3, 3],   # Should be class 0
        [-3, -3], # Should be class 1
        [0, 0],   # Uncertain
    ])
    
    probas = model.predict_proba(test_samples)
    predictions = model.predict(test_samples)
    
    for i, (sample, proba, pred) in enumerate(
        zip(test_samples, probas, predictions)):
        logger.info(f"Sample {sample}:")
        logger.info(f"  P(class=1) = {proba:.4f}")
        logger.info(f"  Predicted class: {pred}")
    logger.info()
    
    # Example 4: Performance measurement
    logger.info("Example 4: Performance on Different Dataset Sizes")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("Logistic Regression")
    
    for n in [100, 1000, 10000]:
        X = np.random.randn(n, 10)
        y = (X[:, 0] + X[:, 1] > 0).astype(int)
        
        def train_model():
            model = LogisticRegression(n_iterations=100)
            model.fit(X, y)
            return model
        
        result, metrics = timer.measure(train_model)
        logger.info(f"Dataset size: {n}")
        logger.info(f"  Time: {metrics['execution_time_ms']:.3f} ms")
        logger.info(f"  Accuracy: {result.score(X, y):.4f}")
    
    logger.info()
    logger.info("=" * 70)
    logger.info("\nComplexity Summary:")
    logger.info("  Time:  O(n * d * iter) - gradient descent")
    logger.info("  Space: O(d) - n=samples, d=features")
    logger.info("\nKey Advantages:")
    logger.info("  - Probabilistic predictions")
    logger.info("  - Works well with linearly separable data")
    logger.info("  - Regularization prevents overfitting")
    logger.info("  - Interpretable coefficients")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Assumes linear decision boundary")
    logger.info("  - Sensitive to outliers")
    logger.info("  - Requires feature scaling")
    logger.info("  - Only for binary classification (basic version)")
    logger.info("\nCommon Use Cases:")
    logger.info("  - Spam detection")
    logger.info("  - Medical diagnosis (disease/no disease)")
    logger.info("  - Credit risk assessment")
    logger.info("  - Click-through rate prediction")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()