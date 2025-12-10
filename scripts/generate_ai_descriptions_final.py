#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final enhanced AI description generator with all improvements:
- Extract detailed descriptions from README files
- Improve complexity detection from docstrings
- Add algorithm-specific examples based on code analysis
- Generate specific use cases based on algorithm type
"""

import sys
import json
import re
import ast
import time
from pathlib import Path
from typing import Dict, Optional, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Fix Windows console encoding
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding='utf-8', errors='replace'
    )


def extract_detailed_description_from_readme(readme_content: str) -> str:
    """Extract detailed description from README file."""
    if not readme_content:
        return ""
    
    # Try to find the main description (usually first paragraph after title)
    lines = readme_content.split('\n')
    description_parts = []
    
    # Look for description after title
    found_title = False
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        
        # Skip empty lines and markdown headers initially
        if not line_stripped or line_stripped.startswith('#'):
            if line_stripped.startswith('#') and len(line_stripped) <= 50:
                found_title = True
            continue
        
        # After title, collect description paragraphs
        if found_title or i < 20:  # Check first 20 lines
            # Skip common markdown elements
            if (line_stripped.startswith('-') or 
                line_stripped.startswith('*') or
                line_stripped.startswith('[') or
                line_stripped.startswith('!') or
                '```' in line_stripped):
                continue
            
            # Collect meaningful description text
            if len(line_stripped) > 30 and not line_stripped.startswith('##'):
                description_parts.append(line_stripped)
                if len(description_parts) >= 3:  # Get first few paragraphs
                    break
    
    return ' '.join(description_parts[:2]) if description_parts else ""


def extract_complexity_from_docstring(code: str) -> Tuple[str, str]:
    """Extract complexity information from docstrings more accurately."""
    time_complexity = "O(n²)"
    space_complexity = "O(1)"
    
    # Pattern to find complexity in docstrings
    patterns = {
        'time': [
            r'Time Complexity[:\s]+O\([^)]+\)',
            r'Time[:\s]+O\([^)]+\)',
            r'O\([^)]+\)[^\n]*time',
            r'complexity[^\n]*O\([^)]+\)'
        ],
        'space': [
            r'Space Complexity[:\s]+O\([^)]+\)',
            r'Space[:\s]+O\([^)]+\)',
            r'O\([^)]+\)[^\n]*space',
            r'memory[^\n]*O\([^)]+\)'
        ]
    }
    
    # Search in docstrings
    docstring_pattern = r'"""(.*?)"""'
    docstrings = re.findall(docstring_pattern, code, re.DOTALL | re.IGNORECASE)
    
    for doc in docstrings:
        doc_lower = doc.lower()
        
        # Extract time complexity
        for pattern in patterns['time']:
            match = re.search(pattern, doc, re.IGNORECASE)
            if match:
                comp_match = re.search(r'O\([^)]+\)', match.group())
                if comp_match:
                    time_complexity = comp_match.group()
                    break
        
        # Extract space complexity
        for pattern in patterns['space']:
            match = re.search(pattern, doc, re.IGNORECASE)
            if match:
                comp_match = re.search(r'O\([^)]+\)', match.group())
                if comp_match:
                    space_complexity = comp_match.group()
                    break
    
    return time_complexity, space_complexity


def extract_code_example(code: str, algorithm_name: str) -> str:
    """Extract or generate code example from algorithm implementation."""
    # Try to find the main function
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_name = node.name
                if func_name == algorithm_name or func_name.replace('_', '') == algorithm_name.replace('_', ''):
                    # Extract function signature and key logic
                    args = [arg.arg for arg in node.args.args]
                    
                    # Find key operations in function body
                    key_lines = []
                    for stmt in node.body[:10]:  # First 10 statements
                        if isinstance(stmt, ast.Assign):
                            key_lines.append(ast.unparse(stmt))
                        elif isinstance(stmt, ast.If):
                            key_lines.append(ast.unparse(stmt))
                        elif isinstance(stmt, ast.For):
                            key_lines.append(ast.unparse(stmt))
                    
                    if key_lines:
                        example = f"def {func_name}({', '.join(args)}):\n"
                        example += "    \"\"\"Implementation.\"\"\"\n"
                        for line in key_lines[:3]:  # First 3 key lines
                            example += f"    {line}\n"
                        example += "    return result"
                        return example
    except:
        pass
    
    # Fallback: simple template
    return f"""def {algorithm_name}(data):
    \"\"\"Implementation of {algorithm_name.replace('_', ' ').title()}.\"\"\"
    # Core algorithm logic
    return result"""


def get_algorithm_specific_use_cases(algorithm_name: str, category: str, analysis: Dict) -> List[str]:
    """Generate algorithm-specific use cases based on type and analysis."""
    use_cases = []
    
    name_lower = algorithm_name.lower()
    
    # Category-based use cases
    if category == 'Sorting' or 'sort' in name_lower:
        use_cases = [
            "Sorting arrays in programming languages (Python sorted(), Java Collections.sort())",
            "Database query optimization and indexing",
            "Operating system process scheduling",
            "E-commerce product listings and price sorting"
        ]
    elif category == 'Graph Algorithms' or 'graph' in name_lower:
        if 'dijkstra' in name_lower or 'shortest' in name_lower:
            use_cases = [
                "GPS navigation systems (Google Maps, Waze)",
                "Network routing protocols (OSPF, IS-IS)",
                "Social media friend recommendations",
                "Game pathfinding (A* algorithm)"
            ]
        elif 'bfs' in name_lower or 'breadth' in name_lower:
            use_cases = [
                "Social network friend-of-friend searches",
                "Web crawling and indexing",
                "Shortest path in unweighted graphs",
                "Level-order tree traversal"
            ]
        elif 'dfs' in name_lower or 'depth' in name_lower:
            use_cases = [
                "Maze solving algorithms",
                "Topological sorting",
                "Cycle detection in graphs",
                "Tree/graph traversal"
            ]
        else:
            use_cases = [
                "Social network analysis",
                "Recommendation systems",
                "Network topology analysis",
                "Dependency resolution"
            ]
    elif category == 'Dynamic Programming' or 'dynamic' in name_lower:
        if 'fibonacci' in name_lower:
            use_cases = [
                "Mathematical sequence generation",
                "Financial modeling (Fibonacci retracements)",
                "Algorithm complexity analysis",
                "Recursive problem optimization"
            ]
        elif 'knapsack' in name_lower:
            use_cases = [
                "Resource allocation problems",
                "Portfolio optimization",
                "Cutting stock problems",
                "Budget allocation"
            ]
        elif 'edit' in name_lower or 'distance' in name_lower:
            use_cases = [
                "Spell checkers and autocorrect",
                "DNA sequence alignment",
                "Version control diff algorithms",
                "Plagiarism detection"
            ]
        else:
            use_cases = [
                "Optimization problems",
                "Sequence alignment",
                "Resource allocation",
                "Game theory strategies"
            ]
    elif category == 'Tree Algorithms' or 'tree' in name_lower:
        use_cases = [
            "Database indexing (B-trees, AVL trees)",
            "File system organization",
            "Expression parsing and evaluation",
            "Decision tree algorithms in ML"
        ]
    elif category == 'Search Algorithms' or 'search' in name_lower:
        use_cases = [
            "Database query optimization",
            "Search engines (binary search in sorted indices)",
            "Autocomplete and suggestion systems",
            "Lookup tables and caches"
        ]
    else:
        use_cases = [
            "Software development frameworks",
            "System optimization",
            "Data processing pipelines",
            "Algorithm libraries"
        ]
    
    return use_cases[:4]  # Return top 4


def read_algorithm_files(algorithm_folder: Path) -> Dict[str, any]:
    """Read and analyze all algorithm files with enhanced extraction."""
    files = {
        'readme': None,
        'readme_description': '',
        'algorithm_py': None,
        'metadata': None,
        'analysis': {},
        'code_example': '',
        'use_cases': []
    }
    
    # Read README.md
    readme_path = algorithm_folder / "README.md"
    if readme_path.exists():
        try:
            files['readme'] = readme_path.read_text(encoding='utf-8')
            files['readme_description'] = extract_detailed_description_from_readme(files['readme'])
        except:
            pass
    
    # Read algorithm.py
    algo_path = algorithm_folder / "algorithm.py"
    if algo_path.exists():
        try:
            files['algorithm_py'] = algo_path.read_text(encoding='utf-8')
            files['code_example'] = extract_code_example(files['algorithm_py'], algorithm_folder.name)
            
            # Enhanced analysis
            files['analysis'] = analyze_algorithm_code(files['algorithm_py'])
            doc_info = extract_docstring_info(files['algorithm_py'])
            files['analysis'].update(doc_info)
            
            # Enhanced complexity extraction
            time_comp, space_comp = extract_complexity_from_docstring(files['algorithm_py'])
            files['analysis']['time_complexity'] = time_comp
            files['analysis']['space_complexity'] = space_comp
        except:
            pass
    
    # Read metadata.json
    metadata_path = algorithm_folder / "metadata.json"
    if metadata_path.exists():
        try:
            files['metadata'] = json.loads(metadata_path.read_text(encoding='utf-8'))
        except:
            pass
    
    # Generate use cases
    category = get_category(files)
    files['use_cases'] = get_algorithm_specific_use_cases(
        algorithm_folder.name, category, files['analysis']
    )
    
    return files


def analyze_algorithm_code(code: str) -> Dict[str, any]:
    """Analyze algorithm code to extract key information."""
    analysis = {
        'type': 'unknown',
        'key_operations': [],
        'data_structures': [],
        'complexity_hints': {}
    }
    
    code_lower = code.lower()
    
    if 'sort' in code_lower or 'sorted' in code_lower:
        analysis['type'] = 'sorting'
    elif 'graph' in code_lower or ('node' in code_lower and 'edge' in code_lower):
        analysis['type'] = 'graph'
    elif 'tree' in code_lower:
        analysis['type'] = 'tree'
    elif 'search' in code_lower or 'find' in code_lower:
        analysis['type'] = 'search'
    elif 'dynamic' in code_lower or 'memo' in code_lower or 'dp' in code_lower:
        analysis['type'] = 'dynamic_programming'
    elif 'pattern' in code_lower or 'design' in code_lower:
        analysis['type'] = 'design_pattern'
    
    if 'swap' in code_lower or 'exchange' in code_lower:
        analysis['key_operations'].append('swapping elements')
    if 'compare' in code_lower:
        analysis['key_operations'].append('comparing elements')
    if 'heap' in code_lower or 'heappush' in code_lower or 'heappop' in code_lower:
        analysis['data_structures'].append('heap/priority queue')
    if 'queue' in code_lower:
        analysis['data_structures'].append('queue')
    if 'stack' in code_lower:
        analysis['data_structures'].append('stack')
    if 'dict' in code_lower or 'hash' in code_lower:
        analysis['data_structures'].append('hash table/dictionary')
    
    return analysis


def extract_docstring_info(code: str) -> Dict[str, str]:
    """Extract information from docstrings."""
    info = {'description': '', 'complexity': '', 'usage': ''}
    
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                if ast.get_docstring(node):
                    doc = ast.get_docstring(node)
                    info['description'] = doc.split('\n')[0] if doc else ''
                    if 'Complexity' in doc or 'O(' in doc:
                        info['complexity'] = doc
                    break
    except:
        pass
    
    docstring_pattern = r'"""(.*?)"""'
    matches = re.findall(docstring_pattern, code, re.DOTALL)
    if matches:
        doc = matches[0].strip()
        info['description'] = doc.split('\n')[0] if doc else ''
    
    return info


def get_algorithm_description(algorithm_name: str, files: Dict) -> str:
    """Get algorithm description prioritizing README, then docstring."""
    # Priority 1: README description
    if files.get('readme_description'):
        return files['readme_description']
    
    # Priority 2: Docstring description
    if files['analysis'].get('description'):
        return files['analysis']['description']
    
    # Priority 3: README first paragraph
    if files['readme']:
        lines = files['readme'].split('\n')
        for line in lines:
            if line.strip() and not line.startswith('#') and len(line) > 20:
                return line.strip()
    
    # Fallback
    readable_name = algorithm_name.replace("_", " ").title()
    return f"{readable_name} algorithm"


def get_complexity_info(files: Dict) -> Tuple[str, str]:
    """Extract time and space complexity with priority to code analysis."""
    time_complexity = "O(n²)"
    space_complexity = "O(1)"
    
    # Priority 1: From code analysis (extracted from docstrings)
    if files['analysis'].get('time_complexity'):
        time_complexity = files['analysis']['time_complexity']
    if files['analysis'].get('space_complexity'):
        space_complexity = files['analysis']['space_complexity']
    
    # Priority 2: From metadata
    if files['metadata']:
        if isinstance(files['metadata'].get('complexity'), dict):
            comp = files['metadata']['complexity']
            time_complexity = comp.get('time', time_complexity)
            space_complexity = comp.get('space', space_complexity)
        elif isinstance(files['metadata'].get('time_complexity'), str):
            time_complexity = files['metadata'].get('time_complexity', time_complexity)
            space_complexity = files['metadata'].get('space_complexity', space_complexity)
    
    return time_complexity, space_complexity


def get_category(files: Dict) -> str:
    """Get algorithm category."""
    if files['metadata'] and files['metadata'].get('category'):
        return files['metadata']['category']
    
    if files['analysis'].get('type') != 'unknown':
        type_map = {
            'sorting': 'Sorting',
            'graph': 'Graph Algorithms',
            'tree': 'Tree Algorithms',
            'search': 'Search Algorithms',
            'dynamic_programming': 'Dynamic Programming',
            'design_pattern': 'Design Pattern'
        }
        return type_map.get(files['analysis']['type'], 'Algorithms')
    
    return 'Algorithms'


def generate_school_en_brief(algorithm_name: str, files: Dict) -> str:
    """Generate enhanced school-level English brief."""
    readable_name = algorithm_name.replace("_", " ").title()
    description = get_algorithm_description(algorithm_name, files)
    time_complexity, space_complexity = get_complexity_info(files)
    category = get_category(files)
    use_cases = files.get('use_cases', [])
    code_example = files.get('code_example', f"def {algorithm_name}(data):\n    return result")
    
    key_ops = files['analysis'].get('key_operations', [])
    operation_desc = ', '.join(key_ops) if key_ops else 'processing data systematically'
    
    brief = f"""# {readable_name}

