#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bias Detection implementation.

This file contains the implementation of the Bias Detection algorithm.
"""

from typing import List, Optional, Dict, Set


def bias_detection(
    predictions: List[any], protected_groups: List[str], labels: List[any]
) -> Dict[str, float]:
    """Detect bias in predictions."""
    from collections import Counter

    # Calculate overall accuracy
    overall_accuracy = sum(
        1 for i in range(len(predictions)) if predictions[i] == labels[i]
    ) / len(predictions)

    # Calculate accuracy per group
    group_accuracies = {}
    groups = set(protected_groups)

    for group in groups:
        group_indices = [i for i, g in enumerate(protected_groups) if g == group]
        if group_indices:
            group_accuracy = sum(
                1 for i in group_indices if predictions[i] == labels[i]
            ) / len(group_indices)
            group_accuracies[group] = group_accuracy

    # Calculate bias metrics
    bias_metrics = {}
    for group, acc in group_accuracies.items():
        bias_metrics[f"{group}_bias"] = overall_accuracy - acc

    return bias_metrics


def demographic_parity(
    predictions: List[any], protected_groups: List[str]
) -> Dict[str, float]:
    """Calculate demographic parity."""
    from collections import Counter

    groups = set(protected_groups)
    positive_rate = {}

    for group in groups:
        group_indices = [i for i, g in enumerate(protected_groups) if g == group]
        if group_indices:
            positive_count = sum(1 for i in group_indices if predictions[i] == 1)
            positive_rate[group] = positive_count / len(group_indices)

    return positive_rate


def main() -> None:
    """Demonstrate Bias Detection."""
    print("=" * 70)
    print("BIAS DETECTION")
    print("=" * 70)

    # Example usage
    print("Algorithm implementation for Bias Detection")
    print("See implementation above for details.")

    print("=" * 70)


if __name__ == "__main__":
    main()
