#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate school.en.md and univer.en.md files for each algorithm folder.
Enriches content with information from Wikipedia and English sources.
"""

import json
import re
import sys
import io
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import urllib.request
from urllib.error import URLError, HTTPError

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parents[1]


def get_wikipedia_content(algorithm_name: str) -> Dict[str, str]:
    """Get Wikipedia content for an algorithm."""
    info = {}
    
    try:
        # Common algorithm name mappings
        name_mappings = {
            'bubble sort': 'Bubble_sort',
            'insertion sort': 'Insertion_sort',
            'selection sort': 'Selection_sort',
            'merge sort': 'Merge_sort',
            'quick sort': 'Quicksort',
            'heap sort': 'Heapsort',
            'binary search': 'Binary_search_algorithm',
            'linear search': 'Linear_search',
            'binary tree': 'Binary_tree',
            'hash table': 'Hash_table',
            'depth first search': 'Depth-first_search',
            'breadth first search': 'Breadth-first_search',
            'batch processing': 'Batch_processing',
            'data monitoring': 'Data_monitoring',
            'data quality': 'Data_quality',
            'stream processing': 'Stream_processing',
            'isolation forest': 'Isolation_forest',
            'neural network': 'Artificial_neural_network',
            'decision tree': 'Decision_tree_learning',
            'k-means': 'K-means_clustering',
            'linear regression': 'Linear_regression',
            'logistic regression': 'Logistic_regression',
            'blockchain': 'Blockchain',
            'blockchain scalability': 'Blockchain_scalability',
            'graph database': 'Graph_database',
            'time series': 'Time_series',
            'machine learning': 'Machine_learning',
            'deep learning': 'Deep_learning',
        }
        
        clean_name = algorithm_name.replace('_', ' ').strip()
        wiki_name = name_mappings.get(clean_name.lower())
        
        if not wiki_name:
            # Try to construct wiki name
            wiki_name = clean_name.title().replace(' ', '_')
        
        # Try to get summary
        variations = [
            wiki_name,
            clean_name.replace(' ', '_'),
            clean_name.replace(' ', '_').title(),
            clean_name.replace('_', ' ').title().replace(' ', '_'),
        ]
        
        for variation in variations:
            try:
                url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{variation}"
                with urllib.request.urlopen(url, timeout=5) as response:
                    data = json.loads(response.read().decode('utf-8'))
                    if 'extract' in data and len(data['extract']) > 100:
                        info['summary'] = data['extract']
                        if 'content_urls' in data and 'desktop' in data['content_urls']:
                            info['url'] = data['content_urls']['desktop']['page']
                        break
            except (URLError, HTTPError, KeyError):
                continue
            except Exception:
                continue
            time.sleep(0.5)  # Rate limiting
        
    except Exception:
        pass
    
    return info


def get_algorithm_name(folder_path: Path) -> Tuple[str, str]:
    """Extract algorithm name from folder path."""
    folder_name = folder_path.name
    # Convert snake_case to Title Case
    display_name = folder_name.replace('_', ' ').title()
    return folder_name, display_name


def determine_discipline(english_name: str, folder_path: Path) -> str:
    """Determine the discipline for the algorithm."""
    lower_name = english_name.lower()
    path_str = str(folder_path).lower()
    
    # Check metadata first
    metadata_file = folder_path / "metadata.json"
    if metadata_file.exists():
        try:
            metadata = json.loads(metadata_file.read_text(encoding='utf-8'))
            category = metadata.get('category', '').lower()
            algo_type = metadata.get('algorithm_type', '').lower()
            
            if 'machine learning' in category or 'ml' in category or algo_type in ['ml', 'ai']:
                return 'Machine Learning / AI'
            if 'data' in category or algo_type in ['data_structure', 'data']:
                return 'Data Engineering / Data Governance'
            if 'security' in category or algo_type == 'security':
                return 'Monitoring & Security'
        except Exception:
            pass
    
    # Check path and name
    if any(x in path_str for x in ['ml_', 'machine_learning', 'ai_', 'neural', 'deep_learning']):
        return 'Machine Learning / AI'
    if any(x in path_str for x in ['data_', 'database', 'data_engineering', 'data_governance']):
        return 'Data Engineering / Data Governance'
    if any(x in path_str for x in ['security', 'monitoring', 'observability']):
        return 'Monitoring & Security'
    if any(x in lower_name for x in ['neural', 'deep learning', 'ml', 'ai', 'classifier', 'regression']):
        return 'Machine Learning / AI'
    
    return 'Computer Science'


def read_russian_file(file_path: Path) -> Optional[str]:
    """Read Russian MD file if it exists."""
    if file_path.exists():
        try:
            return file_path.read_text(encoding='utf-8')
        except Exception:
            pass
    return None


def generate_school_en_content(
    algorithm_name: str,
    display_name: str,
    folder_path: Path,
    discipline: str,
    wiki_info: Dict[str, str],
    russian_content: Optional[str] = None
) -> str:
    """Generate school-level English content."""
    
    # Simple explanation
    simple_explanation = ""
    if wiki_info.get('summary'):
        # Use first 2-3 sentences from Wikipedia
        summary = wiki_info['summary']
        sentences = re.split(r'[.!?]+', summary)
        simple_explanation = '. '.join(sentences[:3]).strip()
        if simple_explanation and not simple_explanation.endswith('.'):
            simple_explanation += '.'
    else:
        simple_explanation = f"{display_name} is an algorithm for solving specific problems in computer science. It performs a sequence of steps to process data and obtain results."
    
    # Applications
    applications = [
        "solving practical programming problems",
        "optimizing application and system performance",
        "processing and analyzing data",
        "automating processes in various fields",
    ]
    
    if wiki_info.get('summary'):
        # Try to extract applications from summary
        summary_lower = wiki_info['summary'].lower()
        if 'used' in summary_lower or 'application' in summary_lower:
            # Extract sentences with "used" or "application"
            sentences = re.split(r'[.!?]+', wiki_info['summary'])
            for sent in sentences:
                if 'used' in sent.lower() or 'application' in sent.lower():
                    if len(sent.strip()) > 20 and len(sent.strip()) < 200:
                        applications.insert(0, sent.strip())
                        break
    
    # Example
    example = f"Consider a specific example of how {display_name.lower()} works:\n\n"
    example += "1. Data preparation: [specific input data]\n"
    example += "2. Algorithm application: [specific steps]\n"
    example += "3. Result: [specific result]\n\n"
    example += "The algorithm performs operations sequentially, processing data according to specific rules."
    
    # Questions
    basic_questions = [
        f"What does the {display_name.lower()} algorithm do?",
        f"In what situations is {display_name.lower()} used?",
        f"What data is needed for the algorithm to work?",
    ]
    
    intermediate_questions = [
        f"How does {display_name.lower()} handle edge cases?",
        f"What are the advantages and disadvantages of {display_name.lower()}?",
        f"Can the performance of {display_name.lower()} be improved?",
    ]
    
    advanced_questions = [
        f"What is the time complexity of {display_name.lower()}?",
        f"How does {display_name.lower()} work with large volumes of data?",
        f"How can {display_name.lower()} be optimized?",
    ]
    
    # Practical tasks
    tasks = {
        'level1': f"Perform a simple operation with the {display_name.lower()} algorithm. Use a small dataset (3-5 elements) and output the result.",
        'level2': f"Apply the {display_name.lower()} algorithm to a more complex dataset. Analyze the result and explain each step of the algorithm's operation.",
        'level3': f"Write an implementation of the {display_name.lower()} algorithm in a programming language. Add error handling, input validation, tests, and documentation.",
    }
    
    # Ethical note (only for AI/ML)
    ethical_note = ""
    if 'machine learning' in discipline.lower() or 'ai' in discipline.lower():
        ethical_note = "\n---\n\n**Ethical Note:**\n\nRemember that machine learning and artificial intelligence algorithms are powerful tools that can affect people's lives. It is important to use them responsibly, considering ethical principles, fairness, transparency, and respect for privacy. Always think about the consequences of your decisions and use technology for the benefit of society."
    
    content = f"""# {display_name}