## Simple Explanation

{description}

This algorithm works by {operation_desc} to achieve its goal. It's part of the **{category}** category of algorithms.

## Algorithm Complexity

The time complexity is **{time_complexity}**, which means the time it takes to run depends on the size of the input data. The space complexity is **{space_complexity}**, indicating how much extra memory is needed.

## Where It's Used in Practice

{readable_name} is commonly used in:
"""
    
    for use_case in use_cases[:3]:  # Top 3 use cases
        brief += f"- {use_case}\n"
    
    brief += f"""- Computer science education and algorithm learning

## What It Can Be Compared To

Think of {readable_name} like a systematic way of organizing or finding information - similar to how you might organize items or search through a collection efficiently.

## Minimal Code Example

```python
{code_example}
```

## Common Mistakes

- Not handling edge cases (empty input, single element)
- Misunderstanding the complexity implications
- Incorrect implementation leading to wrong results
- Not optimizing for the specific use case

## Recommended Literature

- "Introduction to Algorithms" by Cormen, Leiserson, Rivest, and Stein
- "Algorithms" by Robert Sedgewick and Kevin Wayne
- Online resources: GeeksforGeeks, Wikipedia, Algorithm Visualizations
"""
    
    return brief


def generate_school_ru_brief(algorithm_name: str, files: Dict) -> str:
    """Generate enhanced school-level Russian brief."""
    readable_name = algorithm_name.replace("_", " ").title()
    description = get_algorithm_description(algorithm_name, files)
    time_complexity, space_complexity = get_complexity_info(files)
    category = get_category(files)
    use_cases = files.get('use_cases', [])
    code_example = files.get('code_example', f"def {algorithm_name}(data):\n    return result")
    
    key_ops = files['analysis'].get('key_operations', [])
    operation_desc = ', '.join(key_ops) if key_ops else 'систематически обрабатывая данные'
    
    brief = f"""# {readable_name}

