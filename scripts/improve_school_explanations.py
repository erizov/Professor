#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Improve school.ru.md explanations by fetching specific information from Wikipedia and other sources.
"""

import json
import re
import sys
import io
import time
from pathlib import Path
from typing import Dict, Optional, Tuple
import urllib.request
import urllib.parse
from urllib.error import URLError, HTTPError

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parents[1]


def get_wikipedia_summary(algorithm_name: str) -> Optional[str]:
    """Get Wikipedia summary for an algorithm."""
    try:
        # Clean algorithm name
        clean_name = algorithm_name.replace('_', ' ').strip()
        
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
        }
        
        # Try mapped name first
        wiki_name = name_mappings.get(clean_name.lower())
        
        if not wiki_name:
            # Convert to Wikipedia format
            wiki_name = clean_name.title().replace(' ', '_')
        
        # Try different variations
        variations = [
            wiki_name,
            clean_name.replace(' ', '_'),
            clean_name.replace(' ', '_').title(),
            clean_name.replace(' advanced', '').replace(' ', '_').title(),
            clean_name.replace('_', ' ').title().replace(' ', '_'),
        ]
        
        for variation in variations:
            try:
                url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{variation}"
                with urllib.request.urlopen(url, timeout=5) as response:
                    data = json.loads(response.read().decode('utf-8'))
                    if 'extract' in data and len(data['extract']) > 50:
                        return data['extract']
            except (URLError, HTTPError, KeyError):
                continue
        
        return None
    except Exception as e:
        return None


def get_algorithm_info_from_sources(english_name: str, folder_path: Path) -> Dict[str, str]:
    """Get algorithm information from various sources."""
    info = {}
    
    # Try Wikipedia
    wiki_summary = get_wikipedia_summary(english_name)
    if wiki_summary:
        # Clean and shorten summary
        summary = wiki_summary
        # Remove citations [1], [2], etc.
        summary = re.sub(r'\[\d+\]', '', summary)
        # Take first 2-3 sentences (about 300 chars)
        sentences = re.split(r'[.!?]+', summary)
        info['wikipedia'] = '. '.join(sentences[:3]).strip() + '.'
        if len(info['wikipedia']) > 400:
            info['wikipedia'] = info['wikipedia'][:400] + '...'
    
    # Try to extract from README
    readme_path = folder_path / "README.md"
    if readme_path.exists():
        try:
            content = readme_path.read_text(encoding='utf-8')
            
            # Extract from Introduction or Overview
            intro_match = re.search(
                r'(?:## Introduction|## Overview|## Description)\s*\n\n(.+?)(?:\n\n##|\n## |\Z)',
                content, re.DOTALL
            )
            if intro_match:
                desc = intro_match.group(1).strip()
                # Clean up markdown
                desc = re.sub(r'\*\*([^*]+)\*\*', r'\1', desc)
                desc = re.sub(r'`([^`]+)`', r'\1', desc)
                desc = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', desc)
                # Take first paragraph or first 300 chars
                first_para = desc.split('\n\n')[0] if '\n\n' in desc else desc
                if len(first_para) > 300:
                    first_para = first_para[:300] + '...'
                info['readme'] = first_para
        except:
            pass
    
    # Try to extract from code docstrings
    py_file = folder_path / "algorithm.py"
    if py_file.exists():
        try:
            content = py_file.read_text(encoding='utf-8')
            # Find class or function docstring
            docstring_match = re.search(
                r'"""(.*?)"""',
                content, re.DOTALL
            )
            if docstring_match:
                doc = docstring_match.group(1).strip()
                # Skip generic descriptions
                if doc and len(doc) > 30 and 'implementation' not in doc.lower()[:50]:
                    doc = re.sub(r'Time Complexity.*', '', doc, flags=re.IGNORECASE)
                    doc = re.sub(r'Space Complexity.*', '', doc, flags=re.IGNORECASE)
                    if len(doc) > 200:
                        doc = doc[:200] + '...'
                    info['code'] = doc
        except:
            pass
    
    return info


def generate_specific_explanation_from_sources(english_name: str, russian_name: str,
                                               folder_path: Path) -> str:
    """Generate specific explanation using information from sources."""
    
    # Get information from various sources
    sources_info = get_algorithm_info_from_sources(english_name, folder_path)
    
    # Prioritize: Wikipedia > README > Code > Generated
    explanation = None
    
    if 'wikipedia' in sources_info:
        explanation = sources_info['wikipedia']
        # Simplify for school students
        explanation = re.sub(r'\([^)]+\)', '', explanation)  # Remove parenthetical notes
        explanation = re.sub(r'\[\d+\]', '', explanation)  # Remove citations
        # Translate common English phrases to Russian
        explanation = explanation.replace('is a', '— это')
        explanation = explanation.replace('is an', '— это')
        explanation = explanation.replace('are', '— это')
        explanation = explanation.replace('In computer science,', 'В информатике,')
        explanation = explanation.replace('In computing,', 'В вычислениях,')
        # Make it start with algorithm name
        if not explanation.startswith(russian_name):
            # Capitalize first letter after algorithm name
            explanation = explanation.strip()
            if explanation[0].islower():
                explanation = explanation[0].upper() + explanation[1:]
            explanation = f"{russian_name} — {explanation.lower()}"
    elif 'readme' in sources_info:
        explanation = sources_info['readme']
        if not explanation.startswith(russian_name):
            explanation = f"{russian_name} — {explanation.lower()}"
    elif 'code' in sources_info:
        explanation = sources_info['code']
        if not explanation.startswith(russian_name):
            explanation = f"{russian_name} — {explanation.lower()}"
    
    # If we have a good explanation, use it
    if explanation and len(explanation) > 50:
        # Clean up
        explanation = re.sub(r'\s+', ' ', explanation)  # Multiple spaces to single
        explanation = explanation.strip()
        return explanation
    
    # Fallback: Generate based on algorithm name and type
    return generate_fallback_explanation(english_name, russian_name)


def generate_fallback_explanation(english_name: str, russian_name: str) -> str:
    """Generate fallback explanation when no sources available."""
    
    lower_name = english_name.lower()
    
    # Batch processing
    if 'batch' in lower_name and 'process' in lower_name:
        return f"""{russian_name} — это способ обрабатывать большие объёмы данных порциями (батчами), 
