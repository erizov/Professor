"""Count entries with placeholders in target columns."""
from algo_fetcher import init_db, Session, AlgorithmDescription
import re

init_db()
session = Session()

placeholder_patterns = [
    r'\[specific purpose\]', r'\[specific mechanism\]', r'\[конкретная цель\]',
    r'\[конкретный механизм\]', r'\[.*?\]', r'placeholder', r'заполнитель',
    r'конкретный алгоритм/техника', r'конкретных задач в области',
    r'для решения конкретных задач', r'в production-системах для',
    r'используемая для \[', r'работает путем \['
]

all_descriptions = session.query(AlgorithmDescription).all()

target_fields_count = {
    'simple_explanation': 0,
    'algorithm_definition': 0,
    'technical_description': 0,
    'example': 0
}

entries_with_placeholders = 0

for desc in all_descriptions:
    has_placeholder = False
    
    if desc.simple_explanation:
        if any(re.search(pattern, desc.simple_explanation, re.IGNORECASE) for pattern in placeholder_patterns):
            target_fields_count['simple_explanation'] += 1
            has_placeholder = True
    
    if desc.algorithm_definition:
        if any(re.search(pattern, desc.algorithm_definition, re.IGNORECASE) for pattern in placeholder_patterns):
            target_fields_count['algorithm_definition'] += 1
            has_placeholder = True
    
    if desc.technical_description:
        if any(re.search(pattern, desc.technical_description, re.IGNORECASE) for pattern in placeholder_patterns):
            target_fields_count['technical_description'] += 1
            has_placeholder = True
    
    if desc.example:
        if any(re.search(pattern, desc.example, re.IGNORECASE) for pattern in placeholder_patterns):
            target_fields_count['example'] += 1
            has_placeholder = True
    
    if has_placeholder:
        entries_with_placeholders += 1

print("Placeholder Statistics:")
print("="*60)
print(f"Total entries with placeholders: {entries_with_placeholders}")
print(f"\nBreakdown by field:")
print(f"  Simple Explanation: {target_fields_count['simple_explanation']}")
print(f"  Algorithm Definition: {target_fields_count['algorithm_definition']}")
print(f"  Technical Description: {target_fields_count['technical_description']}")
print(f"  Example: {target_fields_count['example']}")
print("="*60)

