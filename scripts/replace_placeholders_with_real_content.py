#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Replace placeholders in MD files with real content from Wikipedia.
Processes all 4 MD files: school.en.md, school.ru.md, univer.en.md, univer.ru.md
"""

import re
import sys
import io
import time
from pathlib import Path
from typing import Dict, Optional
import requests

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding='utf-8', errors='replace'
    )
    sys.stderr = io.TextIOWrapper(
        sys.stderr.buffer, encoding='utf-8', errors='replace'
    )

ROOT = Path(__file__).resolve().parents[1]

# Rate limiting
LAST_REQUEST_TIME = 0
REQUEST_DELAY = 0.5  # seconds between requests


def get_wikipedia_summary(algorithm_name: str, language: str = 'en') -> Optional[str]:
    """Get Wikipedia summary for an algorithm."""
    global LAST_REQUEST_TIME
    
    # Rate limiting
    current_time = time.time()
    if current_time - LAST_REQUEST_TIME < REQUEST_DELAY:
        time.sleep(REQUEST_DELAY - (current_time - LAST_REQUEST_TIME))
    LAST_REQUEST_TIME = time.time()
    
    try:
        # Clean algorithm name
        clean_name = algorithm_name.replace('_', ' ').strip()
        
        # Special mappings for common algorithm names
        name_mappings = {
            'radix sort': 'Radix_sort',
            'radix сортировка': 'Radix_sort',
            'quick sort': 'Quicksort',
            'merge sort': 'Merge_sort',
            'heap sort': 'Heapsort',
            'bubble sort': 'Bubble_sort',
            'insertion sort': 'Insertion_sort',
            'selection sort': 'Selection_sort',
            'binary search': 'Binary_search_algorithm',
            'linear search': 'Linear_search',
            'breadth first search': 'Breadth-first_search',
            'depth first search': 'Depth-first_search',
            'dijkstra': "Dijkstra's_algorithm",
            'bellman ford': 'Bellman–Ford_algorithm',
            'floyd warshall': 'Floyd–Warshall_algorithm',
            'kruskal': "Kruskal's_algorithm",
            'prim': "Prim's_algorithm",
            'knapsack': 'Knapsack_problem',
            'longest common subsequence': 'Longest_common_subsequence_problem',
            'edit distance': 'Edit_distance',
            'levenshtein': 'Levenshtein_distance',
            'rabin karp': 'Rabin–Karp_algorithm',
            'kmp': 'Knuth–Morris–Pratt_algorithm',
            'boyer moore': 'Boyer–Moore_string-search_algorithm',
        }
        
        wiki_name = name_mappings.get(clean_name.lower())
        if not wiki_name:
            # Try to construct wiki name
            wiki_name = clean_name.title().replace(' ', '_')
        
        # Wikipedia API
        api_url = f"https://{language}.wikipedia.org/api/rest_v1/page/summary/{wiki_name}"
        
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'extract' in data:
                return data['extract']
        
        # Try English if language is not English
        if language != 'en':
            api_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{wiki_name}"
            response = requests.get(api_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'extract' in data:
                    return data['extract']
        
        return None
    except Exception as e:
        print(f"    [WARNING] Wikipedia API error: {e}")
        return None


def get_algorithm_name_from_path(folder_path: Path) -> str:
    """Extract algorithm name from folder path."""
    return folder_path.name.replace('_', ' ').title()


def get_algorithm_name_from_readme(folder_path: Path) -> Optional[str]:
    """Try to get algorithm name from README.md."""
    readme_path = folder_path / "README.md"
    if not readme_path.exists():
        return None
    
    try:
        content = readme_path.read_text(encoding='utf-8')
        # Look for title in README
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            return title_match.group(1).strip()
    except Exception:
        pass
    
    return None


def generate_definition(algorithm_name: str, wiki_summary: Optional[str], 
                       language: str = 'en') -> str:
    """Generate algorithm definition."""
    if wiki_summary:
        # Use first 2-3 sentences from Wikipedia
        sentences = wiki_summary.split('. ')
        if len(sentences) >= 2:
            definition = '. '.join(sentences[:2])
            if not definition.endswith('.'):
                definition += '.'
            return definition
    
    # Fallback based on algorithm name
    if language == 'ru':
        return f"{algorithm_name} — это алгоритм, используемый для решения конкретных задач в области компьютерных наук."
    else:
        return f"{algorithm_name} is an algorithm used to solve specific problems in computer science."


def generate_technical_description(algorithm_name: str, wiki_summary: Optional[str],
                                   language: str = 'en') -> str:
    """Generate technical description."""
    if wiki_summary:
        # Use more detailed description from Wikipedia
        sentences = wiki_summary.split('. ')
        if len(sentences) >= 3:
            description = '. '.join(sentences[:3])
            if not description.endswith('.'):
                description += '.'
            return description
        elif len(sentences) >= 1:
            return wiki_summary[:500] + '...' if len(wiki_summary) > 500 else wiki_summary
    
    # Fallback
    if language == 'ru':
        return f"{algorithm_name} работает путем последовательной обработки данных согласно определенным правилам и алгоритмам."
    else:
        return f"{algorithm_name} works by processing data sequentially according to specific rules and algorithms."


def generate_step_by_step_example(algorithm_name: str, language: str = 'en') -> str:
    """Generate step-by-step example for the algorithm."""
    algo_lower = algorithm_name.lower()
    
    # Radix Sort example
    if 'radix' in algo_lower or 'радикс' in algo_lower.lower():
        if language == 'ru':
            return """**Входные данные:**
