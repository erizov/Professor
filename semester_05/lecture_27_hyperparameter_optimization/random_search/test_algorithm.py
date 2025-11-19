#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for Random Search.
"""

import unittest
import sys
from pathlib import Path

# Add parent directories to path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from tests.test_framework_setup import AlgorithmTestCase


class TestRandomsearch(AlgorithmTestCase):
    """Test Random Search implementation."""

    def setUp(self):
        """Set up test fixtures."""
        from semester_05.lecture_27_hyperparameter_optimization.random_search.algorithm import (
            random_search,
        )

        self.algorithm = random_search

    def test_basic_search(self):
        """Test basic random search functionality."""
        import random
        param_distributions = {
            'learning_rate': lambda: random.uniform(0.001, 0.1),
            'batch_size': lambda: random.choice([16, 32, 64, 128])
        }
        
        def objective_func(params):
            # Simple mock objective function
            return -abs(params['learning_rate'] - 0.05) - abs(params['batch_size'] - 64)
        
        result = self.algorithm(param_distributions, n_iter=10, objective_func=objective_func)
        self.assertIsNotNone(result)
        self.assertIn('best_params', result)
        self.assertIn('best_score', result)

    def test_performance(self):
        """Test algorithm performance."""
        import random
        param_distributions = {
            'param1': lambda: random.uniform(0, 1),
            'param2': lambda: random.choice([1, 2, 3])
        }
        
        def objective_func(params):
            return -(params['param1'] - 0.5)**2
        
        # Test that it completes in reasonable time
        result = self.algorithm(param_distributions, n_iter=100, objective_func=objective_func)
        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