## Simple Explanation

{simple_explanation}

## Where It's Used

- {applications[0]};
- {applications[1]};
- {applications[2]};
- {applications[3]};

## Example

{example}

## Self-Check Questions

### Basic

1. {basic_questions[0]}
2. {basic_questions[1]}
3. {basic_questions[2]}

### Intermediate

1. {intermediate_questions[0]}
2. {intermediate_questions[1]}
3. {intermediate_questions[2]}

### Advanced

1. {advanced_questions[0]}
2. {advanced_questions[1]}
3. {advanced_questions[2]}

## Practical Tasks

### Level 1 (Easy)

{tasks['level1']}

### Level 2 (Medium)

{tasks['level2']}

### Level 3 (Advanced)

{tasks['level3']}
{ethical_note}
"""
    
    return content


def generate_univer_en_content(
    algorithm_name: str,
    display_name: str,
    folder_path: Path,
    discipline: str,
    wiki_info: Dict[str, str],
    russian_content: Optional[str] = None
) -> str:
    """Generate university-level English content."""
    
    # Algorithm definition
    definition = ""
    if wiki_info.get('summary'):
        definition = wiki_info['summary']
    else:
        definition = f"{display_name} is an algorithm for solving problems in the field of {discipline.lower()}, which performs a sequence of operations to process data and obtain results."
    
    # Technical description
    technical_desc = definition
    
    # Key steps
    key_steps = [
        "Data input and validation",
        "Algorithm execution",
        "Result processing and output",
    ]
    
    # Data structures
    data_structures = [
        "Arrays or lists for data storage",
        "Variables for intermediate results",
        "Control structures for flow management",
    ]
    
    # Applications
    applications = [
        f"Data classification: applying the algorithm to predict object categories based on features",
        f"Regression analysis: building a model to predict continuous values",
        f"Clustering: grouping similar objects without prior labels",
    ]
    
    if discipline == 'Data Engineering / Data Governance':
        applications = [
            "ETL processes in banking systems: processing millions of transactions per day",
            "Report generation in corporate systems: daily processing of web server logs",
            "Image processing in social networks: batch processing of uploaded photos",
        ]
    
    # Step-by-step scenario
    scenario = f"""**Input Data:**