а не по одному элементу. Это позволяет эффективно использовать ресурсы компьютера и 
ускорить обработку данных. Вместо обработки каждого элемента отдельно, алгоритм собирает 
несколько элементов вместе и обрабатывает их одновременно."""
    
    # Data engineering
    elif 'data engineering' in lower_name or 'data pipeline' in lower_name:
        return f"""{russian_name} — это процесс создания систем для сбора, обработки и хранения данных. 
Алгоритм помогает автоматизировать работу с большими объёмами информации, обеспечивая 
надёжность и скорость обработки."""
    
    # Data monitoring
    elif 'monitoring' in lower_name and 'data' in lower_name:
        return f"""{russian_name} — это процесс непрерывного отслеживания состояния данных и систем. 
Алгоритм собирает метрики (показатели), такие как скорость обработки, количество ошибок, 
использование ресурсов, и сравнивает их с установленными порогами. Если значение превышает 
порог, система отправляет предупреждение."""
    
    # Stream processing
    elif 'stream' in lower_name and 'process' in lower_name:
        return f"""{russian_name} — это способ обрабатывать данные в реальном времени, по мере их поступления. 
Вместо ожидания накопления всех данных, алгоритм обрабатывает их непрерывным потоком, 
что позволяет быстро реагировать на изменения."""
    
    # Machine learning
    elif 'machine learning' in lower_name or 'ml' in lower_name or 'neural' in lower_name:
        return f"""{russian_name} — это алгоритм машинного обучения, который позволяет компьютеру 
учиться на примерах и делать предсказания или принимать решения без явного программирования 
каждого шага."""
    
    # Graph algorithms
    elif 'graph' in lower_name:
        if 'traversal' in lower_name:
            return f"""{russian_name} — это способ обойти все узлы графа, посетив каждый ровно один раз. 
Алгоритм систематически проходит по связям между узлами, исследуя структуру графа."""
        else:
            return f"""{russian_name} — это алгоритм для работы с графами (структурами данных, 
представляющими связи между объектами). Он помогает находить пути, анализировать связи 
и решать задачи на графах."""
    
    # Database
    elif 'database' in lower_name or 'index' in lower_name or 'query' in lower_name:
        return f"""{russian_name} — это способ эффективно работать с базами данных. Алгоритм помогает 
