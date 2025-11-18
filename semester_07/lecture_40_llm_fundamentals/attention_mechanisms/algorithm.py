#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Attention Mechanisms implementation.

This file contains the implementation of the Attention Mechanisms algorithm.
"""

from typing import List, Optional, Dict, Set


def scaled_dot_product_attention(query: List[List[float]], 
                                    key: List[List[float]], 
                                    value: List[List[float]], 
                                    mask: Optional[List[List[bool]]] = None) -> tuple:
    """Scaled dot-product attention."""
    import math
    
    d_k = len(query[0])
    scores = []
    
    # Compute attention scores
    for q in query:
        row_scores = []
        for k in key:
            score = sum(q[i] * k[i] for i in range(d_k)) / math.sqrt(d_k)
            row_scores.append(score)
        scores.append(row_scores)
    
    # Apply mask if provided
    if mask:
        for i in range(len(scores)):
            for j in range(len(scores[i])):
                if not mask[i][j]:
                    scores[i][j] = float('-inf')
    
    # Softmax
    attention_weights = []
    for row in scores:
        max_score = max(row)
        exp_scores = [math.exp(s - max_score) for s in row]
        sum_exp = sum(exp_scores)
        attention_weights.append([exp / sum_exp for exp in exp_scores])
    
    # Apply attention to values
    output = []
    for weights in attention_weights:
        output_row = [0.0] * len(value[0])
        for i, weight in enumerate(weights):
            for j in range(len(value[i])):
                output_row[j] += weight * value[i][j]
        output.append(output_row)
    
    return output, attention_weights


def main() -> None:
    """Demonstrate Attention Mechanisms."""
    print("=" * 70)
    print("ATTENTION MECHANISMS")
    print("=" * 70)
    
    # Example usage
    print("Algorithm implementation for Attention Mechanisms")
    print("See implementation above for details.")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