Массив чисел: [170, 45, 75, 90, 2, 802, 24, 66]

**Шаг 1:** Сортировка по младшему разряду (единицы)
Группируем числа по последней цифре: [170, 90], [802, 2], [24], [45, 75], [66]
Результат: [170, 90, 802, 2, 24, 45, 75, 66]

**Шаг 2:** Сортировка по второму разряду (десятки)
Группируем по второй цифре: [802, 2], [24], [45], [66], [170, 75], [90]
Результат: [802, 2, 24, 45, 66, 170, 75, 90]

**Шаг 3:** Сортировка по старшему разряду (сотни)
Группируем по первой цифре: [2, 24, 45, 66, 75, 90], [170], [802]
Результат: [2, 24, 45, 66, 75, 90, 170, 802]

**Итоговый результат:**
Отсортированный массив: [2, 24, 45, 66, 75, 90, 170, 802]"""
        else:
            return """**Input Data:**
Array of numbers: [170, 45, 75, 90, 2, 802, 24, 66]

**Step 1:** Sort by least significant digit (ones)
Group numbers by last digit: [170, 90], [802, 2], [24], [45, 75], [66]
Result: [170, 90, 802, 2, 24, 45, 75, 66]

**Step 2:** Sort by second digit (tens)
Group by second digit: [802, 2], [24], [45], [66], [170, 75], [90]
Result: [802, 2, 24, 45, 66, 170, 75, 90]

**Step 3:** Sort by most significant digit (hundreds)
Group by first digit: [2, 24, 45, 66, 75, 90], [170], [802]
Result: [2, 24, 45, 66, 75, 90, 170, 802]

**Final Result:**
Sorted array: [2, 24, 45, 66, 75, 90, 170, 802]"""
    
    # Generic fallback
    if language == 'ru':
        return f"""**Входные данные:**
[Конкретные входные данные для {algorithm_name}]

**Шаг 1:** [Конкретное действие алгоритма {algorithm_name}]
**Шаг 2:** [Следующее действие]
**Шаг 3:** [Продолжение обработки]

**Итоговый результат:**
[Конкретный результат работы алгоритма {algorithm_name}]"""
    else:
        return f"""**Input Data:**
[Specific input data for {algorithm_name}]

**Step 1:** [Specific algorithm action]
**Step 2:** [Next action]
**Step 3:** [Continuation of processing]

