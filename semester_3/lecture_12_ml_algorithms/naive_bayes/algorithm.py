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
from framework.logging_utils import get_logger
logger = get_logger(__name__)


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
    logger.info("=" * 70)
    logger.info("NAIVE BAYES CLASSIFIER DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Simple classification
    logger.info("Example 1: Simple Classification")
    logger.info("-" * 70)
    
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
    logger.info("Test predictions:")
    for i, pred in enumerate(predictions):
        logger.info(f"  Sample {i+1}: {pred} ({'Yes' if pred == 1 else 'No'})")
    logger.info()
    
    # Example 2: Text classification (simplified)
    logger.info("Example 2: Text Classification (Simplified)")
    logger.info("-" * 70)
    
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
    logger.info(f"Text with 'good': {'Positive' if pred_text[0] == 1 else 'Negative'}")
    logger.info()
    
    # Example 3: Performance measurement
    logger.info("Example 3: Performance Measurement")
    logger.info("-" * 70)
    
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
        logger.info(f"Dataset size: {n}")
        logger.info(f"  Time: {metrics['execution_time_ms']:.3f} ms")
        logger.info(f"  Accuracy: {accuracy:.4f}")
    
    logger.info()
    logger.info("=" * 70)
    logger.info("\nComplexity Summary:")
    logger.info("  Training: O(n * d) - n samples, d features")
    logger.info("  Prediction: O(d * c) - c classes")
    logger.info("  Space: O(d * c * v) - v unique values per feature")
    logger.info("\nKey Advantages:")
    logger.info("  - Fast training and prediction")
    logger.info("  - Works well with small datasets")
    logger.info("  - Handles multiple classes")
    logger.info("  - Probabilistic predictions")
    logger.info("  - Not sensitive to irrelevant features")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Strong independence assumption (often violated)")
    logger.info("  - Requires feature independence")
    logger.info("  - Can be outperformed by more complex models")
    logger.info("  - Zero probability problem (needs smoothing)")
    logger.info("\nWhen to Use:")
    logger.info("  - Text classification (spam detection)")
    logger.info("  - Document classification")
    logger.info("  - Sentiment analysis")
    logger.info("  - Medical diagnosis")
    logger.info("  - Real-time prediction (fast)")
    logger.info("\nCommon Use Cases:")
    logger.info("  - Spam email detection")
    logger.info("  - Text categorization")
    logger.info("  - Sentiment analysis")
    logger.info("  - Medical diagnosis")
    logger.info("  - News article classification")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()