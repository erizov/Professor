#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Evaluation Metrics implementation.

This file contains the implementation of the Evaluation Metrics algorithm.
"""

from typing import List, Optional, Dict, Set


class EvaluationMetrics:
    """ML model evaluation metrics."""
    def __init__(self):
        self.predictions: List[any] = []
        self.labels: List[any] = []
    
    def add_prediction(self, prediction: any, label: any) -> None:
        """Add prediction and label."""
        self.predictions.append(prediction)
        self.labels.append(label)
    
    def accuracy(self) -> float:
        """Calculate accuracy."""
        if not self.predictions:
            return 0.0
        correct = sum(1 for p, l in zip(self.predictions, self.labels) if p == l)
        return correct / len(self.predictions)
    
    def precision(self, positive_class: any = 1) -> float:
        """Calculate precision."""
        tp = sum(1 for p, l in zip(self.predictions, self.labels) 
                if p == positive_class and l == positive_class)
        fp = sum(1 for p, l in zip(self.predictions, self.labels) 
                if p == positive_class and l != positive_class)
        return tp / (tp + fp) if (tp + fp) > 0 else 0.0
    
    def recall(self, positive_class: any = 1) -> float:
        """Calculate recall."""
        tp = sum(1 for p, l in zip(self.predictions, self.labels) 
                if p == positive_class and l == positive_class)
        fn = sum(1 for p, l in zip(self.predictions, self.labels) 
                if p != positive_class and l == positive_class)
        return tp / (tp + fn) if (tp + fn) > 0 else 0.0
    
    def f1_score(self, positive_class: any = 1) -> float:
        """Calculate F1 score."""
        prec = self.precision(positive_class)
        rec = self.recall(positive_class)
        return 2 * (prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0
    
    def confusion_matrix(self) -> Dict[tuple, int]:
        """Calculate confusion matrix."""
        from collections import Counter
        return Counter((p, l) for p, l in zip(self.predictions, self.labels))


def main() -> None:
    """Demonstrate Evaluation Metrics."""
    print("=" * 70)
    print("EVALUATION METRICS")
    print("=" * 70)
    
    # Example usage
    print("Algorithm implementation for Evaluation Metrics")
    print("See implementation above for details.")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