## Простое объяснение

{description}

Этот алгоритм работает, {operation_desc}, чтобы достичь своей цели. Он относится к категории алгоритмов **{category}**.

## Сложность алгоритма

Временная сложность составляет **{time_complexity}**, что означает, что время выполнения зависит от размера входных данных. Пространственная сложность — **{space_complexity}**, что указывает на количество дополнительной памяти.

## Где применяется на практике

{readable_name} обычно используется в:
"""
    
    for use_case in use_cases[:3]:
        brief += f"- {use_case}\n"
    
    brief += f"""- Образовании по информатике и изучении алгоритмов

## С чем можно сравнить

Представьте {readable_name} как систематический способ организации или поиска информации — похоже на то, как вы можете эффективно организовывать предметы или искать в коллекции.

## Минимальный пример кода

```python
{code_example}
```

## Частые ошибки

- Не обрабатываются граничные случаи (пустой ввод, один элемент)
- Непонимание последствий сложности
- Неправильная реализация, приводящая к неверным результатам
- Не оптимизировано для конкретного случая использования

## Рекомендуемая литература

- "Алгоритмы: построение и анализ" Томас Кормен и др.
- "Алгоритмы" Роберт Седжвик
- Онлайн-ресурсы: GeeksforGeeks, Википедия, Визуализации алгоритмов
"""
    
    return brief


def generate_univer_en_brief(algorithm_name: str, files: Dict) -> str:
    """Generate enhanced university-level English brief."""
    readable_name = algorithm_name.replace("_", " ").title()
    description = get_algorithm_description(algorithm_name, files)
    time_complexity, space_complexity = get_complexity_info(files)
    category = get_category(files)
    use_cases = files.get('use_cases', [])
    code_example = files.get('code_example', f"def {algorithm_name}(data):\n    return result")
    
    key_ops = files['analysis'].get('key_operations', [])
    data_structs = files['analysis'].get('data_structures', [])
    
    brief = f"""# {readable_name}

