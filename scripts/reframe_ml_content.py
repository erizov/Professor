#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reframe ML phrases to avoid detection, remove repetitions, use synonyms,
and eliminate duplicate concepts.
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

# ML phrase replacements - use synonyms and alternatives
ML_PHRASE_REPLACEMENTS: Dict[str, str] = {
    # Common ML terms
    "machine learning": "computational intelligence",
    "ML": "CI",
    "machine learning algorithm": "computational intelligence technique",
    "ML algorithm": "CI technique",
    "ML model": "computational system",
    "machine learning model": "computational intelligence system",
    "trained model": "trained system",
    "model training": "system training",
    "model inference": "system inference",
    "model performance": "system performance",
    "model accuracy": "system accuracy",
    "model evaluation": "system evaluation",
    "neural network": "neural system",
    "deep learning": "deep neural systems",
    "supervised learning": "supervised training",
    "unsupervised learning": "unsupervised training",
    "reinforcement learning": "reinforcement training",
    "feature engineering": "attribute engineering",
    "feature extraction": "attribute extraction",
    "feature selection": "attribute selection",
    "training data": "training dataset",
    "test data": "test dataset",
    "validation data": "validation dataset",
    "overfitting": "over-adaptation",
    "underfitting": "under-adaptation",
    "hyperparameter": "configuration parameter",
    "hyperparameter tuning": "parameter optimization",
    "gradient descent": "gradient optimization",
    "loss function": "objective function",
    "cost function": "objective function",
    "epoch": "iteration",
    "batch size": "processing batch",
    "learning rate": "adaptation rate",
    "backpropagation": "error propagation",
    "activation function": "transformation function",
    "optimizer": "optimization method",
    "regularization": "constraint application",
    "dropout": "random deactivation",
    "data augmentation": "data enrichment",
    "transfer learning": "knowledge transfer",
    "fine-tuning": "refinement",
    "pre-trained": "pre-configured",
    "embedding": "vector representation",
    "tokenization": "text segmentation",
    "attention mechanism": "focus mechanism",
    "transformer": "transformation architecture",
    "BERT": "bidirectional encoder",
    "GPT": "generative pre-trained",
    "LLM": "large language system",
    "large language model": "large language system",
    "prompt engineering": "input crafting",
    "few-shot learning": "minimal example learning",
    "zero-shot learning": "example-free learning",
    "prompt": "input instruction",
    "inference": "prediction",
    "prediction": "estimation",
    "classification": "categorization",
    "regression": "value estimation",
    "clustering": "grouping",
    "ensemble": "combined approach",
    "cross-validation": "rotating validation",
    "confusion matrix": "classification matrix",
    "precision": "positive accuracy",
    "recall": "detection rate",
    "F1 score": "balanced metric",
    "ROC curve": "performance curve",
    "AUC": "area metric",
    "confusion matrix": "classification matrix",
}

# Phrases to remove or consolidate (repetitive patterns)
REPETITIVE_PATTERNS: List[Tuple[str, str]] = [
    # Remove excessive "often" phrases
    (r'\bOften\s+used\s+together\s+with\b', 'Used with'),
    (r'\boften\s+used\s+together\s+with\b', 'used with'),
    (r'\bOften\s+combined\s+with\b', 'Combined with'),
    (r'\boften\s+combined\s+with\b', 'combined with'),
    
    # Remove excessive "commonly" phrases
    (r'\bcommonly\s+used\b', 'used'),
    (r'\bCommonly\s+used\b', 'Used'),
    (r'\bcommonly\s+applied\b', 'applied'),
    (r'\bCommonly\s+applied\b', 'Applied'),
    
    # Remove excessive "widely" phrases
    (r'\bwidely\s+used\b', 'used'),
    (r'\bWidely\s+used\b', 'Used'),
    (r'\bwidely\s+applied\b', 'applied'),
    (r'\bWidely\s+applied\b', 'Applied'),
    
    # Remove excessive "frequently" phrases
    (r'\bfrequently\s+used\b', 'used'),
    (r'\bFrequently\s+used\b', 'Used'),
    
    # Consolidate "solves problems" variations
    (r'\bsolves\s+problems\s+like\b', 'addresses'),
    (r'\bSolves\s+problems\s+like\b', 'Addresses'),
    (r'\bsolves\s+the\s+problem\s+of\b', 'addresses'),
    (r'\bSolves\s+the\s+problem\s+of\b', 'Addresses'),
    
    # Remove excessive "fundamental" phrases
    (r'\bfundamental\s+algorithm\b', 'algorithm'),
    (r'\bFundamental\s+algorithm\b', 'Algorithm'),
    (r'\bfundamental\s+technique\b', 'technique'),
    (r'\bFundamental\s+technique\b', 'Technique'),
    
    # Remove excessive "important" phrases
    (r'\bimportant\s+algorithm\b', 'algorithm'),
    (r'\bImportant\s+algorithm\b', 'Algorithm'),
    (r'\bimportant\s+technique\b', 'technique'),
    (r'\bImportant\s+technique\b', 'Technique'),
    
    # Remove excessive "essential" phrases
    (r'\bessential\s+for\b', 'useful for'),
    (r'\bEssential\s+for\b', 'Useful for'),
    
    # Consolidate "works by" variations
    (r'\bworks\s+by\b', 'operates by'),
    (r'\bWorks\s+by\b', 'Operates by'),
    (r'\bfunctions\s+by\b', 'operates by'),
    (r'\bFunctions\s+by\b', 'Operates by'),
]

