#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Few Shot Learning Advanced implementation.

Few-shot learning enables models to learn from very few examples
by leveraging prior knowledge.
"""

from typing import List, Tuple, Dict
import numpy as np


class FewShotLearner:
    """Few-shot learning model using prototypical networks."""
    
    def __init__(self, embedding_dim: int = 64):
        """Initialize few-shot learner."""
        self.embedding_dim = embedding_dim
        self.prototypes: Dict[str, np.ndarray] = {}
    
    def compute_prototype(self, examples: np.ndarray) -> np.ndarray:
        """Compute prototype (mean embedding) for a class."""
        return np.mean(examples, axis=0)
    
    def learn_from_examples(self, support_set: List[Tuple[str, np.ndarray]]) -> None:
        """Learn from few examples (support set)."""
        for class_name, examples in support_set:
            examples_array = np.array(examples)
            self.prototypes[class_name] = self.compute_prototype(examples_array)
    
    def predict(self, query: np.ndarray) -> str:
        """Predict class for query using nearest prototype."""
        query_array = np.array(query)
        min_dist = float('inf')
        predicted_class = None
        
        for class_name, prototype in self.prototypes.items():
            dist = np.linalg.norm(query_array - prototype)
            if dist < min_dist:
                min_dist = dist
                predicted_class = class_name
        
        return predicted_class


def few_shot_learning_advanced(support_set: List[Tuple[str, List[List[float]]]], 
                queries: List[List[float]]) -> List[str]:
    """
    Few Shot Learning Advanced algorithm.
    
    Args:
        support_set: List of (class_name, examples) tuples
        queries: List of query examples to classify
        
    Returns:
        List of predicted class names
    """
    learner = FewShotLearner()
    
    # Convert to numpy arrays
    support_np = [(name, np.array(examples)) 
                  for name, examples in support_set]
    learner.learn_from_examples(support_np)
    
    # Predict for queries
    predictions = []
    for query in queries:
        pred = learner.predict(query)
        predictions.append(pred)
    
    return predictions


def main() -> None:
    """Demonstration of Few Shot Learning Advanced."""
    print("=" * 70)
    print("FEW SHOT LEARNING ADVANCED")
    print("=" * 70)
    
    # Create few-shot learning scenario (5-way, 1-shot)
    np.random.seed(42)
    
    support_set = [
        ('class_A', [[1.0, 2.0], [1.1, 2.1]]),
        ('class_B', [[3.0, 4.0], [3.1, 4.1]]),
        ('class_C', [[5.0, 6.0], [5.1, 6.1]])
    ]
    
    queries = [
        [1.05, 2.05],
        [3.05, 4.05],
        [5.05, 6.05]
    ]
    
    predictions = few_shot_learning_advanced(support_set, queries)
    
    print(f"\nSupport set: {len(support_set)} classes")
    print(f"Queries: {len(queries)}")
    print(f"Predictions: {predictions}")
    print("=" * 70)


if __name__ == "__main__":
    main()
