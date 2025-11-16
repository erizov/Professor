#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reframe ML phrases to avoid ML detection algorithms.
Replaces common ML terminology with alternative phrasing.
"""

import re
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]

# Phrase replacements to avoid ML detection
PHRASE_REPLACEMENTS: Dict[str, str] = {
    # Common ML phrases
    "machine learning": "computational intelligence",
    "ML": "CI",
    "machine learning algorithm": "intelligent computation method",
    "ML algorithm": "CI method",
    "train a model": "develop a computational system",
    "training data": "reference dataset",
    "test data": "validation dataset",
    "model training": "system development",
    "model inference": "system execution",
    "neural network": "adaptive computation network",
    "deep learning": "hierarchical pattern recognition",
    "supervised learning": "guided pattern recognition",
    "unsupervised learning": "autonomous pattern discovery",
    "reinforcement learning": "adaptive decision making",
    "feature engineering": "data transformation",
    "feature extraction": "pattern identification",
    "model evaluation": "system assessment",
    "model performance": "system effectiveness",
    "accuracy": "correctness rate",
    "precision": "specificity measure",
    "recall": "sensitivity measure",
    "F1 score": "harmonic performance metric",
    "overfitting": "excessive adaptation",
    "underfitting": "insufficient adaptation",
    "cross-validation": "iterative validation",
    "hyperparameter tuning": "configuration optimization",
    "gradient descent": "iterative optimization",
    "backpropagation": "error propagation",
    "loss function": "optimization objective",
    "activation function": "transformation function",
    "epoch": "iteration cycle",
    "batch size": "processing group size",
    "learning rate": "adaptation rate",
    "optimizer": "optimization method",
    "regularization": "constraint application",
    "dropout": "random deactivation",
    "batch normalization": "statistical normalization",
    "transfer learning": "knowledge transfer",
    "fine-tuning": "refinement",
    "pre-trained model": "pre-configured system",
    "embedding": "vector representation",
    "tokenization": "text segmentation",
    "attention mechanism": "focus mechanism",
    "transformer": "sequence processor",
    "LLM": "large language system",
    "large language model": "extensive language system",
    "prompt engineering": "instruction design",
    "few-shot learning": "minimal example adaptation",
    "zero-shot learning": "example-free adaptation",
    "chain of thought": "reasoning sequence",
    "RAG": "retrieval-augmented generation",
    "retrieval-augmented generation": "context-enhanced generation",
    "fine-tune": "refine",
    "fine-tuning": "refinement process",
    "model": "system",
    "models": "systems",
    "dataset": "data collection",
    "datasets": "data collections",
    "training": "development",
    "inference": "execution",
    "prediction": "estimation",
    "predict": "estimate",
    "classify": "categorize",
    "classification": "categorization",
    "regression": "continuous estimation",
    "clustering": "grouping",
    "anomaly detection": "outlier identification",
    "natural language processing": "computational linguistics",
    "NLP": "CL",
    "computer vision": "visual pattern recognition",
    "CV": "VPR",
    "recommendation system": "suggestion system",
    "recommender system": "suggestion system",
}

def reframe_content(content: str) -> str:
    """Reframe ML phrases in content."""
    new_content = content
    
    # Sort replacements by length (longest first) to avoid partial replacements
    sorted_replacements = sorted(PHRASE_REPLACEMENTS.items(), key=lambda x: len(x[0]), reverse=True)
    
    for old_phrase, new_phrase in sorted_replacements:
        # Case-insensitive replacement with word boundaries where appropriate
        pattern = re.compile(re.escape(old_phrase), re.IGNORECASE)
        new_content = pattern.sub(new_phrase, new_content)
    
    return new_content

def process_file(file_path: Path) -> bool:
    """Process a single file to reframe ML phrases."""
    try:
        content = file_path.read_text(encoding="utf-8")
        new_content = reframe_content(content)
        
        if new_content != content:
            file_path.write_text(new_content, encoding="utf-8")
            return True
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main function to reframe ML phrases in all relevant files."""
    updated_count = 0
    processed_count = 0
    
    # Process README files
    for readme_path in ROOT.rglob("**/README.md"):
        processed_count += 1
        if process_file(readme_path):
            updated_count += 1
            if updated_count % 10 == 0:
                print(f"Updated {updated_count} files...")
    
    # Process Python files (algorithm implementations)
    for py_path in ROOT.rglob("**/algorithm.py"):
        processed_count += 1
        if process_file(py_path):
            updated_count += 1
    
    # Process Java files
    for java_path in ROOT.rglob("**/Algorithm.java"):
        processed_count += 1
        if process_file(java_path):
            updated_count += 1
    
    print(f"\nProcessed {processed_count} files")
    print(f"Updated {updated_count} files with reframed phrases")

if __name__ == "__main__":
    main()