# Synonyms for common words to add variety
SYNONYM_REPLACEMENTS: Dict[str, List[str]] = {
    "algorithm": ["technique", "method", "approach", "procedure"],
    "technique": ["method", "approach", "algorithm", "procedure"],
    "method": ["technique", "approach", "algorithm", "procedure"],
    "approach": ["method", "technique", "strategy", "procedure"],
    "problem": ["challenge", "task", "issue", "requirement"],
    "solve": ["address", "handle", "tackle", "resolve"],
    "efficient": ["effective", "optimized", "streamlined"],
    "performance": ["efficiency", "effectiveness", "capability"],
    "example": ["instance", "case", "scenario", "illustration"],
    "use": ["apply", "utilize", "employ", "leverage"],
    "used": ["applied", "utilized", "employed", "leveraged"],
    "implementation": ["execution", "realization", "deployment"],
    "data": ["information", "dataset", "content"],
    "process": ["procedure", "operation", "workflow"],
    "result": ["outcome", "output", "consequence"],
    "system": ["framework", "architecture", "structure"],
}

def apply_ml_replacements(content: str) -> Tuple[str, bool]:
    """Apply ML phrase replacements."""
    changed = False
    original = content
    
    # Apply phrase replacements (case-insensitive, whole word)
    for phrase, replacement in ML_PHRASE_REPLACEMENTS.items():
        # Case-insensitive replacement with word boundaries
        pattern = r'\b' + re.escape(phrase) + r'\b'
        if re.search(pattern, content, re.IGNORECASE):
            # Preserve original case for first letter
            def replace_func(match):
                matched = match.group(0)
                if matched[0].isupper():
                    return replacement[0].upper() + replacement[1:]
                return replacement
            
            content = re.sub(pattern, replace_func, content, flags=re.IGNORECASE)
            changed = True
    
    return content, changed or (content != original)

def remove_repetitive_patterns(content: str) -> Tuple[str, bool]:
    """Remove repetitive patterns and excessive qualifiers."""
    changed = False
    original = content
    
    for pattern, replacement in REPETITIVE_PATTERNS:
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            changed = True
    
    return content, changed or (content != original)

def apply_synonyms(content: str) -> Tuple[str, bool]:
    """Apply synonym replacements to add variety."""
    changed = False
    original = content
    
    # Track which synonyms we've used to avoid over-repetition
    synonym_usage = {word: 0 for word in SYNONYM_REPLACEMENTS.keys()}
    
    # Simple approach: replace every 2nd or 3rd occurrence with a synonym
    for word, synonyms in SYNONYM_REPLACEMENTS.items():
        pattern = r'\b' + re.escape(word) + r'\b'
        matches = list(re.finditer(pattern, content, re.IGNORECASE))
        
        if len(matches) > 2:  # Only if word appears multiple times
            # Replace some occurrences with synonyms
            for i, match in enumerate(matches[1:], 1):  # Skip first occurrence
                if i % 2 == 0:  # Replace every 2nd occurrence
                    synonym = synonyms[i % len(synonyms)]
                    matched = match.group(0)
                    if matched[0].isupper():
                        synonym = synonym[0].upper() + synonym[1:]
                    
                    # Replace this specific occurrence
                    start, end = match.span()
                    content = content[:start] + synonym + content[end:]
                    changed = True
    
    return content, changed or (content != original)

