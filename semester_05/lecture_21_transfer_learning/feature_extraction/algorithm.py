#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Feature Extraction implementation.

This file contains the implementation of the Feature Extraction algorithm.
"""

from typing import List, Optional, Dict, Set


def feature_extraction(data: List[any], 
                        extraction_method: str = "statistical") -> List[List[float]]:
    """Feature extraction from raw data."""
    features = []
    
    if extraction_method == "statistical":
        for item in data:
            if isinstance(item, list):
                # Statistical features
                if item:
                    features.append([
                        len(item),
                        sum(item) / len(item) if item else 0.0,  # mean
                        min(item) if item else 0.0,  # min
                        max(item) if item else 0.0,  # max
                        sum((x - sum(item)/len(item))**2 for x in item) / len(item) if item else 0.0  # variance
                    ])
                else:
                    features.append([0.0, 0.0, 0.0, 0.0, 0.0])
            else:
                features.append([float(item)])
    
    return features

def tfidf_feature_extraction(documents: List[str]) -> List[List[float]]:
    """TF-IDF feature extraction."""
    from collections import Counter
    
    # Calculate term frequencies
    all_terms = set()
    doc_terms = []
    for doc in documents:
        terms = doc.lower().split()
        all_terms.update(terms)
        doc_terms.append(Counter(terms))
    
    # Calculate IDF
    idf = {}
    for term in all_terms:
        doc_count = sum(1 for dt in doc_terms if term in dt)
        idf[term] = math.log(len(documents) / (doc_count + 1))
    
    # Calculate TF-IDF
    features = []
    for dt in doc_terms:
        feature_vector = []
        for term in sorted(all_terms):
            tf = dt.get(term, 0) / sum(dt.values()) if dt else 0
            tfidf = tf * idf[term]
            feature_vector.append(tfidf)
        features.append(feature_vector)
    
    return features


def main() -> None:
    """Demonstrate Feature Extraction."""
    print("=" * 70)
    print("FEATURE EXTRACTION")
    print("=" * 70)
    
    # Example usage
    print("Algorithm implementation for Feature Extraction")
    print("See implementation above for details.")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
