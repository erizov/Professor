#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Linear Regression implementation.

Simple yet powerful algorithm for modeling linear relationships
between variables using gradient descent.
"""

import sys
from pathlib import Path
import random
import math

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer


class LinearRegression:
    """Linear Regression using Gradient Descent."""
    
    def __init__(self, learning_rate: float = 0.01, 
                 n_iterations: int = 1000):
        """
        Initialize Linear Regression.
        
        Args:
            learning_rate: Step size for gradient descent
            n_iterations: Number of training iterations
        """
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
        self.weights = None
        self.bias = None
        self.losses = []
    
    def fit(self, X: list, y: list) -> None:
        """
        Train the linear regression model.
        
        Args:
            X: Training features (list of lists)
            y: Training targets (list)
        """
        n_samples = len(X)
        n_features = len(X[0]) if n_samples > 0 else 0
        
        # Initialize parameters
        self.weights = [0.0] * n_features
        self.bias = 0.0
        self.losses = []
        
        # Gradient descent
        for iteration in range(self.n_iterations):
            # Forward pass: compute predictions
            predictions = self.predict(X)
            
            # Compute gradients
            dw = [0.0] * n_features
            db = 0.0
            
            for i in range(n_samples):
                error = predictions[i] - y[i]
                db += error
                for j in range(n_features):
                    dw[j] += error * X[i][j]
            
            # Update parameters
            for j in range(n_features):
                self.weights[j] -= self.learning_rate * dw[j] / n_samples
            self.bias -= self.learning_rate * db / n_samples
            
            # Track loss (MSE)
            if iteration % 100 == 0:
                loss = self.mse(y, predictions)
                self.losses.append(loss)
    
    def predict(self, X: list) -> list:
        """
        Make predictions.
        
        Args:
            X: Features to predict on
            
        Returns:
            List of predictions
        """
        predictions = []
        for x in X:
            pred = self.bias
            for j, weight in enumerate(self.weights):
                pred += weight * x[j]
            predictions.append(pred)
        return predictions
    
    def mse(self, y_true: list, y_pred: list) -> float:
        """Calculate Mean Squared Error."""
        n = len(y_true)
        return sum((y_true[i] - y_pred[i]) ** 2 for i in range(n)) / n
    
    def r2_score(self, y_true: list, y_pred: list) -> float:
        """Calculate R² score (coefficient of determination)."""
        mean_y = sum(y_true) / len(y_true)
        ss_tot = sum((y - mean_y) ** 2 for y in y_true)
        ss_res = sum((y_true[i] - y_pred[i]) ** 2 
                    for i in range(len(y_true)))
        return 1 - (ss_res / ss_tot) if ss_tot != 0 else 0


def main() -> None:
    """Demonstration of Linear Regression."""
    print("=" * 70)
    print("LINEAR REGRESSION DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Simple 1D linear relationship
    print("Example 1: Simple Linear Relationship (y = 2x + 3)")
    print("-" * 70)
    
    # Generate synthetic data: y = 2x + 3 + noise
    random.seed(42)
    X_train = [[x] for x in range(0, 100, 2)]
    y_train = [2 * x[0] + 3 + random.gauss(0, 5) for x in X_train]
    
    X_test = [[x] for x in range(1, 100, 2)]
    y_test = [2 * x[0] + 3 + random.gauss(0, 5) for x in X_test]
    
    # Train model
    model = LinearRegression(learning_rate=0.0001, n_iterations=1000)
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    
    # Evaluate
    train_mse = model.mse(y_train, y_pred_train)
    test_mse = model.mse(y_test, y_pred_test)
    train_r2 = model.r2_score(y_train, y_pred_train)
    test_r2 = model.r2_score(y_test, y_pred_test)
    
    print(f"True equation: y = 2x + 3")
    print(f"Learned equation: y = {model.weights[0]:.3f}x + "
          f"{model.bias:.3f}")
    print(f"\nTraining MSE: {train_mse:.2f}")
    print(f"Testing MSE:  {test_mse:.2f}")
    print(f"Training R²:  {train_r2:.3f}")
    print(f"Testing R²:   {test_r2:.3f}")
    print()
    
    # Example 2: Multiple features
    print("Example 2: Multiple Linear Regression")
    print("-" * 70)
    
    # Generate data: y = 3x1 + 2x2 + 1
    X_multi = [[x1, x2] 
               for x1 in range(10) 
               for x2 in range(10)]
    y_multi = [3 * x[0] + 2 * x[1] + 1 + random.gauss(0, 2) 
               for x in X_multi]
    
    # Split train/test
    split = int(0.8 * len(X_multi))
    X_train_m = X_multi[:split]
    y_train_m = y_multi[:split]
    X_test_m = X_multi[split:]
    y_test_m = y_multi[split:]
    
    # Train
    model_multi = LinearRegression(learning_rate=0.0001, 
                                   n_iterations=2000)
    model_multi.fit(X_train_m, y_train_m)
    
    # Evaluate
    y_pred_m = model_multi.predict(X_test_m)
    test_r2_m = model_multi.r2_score(y_test_m, y_pred_m)
    
    print(f"True equation: y = 3x₁ + 2x₂ + 1")
    print(f"Learned equation: y = {model_multi.weights[0]:.3f}x₁ + "
          f"{model_multi.weights[1]:.3f}x₂ + {model_multi.bias:.3f}")
    print(f"Test R² score: {test_r2_m:.3f}")
    print()
    
    # Example 3: Learning curve
    print("Example 3: Learning Curve")
    print("-" * 70)
    print("Loss over iterations:")
    for i, loss in enumerate(model.losses):
        print(f"  Iteration {i * 100:4d}: Loss = {loss:.2f}")
    print()
    
    # Example 4: Performance measurement
    print("Example 4: Performance Measurement")
    print("-" * 70)
    
    timer = PerformanceTimer("Linear Regression")
    
    # Generate larger dataset
    X_large = [[random.random() * 100, random.random() * 100] 
               for _ in range(1000)]
    y_large = [2 * x[0] + 3 * x[1] + 5 + random.gauss(0, 10) 
               for x in X_large]
    
    model_large = LinearRegression(learning_rate=0.0001, 
                                   n_iterations=1000)
    
    # Measure training time
    _, train_metrics = timer.measure(model_large.fit, X_large, y_large)
    
    # Measure prediction time
    _, pred_metrics = timer.measure(model_large.predict, X_large)
    
    print(f"Dataset: {len(X_large)} samples, "
          f"{len(X_large[0])} features")
    print(f"Training time:   {train_metrics['execution_time_ms']:.3f} ms")
    print(f"Prediction time: {pred_metrics['execution_time_ms']:.3f} ms")
    print(f"Memory used:     {train_metrics['memory_peak_kb']:.2f} KB")
    print()
    
    print("=" * 70)
    print("\nComplexity Summary:")
    print("  Training Time:  O(n*d*iterations)")
    print("    n = number of samples")
    print("    d = number of features")
    print("  Prediction Time: O(n*d)")
    print("  Space: O(d) for weights")
    print("\nKey Points:")
    print("  ✓ Simple and interpretable")
    print("  ✓ Fast training and prediction")
    print("  ✓ Works well for linear relationships")
    print("  ✓ No hyperparameters (except learning rate)")
    print("  ✗ Assumes linear relationship")
    print("  ✗ Sensitive to outliers")
    print("  ✗ Requires feature scaling")
    print("\nBest For:")
    print("  - Linear relationships")
    print("  - When interpretability is important")
    print("  - Baseline model for comparison")
    print("  - Small to medium datasets")
    print("  - Real-time predictions")
    print("=" * 70)


if __name__ == "__main__":
    main()