## Algorithm Overview

{description}

This algorithm belongs to the **{category}** category and employs {' and '.join(key_ops) if key_ops else 'systematic data processing'} to achieve its objectives.

## Complexity Analysis

**Time Complexity:** {time_complexity}
- The algorithm's performance scales according to this complexity class
- Best, average, and worst cases may vary based on input characteristics

**Space Complexity:** {space_complexity}
- Indicates the amount of additional memory required during execution

**Key Data Structures:** {', '.join(data_structs) if data_structs else 'Standard data structures'}

## Real-World Applications

{readable_name} is used in:
"""
    
    for use_case in use_cases:
        brief += f"- {use_case}\n"
    
    brief += f"""
## Conceptual Similarities

This algorithm shares conceptual similarities with other algorithms in the {category} category, following similar design patterns and optimization strategies.

## Related Algorithms

{readable_name} is often used in combination with:
- Complementary algorithms for preprocessing or post-processing
- Data structures that optimize its performance
- Other algorithms in the same complexity class

## Key Implementation Details

```python
{code_example}
```

## Common Application Errors

- Incorrect handling of edge cases (empty input, single element, boundary conditions)
- Misunderstanding of complexity implications in large-scale systems
- Suboptimal implementation leading to performance degradation
- Incorrect assumptions about input data characteristics
- Not considering alternative algorithms for specific use cases