быстро находить, сортировать и обрабатывать информацию, хранящуюся в структурированном виде."""
    
    # Security/Cryptography
    elif 'crypt' in lower_name or 'security' in lower_name or 'encrypt' in lower_name:
        return f"""{russian_name} — это алгоритм для защиты информации. Он преобразует данные таким образом, 
чтобы только авторизованные пользователи могли их прочитать или использовать."""
    
    # Default
    else:
        # Try to infer from words
        words = re.split(r'[_\s]+', english_name.lower())
        
        if 'sort' in words:
            return f"""{russian_name} — это алгоритм упорядочивания элементов списка по определённому правилу 
(например, по возрастанию или убыванию). Алгоритм сравнивает элементы и переставляет их, 
пока все не будут в нужном порядке."""
        
        elif 'search' in words:
            return f"""{russian_name} — это алгоритм поиска определённого элемента в структуре данных. 
Алгоритм проверяет элементы по определённой стратегии, пока не найдёт нужный или не убедится, 
что его нет."""
        
        elif 'tree' in words:
            return f"""{russian_name} — это структура данных, похожая на дерево с корнем, ветками и листьями. 
Каждый узел может иметь дочерние узлы, что позволяет эффективно организовывать и находить данные."""
        
        elif 'hash' in words:
            return f"""{russian_name} — это способ быстро находить данные по ключу. Алгоритм преобразует ключ 
в число (хеш-код), которое указывает, где хранится нужная информация."""
        
        else:
            return f"""{russian_name} — это алгоритм для решения конкретной задачи в области компьютерных наук. 
Он выполняет последовательность шагов для обработки данных и получения результата."""


def improve_school_file(school_file: Path, folder_path: Path) -> bool:
    """Improve the explanation section in a school.ru.md file."""
    try:
        content = school_file.read_text(encoding='utf-8')
        
        # Extract algorithm names
        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        if not title_match:
            return False
        
        russian_name = title_match.group(1).strip()
        
        # Get English name from folder or metadata
        folder_name = folder_path.name
        metadata_file = folder_path / "metadata.json"
        english_name = folder_name
        if metadata_file.exists():
            try:
                metadata = json.loads(metadata_file.read_text(encoding='utf-8'))
                if 'name' in metadata:
                    english_name = metadata['name']
                elif 'display_name' in metadata:
                    english_name = metadata['display_name']
            except:
                pass
        
        # Generate new explanation
        new_explanation = generate_specific_explanation_from_sources(
            english_name, russian_name, folder_path
        )
        
        # Replace the explanation section
        explanation_pattern = r'(## Простое объяснение\s*\n\n)(.+?)(\n\n## )'
        match = re.search(explanation_pattern, content, re.DOTALL)
        
        if match:
            new_content = (
                content[:match.start()] +
                match.group(1) +
                new_explanation +
                match.group(3) +
                content[match.end():]
            )
            
            school_file.write_text(new_content, encoding='utf-8')
            return True
        
        return False
        
    except Exception as e:
        print(f"  [ERROR] {e}")
        return False


def main():
    """Main function to improve all school.ru.md files."""
    print("=" * 70)
    print("УЛУЧШЕНИЕ ОБЪЯСНЕНИЙ В school.ru.md")
    print("=" * 70)
    print()
    
    # Find all school.ru.md files
    school_files = list(ROOT.rglob("school.ru.md"))
    school_files.sort()
    
    print(f"Найдено {len(school_files)} файлов school.ru.md")
    print()
    
    improved_count = 0
    error_count = 0
    
    for idx, school_file in enumerate(school_files, 1):
        folder_path = school_file.parent
        relative_path = folder_path.relative_to(ROOT)
        
        print(f"[{idx}/{len(school_files)}] Обработка: {relative_path}")
        
        if improve_school_file(school_file, folder_path):
            print(f"  [OK] Объяснение улучшено")
            improved_count += 1
        else:
            print(f"  [SKIP] Не удалось улучшить")
            error_count += 1
        
        # Rate limiting for web requests
        if idx % 10 == 0:
            time.sleep(1)  # Small delay to avoid overwhelming Wikipedia API
        
        if idx % 50 == 0:
            print(f"\nПрогресс: {idx}/{len(school_files)} обработано\n")
    
    print()
    print("=" * 70)
    print(f"Итоги:")
    print(f"  Всего файлов: {len(school_files)}")
    print(f"  Улучшено: {improved_count}")
    print(f"  Ошибок: {error_count}")
    print("=" * 70)


if __name__ == "__main__":
    main()

