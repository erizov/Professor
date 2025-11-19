#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Constraint-based algorithm selector.

Helps select optimal algorithm based on resource constraints.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class ResourceLevel(Enum):
    """Resource availability levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    UNLIMITED = "unlimited"


@dataclass
class Constraints:
    """Resource constraints for algorithm selection."""

    memory: ResourceLevel = ResourceLevel.MEDIUM
    cpu_power: ResourceLevel = ResourceLevel.MEDIUM
    network_bandwidth: ResourceLevel = ResourceLevel.MEDIUM
    storage: ResourceLevel = ResourceLevel.MEDIUM
    latency_requirement: str = "medium"  # low, medium, high, ultra
    dataset_size: str = "medium"  # small, medium, large, huge
    is_distributed: bool = False
    is_edge_device: bool = False
    power_constrained: bool = False
    cost_sensitive: bool = False


class AlgorithmSelector:
    """Select optimal algorithm based on constraints."""

    # Algorithm database with characteristics
    SORTING_ALGORITHMS = {
        "bubble_sort": {
            "time": "O(n²)",
            "space": "O(1)",
            "stable": True,
            "in_place": True,
            "best_for": ["very_small", "nearly_sorted"],
            "avoid_for": ["large", "random"],
            "memory_level": ResourceLevel.LOW,
            "cpu_level": ResourceLevel.LOW,
        },
        "merge_sort": {
            "time": "O(n log n)",
            "space": "O(n)",
            "stable": True,
            "in_place": False,
            "best_for": ["medium", "large", "stability_required"],
            "avoid_for": ["low_memory"],
            "memory_level": ResourceLevel.MEDIUM,
            "cpu_level": ResourceLevel.MEDIUM,
        },
        "quick_sort": {
            "time": "O(n log n)",
            "space": "O(log n)",
            "stable": False,
            "in_place": True,
            "best_for": ["large", "random", "general_purpose"],
            "avoid_for": ["stability_required", "worst_case_critical"],
            "memory_level": ResourceLevel.LOW,
            "cpu_level": ResourceLevel.MEDIUM,
        },
        "heap_sort": {
            "time": "O(n log n)",
            "space": "O(1)",
            "stable": False,
            "in_place": True,
            "best_for": ["low_memory", "guaranteed_performance"],
            "avoid_for": ["cache_efficiency_critical"],
            "memory_level": ResourceLevel.LOW,
            "cpu_level": ResourceLevel.MEDIUM,
        },
        "tim_sort": {
            "time": "O(n log n)",
            "space": "O(n)",
            "stable": True,
            "in_place": False,
            "best_for": ["real_world", "partially_sorted", "production"],
            "avoid_for": ["low_memory"],
            "memory_level": ResourceLevel.MEDIUM,
            "cpu_level": ResourceLevel.MEDIUM,
        },
    }

    ML_ALGORITHMS = {
        "linear_regression": {
            "time": "O(n²d)",
            "space": "O(nd)",
            "training_speed": "fast",
            "inference_speed": "very_fast",
            "best_for": ["regression", "linear_relationships", "interpretability"],
            "avoid_for": ["non_linear", "complex_patterns"],
            "memory_level": ResourceLevel.LOW,
            "cpu_level": ResourceLevel.LOW,
            "gpu_required": False,
        },
        "logistic_regression": {
            "time": "O(nd)",
            "space": "O(d)",
            "training_speed": "fast",
            "inference_speed": "very_fast",
            "best_for": ["binary_classification", "probability_estimates"],
            "avoid_for": ["multi_class_complex", "non_linear"],
            "memory_level": ResourceLevel.LOW,
            "cpu_level": ResourceLevel.LOW,
            "gpu_required": False,
        },
        "decision_tree": {
            "time": "O(n log n)",
            "space": "O(n)",
            "training_speed": "medium",
            "inference_speed": "fast",
            "best_for": ["interpretability", "mixed_features", "non_linear"],
            "avoid_for": ["overfitting_prone", "unstable"],
            "memory_level": ResourceLevel.MEDIUM,
            "cpu_level": ResourceLevel.MEDIUM,
            "gpu_required": False,
        },
        "random_forest": {
            "time": "O(n log n * trees)",
            "space": "O(n * trees)",
            "training_speed": "medium",
            "inference_speed": "medium",
            "best_for": ["general_purpose", "robust", "feature_importance"],
            "avoid_for": ["real_time_inference", "low_memory"],
            "memory_level": ResourceLevel.MEDIUM,
            "cpu_level": ResourceLevel.MEDIUM,
            "gpu_required": False,
        },
        "neural_network": {
            "time": "O(n*d*h*epochs)",
            "space": "O(d*h)",
            "training_speed": "slow",
            "inference_speed": "fast",
            "best_for": ["complex_patterns", "large_data", "deep_learning"],
            "avoid_for": ["small_data", "interpretability", "edge_devices"],
            "memory_level": ResourceLevel.HIGH,
            "cpu_level": ResourceLevel.HIGH,
            "gpu_required": True,
        },
        "knn": {
            "time": "O(nd)",
            "space": "O(nd)",
            "training_speed": "instant",
            "inference_speed": "slow",
            "best_for": ["small_datasets", "simple_patterns"],
            "avoid_for": ["large_data", "real_time", "high_dimensions"],
            "memory_level": ResourceLevel.MEDIUM,
            "cpu_level": ResourceLevel.MEDIUM,
            "gpu_required": False,
        },
    }

    @classmethod
    def select_sorting_algorithm(cls, constraints: Constraints) -> Dict[str, Any]:
        """
        Select optimal sorting algorithm based on constraints.

        Args:
            constraints: Resource constraints

        Returns:
            Recommendation dict with algorithm and reasoning
        """
        candidates = []

        for name, props in cls.SORTING_ALGORITHMS.items():
            score = cls._score_algorithm(props, constraints)
            candidates.append((name, props, score))

        # Sort by score
        candidates.sort(key=lambda x: x[2], reverse=True)

        best = candidates[0]

        return {
            "recommended": best[0],
            "properties": best[1],
            "score": best[2],
            "alternatives": [{"name": c[0], "score": c[2]} for c in candidates[1:3]],
            "reasoning": cls._generate_reasoning(best[0], best[1], constraints),
        }

    @classmethod
    def select_ml_algorithm(
        cls, constraints: Constraints, problem_type: str = "classification"
    ) -> Dict[str, Any]:
        """
        Select optimal ML algorithm based on constraints.

        Args:
            constraints: Resource constraints
            problem_type: 'classification', 'regression', or 'clustering'

        Returns:
            Recommendation dict
        """
        candidates = []

        for name, props in cls.ML_ALGORITHMS.items():
            # Filter by problem type
            if problem_type == "regression" and "regression" not in name:
                if name not in ["neural_network", "knn"]:
                    continue

            score = cls._score_ml_algorithm(props, constraints, problem_type)
            candidates.append((name, props, score))

        candidates.sort(key=lambda x: x[2], reverse=True)

        if not candidates:
            return {"error": "No suitable algorithm found"}

        best = candidates[0]

        return {
            "recommended": best[0],
            "properties": best[1],
            "score": best[2],
            "alternatives": [{"name": c[0], "score": c[2]} for c in candidates[1:3]],
            "reasoning": cls._generate_ml_reasoning(
                best[0], best[1], constraints, problem_type
            ),
        }

    @staticmethod
    def _score_algorithm(props: Dict[str, Any], constraints: Constraints) -> float:
        """Score algorithm based on how well it matches constraints."""
        score = 100.0

        # Memory constraint
        if constraints.memory == ResourceLevel.LOW:
            if props["memory_level"] == ResourceLevel.LOW:
                score += 30
            else:
                score -= 30

        # Dataset size
        dataset_match = False
        if constraints.dataset_size == "small":
            dataset_match = "very_small" in props["best_for"]
        elif constraints.dataset_size == "large":
            dataset_match = "large" in props["best_for"]

        if dataset_match:
            score += 20

        # Edge device
        if constraints.is_edge_device:
            if props["space"] == "O(1)":
                score += 25
            else:
                score -= 15

        return max(0, score)

    @staticmethod
    def _score_ml_algorithm(
        props: Dict[str, Any], constraints: Constraints, problem_type: str
    ) -> float:
        """Score ML algorithm based on constraints."""
        score = 100.0

        # GPU requirement
        if constraints.is_edge_device or constraints.power_constrained:
            if props.get("gpu_required", False):
                score -= 50

        # Memory
        if constraints.memory == ResourceLevel.LOW:
            if props["memory_level"] == ResourceLevel.LOW:
                score += 30
            elif props["memory_level"] == ResourceLevel.HIGH:
                score -= 40

        # Latency requirement
        if constraints.latency_requirement in ["low", "ultra"]:
            if props["inference_speed"] == "very_fast":
                score += 30
            elif props["inference_speed"] == "slow":
                score -= 30

        # Dataset size
        if constraints.dataset_size == "huge":
            if "large_data" in props["best_for"]:
                score += 20
            if "small_data" in props["avoid_for"]:
                score += 10
        elif constraints.dataset_size == "small":
            if "small_data" in props["avoid_for"]:
                score -= 20

        return max(0, score)

    @staticmethod
    def _generate_reasoning(
        name: str, props: Dict[str, Any], constraints: Constraints
    ) -> List[str]:
        """Generate human-readable reasoning."""
        reasons = []

        reasons.append(
            f"Time complexity: {props['time']}, " f"Space complexity: {props['space']}"
        )

        if constraints.memory == ResourceLevel.LOW:
            reasons.append("Selected for low memory footprint")

        if constraints.is_edge_device:
            reasons.append("Suitable for edge deployment")

        if props["stable"]:
            reasons.append("Provides stable sorting")

        return reasons

    @staticmethod
    def _generate_ml_reasoning(
        name: str, props: Dict[str, Any], constraints: Constraints, problem_type: str
    ) -> List[str]:
        """Generate ML-specific reasoning."""
        reasons = []

        reasons.append(f"Suitable for {problem_type} problems")
        reasons.append(
            f"Training speed: {props['training_speed']}, "
            f"Inference speed: {props['inference_speed']}"
        )

        if not props.get("gpu_required", False):
            reasons.append("Can run on CPU only")
        else:
            reasons.append("Requires GPU for optimal performance")

        if constraints.is_edge_device:
            reasons.append("Optimized for edge deployment")

        return reasons


def print_recommendation(recommendation: Dict[str, Any]) -> None:
    """Print formatted recommendation."""
    print("\n" + "=" * 70)
    print("ALGORITHM RECOMMENDATION")
    print("=" * 70)

    print(f"\n✓ Recommended: {recommendation['recommended']}")
    print(f"  Score: {recommendation['score']:.1f}/100")

    print("\nProperties:")
    for key, value in recommendation["properties"].items():
        if key not in ["best_for", "avoid_for"]:
            print(f"  {key}: {value}")

    print("\nReasoning:")
    for i, reason in enumerate(recommendation["reasoning"], 1):
        print(f"  {i}. {reason}")

    if recommendation.get("alternatives"):
        print("\nAlternatives:")
        for alt in recommendation["alternatives"]:
            print(f"  - {alt['name']} (score: {alt['score']:.1f})")

    print("=" * 70)
