#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Linear Regression implementation.

Simple regression algorithm that models relationship between dependent
variable and one or more independent variables using a linear equation.
"""

import sys
from pathlib import Path
import numpy as np
import time
import psutil
import os

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer
from framework.logging_utils import get_logger
logger = get_logger(__name__)


class LinearRegression:
    """
    Linear Regression using Gradient Descent or Normal Equation.
    
    y = w0 + w1*x1 + w2*x2 + ... + wn*xn
    """
    
    def __init__(self, learning_rate: float = 0.01, 
                 n_iterations: int = 1000,
                 method: str = 'gradient_descent'):
        """
        Initialize Linear Regression.
        
        Args:
            learning_rate: Learning rate for gradient descent
            n_iterations: Number of iterations
            method: 'gradient_descent' or 'normal_equation'
        """
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
        self.method = method
        self.weights = None
        self.bias = None
        self.losses = []
    
    def fit(self, X: np.ndarray, y: np.ndarray) -> 'LinearRegression':
        """
        Fit linear regression model.
        
        Args:
            X: Training features (n_samples, n_features)
            y: Training targets (n_samples,)
            
        Returns:
            self
        """
        if self.method == 'normal_equation':
            return self._fit_normal_equation(X, y)
        else:
            return self._fit_gradient_descent(X, y)
    
    def _fit_gradient_descent(self, X: np.ndarray, 
                              y: np.ndarray) -> 'LinearRegression':
        """Fit using gradient descent."""
        n_samples, n_features = X.shape
        
        # Initialize parameters
        self.weights = np.zeros(n_features)
        self.bias = 0
        self.losses = []
        
        # Gradient descent
        for i in range(self.n_iterations):
            # Predictions
            y_pred = np.dot(X, self.weights) + self.bias
            
            # Calculate loss (MSE)
            loss = np.mean((y - y_pred) ** 2)
            self.losses.append(loss)
            
            # Calculate gradients
            dw = -(2 / n_samples) * np.dot(X.T, (y - y_pred))
            db = -(2 / n_samples) * np.sum(y - y_pred)
            
            # Update parameters
            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db
        
        return self
    
    def _fit_normal_equation(self, X: np.ndarray, 
                            y: np.ndarray) -> 'LinearRegression':
        """Fit using normal equation (closed form solution)."""
        # Add bias term
        X_b = np.c_[np.ones((X.shape[0], 1)), X]
        
        # Normal equation: theta = (X^T X)^-1 X^T y
        theta = np.linalg.inv(X_b.T.dot(X_b)).dot(X_b.T).dot(y)
        
        self.bias = theta[0]
        self.weights = theta[1:]
        
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Make predictions.
        
        Args:
            X: Features (n_samples, n_features)
            
        Returns:
            Predictions (n_samples,)
        """
        return np.dot(X, self.weights) + self.bias
    
    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """
        Calculate R² score.
        
        Args:
            X: Features
            y: True values
            
        Returns:
            R² score
        """
        y_pred = self.predict(X)
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        return 1 - (ss_res / ss_tot)


