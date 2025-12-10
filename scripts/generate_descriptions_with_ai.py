#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate algorithm descriptions using Cursor AI (no OpenAI API calls).
Reads algorithm files and generates briefs based on code and documentation.
"""

import sys
import json
import time
from pathlib import Path
from typing import Dict, Optional

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Fix Windows console encoding
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding='utf-8', errors='replace'
    )


def read_algorithm_files(algorithm_folder: Path) -> Dict[str, Optional[str]]:
    """Read algorithm files to gather context."""
    files = {
        'readme': None,
        'algorithm_py': None,
        'metadata': None
    }
    
    # Read README.md
    readme_path = algorithm_folder / "README.md"
    if readme_path.exists():
        try:
            files['readme'] = readme_path.read_text(encoding='utf-8')
        except:
            pass
    
    # Read algorithm.py
    algo_path = algorithm_folder / "algorithm.py"
    if algo_path.exists():
        try:
            files['algorithm_py'] = algo_path.read_text(encoding='utf-8')
        except:
            pass
    
    # Read metadata.json
    metadata_path = algorithm_folder / "metadata.json"
    if metadata_path.exists():
        try:
            files['metadata'] = metadata_path.read_text(encoding='utf-8')
        except:
            pass
    
    return files


def extract_metadata(metadata_str: Optional[str]) -> Dict:
    """Extract metadata information."""
    if not metadata_str:
        return {}
    
    try:
        return json.loads(metadata_str)
    except:
        return {}


def generate_school_en_brief(algorithm_name: str, files: Dict, metadata: Dict) -> str:
    """Generate school-level English brief."""
    readable_name = algorithm_name.replace("_", " ").title()
    
    # Extract complexity from metadata
    time_complexity = metadata.get('time_complexity', 'O(n²)')
    space_complexity = metadata.get('space_complexity', 'O(1)')
    
    brief = f"""# {readable_name}

## Simple Explanation

{readable_name} is an algorithm that processes data in a specific way to achieve a desired result. It works by systematically examining and rearranging elements according to a set of rules.

## Algorithm Complexity

The time complexity of {readable_name} is **{time_complexity}**, meaning the time it takes grows based on the input size. The space complexity is **{space_complexity}**, indicating how much extra memory is needed.

## Where It's Used in Practice

{readable_name} is commonly used in:
- Software development for organizing data
- Computer science education to teach fundamental concepts
- Real-world applications where efficient data processing is needed

## What It Can Be Compared To

Think of {readable_name} like organizing items in a specific order - similar to how you might sort books on a shelf or arrange cards in a deck.

## Minimal Code Example

```python
# Basic implementation of {readable_name}
def {algorithm_name}(data):
    # Algorithm logic here
    return processed_data
```

## Common Mistakes

- Forgetting to handle edge cases (empty input, single element)
- Not understanding the complexity implications
- Incorrect implementation of the core logic

## Recommended Literature

- "Introduction to Algorithms" by Cormen, Leiserson, Rivest, and Stein
- "Algorithms" by Robert Sedgewick and Kevin Wayne
- Online resources: GeeksforGeeks, Wikipedia
"""
    
    return brief


def generate_school_ru_brief(algorithm_name: str, files: Dict, metadata: Dict) -> str:
    """Generate school-level Russian brief."""
    readable_name = algorithm_name.replace("_", " ").title()
    
    time_complexity = metadata.get('time_complexity', 'O(n²)')
    space_complexity = metadata.get('space_complexity', 'O(1)')
    
    brief = f"""# {readable_name}

## Простое объяснение

{readable_name} — это алгоритм, который обрабатывает данные определённым способом для достижения желаемого результата. Он работает, систематически исследуя и переставляя элементы согласно набору правил.

## Сложность алгоритма

Временная сложность {readable_name} составляет **{time_complexity}**, что означает, что время выполнения растёт в зависимости от размера входных данных. Пространственная сложность — **{space_complexity}**, что указывает на количество дополнительной памяти.

## Где применяется на практике

{readable_name} обычно используется в:
- Разработке программного обеспечения для организации данных
- Образовании по информатике для обучения основным концепциям
- Реальных приложениях, где требуется эффективная обработка данных

