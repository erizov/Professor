#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Random Forest Algorithm.

Ensemble learning method that constructs multiple decision trees and
outputs the mode (classification) or mean (regression) of individual trees.
"""

import sys
from pathlib import Path
import random
import math
from typing import List, Tuple, Any, Optional
from collections import Counter

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer


class DecisionTree:
    """Simple decision tree for Random Forest."""
    
    def __init__(self, max_depth: int = 10, min_samples_split: int = 2):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.root = None
    
    def fit(self, X: List[List[float]], y: List[Any]) -> None:
        """Train decision tree."""
        self.root = self._build_tree(X, y, depth=0)
    
    def _build_tree(self, X: List[List[float]], y: List[Any], depth: int) -> dict:
        """Build tree recursively."""
        n_samples = len(X)
        n_features = len(X[0]) if X else 0
        
        # Stopping criteria
        if depth >= self.max_depth or n_samples < self.min_samples_split:
            return {'prediction': self._most_common(y)}
        
        # Check if all labels are same
        if len(set(y)) == 1:
            return {'prediction': y[0]}
        
        # Find best split
        best_split = self._find_best_split(X, y)
        
        if best_split is None:
            return {'prediction': self._most_common(y)}
        
        feature_idx, threshold = best_split
        
        # Split data
        left_X, left_y, right_X, right_y = self._split(X, y, feature_idx, threshold)
        
        # Build children
        left_child = self._build_tree(left_X, left_y, depth + 1)
        right_child = self._build_tree(right_X, right_y, depth + 1)
        
        return {
            'feature_idx': feature_idx,
            'threshold': threshold,
            'left': left_child,
            'right': right_child
        }
    
    def _find_best_split(self, X: List[List[float]], y: List[Any]) -> Optional[Tuple[int, float]]:
        """Find best feature and threshold to split on."""
        best_gini = float('inf')
        best_split = None
        
        n_features = len(X[0]) if X else 0
        
        # Try random subset of features
        feature_indices = random.sample(range(n_features), min(int(math.sqrt(n_features)), n_features))
        
        for feature_idx in feature_indices:
            values = sorted(set([row[feature_idx] for row in X]))
            
            for i in range(len(values) - 1):
                threshold = (values[i] + values[i + 1]) / 2
                gini = self._gini_impurity(X, y, feature_idx, threshold)
                
                if gini < best_gini:
                    best_gini = gini
                    best_split = (feature_idx, threshold)
        
        return best_split
    
    def _gini_impurity(self, X: List[List[float]], y: List[Any], 
                      feature_idx: int, threshold: float) -> float:
        """Calculate Gini impurity for split."""
        left_y = [y[i] for i in range(len(X)) if X[i][feature_idx] <= threshold]
        right_y = [y[i] for i in range(len(X)) if X[i][feature_idx] > threshold]
        
        if not left_y or not right_y:
            return float('inf')
        
        left_gini = self._calculate_gini(left_y)
        right_gini = self._calculate_gini(right_y)
        
        n = len(y)
        return (len(left_y) / n) * left_gini + (len(right_y) / n) * right_gini
    
    def _calculate_gini(self, y: List[Any]) -> float:
        """Calculate Gini impurity."""
        if not y:
            return 0.0
        
        counts = Counter(y)
        n = len(y)
        gini = 1.0
        
        for count in counts.values():
            p = count / n
            gini -= p * p
        
        return gini
    
    def _split(self, X: List[List[float]], y: List[Any], 
              feature_idx: int, threshold: float) -> Tuple:
        """Split data based on feature and threshold."""
        left_X, left_y = [], []
        right_X, right_y = [], []
        
        for i in range(len(X)):
            if X[i][feature_idx] <= threshold:
                left_X.append(X[i])
                left_y.append(y[i])
            else:
                right_X.append(X[i])
                right_y.append(y[i])
        
        return left_X, left_y, right_X, right_y
    
    def _most_common(self, y: List[Any]) -> Any:
        """Get most common label."""
        return Counter(y).most_common(1)[0][0]
    
    def predict(self, X: List[List[float]]) -> List[Any]:
        """Predict for multiple samples."""
        return [self._predict_one(x) for x in X]
    
    def _predict_one(self, x: List[float]) -> Any:
        """Predict for single sample."""
        node = self.root
        
        while 'prediction' not in node:
            if x[node['feature_idx']] <= node['threshold']:
                node = node['left']
            else:
                node = node['right']
        
        return node['prediction']


class RandomForest:
    """Random Forest classifier."""
    
    def __init__(self, n_estimators: int = 100, max_depth: int = 10, 
                 min_samples_split: int = 2, random_state: int = None):
        """
        Initialize Random Forest.
        
        Args:
            n_estimators: Number of trees
            max_depth: Maximum tree depth
            min_samples_split: Minimum samples to split
            random_state: Random seed
        """
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.random_state = random_state
        self.trees: List[DecisionTree] = []
    
    def fit(self, X: List[List[float]], y: List[Any]) -> None:
        """Train Random Forest."""
        if self.random_state is not None:
            random.seed(self.random_state)
        
        n_samples = len(X)
        
        for i in range(self.n_estimators):
            # Bootstrap sampling
            indices = [random.randint(0, n_samples - 1) for _ in range(n_samples)]
            bootstrap_X = [X[idx] for idx in indices]
            bootstrap_y = [y[idx] for idx in indices]
            
            # Train tree
            tree = DecisionTree(max_depth=self.max_depth, 
                              min_samples_split=self.min_samples_split)
            tree.fit(bootstrap_X, bootstrap_y)
            self.trees.append(tree)
    
    def predict(self, X: List[List[float]]) -> List[Any]:
        """Predict using majority voting."""
        predictions = []
        
        for x in X:
            tree_predictions = [tree._predict_one(x) for tree in self.trees]
            # Majority vote
            prediction = Counter(tree_predictions).most_common(1)[0][0]
            predictions.append(prediction)
        
        return predictions
    
    def predict_proba(self, X: List[List[float]]) -> List[dict]:
        """Predict probabilities."""
        probabilities = []
        
        for x in X:
            tree_predictions = [tree._predict_one(x) for tree in self.trees]
            counts = Counter(tree_predictions)
            total = len(tree_predictions)
            
            proba = {label: count / total for label, count in counts.items()}
            probabilities.append(proba)
        
        return probabilities


def main() -> None:
    """Demonstration of Random Forest Algorithm."""
    print("=" * 70)
    print("RANDOM FOREST ALGORITHM DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Simple Classification
    print("Example 1: Simple Classification")
    print("-" * 70)
    
    # Simple dataset: [feature1, feature2] -> label
    X = [
        [1.0, 2.0], [1.5, 2.5], [2.0, 3.0],  # Class A
        [5.0, 6.0], [5.5, 6.5], [6.0, 7.0],  # Class B
        [1.0, 6.0], [1.5, 6.5], [2.0, 7.0],  # Class A
        [5.0, 2.0], [5.5, 2.5], [6.0, 3.0],  # Class B
    ]
    y = ['A', 'A', 'A', 'B', 'B', 'B', 'A', 'A', 'A', 'B', 'B', 'B']
    
    # Train Random Forest
    rf = RandomForest(n_estimators=10, max_depth=5, random_state=42)
    rf.fit(X, y)
    
    # Predict
    test_X = [[1.2, 2.3], [5.8, 6.2]]
    predictions = rf.predict(test_X)
    
    print("Training samples: 12")
    print("Number of trees: 10")
    print("\nPredictions:")
    for i, (x, pred) in enumerate(zip(test_X, predictions)):
        print(f"  Sample {i+1} {x}: {pred}")
    print()
    
    # Example 2: Feature Importance (simplified)
    print("Example 2: Prediction Probabilities")
    print("-" * 70)
    
    probabilities = rf.predict_proba(test_X)
    for i, proba in enumerate(probabilities):
        print(f"Sample {i+1} probabilities:")
        for label, prob in proba.items():
            print(f"  {label}: {prob:.2%}")
    print()
    
    # Example 3: Performance measurement
    print("Example 3: Performance Measurement")
    print("-" * 70)
    
    timer = PerformanceTimer("Random Forest")
    
    # Generate larger dataset
    X_large = [[random.random() * 10, random.random() * 10] for _ in range(100)]
    y_large = ['A' if x[0] + x[1] < 10 else 'B' for x in X_large]
    
    def train_forest():
        rf = RandomForest(n_estimators=20, max_depth=5, random_state=42)
        rf.fit(X_large, y_large)
        return len(rf.trees)
    
    result, metrics = timer.measure(train_forest)
    print(f"Time to train Random Forest with 20 trees: "
          f"{metrics['execution_time_ms']:.3f} ms")
    print(f"Trees trained: {result}")
    print()
    
    print("=" * 70)
    print("\nAlgorithm Summary:")
    print("\nDescription:")
    print("  Ensemble learning method that constructs multiple decision")
    print("  trees and outputs the mode (classification) or mean (regression).")
    print("\nTime Complexity:")
    print("  Training: O(n * m * log(n) * k) where:")
    print("    n = number of samples")
    print("    m = number of features")
    print("    k = number of trees")
    print("  Prediction: O(k * log(n))")
    print("\nKey Advantages:")
    print("  - Reduces overfitting")
    print("  - Handles missing values")
    print("  - Feature importance")
    print("  - Works well with default parameters")
    print("\nKey Disadvantages:")
    print("  - Less interpretable than single tree")
    print("  - Can be slow for large datasets")
    print("  - Memory intensive")
    print("\nWhen to Use:")
    print("  - Classification and regression")
    print("  - Need feature importance")
    print("  - Large datasets")
    print("  - Want robust predictions")
    print("\nCommon Use Cases:")
    print("  - Image classification")
    print("  - Feature selection")
    print("  - Anomaly detection")
    print("  - Bioinformatics")
    print("=" * 70)


if __name__ == "__main__":
    main()