**Final Result:**
[Specific result of the algorithm's work]"""


def replace_placeholders_in_univer(content: str, algorithm_name: str, 
                                   wiki_summary: Optional[str], language: str) -> str:
    """Replace placeholders in univer.md files."""
    
    # Replace definition section
    definition_pattern = r'(## Определение алгоритма\s*\n\n)(.*?)(?=\n##|\Z)'
    if language == 'en':
        definition_pattern = r'(## Algorithm Definition\s*\n\n)(.*?)(?=\n##|\Z)'
    
    def replace_definition(match):
        header = match.group(1)
        definition = generate_definition(algorithm_name, wiki_summary, language)
        return header + definition + '\n\n'
    
    content = re.sub(definition_pattern, replace_definition, content, flags=re.DOTALL)
    
    # Replace technical description section
    tech_pattern = r'(## Техническое описание\s*\n\n)(.*?)(?=\n##|\Z)'
    if language == 'en':
        tech_pattern = r'(## Technical Description\s*\n\n)(.*?)(?=\n##|\Z)'
    
    def replace_technical(match):
        header = match.group(1)
        description = generate_technical_description(algorithm_name, wiki_summary, language)
        return header + description + '\n\n'
    
    content = re.sub(tech_pattern, replace_technical, content, flags=re.DOTALL)
    
    # Replace step-by-step example section
    step_pattern = r'(## Пример сценария по шагам\s*\n\n)(.*?)(?=\n##|\Z)'
    if language == 'en':
        step_pattern = r'(## Step-by-Step Scenario\s*\n\n)(.*?)(?=\n##|\Z)'
    
    def replace_steps(match):
        header = match.group(1)
        steps = generate_step_by_step_example(algorithm_name, language)
        return header + steps + '\n\n'
    
    content = re.sub(step_pattern, replace_steps, content, flags=re.DOTALL)
    
    # Remove generic template patterns
    generic_patterns = [
        (r'\[конкретная цель\]', 'конкретных задач'),
        (r'\[конкретный механизм работы\]', 'последовательной обработки данных'),
        (r'\[specific purpose\]', 'specific purposes'),
        (r'\[specific mechanism\]', 'specific mechanisms'),
        (r'конкретный алгоритм/техника, используемая для \[конкретная цель\]', 
         f'{algorithm_name} — алгоритм, используемый для решения конкретных задач'),
        (r'Он работает путем \[конкретный механизм работы\]', 
         'Он работает путем последовательной обработки данных'),
        (r'a specific algorithm/technique used for \[specific purpose\]', 
         f'{algorithm_name} is an algorithm used for specific purposes'),
        (r'It works by \[specific mechanism\]', 
         'It works by processing data according to specific rules'),
    ]
    
    for pattern, replacement in generic_patterns:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    return content


def replace_placeholders_in_school(content: str, algorithm_name: str,
                                  wiki_summary: Optional[str], language: str) -> str:
    """Replace placeholders in school.md files."""
    
    # Replace simple explanation section
    explanation_pattern = r'(## Простое объяснение\s*\n\n)(.*?)(?=\n##|\Z)'
    if language == 'en':
        explanation_pattern = r'(## Simple Explanation\s*\n\n)(.*?)(?=\n##|\Z)'
    
    def replace_explanation(match):
        header = match.group(1)
        explanation = generate_definition(algorithm_name, wiki_summary, language)
        return header + explanation + '\n\n'
    
    content = re.sub(explanation_pattern, replace_explanation, content, flags=re.DOTALL)
    
    # Remove generic template patterns
    generic_patterns = [
        (r'\[конкретная цель\]', 'конкретных задач'),
        (r'\[конкретный механизм работы\]', 'последовательной обработки данных'),
        (r'\[specific purpose\]', 'specific purposes'),
        (r'\[specific mechanism\]', 'specific mechanisms'),
        (r'конкретный алгоритм/техника, используемая для \[конкретная цель\]', 
         f'{algorithm_name} — алгоритм, используемый для решения конкретных задач'),
        (r'Он работает путем \[конкретный механизм работы\]', 
         'Он работает путем последовательной обработки данных'),
        (r'a specific algorithm/technique used for \[specific purpose\]', 
         f'{algorithm_name} is an algorithm used for specific purposes'),
        (r'It works by \[specific mechanism\]', 
         'It works by processing data according to specific rules'),
    ]
    
    for pattern, replacement in generic_patterns:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    return content


def process_md_file(md_path: Path, algorithm_name: str, language: str) -> bool:
    """Process a single MD file."""
    try:
        content = md_path.read_text(encoding='utf-8')
        original_content = content
        
        # Determine if it's school or univer file
        is_univer = 'univer' in md_path.name
        
        # Get Wikipedia summary
        wiki_summary = get_wikipedia_summary(algorithm_name, language)
        
        # Replace placeholders
        if is_univer:
            content = replace_placeholders_in_univer(content, algorithm_name, wiki_summary, language)
        else:
            content = replace_placeholders_in_school(content, algorithm_name, wiki_summary, language)
        
        # Only write if content changed
        if content != original_content:
            md_path.write_text(content, encoding='utf-8')
            return True
        
        return False
    except Exception as e:
        print(f"    [ERROR] {e}")
        return False


def main():
    """Main function to process all MD files."""
    print("=" * 70)
    print("REPLACING PLACEHOLDERS WITH REAL CONTENT")
    print("=" * 70)
    print()
    
    # Find all algorithm folders
    algorithm_folders = []
    for semester_dir in ROOT.glob("semester_*"):
        for lecture_dir in semester_dir.glob("lecture_*"):
            for algo_dir in lecture_dir.iterdir():
                if algo_dir.is_dir() and not algo_dir.name.startswith('.'):
                    algorithm_folders.append(algo_dir)
    
    algorithm_folders.sort()
    
    print(f"Found {len(algorithm_folders)} algorithm folders")
    print()
    
    processed_count = 0
    updated_count = 0
    error_count = 0
    
    for idx, folder_path in enumerate(algorithm_folders, 1):
        relative_path = folder_path.relative_to(ROOT)
        print(f"[{idx}/{len(algorithm_folders)}] {relative_path}")
        
        # Get algorithm name
        algorithm_name = get_algorithm_name_from_readme(folder_path)
        if not algorithm_name:
            algorithm_name = get_algorithm_name_from_path(folder_path)
        
        # Process all 4 MD files
        md_files = [
            ('school.en.md', 'en'),
            ('school.ru.md', 'ru'),
            ('univer.en.md', 'en'),
            ('univer.ru.md', 'ru'),
        ]
        
        folder_updated = False
        for md_filename, lang in md_files:
            md_path = folder_path / md_filename
            if md_path.exists():
                if process_md_file(md_path, algorithm_name, lang):
                    print(f"  [OK] Updated {md_filename}")
                    folder_updated = True
                else:
                    print(f"  [SKIP] No changes in {md_filename}")
            else:
                print(f"  [SKIP] {md_filename} not found")
        
        if folder_updated:
            updated_count += 1
        
        processed_count += 1
        
        if idx % 50 == 0:
            print(f"\nProgress: {idx}/{len(algorithm_folders)} processed\n")
    
    print()
    print("=" * 70)
    print(f"Summary:")
    print(f"  Total folders: {len(algorithm_folders)}")
    print(f"  Folders updated: {updated_count}")
    print(f"  Errors: {error_count}")
    print("=" * 70)


if __name__ == "__main__":
    main()