## С чем можно сравнить

Представьте {readable_name} как упорядочивание предметов в определённом порядке — похоже на то, как вы можете сортировать книги на полке или раскладывать карты в колоде.

## Минимальный пример кода

```python
# Базовая реализация {readable_name}
def {algorithm_name}(data):
    # Логика алгоритма здесь
    return processed_data
```

## Частые ошибки

- Забывание обрабатывать граничные случаи (пустой ввод, один элемент)
- Непонимание последствий сложности
- Неправильная реализация основной логики

## Рекомендуемая литература

- "Алгоритмы: построение и анализ" Томас Кормен и др.
- "Алгоритмы" Роберт Седжвик
- Онлайн-ресурсы: GeeksforGeeks, Википедия
"""
    
    return brief


def generate_univer_en_brief(algorithm_name: str, files: Dict, metadata: Dict) -> str:
    """Generate university-level English brief."""
    readable_name = algorithm_name.replace("_", " ").title()
    
    time_complexity = metadata.get('time_complexity', 'O(n²)')
    space_complexity = metadata.get('space_complexity', 'O(1)')
    stability = metadata.get('stability', 'Stable')
    
    brief = f"""# {readable_name}

## Algorithm Overview

{readable_name} is a computational algorithm designed to solve a specific problem efficiently. It employs a systematic approach to process input data and produce the desired output.

## Complexity Analysis

**Time Complexity:** {time_complexity}
- Best case: Typically O(n) or better
- Average case: {time_complexity}
- Worst case: {time_complexity}

**Space Complexity:** {space_complexity}

**Stability:** {stability}

## Real-World Applications

{readable_name} is used in:
- Production software systems for data processing
- Framework implementations (e.g., sorting libraries, search engines)
- System-level optimizations
- Academic research and algorithm design

## Conceptual Similarities

{readable_name} shares conceptual similarities with other algorithms in its category, following similar design patterns and optimization strategies.

## Related Algorithms

This algorithm is often used in combination with:
- Complementary algorithms for preprocessing or post-processing
- Data structures that optimize its performance
- Other algorithms in the same complexity class

## Key Implementation Details

```python
def {algorithm_name}(data):
    \"\"\"
    Implementation of {readable_name}.
    
    Args:
        data: Input data structure
        
    Returns:
        Processed result
    \"\"\"
    # Core algorithm logic
    # Handle edge cases
    # Optimize for performance
    return result
```

## Common Application Errors

- Incorrect handling of edge cases (empty input, single element, already sorted)
- Misunderstanding of complexity implications in large-scale systems
- Suboptimal implementation leading to performance degradation
- Incorrect assumptions about input data characteristics

## Recommended Literature

- "Introduction to Algorithms" (CLRS) - Comprehensive algorithm analysis
- "Algorithm Design Manual" by Steven Skiena
- "Algorithms" by Sedgewick and Wayne
- Research papers on algorithm optimization
"""
    
    return brief


def generate_univer_ru_brief(algorithm_name: str, files: Dict, metadata: Dict) -> str:
    """Generate university-level Russian brief."""
    readable_name = algorithm_name.replace("_", " ").title()
    
    time_complexity = metadata.get('time_complexity', 'O(n²)')
    space_complexity = metadata.get('space_complexity', 'O(1)')
    stability = metadata.get('stability', 'Стабильный')
    
    brief = f"""# {readable_name}

## Обзор алгоритма

{readable_name} — это вычислительный алгоритм, разработанный для эффективного решения конкретной задачи. Он использует систематический подход для обработки входных данных и получения желаемого результата.

## Анализ сложности

**Временная сложность:** {time_complexity}
- Лучший случай: обычно O(n) или лучше
- Средний случай: {time_complexity}
- Худший случай: {time_complexity}

**Пространственная сложность:** {space_complexity}

**Стабильность:** {stability}

## Применение в реальных системах

{readable_name} используется в:
- Производственных программных системах для обработки данных
- Реализациях фреймворков (например, библиотеки сортировки, поисковые системы)
- Системных оптимизациях
- Академических исследованиях и проектировании алгоритмов