## Recommended Literature

- "Introduction to Algorithms" (CLRS) - Comprehensive algorithm analysis
- "Algorithm Design Manual" by Steven Skiena
- "Algorithms" by Sedgewick and Wayne
- Research papers on algorithm optimization and analysis
- Framework documentation and implementation guides
"""
    
    return brief


def generate_univer_ru_brief(algorithm_name: str, files: Dict) -> str:
    """Generate enhanced university-level Russian brief."""
    readable_name = algorithm_name.replace("_", " ").title()
    description = get_algorithm_description(algorithm_name, files)
    time_complexity, space_complexity = get_complexity_info(files)
    category = get_category(files)
    use_cases = files.get('use_cases', [])
    code_example = files.get('code_example', f"def {algorithm_name}(data):\n    return result")
    
    key_ops = files['analysis'].get('key_operations', [])
    data_structs = files['analysis'].get('data_structures', [])
    
    brief = f"""# {readable_name}

## Обзор алгоритма

{description}

Этот алгоритм относится к категории **{category}** и использует {' и '.join(key_ops) if key_ops else 'систематическую обработку данных'} для достижения своих целей.

## Анализ сложности

**Временная сложность:** {time_complexity}
- Производительность алгоритма масштабируется согласно этому классу сложности
- Лучший, средний и худший случаи могут различаться в зависимости от характеристик входных данных