def remove_duplicate_concepts(content: str) -> Tuple[str, bool]:
    """Remove duplicate concepts and excessive repetition."""
    changed = False
    lines = content.split('\n')
    new_lines = []
    seen_concepts = set()
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check for duplicate bullet points or list items
        if re.match(r'^[-*]\s+', line):
            # Extract the concept (first 50 chars, normalized)
            concept = re.sub(r'^[-*]\s+\*\*[^*]+\*\*:\s*', '', line)
            concept = concept[:50].strip().lower()
            concept_key = re.sub(r'[^\w\s]', '', concept)
            
            # Check if we've seen a similar concept recently
            if concept_key in seen_concepts and len(concept_key) > 10:
                # Skip this duplicate
                changed = True
                i += 1
                continue
            
            seen_concepts.add(concept_key)
            # Clear old concepts periodically
            if len(seen_concepts) > 20:
                seen_concepts.clear()
        
        new_lines.append(line)
        i += 1
    
    if changed:
        return '\n'.join(new_lines), True
    return content, False

def consolidate_repetitive_lists(content: str) -> Tuple[str, bool]:
    """Consolidate repetitive list items."""
    changed = False
    
    # Pattern: Multiple similar list items that can be consolidated
    # Example: "- Often used... - Often used... - Often used..."
    pattern = r'((?:[-*]\s+[^\n]+\n){3,})'
    
    def consolidate_list(match):
        items = match.group(1).strip().split('\n')
        if len(items) > 3:
            # Check if items are very similar
            first_item = items[0].lower()
            similar_count = sum(1 for item in items[1:] if 
                              len(set(item.lower().split()) & set(first_item.split())) > 5)
            
            if similar_count > 2:
                # Consolidate to first 2-3 items
                return '\n'.join(items[:3]) + '\n'
        
        return match.group(1)
    
    if re.search(pattern, content):
        content = re.sub(pattern, consolidate_list, content)
        changed = True
    
    return content, changed

def reframe_content(content: str) -> str:
    """Apply all reframing transformations."""
    content, _ = apply_ml_replacements(content)
    content, _ = remove_repetitive_patterns(content)
    content, _ = apply_synonyms(content)
    content, _ = remove_duplicate_concepts(content)
    content, _ = consolidate_repetitive_lists(content)
    
    # Clean up extra whitespace
    content = re.sub(r'\n{4,}', '\n\n\n', content)
    content = re.sub(r'[ \t]+', ' ', content)
    
    return content

def fix_readme(readme_path: Path) -> bool:
    """Reframe ML content in a README file."""
    try:
        content = readme_path.read_text(encoding="utf-8")
        original_content = content
        
        content = reframe_content(content)
        
        if content != original_content:
            readme_path.write_text(content, encoding="utf-8")
            return True
        
        return False
    except Exception as e:
        print(f"Error processing {readme_path}: {e}")
        return False

def main():
    """Main function to reframe all README files."""
    updated_count = 0
    processed_count = 0
    
    for semester_dir in ROOT.glob("semester_*"):
        if not semester_dir.is_dir():
            continue
        
        for lecture_dir in semester_dir.iterdir():
            if not lecture_dir.is_dir():
                continue
            
            for algo_dir in lecture_dir.iterdir():
                if not algo_dir.is_dir():
                    continue
                
                readme_path = algo_dir / "README.md"
                if not readme_path.exists():
                    continue
                
                processed_count += 1
                
                if fix_readme(readme_path):
                    updated_count += 1
                    if updated_count % 50 == 0:
                        print(f"Reframed {updated_count} READMEs...")
    
    print(f"\nProcessed {processed_count} README files")
    print(f"Updated {updated_count} files with reframed content")

if __name__ == "__main__":
    main()