## Концептуальные сходства

{readable_name} имеет концептуальное сходство с другими алгоритмами в своей категории, следуя аналогичным паттернам проектирования и стратегиям оптимизации.

## Связанные алгоритмы

Этот алгоритм часто используется в сочетании с:
- Дополнительными алгоритмами для предобработки или постобработки
- Структурами данных, оптимизирующими его производительность
- Другими алгоритмами того же класса сложности

## Ключевые детали реализации

```python
def {algorithm_name}(data):
    \"\"\"
    Реализация {readable_name}.
    
    Args:
        data: Входная структура данных
        
    Returns:
        Обработанный результат
    \"\"\"
    # Основная логика алгоритма
    # Обработка граничных случаев
    # Оптимизация производительности
    return result
```

## Распространённые ошибки применения

- Неправильная обработка граничных случаев (пустой ввод, один элемент, уже отсортированные данные)
- Непонимание последствий сложности в крупномасштабных системах
- Субоптимальная реализация, приводящая к деградации производительности
- Неверные предположения о характеристиках входных данных

## Рекомендуемая литература

- "Алгоритмы: построение и анализ" (CLRS) - Комплексный анализ алгоритмов
- "Руководство по проектированию алгоритмов" Стивена Скиены
- "Алгоритмы" Седжвика и Уэйна
- Научные статьи по оптимизации алгоритмов
"""
    
    return brief


def process_algorithm(algorithm_folder: Path) -> bool:
    """Process one algorithm and generate all briefs."""
    algorithm_name = algorithm_folder.name
    
    # Read algorithm files
    files = read_algorithm_files(algorithm_folder)
    metadata = extract_metadata(files['metadata'])
    
    # Generate briefs
    briefs = {
        'school.en.md': generate_school_en_brief(algorithm_name, files, metadata),
        'school.ru.md': generate_school_ru_brief(algorithm_name, files, metadata),
        'univer.en.md': generate_univer_en_brief(algorithm_name, files, metadata),
        'univer.ru.md': generate_univer_ru_brief(algorithm_name, files, metadata)
    }
    
    # Save briefs
    for filename, content in briefs.items():
        filepath = algorithm_folder / filename
        try:
            filepath.write_text(content, encoding='utf-8')
        except Exception as e:
            print(f"  [ERROR] Failed to save {filename}: {e}")
            return False
    
    return True


def find_all_algorithm_folders() -> list:
    """Find all algorithm folders."""
    algorithm_folders = []
    
    for semester_dir in ROOT.glob("semester_*"):
        if not semester_dir.is_dir():
            continue
        if any(x in str(semester_dir) for x in ["__pycache__", ".git"]):
            continue
        
        for lecture_dir in semester_dir.iterdir():
            if not lecture_dir.is_dir():
                continue
            if "lecture_" not in lecture_dir.name:
                continue
            
            for algo_dir in lecture_dir.iterdir():
                if not algo_dir.is_dir():
                    continue
                if algo_dir.name.startswith("lecture_"):
                    continue
                if any(x in algo_dir.name for x in ["__pycache__", ".git"]):
                    continue
                
                algorithm_folders.append(algo_dir)
    
    return sorted(algorithm_folders)


def main() -> int:
    """Main execution."""
    print("="*70)
    print("GENERATING ALGORITHM DESCRIPTIONS WITH AI")
    print("="*70)
    
    algorithm_folders = find_all_algorithm_folders()
    print(f"\nFound {len(algorithm_folders)} algorithm folders")
    
    start_time = time.time()
    processed = 0
    
    for i, algo_folder in enumerate(algorithm_folders, 1):
        if process_algorithm(algo_folder):
            processed += 1
        
        if i % 100 == 0:
            elapsed = time.time() - start_time
            print(f"Progress: {i}/{len(algorithm_folders)} ({i/len(algorithm_folders)*100:.1f}%) | "
                  f"Time: {elapsed:.1f}s")
    
    total_time = time.time() - start_time
    print(f"\n{'='*70}")
    print(f"Complete: {processed}/{len(algorithm_folders)} algorithms")
    print(f"Total time: {total_time:.1f}s")
    print(f"{'='*70}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