[Specific input data for {display_name.lower()}]

**Step 1:** [Specific algorithm action]
**Step 2:** [Next action]
**Step 3:** [Continuation of processing]
...

**Final Result:**
[Specific result of the algorithm's work]"""
    
    # Questions
    basic_questions = [
        f"Describe the main stages of the {display_name.lower()} algorithm. What data structures are used?",
        f"What are the time and space complexity of {display_name.lower()}? Justify your answer.",
    ]
    
    intermediate_questions = [
        f"In what cases is the {display_name.lower()} algorithm most effective? When is its use not advisable?",
        f"How can {display_name.lower()} be optimized? Suggest specific improvements.",
    ]
    
    advanced_questions = [
        f"Compare {display_name.lower()} with alternative approaches. Under what conditions is each preferable?",
        f"Analyze edge cases and implementation errors of {display_name.lower()}. How to ensure algorithm correctness?",
    ]
    
    # Practical tasks
    tasks = {
        'level1': f"Implement a basic version of the {display_name.lower()} algorithm in a programming language. Add edge case handling and tests.",
        'level2': f"Create a full implementation of {display_name.lower()} with error handling, logging, and testing. Apply to real data and analyze results.",
        'level3': f"Conduct a research analysis of {display_name.lower()}: compare with alternative algorithms, measure performance, analyze complexity, and formulate conclusions about applicability.",
    }
    
    # Ethical reasoning (only for ML/AI)
    ethical_reasoning = ""
    if 'machine learning' in discipline.lower() or 'ai' in discipline.lower():
        ethical_reasoning = """
## Ethical Reasoning

The application of machine learning algorithms requires an ethical approach:

**Key Ethical Principles:**
- Fairness: the algorithm should not discriminate against user groups
- Transparency: users should understand how decisions are made
- Privacy: protection of personal data
- Responsibility: human oversight of critical decisions
- Security: protection against abuse and attacks
"""
    
    content = f"""# {display_name}

**Algorithm:** {algorithm_name}  
**Discipline:** {discipline}

## Algorithm Definition

{definition}

## Technical Description

### What the Algorithm Does

{technical_desc}

**Key Steps:**
1. {key_steps[0]}
2. {key_steps[1]}
3. {key_steps[2]}

**Key Data Structures:**
- {data_structures[0]}
- {data_structures[1]}
- {data_structures[2]}

## Application in {discipline}

1. {applications[0]}
2. {applications[1]}
3. {applications[2]}

## Step-by-Step Scenario

{scenario}

## Self-Check Questions

### Basic Level

1. {basic_questions[0]}
2. {basic_questions[1]}

### Intermediate Level

1. {intermediate_questions[0]}
2. {intermediate_questions[1]}

### Advanced Level

1. {advanced_questions[0]}
2. {advanced_questions[1]}

## Practical Tasks

### Level 1 — Basic

{tasks['level1']}

### Level 2 — Applied

{tasks['level2']}

### Level 3 — Research

{tasks['level3']}
{ethical_reasoning}
"""
    
    return content


def main():
    """Main function to generate English MD files."""
    print("=" * 70)
    print("GENERATING ENGLISH MD FILES (school.en.md and univer.en.md)")
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
    
    generated_count = 0
    skipped_count = 0
    error_count = 0
    
    for idx, folder_path in enumerate(algorithm_folders, 1):
        relative_path = folder_path.relative_to(ROOT)
        print(f"[{idx}/{len(algorithm_folders)}] {relative_path}")
        
        try:
            algorithm_name, display_name = get_algorithm_name(folder_path)
            discipline = determine_discipline(algorithm_name, folder_path)
            
            # Get Wikipedia info
            wiki_info = get_wikipedia_content(algorithm_name)
            if wiki_info:
                print(f"  [OK] Wikipedia info found")
            else:
                print(f"  [INFO] No Wikipedia info found")
            
            # Read Russian files for reference
            school_ru = read_russian_file(folder_path / "school.ru.md")
            univer_ru = read_russian_file(folder_path / "univer.ru.md")
            
            # Generate school.en.md
            school_en_path = folder_path / "school.en.md"
            if not school_en_path.exists() or True:  # Always regenerate
                school_en_content = generate_school_en_content(
                    algorithm_name, display_name, folder_path, discipline, wiki_info, school_ru
                )
                school_en_path.write_text(school_en_content, encoding='utf-8')
                print(f"  [OK] Generated school.en.md")
                generated_count += 1
            else:
                print(f"  [SKIP] school.en.md already exists")
                skipped_count += 1
            
            # Generate univer.en.md
            univer_en_path = folder_path / "univer.en.md"
            if not univer_en_path.exists() or True:  # Always regenerate
                univer_en_content = generate_univer_en_content(
                    algorithm_name, display_name, folder_path, discipline, wiki_info, univer_ru
                )
                univer_en_path.write_text(univer_en_content, encoding='utf-8')
                print(f"  [OK] Generated univer.en.md")
                generated_count += 1
            else:
                print(f"  [SKIP] univer.en.md already exists")
                skipped_count += 1
            
            # Rate limiting for Wikipedia API
            time.sleep(0.5)
            
        except Exception as e:
            print(f"  [ERROR] {e}")
            error_count += 1
        
        if idx % 50 == 0:
            print(f"\nProgress: {idx}/{len(algorithm_folders)} processed\n")
    
    print()
    print("=" * 70)
    print(f"Summary:")
    print(f"  Total folders: {len(algorithm_folders)}")
    print(f"  Files generated: {generated_count}")
    print(f"  Files skipped: {skipped_count}")
    print(f"  Errors: {error_count}")
    print("=" * 70)


if __name__ == "__main__":
    main()
