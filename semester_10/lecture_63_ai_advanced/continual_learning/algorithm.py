#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Continual Learning implementation.

Continual learning enables models to learn from new data while
retaining knowledge from previous tasks.
"""

from typing import List, Dict, Any
import numpy as np


class ContinualLearner:
    """Continual learning model that adapts to new tasks."""
    
    def __init__(self, model_size: int = 100):
        """Initialize continual learner."""
        self.model_size = model_size
        self.weights = np.random.randn(model_size)
        self.task_memory: Dict[str, np.ndarray] = {}
        self.importance_weights = np.ones(model_size)
    
    def learn_task(self, task_name: str, data: np.ndarray, 
                   labels: np.ndarray) -> None:
        """Learn a new task while preserving previous knowledge."""
        # Elastic Weight Consolidation (EWC) approach
        old_weights = self.weights.copy()
        
        # Train on new task (simplified)
        for epoch in range(10):
            predictions = np.dot(data, self.weights)
            error = labels - predictions
            gradient = -2 * np.dot(data.T, error) / len(data)
            
            # Apply importance-weighted regularization
            penalty = self.importance_weights * (self.weights - old_weights)
            self.weights -= 0.01 * (gradient + 0.1 * penalty)
        
        # Update importance weights
        self.importance_weights += np.abs(self.weights - old_weights)
        self.task_memory[task_name] = self.weights.copy()
    
    def predict(self, data: np.ndarray) -> np.ndarray:
        """Make predictions."""
        return np.dot(data, self.weights)


def continual_learning(tasks: List[Dict[str, Any]]) -> ContinualLearner:
    """
    Continual Learning algorithm.
    
    Args:
        tasks: List of tasks, each with 'name', 'data', 'labels'
        
    Returns:
        Trained continual learner
    """
    learner = ContinualLearner()
    
    for task in tasks:
        learner.learn_task(
            task['name'],
            np.array(task['data']),
            np.array(task['labels'])
        )
    
    return learner


def main() -> None:
    """Demonstration of Continual Learning."""
    print("=" * 70)
    print("CONTINUAL LEARNING")
    print("=" * 70)
    
    # Create sample tasks
    np.random.seed(42)
    task1_data = np.random.randn(50, 10)
    task1_labels = np.random.randn(50)
    
    task2_data = np.random.randn(50, 10)
    task2_labels = np.random.randn(50)
    
    tasks = [
        {'name': 'task1', 'data': task1_data.tolist(), 
          'labels': task1_labels.tolist()},
        {'name': 'task2', 'data': task2_data.tolist(), 
          'labels': task2_labels.tolist()}
    ]
    
    # Train continual learner
    learner = continual_learning(tasks)
    
    # Test on new data
    test_data = np.random.randn(10, 10)
    predictions = learner.predict(test_data)
    
    print(f"\nLearned {len(learner.task_memory)} tasks")
    print(f"Sample predictions: {predictions[:5]}")
    print("=" * 70)


if __name__ == "__main__":
    main()