**Пространственная сложность:** {space_complexity}
- Указывает на количество дополнительной памяти, необходимой во время выполнения

**Ключевые структуры данных:** {', '.join(data_structs) if data_structs else 'Стандартные структуры данных'}

## Применение в реальных системах

{readable_name} используется в:
"""
    
    for use_case in use_cases:
        brief += f"- {use_case}\n"
    
    brief += f"""
## Концептуальные сходства

Этот алгоритм имеет концептуальное сходство с другими алгоритмами в категории {category}, следуя аналогичным паттернам проектирования и стратегиям оптимизации.

## Связанные алгоритмы

{readable_name} часто используется в сочетании с:
- Дополнительными алгоритмами для предобработки или постобработки
- Структурами данных, оптимизирующими его производительность
- Другими алгоритмами того же класса сложности

## Ключевые детали реализации

```python
{code_example}
```

## Распространённые ошибки применения

- Неправильная обработка граничных случаев (пустой ввод, один элемент, граничные условия)
- Непонимание последствий сложности в крупномасштабных системах
- Субоптимальная реализация, приводящая к деградации производительности
- Неверные предположения о характеристиках входных данных
- Не рассмотрение альтернативных алгоритмов для конкретных случаев использования

## Рекомендуемая литература

- "Алгоритмы: построение и анализ" (CLRS) - Комплексный анализ алгоритмов
- "Руководство по проектированию алгоритмов" Стивена Скиены
- "Алгоритмы" Седжвика и Уэйна
- Научные статьи по оптимизации и анализу алгоритмов
- Документация фреймворков и руководства по реализации
"""
    
    return brief


def process_algorithm(algorithm_folder: Path) -> bool:
    """Process one algorithm and generate all enhanced briefs."""
    algorithm_name = algorithm_folder.name
    
    # Read and analyze algorithm files with all enhancements
    files = read_algorithm_files(algorithm_folder)
    
    # Generate enhanced briefs
    briefs = {
        'school.en.md': generate_school_en_brief(algorithm_name, files),
        'school.ru.md': generate_school_ru_brief(algorithm_name, files),
        'univer.en.md': generate_univer_en_brief(algorithm_name, files),
        'univer.ru.md': generate_univer_ru_brief(algorithm_name, files)
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
    print("FINAL ENHANCED AI DESCRIPTION GENERATOR")
    print("="*70)
    print("With all improvements:")
    print("  - Detailed descriptions from README files")
    print("  - Improved complexity detection from docstrings")
    print("  - Algorithm-specific examples from code analysis")
    print("  - Specific use cases based on algorithm type")
    print()
    
    algorithm_folders = find_all_algorithm_folders()
    print(f"Found {len(algorithm_folders)} algorithm folders")
    
    start_time = time.time()
    processed = 0
    errors = 0
    
    for i, algo_folder in enumerate(algorithm_folders, 1):
        try:
            if process_algorithm(algo_folder):
                processed += 1
            else:
                errors += 1
        except Exception as e:
            print(f"  [ERROR] {algo_folder.name}: {e}")
            errors += 1
        
        if i % 100 == 0:
            elapsed = time.time() - start_time
            rate = i / elapsed if elapsed > 0 else 0
            print(f"Progress: {i}/{len(algorithm_folders)} ({i/len(algorithm_folders)*100:.1f}%) | "
                  f"Time: {elapsed:.1f}s | Rate: {rate:.1f} alg/s")
    
    total_time = time.time() - start_time
    print(f"\n{'='*70}")
    print(f"Complete: {processed}/{len(algorithm_folders)} algorithms")
    print(f"Errors: {errors}")
    print(f"Total time: {total_time:.1f}s")
    print(f"Average: {total_time/len(algorithm_folders)*1000:.1f} ms per algorithm")
    print(f"Total files updated: {processed * 4}")
    print(f"{'='*70}")
    
    return 0 if errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

