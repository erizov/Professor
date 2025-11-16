#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Decision Tree implementation for classification.

Tree-based model that makes predictions by learning simple decision rules.
"""

import sys
from pathlib import Path
from typing import List, Tuple, Optional
import random
import math

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer
from framework.logging_utils import get_logger
logger = get_logger(__name__)


class Node:
    """Node in a decision tree."""
    
    def __init__(self, feature: Optional[int] = None,
                 threshold: Optional[float] = None,
                 left: Optional['Node'] = None,
                 right: Optional['Node'] = None,
                 value: Optional[int] = None):
        self.feature = feature  # Feature index to split on
        self.threshold = threshold  # Threshold value for split
        self.left = left  # Left child
        self.right = right  # Right child
        self.value = value  # Class label for leaf node


class DecisionTreeClassifier:
    """
    Decision Tree for classification using ID3 algorithm.
    """
    
    def __init__(self, max_depth: int = 10, min_samples_split: int = 2):
        """
        Initialize Decision Tree.
        
        Args:
            max_depth: Maximum tree depth
            min_samples_split: Minimum samples required to split
        """
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.root = None
    
    def fit(self, X: List[List[float]], y: List[int]) -> None:
        """
        Build decision tree.
        
        Args:
            X: Training features
            y: Training labels
        """
        self.root = self._grow_tree(X, y, depth=0)
    
    def _grow_tree(self, X: List[List[float]], y: List[int], 
                   depth: int) -> Node:
        """Recursively grow the decision tree."""
        n_samples = len(y)
        n_features = len(X[0]) if X else 0
        
        # Stopping criteria
        if (depth >= self.max_depth or 
            n_samples < self.min_samples_split or
            len(set(y)) == 1):
            # Create leaf node with majority class
            leaf_value = max(set(y), key=y.count) if y else 0
            return Node(value=leaf_value)
        
        # Find best split
        best_feature, best_threshold = self._best_split(X, y)
        
        if best_feature is None:
            # No valid split found, create leaf
            leaf_value = max(set(y), key=y.count)
            return Node(value=leaf_value)
        
        # Split data
        left_indices = [i for i in range(n_samples) 
                       if X[i][best_feature] < best_threshold]
        right_indices = [i for i in range(n_samples) 
                        if X[i][best_feature] >= best_threshold]
        
        # Recursively grow left and right subtrees
        left = self._grow_tree([X[i] for i in left_indices],
                              [y[i] for i in left_indices],
                              depth + 1)
        right = self._grow_tree([X[i] for i in right_indices],
                               [y[i] for i in right_indices],
                               depth + 1)
        
        return Node(feature=best_feature, threshold=best_threshold,
                   left=left, right=right)
    
    def _best_split(self, X: List[List[float]], y: List[int]) \
            -> Tuple[Optional[int], Optional[float]]:
        """Find the best feature and threshold to split on."""
        best_gini = float('inf')
        best_feature = None
        best_threshold = None
        
        n_features = len(X[0])
        
        for feature in range(n_features):
            # Get unique values for this feature
            values = sorted(set(row[feature] for row in X))
            
            # Try thresholds between consecutive values
            for i in range(len(values) - 1):
                threshold = (values[i] + values[i + 1]) / 2
                
                # Split data
                left_y = [y[j] for j in range(len(X)) 
                         if X[j][feature] < threshold]
                right_y = [y[j] for j in range(len(X)) 
                          if X[j][feature] >= threshold]
                
                if not left_y or not right_y:
                    continue
                
                # Calculate weighted Gini impurity
                n = len(y)
                gini = (len(left_y) / n * self._gini_impurity(left_y) +
                       len(right_y) / n * self._gini_impurity(right_y))
                
                if gini < best_gini:
                    best_gini = gini
                    best_feature = feature
                    best_threshold = threshold
        
        return best_feature, best_threshold
    
    def _gini_impurity(self, y: List[int]) -> float:
        """Calculate Gini impurity."""
        n = len(y)
        if n == 0:
            return 0
        
        counts = {}
        for label in y:
            counts[label] = counts.get(label, 0) + 1
        
        impurity = 1.0
        for count in counts.values():
            prob = count / n
            impurity -= prob ** 2
        
        return impurity
    
    def predict(self, X: List[List[float]]) -> List[int]:
        """
        Predict class labels.
        
        Args:
            X: Features to predict
            
        Returns:
            Predicted labels
        """
        return [self._traverse_tree(x, self.root) for x in X]
    
    def _traverse_tree(self, x: List[float], node: Node) -> int:
        """Traverse tree to make prediction."""
        if node.value is not None:
            return node.value
        
        if x[node.feature] < node.threshold:
            return self._traverse_tree(x, node.left)
        else:
            return self._traverse_tree(x, node.right)
    
    def score(self, X: List[List[float]], y: List[int]) -> float:
        """Calculate accuracy."""
        predictions = self.predict(X)
        correct = sum(1 for i in range(len(y)) 
                     if predictions[i] == y[i])
        return correct / len(y)


def generate_classification_data(n: int, seed: int = 42) \
        -> Tuple[List[List[float]], List[int]]:
    """Generate synthetic classification data."""
    random.seed(seed)
    
    X = []
    y = []
    
    # Class 0: small values
    for _ in range(n):
        X.append([random.uniform(0, 3), random.uniform(0, 3)])
        y.append(0)
    
    # Class 1: large values
    for _ in range(n):
        X.append([random.uniform(4, 7), random.uniform(4, 7)])
        y.append(1)
    
    return X, y


def main() -> None:
    """Demonstration of Decision Tree."""
    logger.info("=" * 70)
    logger.info("DECISION TREE CLASSIFIER DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Basic classification
    logger.info("Example 1: Binary Classification")
    logger.info("-" * 70)
    
    X_train, y_train = generate_classification_data(40)
    
    logger.info(f"Generated {len(X_train)} training samples")
    logger.info(f"Class 0: {sum(1 for label in y_train if label == 0)}")
    logger.info(f"Class 1: {sum(1 for label in y_train if label == 1)}")
    logger.info()
    
    tree = DecisionTreeClassifier(max_depth=5, min_samples_split=2)
    tree.fit(X_train, y_train)
    
    accuracy = tree.score(X_train, y_train)
    logger.info(f"Training Accuracy: {accuracy:.4f}")
    logger.info()
    
    # Example 2: Predictions
    logger.info("Example 2: Making Predictions")
    logger.info("-" * 70)
    
    X_test = [
        [1.0, 1.0],  # Should be class 0
        [6.0, 6.0],  # Should be class 1
        [3.5, 3.5],  # Boundary case
    ]
    
    predictions = tree.predict(X_test)
    
    logger.info("Predictions:")
    for x, pred in zip(X_test, predictions):
        logger.info(f"  Sample {x} → Class {pred}")
    logger.info()
    
    # Example 3: Performance measurement
    logger.info("Example 3: Performance Measurement")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("Decision Tree")
    
    sizes = [50, 100, 200]
    for size in sizes:
        X, y = generate_classification_data(size)
        model = DecisionTreeClassifier(max_depth=10)
        
        _, metrics = timer.measure(model.fit, X, y)
        
        logger.info(f"n={size*2:4d}: {metrics['execution_time_ms']:8.3f} ms, "
              f"{metrics['memory_peak_kb']:8.2f} KB")
    
    logger.info()
    timer.print_summary()
    
    logger.info("\n" + "=" * 70)
    logger.info("\nComplexity Summary:")
    logger.info("  Training Time:  O(n*d*log(n))")
    logger.info("  Prediction Time: O(log(n)) per sample")
    logger.info("  Space: O(n) for storing tree")
    logger.info("\nKey Points:")
    logger.info("  + Easy to interpret")
    logger.info("  + No feature scaling needed")
    logger.info("  + Handles non-linear relationships")
    logger.info("  + Can handle missing values")
    logger.info("  + Fast prediction")
    logger.info("  - Prone to overfitting")
    logger.info("  - Unstable (small changes = different tree)")
    logger.info("  - Biased towards features with more levels")
    logger.info("\nWhen to use:")
    logger.info("  • Need interpretable model")
    logger.info("  • Mixed data types")
    logger.info("  • Non-linear relationships")
    logger.info("  • No feature engineering")
    logger.info("  • Fast predictions needed")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()