#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classify algorithms into well-known types.
Uses algorithm name, lecture name, and content to determine type.
"""

from pathlib import Path
from typing import Optional, Dict
import re

ROOT = Path(__file__).resolve().parents[1]

# Well-known algorithm types
ALGORITHM_TYPES = {
    "fundamental": [
        "sort", "search", "bubble", "insertion", "selection", "merge", "quick", "heap",
        "radix", "counting", "bucket", "linear_search", "binary_search", "jump_search",
        "interpolation_search", "fibonacci", "factorial", "gcd", "prime", "euclidean"
    ],
    "data_structure": [
        "tree", "heap", "queue", "stack", "linked_list", "array", "hash_table", "hash",
        "trie", "graph", "avl", "red_black", "b_tree", "binary_tree", "bst", "priority_queue",
        "chaining", "open_addressing", "adjacency", "matrix"
    ],
    "graph": [
        "bfs", "dfs", "dijkstra", "bellman_ford", "floyd_warshall", "kruskal", "prim",
        "topological", "shortest_path", "minimum_spanning", "graph", "network"
    ],
    "dynamic_programming": [
        "knapsack", "edit_distance", "longest_common", "subsequence", "substring",
        "fibonacci", "memoization", "dynamic_programming", "dp"
    ],
    "greedy": [
        "greedy", "activity_selection", "fractional_knapsack", "huffman", "kruskal", "prim"
    ],
    "string": [
        "kmp", "rabin_karp", "boyer_moore", "string", "pattern", "matching", "trie"
    ],
    "ml": [
        "linear_regression", "logistic_regression", "decision_tree", "random_forest",
        "kmeans", "knn", "naive_bayes", "svm", "neural_network", "gradient_descent",
        "clustering", "classification", "regression", "supervised", "unsupervised"
    ],
    "ai": [
        "a_star", "minimax", "alpha_beta", "genetic", "simulated_annealing", "particle_swarm",
        "reinforcement", "q_learning", "monte_carlo", "heuristic", "search_algorithm"
    ],
    "db": [
        "sql", "query", "join", "index", "transaction", "database", "nosql", "mongodb",
        "postgresql", "mysql", "schema", "migration", "data_warehouse", "data_lake",
        "etl", "data_pipeline", "data_modeling", "normalization", "denormalization"
    ],
    "security": [
        "encryption", "decryption", "hash", "cryptography", "rsa", "aes", "ssl", "tls",
        "authentication", "authorization", "jwt", "oauth", "security", "audit", "masking",
        "row_level", "column_level", "gdpr", "compliance"
    ],
    "integration": [
        "api", "rest", "soap", "graphql", "microservice", "message_queue", "event_sourcing",
        "cqrs", "publish_subscribe", "message_broker", "integration", "service_bus"
    ],
    "multithreading": [
        "thread", "concurrent", "parallel", "multithreading", "async", "await", "lock",
        "mutex", "semaphore", "deadlock", "race_condition", "producer_consumer",
        "readers_writers", "thread_pool", "executor", "futures", "promises"
    ],
    "system": [
        "scheduling", "memory", "process", "cache", "paging", "virtual_memory",
        "file_system", "operating_system", "os", "kernel"
    ],
    "design_pattern": [
        "singleton", "factory", "observer", "strategy", "adapter", "decorator", "proxy",
        "command", "iterator", "composite", "facade", "template", "builder", "prototype",
        "chain", "bridge", "memento", "state", "visitor", "pattern"
    ],
    "architecture": [
        "mvc", "mvvm", "clean_architecture", "hexagonal", "microservice", "monolith",
        "layered", "event_driven", "domain_driven", "architecture"
    ],
    "data_engineering": [
        "data_pipeline", "etl", "data_warehouse", "data_lake", "streaming", "batch",
        "lambda", "kappa", "data_mesh", "data_ops", "data_governance", "data_catalog"
    ],
    "devops": [
        "ci_cd", "docker", "kubernetes", "deployment", "monitoring", "logging", "metrics",
        "observability", "tracing", "infrastructure", "automation"
    ]
}


def classify_algorithm_type(
    algorithm_name: str,
    lecture_name: Optional[str] = None,
    content: Optional[str] = None
) -> str:
    """
    Classify algorithm into a well-known type.
    
    Args:
        algorithm_name: Name of the algorithm
        lecture_name: Name of the lecture (optional)
        content: Algorithm content/description (optional)
    
    Returns:
        Algorithm type string
    """
    algo_lower = algorithm_name.lower()
    lecture_lower = (lecture_name or "").lower()
    content_lower = (content or "").lower()
    
    combined_text = f"{algo_lower} {lecture_lower} {content_lower}"
    
    # Check each type in order of specificity
    type_scores = {}
    
    for algo_type, keywords in ALGORITHM_TYPES.items():
        score = 0
        for keyword in keywords:
            if keyword in algo_lower:
                score += 3  # Strong match in algorithm name
            if keyword in lecture_lower:
                score += 2  # Match in lecture name
            if keyword in content_lower:
                score += 1  # Match in content
        if score > 0:
            type_scores[algo_type] = score
    
    if type_scores:
        # Return type with highest score
        return max(type_scores.items(), key=lambda x: x[1])[0]
    
    # Additional heuristics based on lecture names
    if "pattern" in lecture_lower or "design" in lecture_lower:
        if any(x in algo_lower for x in ["singleton", "factory", "observer", "strategy"]):
            return "design_pattern"
    
    if "concurrency" in lecture_lower or "thread" in lecture_lower:
        return "multithreading"
    
    if "security" in lecture_lower:
        return "security"
    
    if "integration" in lecture_lower:
        return "integration"
    
    if "database" in lecture_lower or "db" in lecture_lower:
        return "db"
    
    if "ml" in lecture_lower or "machine_learning" in lecture_lower:
        return "ml"
    
    if "ai" in lecture_lower or "artificial" in lecture_lower:
        return "ai"
    
    # Default classification based on common patterns
    if any(x in algo_lower for x in ["sort", "search"]):
        return "fundamental"
    
    if any(x in algo_lower for x in ["tree", "heap", "queue", "stack", "hash"]):
        return "data_structure"
    
    # Default
    return "fundamental"


def update_algorithm_metadata_files():
    """Update all metadata.json files with algorithm_type."""
    updated_count = 0
    
    for algo_dir in ROOT.rglob("*/algorithm.py"):
        algo_dir = algo_dir.parent
        metadata_file = algo_dir / "metadata.json"
        
        # Read existing metadata or create new
        metadata = {}
        if metadata_file.exists():
            try:
                metadata = json.loads(metadata_file.read_text(encoding="utf-8"))
            except:
                pass
        
        # Determine algorithm type
        algorithm_name = algo_dir.name
        lecture_name = algo_dir.parent.name if algo_dir.parent else None
        
        # Try to read README for content
        content = ""
        readme_file = algo_dir / "README.md"
        if readme_file.exists():
            try:
                content = readme_file.read_text(encoding="utf-8")[:1000]  # First 1000 chars
            except:
                pass
        
        algorithm_type = classify_algorithm_type(algorithm_name, lecture_name, content)
        
        # Update metadata
        if metadata.get("algorithm_type") != algorithm_type:
            metadata["algorithm_type"] = algorithm_type
            import json
            metadata_file.write_text(
                json.dumps(metadata, indent=2, ensure_ascii=False),
                encoding="utf-8"
            )
            updated_count += 1
            print(f"Updated {algo_dir.relative_to(ROOT)}: {algorithm_type}")
    
    print(f"\nUpdated {updated_count} algorithm metadata files")
    return updated_count


if __name__ == "__main__":
    import json
    update_algorithm_metadata_files()

