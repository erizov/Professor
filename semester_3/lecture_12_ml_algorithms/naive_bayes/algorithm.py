#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Naive Bayes Classifier implementation.

Probabilistic classifier based on Bayes' theorem with strong independence
assumptions between features.
"""

import sys
from pathlib import Path
from collections import defaultdict
import numpy as np
from typing import Dict, List, Any

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer


class NaiveBayes:
    """
    Naive Bayes Classifier.
    
    Assumes features are conditionally independent given the class.
    """
    
    def __init__(self):
        """Initialize Naive Bayes classifier."""
        self.class_priors: Dict[Any, float] = {}
        self.class_likelihoods: Dict[Any, Dict[int, Dict[Any, float]]] = {}
        self.classes: List[Any] = []
    
    def fit(self, X: np.ndarray, y: np.ndarray) -> 'NaiveBayes':
        """
        Fit Naive Bayes model.
        
        Args:
            X: Training features (n_samples, n_features)
            y: Training labels (n_samples,)
            
        Returns:
            self
        """
        n_samples, n_features = X.shape
        self.classes = np.unique(y)
        
        # Calculate class priors
        for cls in self.classes:
            self.class_priors[cls] = np.sum(y == cls) / n_samples
        
        # Calculate likelihoods for each class and feature
        self.class_likelihoods = {}
        
        for cls in self.classes:
            X_cls = X[y == cls]
            self.class_likelihoods[cls] = {}
            
            for feature_idx in range(n_features):
                feature_values = X_cls[:, feature_idx]
                value_counts = defaultdict(int)
                
                for val in feature_values:
                    value_counts[val] += 1
                
                # Convert to probabilities (with Laplace smoothing)
                total = len(feature_values)
                self.class_likelihoods[cls][feature_idx] = {
                    val: (count + 1) / (total + len(np.unique(X[:, feature_idx])))
                    for val, count in value_counts.items()
                }
        
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict class labels.
        
        Args:
            X: Features (n_samples, n_features)
            
        Returns:
            Predicted class labels
        """
        predictions = []
        
        for sample in X:
            class_scores = {}
            
            for cls in self.classes:
                # Start with prior probability
                score = np.log(self.class_priors[cls])
                
                # Multiply by likelihoods (add logs)
                for feature_idx, feature_value in enumerate(sample):
                    likelihoods = self.class_likelihoods[cls].get(feature_idx, {})
                    prob = likelihoods.get(feature_value, 1e-10)  # Small value if unseen
                    score += np.log(prob)
                
                class_scores[cls] = score
            
            # Predict class with highest score
            predicted_class = max(class_scores, key=class_scores.get)
            predictions.append(predicted_class)
        
        return np.array(predictions)
    
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Predict class probabilities.
        
        Args:
            X: Features (n_samples, n_features)
            
        Returns:
            Class probabilities (n_samples, n_classes)
        """
        probabilities = []
        
        for sample in X:
            class_scores = {}
            
            for cls in self.classes:
                score = np.log(self.class_priors[cls])
                
                for feature_idx, feature_value in enumerate(sample):
                    likelihoods = self.class_likelihoods[cls].get(feature_idx, {})
                    prob = likelihoods.get(feature_value, 1e-10)
                    score += np.log(prob)
                
                class_scores[cls] = score
            
            # Convert to probabilities
            max_score = max(class_scores.values())
            exp_scores = {cls: np.exp(score - max_score) 
                         for cls, score in class_scores.items()}
            total = sum(exp_scores.values())
            
            probs = [exp_scores.get(cls, 0) / total for cls in self.classes]
            probabilities.append(probs)
        
        return np.array(probabilities)


def main() -> None:
    """Demonstration of Naive Bayes."""
    print("=" * 70)
    print("NAIVE BAYES CLASSIFIER DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Simple classification
    print("Example 1: Simple Classification")
    print("-" * 70)
    
    # Weather dataset example
    X = np.array([
        [0, 0, 0],  # Sunny, Hot, High -> No
        [0, 0, 1],  # Sunny, Hot, Normal -> No
        [1, 0, 0],  # Overcast, Hot, High -> Yes
        [2, 1, 0],  # Rain, Mild, High -> Yes
        [2, 2, 1],  # Rain, Cool, Normal -> Yes
        [1, 2, 1],  # Overcast, Cool, Normal -> Yes
        [0, 1, 0],  # Sunny, Mild, High -> No
        [0, 2, 1],  # Sunny, Cool, Normal -> Yes
        [2, 1, 1],  # Rain, Mild, Normal -> Yes
        [0, 1, 1],  # Sunny, Mild, Normal -> Yes
    ])
    y = np.array([0, 0, 1, 1, 1, 1, 0, 1, 1, 1])  # 0=No, 1=Yes
    
    nb = NaiveBayes()
    nb.fit(X, y)
    
    # Test
    X_test = np.array([
        [0, 2, 0],  # Sunny, Cool, High
        [2, 1, 0],  # Rain, Mild, High
    ])
    
    predictions = nb.predict(X_test)
    print("Test predictions:")
    for i, pred in enumerate(predictions):
        print(f"  Sample {i+1}: {pred} ({'Yes' if pred == 1 else 'No'})")
    print()
    
    # Example 2: Text classification (simplified)
    print("Example 2: Text Classification (Simplified)")
    print("-" * 70)
    
    # Simple word-based features
    # Features: [word1_present, word2_present, word3_present]
    X_text = np.array([
        [1, 1, 0],  # Contains "good", "great" -> Positive
        [1, 0, 1],  # Contains "good", "bad" -> Negative
        [0, 1, 0],  # Contains "great" -> Positive
        [0, 0, 1],  # Contains "bad" -> Negative
        [1, 1, 0],  # Contains "good", "great" -> Positive
    ])
    y_text = np.array([1, 0, 1, 0, 1])  # 1=Positive, 0=Negative
    
    nb_text = NaiveBayes()
    nb_text.fit(X_text, y_text)
    
    test_text = np.array([[1, 0, 0]])  # Contains "good"
    pred_text = nb_text.predict(test_text)
    print(f"Text with 'good': {'Positive' if pred_text[0] == 1 else 'Negative'}")
    print()
    
    # Example 3: Performance measurement
    print("Example 3: Performance Measurement")
    print("-" * 70)
    
    timer = PerformanceTimer("Naive Bayes")
    
    for n in [100, 500, 1000]:
        X = np.random.randint(0, 5, size=(n, 10))
        y = np.random.randint(0, 3, size=n)
        
        def train_model():
            model = NaiveBayes()
            model.fit(X, y)
            return model
        
        result, metrics = timer.measure(train_model)
        accuracy = np.mean(result.predict(X) == y)
        print(f"Dataset size: {n}")
        print(f"  Time: {metrics['execution_time_ms']:.3f} ms")
        print(f"  Accuracy: {accuracy:.4f}")
    
    print()
    print("=" * 70)
    print("\nComplexity Summary:")
    print("  Training: O(n * d) - n samples, d features")
    print("  Prediction: O(d * c) - c classes")
    print("  Space: O(d * c * v) - v unique values per feature")
    print("\nKey Advantages:")
    print("  - Fast training and prediction")
    print("  - Works well with small datasets")
    print("  - Handles multiple classes")
    print("  - Probabilistic predictions")
    print("  - Not sensitive to irrelevant features")
    print("\nKey Disadvantages:")
    print("  - Strong independence assumption (often violated)")
    print("  - Requires feature independence")
    print("  - Can be outperformed by more complex models")
    print("  - Zero probability problem (needs smoothing)")
    print("\nWhen to Use:")
    print("  - Text classification (spam detection)")
    print("  - Document classification")
    print("  - Sentiment analysis")
    print("  - Medical diagnosis")
    print("  - Real-time prediction (fast)")
    print("\nCommon Use Cases:")
    print("  - Spam email detection")
    print("  - Text categorization")
    print("  - Sentiment analysis")
    print("  - Medical diagnosis")
    print("  - News article classification")
    print("=" * 70)


if __name__ == "__main__":
    main()