def main() -> None:
    """Demonstration of Linear Regression."""
    logger.info("=" * 70)
    logger.info("LINEAR REGRESSION DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Simple linear regression
    logger.info("Example 1: Simple Linear Regression (1 feature)")
    logger.info("-" * 70)
    
    # Generate synthetic data: y = 3x + 5 + noise
    np.random.seed(42)
    X_simple = np.random.rand(100, 1) * 10
    y_simple = 3 * X_simple.squeeze() + 5 + np.random.randn(100) * 2
    
    model1 = LinearRegression(learning_rate=0.01, n_iterations=1000)
    model1.fit(X_simple, y_simple)
    
    logger.info(f"True equation: y = 3x + 5")
    logger.info(f"Learned: y = {model1.weights[0]:.2f}x + {model1.bias:.2f}")
    logger.info(f"R² score: {model1.score(X_simple, y_simple):.4f}")
    logger.info(f"Final loss: {model1.losses[-1]:.4f}")
    logger.info()
    
    # Example 2: Multiple linear regression
    logger.info("Example 2: Multiple Linear Regression (3 features)")
    logger.info("-" * 70)
    
    # Generate data: y = 2x1 + 3x2 - 1x3 + 10
    X_multi = np.random.rand(100, 3) * 10
    y_multi = (2 * X_multi[:, 0] + 
               3 * X_multi[:, 1] - 
               1 * X_multi[:, 2] + 
               10 + np.random.randn(100) * 2)
    
    model2 = LinearRegression(learning_rate=0.01, n_iterations=1000)
    model2.fit(X_multi, y_multi)
    
    logger.info(f"True equation: y = 2x₁ + 3x₂ - 1x₃ + 10")
    logger.info(f"Learned: y = {model2.weights[0]:.2f}x₁ + " + 
          f"{model2.weights[1]:.2f}x₂ + " +
          f"{model2.weights[2]:.2f}x₃ + {model2.bias:.2f}")
    logger.info(f"R² score: {model2.score(X_multi, y_multi):.4f}")
    logger.info()
    
    # Example 3: Normal equation vs Gradient Descent
    logger.info("Example 3: Normal Equation vs Gradient Descent")
    logger.info("-" * 70)
    
    X_test = np.random.rand(100, 2) * 10
    y_test = 5 * X_test[:, 0] + 2 * X_test[:, 1] + 3
    
    # Gradient Descent
    start_time = time.perf_counter()
    model_gd = LinearRegression(method='gradient_descent', 
                                n_iterations=1000)
    model_gd.fit(X_test, y_test)
    time_gd = time.perf_counter() - start_time
    
    # Normal Equation
    start_time = time.perf_counter()
    model_ne = LinearRegression(method='normal_equation')
    model_ne.fit(X_test, y_test)
    time_ne = time.perf_counter() - start_time
    
    logger.info("Gradient Descent:")
    logger.info(f"  Time: {time_gd*1000:.3f} ms")
    logger.info(f"  Weights: {model_gd.weights}")
    logger.info(f"  R² score: {model_gd.score(X_test, y_test):.4f}")
    
    logger.info("\nNormal Equation:")
    logger.info(f"  Time: {time_ne*1000:.3f} ms")
    logger.info(f"  Weights: {model_ne.weights}")
    logger.info(f"  R² score: {model_ne.score(X_test, y_test):.4f}")
    logger.info()
    
    # Example 4: Performance measurement
    logger.info("Example 4: Performance on Different Dataset Sizes")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("Linear Regression")
    
    for n in [100, 1000, 10000]:
        X = np.random.rand(n, 5)
        y = np.random.rand(n)
        
        def train_model():
            model = LinearRegression(n_iterations=100)
            model.fit(X, y)
            return model
        
        _, metrics = timer.measure(train_model)
        logger.info(f"Dataset size: {n}")
        logger.info(f"  Time: {metrics['execution_time_ms']:.3f} ms")
        logger.info(f"  Memory: {metrics['memory_peak_kb']:.2f} KB")
    
    logger.info()
    logger.info("=" * 70)
    logger.info("\nComplexity Summary:")
    logger.info("  Gradient Descent:")
    logger.info("    Time:  O(n * d * iter) - n=samples, d=features")
    logger.info("    Space: O(d)")
    logger.info("  Normal Equation:")
    logger.info("    Time:  O(d³ + d²n) - matrix inversion")
    logger.info("    Space: O(d²)")
    logger.info("\nKey Advantages:")
    logger.info("  - Simple and interpretable")
    logger.info("  - Fast training (normal equation)")
    logger.info("  - No hyperparameters (normal equation)")
    logger.info("  - Works well for linear relationships")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Assumes linear relationship")
    logger.info("  - Sensitive to outliers")
    logger.info("  - Cannot handle non-linear patterns")
    logger.info("  - Normal equation expensive for large features")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()