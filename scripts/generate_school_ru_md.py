#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate school.ru.md files for each algorithm folder.
Creates Russian educational content for school students (grades 6-9).
"""

import json
import re
import sys
import io
from pathlib import Path
from typing import Dict, Optional

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parents[1]


def get_algorithm_name(folder_path: Path) -> str:
    """Extract algorithm name from folder path and metadata."""
    # Try to get from metadata.json
    metadata_file = folder_path / "metadata.json"
    if metadata_file.exists():
        try:
            metadata = json.loads(metadata_file.read_text(encoding='utf-8'))
            if 'name' in metadata:
                return metadata['name']
        except:
            pass
    
    # Try to get from README.md
    readme_file = folder_path / "README.md"
    if readme_file.exists():
        try:
            content = readme_file.read_text(encoding='utf-8')
            # Extract title from first line
            first_line = content.split('\n')[0].strip()
            if first_line.startswith('#'):
                name = first_line.lstrip('#').strip()
                return name
        except:
            pass
    
    # Fallback: convert folder name to readable format
    folder_name = folder_path.name
    # Replace underscores with spaces and title case
    name = folder_name.replace('_', ' ').title()
    return name


def get_algorithm_category(folder_path: Path) -> str:
    """Get algorithm category from metadata."""
    metadata_file = folder_path / "metadata.json"
    if metadata_file.exists():
        try:
            metadata = json.loads(metadata_file.read_text(encoding='utf-8'))
            if 'category' in metadata:
                return metadata['category']
        except:
            pass
    return "Алгоритм"


def generate_russian_content(algorithm_name: str, folder_name: str, 
                           category: str, folder_path: Path) -> str:
    """Generate Russian educational content for the algorithm."""
    
    # Translate common algorithm names to Russian
    name_translations = {
        'bubble_sort': 'Пузырьковая сортировка',
        'insertion_sort': 'Сортировка вставками',
        'selection_sort': 'Сортировка выбором',
        'merge_sort': 'Сортировка слиянием',
        'quick_sort': 'Быстрая сортировка',
        'heap_sort': 'Сортировка кучей',
        'binary_search': 'Бинарный поиск',
        'linear_search': 'Линейный поиск',
        'binary_tree': 'Бинарное дерево',
        'hash_table': 'Хеш-таблица',
        'dfs': 'Поиск в глубину',
        'bfs': 'Поиск в ширину',
    }
    
    # Get Russian name
    russian_name = name_translations.get(folder_name.lower(), algorithm_name)
    
    # Generate content based on algorithm type
    content = f"""# {russian_name}

## Простое объяснение

"""
    
    # Add simple explanation based on algorithm type
    if 'sort' in folder_name.lower() or 'сортиров' in russian_name.lower():
        content += f"""{russian_name} — это способ упорядочить элементы списка по возрастанию или убыванию. 
Алгоритм сравнивает элементы и меняет их местами, пока все не будут в правильном порядке.

"""
    elif 'search' in folder_name.lower() or 'поиск' in russian_name.lower():
        content += f"""{russian_name} — это способ найти нужный элемент в списке. 
Алгоритм просматривает элементы один за другим или использует специальную стратегию, 
чтобы быстро найти то, что нужно.

"""
    elif 'tree' in folder_name.lower() or 'дерев' in russian_name.lower():
        content += f"""{russian_name} — это структура данных, которая похожа на дерево с ветками. 
Каждый элемент (узел) может иметь дочерние элементы, что позволяет эффективно 
организовывать и находить информацию.

"""
    elif 'hash' in folder_name.lower() or 'хеш' in russian_name.lower():
        content += f"""{russian_name} — это способ быстро находить данные по ключу. 
Алгоритм преобразует ключ в число (хеш), которое указывает, где хранится нужная информация.

"""
    else:
        content += f"""{russian_name} — это алгоритм для решения определённой задачи. 
Он использует последовательность шагов, чтобы получить нужный результат.

"""
    
    content += """## Где применяется

"""
    
    # Add real-life applications
    if 'sort' in folder_name.lower():
        content += """- упорядочивание оценок в журнале;
- сортировка товаров по цене в интернет-магазине;
- организация списка друзей по алфавиту;
- упорядочивание файлов по дате создания.

"""
    elif 'search' in folder_name.lower():
        content += """- поиск ученика в списке класса;
- поиск нужного файла в папке;
- поиск нужного слова в тексте;
- поиск предмета в ящике.

"""
    elif 'tree' in folder_name.lower():
        content += """- организация файлов и папок на компьютере;
- структура меню в программах;
- организация категорий товаров в магазине;
- построение генеалогического дерева.

"""
    elif 'hash' in folder_name.lower():
        content += """- быстрый поиск контактов в телефонной книге;
- хранение паролей в безопасном виде;
- индексация страниц в поисковых системах;
- кэширование данных для ускорения работы.

"""
    else:
        content += """- решение практических задач в программировании;
- оптимизация работы приложений;
- обработка данных;
- автоматизация процессов.

"""
    
    content += """## Пример

"""
    
    # Add example based on algorithm type
    if 'bubble' in folder_name.lower():
        content += """Нужно отсортировать числа: 5, 2, 8, 1, 9

Шаг 1: Сравниваем 5 и 2 → 5 > 2, меняем местами → 2, 5, 8, 1, 9
Шаг 2: Сравниваем 5 и 8 → 5 < 8, не меняем → 2, 5, 8, 1, 9
Шаг 3: Сравниваем 8 и 1 → 8 > 1, меняем местами → 2, 5, 1, 8, 9
Шаг 4: Сравниваем 8 и 9 → 8 < 9, не меняем → 2, 5, 1, 8, 9

Повторяем процесс, пока все числа не будут в порядке: 1, 2, 5, 8, 9

"""
    elif 'linear_search' in folder_name.lower() or 'линейный' in russian_name.lower():
        content += """Нужно найти число 25 в списке: 10, 7, 25, 3

Алгоритм смотрит первое число → 10, не то
Второе → 7, не то
Третье → 25, найдено!
Останавливается.

"""
    elif 'binary_search' in folder_name.lower() or 'бинарный' in russian_name.lower():
        content += """Нужно найти число 7 в упорядоченном списке: 1, 3, 5, 7, 9, 11, 13

Шаг 1: Смотрим середину → 7 (найдено!)
Если бы искали 5:
Шаг 1: Середина → 7, ищем слева
Шаг 2: Середина левой части → 3, ищем справа
Шаг 3: Находим 5

"""
    else:
        content += f"""Рассмотрим простой пример работы алгоритма:

1. Исходные данные: [пример входных данных]
2. Применяем алгоритм: выполняем шаги по порядку
3. Получаем результат: [пример выходных данных]

Алгоритм работает последовательно, проверяя условия и выполняя действия.

"""
    
    content += """## Вопросы для самопроверки

### Базовые

"""
    
    # Add basic questions
    if 'sort' in folder_name.lower():
        content += """1. Что делает алгоритм сортировки?
2. В каких случаях нужна сортировка?
3. Сколько элементов можно отсортировать этим способом?

"""
    elif 'search' in folder_name.lower():
        content += """1. Что делает алгоритм поиска?
2. В каких случаях он подходит?
3. Что происходит, если элемент не найден?

"""
    else:
        content += """1. Что делает этот алгоритм?
2. В каких ситуациях его используют?
3. Какие данные нужны для работы алгоритма?

"""
    
    content += """### Средние

"""
    
    # Add medium questions
    if 'sort' in folder_name.lower():
        content += """4. Как работает алгоритм, если элементы уже отсортированы?
5. Почему некоторые алгоритмы сортировки быстрее других?
6. Сколько сравнений нужно для сортировки n элементов?

"""
    elif 'search' in folder_name.lower():
        content += """4. Как работает алгоритм, если элемента нет в списке?
5. Почему бинарный поиск быстрее линейного?
6. В каких случаях нельзя использовать бинарный поиск?

"""
    else:
        content += """4. Как алгоритм обрабатывает граничные случаи?
5. Какие преимущества и недостатки у этого алгоритма?
6. Можно ли улучшить работу алгоритма?

"""
    
    content += """### Сложные

"""
    
    # Add advanced questions
    if 'sort' in folder_name.lower():
        content += """7. Что изменится, если список очень большой?
8. Как оценить эффективность алгоритма?
9. Можно ли отсортировать данные за один проход?

"""
    elif 'search' in folder_name.lower():
        content += """7. Что изменится, если список упорядочен?
8. Как улучшить время поиска?
9. Как работает поиск в неупорядоченном списке?

"""
    else:
        content += """7. Как алгоритм работает с большими объёмами данных?
8. Какая сложность у этого алгоритма?
9. Как можно оптимизировать алгоритм?

"""
    
    content += """## Практические задания

### Уровень 1 (Лёгкий)

"""
    
    # Add level 1 tasks
    if 'sort' in folder_name.lower():
        content += """Отсортируй список фруктов по алфавиту: ["яблоко", "банан", "апельсин", "груша"]

"""
    elif 'search' in folder_name.lower():
        content += """Найди слово "яблоко" в списке фруктов: ["банан", "яблоко", "апельсин", "груша"]

"""
    else:
        content += f"""Выполни простую операцию с алгоритмом {russian_name.lower()}.
Используй небольшой набор данных (3-5 элементов).

"""
    
    content += """### Уровень 2 (Средний)

"""
    
    # Add level 2 tasks
    if 'sort' in folder_name.lower():
        content += """Определи, сколько шагов сделает алгоритм при сортировке списка из 10 элементов.
Отсортируй список чисел: [64, 34, 25, 12, 22, 11, 90, 5, 77, 1]

"""
    elif 'search' in folder_name.lower():
        content += """Определи, сколько шагов сделает алгоритм при поиске числа 18 в списке из 20 элементов.
Найди все вхождения числа 5 в списке: [1, 5, 3, 5, 7, 5, 9, 2, 5, 4]

"""
    else:
        content += f"""Примени алгоритм {russian_name.lower()} к более сложному набору данных.
Проанализируй результат и объясни, как работает алгоритм.

"""
    
    content += """### Уровень 3 (Продвинутый)

"""
    
    # Add level 3 tasks
    if 'sort' in folder_name.lower():
        content += """Напиши простую программу сортировки на любом языке программирования, 
которая выводит каждый шаг процесса сортировки.
Сравни время работы с разными размерами списков.

"""
    elif 'search' in folder_name.lower():
        content += """Напиши простой алгоритм поиска на любом языке программирования, 
который выводит номер найденного элемента и количество выполненных сравнений.
Реализуй поиск для упорядоченного и неупорядоченного списка.

"""
    else:
        content += f"""Напиши реализацию алгоритма {russian_name.lower()} на языке программирования.
Добавь обработку ошибок и проверку входных данных.
Протестируй алгоритм на разных наборах данных.

"""
    
    content += """---

**Этическое замечание:**

Помни, что алгоритмы — это инструменты для решения задач. Выбор способа решения должен 
учитывать честность, логику и уважение к другим. Алгоритмы помогают нам работать эффективнее, 
но важно использовать их ответственно и понимать, как они работают.

"""
    
    return content


def process_algorithm_folder(folder_path: Path) -> bool:
    """Process a single algorithm folder and generate school.ru.md."""
    try:
        # Check if this is an algorithm folder (has Algorithm.java or algorithm.py)
        has_java = (folder_path / "Algorithm.java").exists()
        has_python = (folder_path / "algorithm.py").exists()
        
        if not (has_java or has_python):
            return False
        
        # Skip if school.ru.md already exists and is recent
        school_file = folder_path / "school.ru.md"
        if school_file.exists():
            # Optionally skip existing files, or regenerate
            # For now, we'll regenerate to ensure consistency
            pass
        
        # Get algorithm information
        algorithm_name = get_algorithm_name(folder_path)
        category = get_algorithm_category(folder_path)
        folder_name = folder_path.name
        
        # Generate content
        content = generate_russian_content(algorithm_name, folder_name, category, folder_path)
        
        # Write file
        school_file.write_text(content, encoding='utf-8')
        return True
        
    except Exception as e:
        print(f"  [ERROR] Failed to process {folder_path}: {e}")
        return False


def main():
    """Main function to generate school.ru.md for all algorithm folders."""
    print("=" * 70)
    print("ГЕНЕРАЦИЯ ФАЙЛОВ school.ru.md")
    print("=" * 70)
    print()
    
    # Find all algorithm folders
    algorithm_folders = []
    
    # Look for folders containing Algorithm.java or algorithm.py
    for java_file in ROOT.rglob("Algorithm.java"):
        folder = java_file.parent
        if folder not in algorithm_folders:
            algorithm_folders.append(folder)
    
    for py_file in ROOT.rglob("algorithm.py"):
        folder = py_file.parent
        if folder not in algorithm_folders:
            algorithm_folders.append(folder)
    
    # Sort for consistent processing
    algorithm_folders.sort()
    
    print(f"Найдено {len(algorithm_folders)} папок с алгоритмами")
    print()
    
    generated_count = 0
    skipped_count = 0
    error_count = 0
    
    for idx, folder_path in enumerate(algorithm_folders, 1):
        relative_path = folder_path.relative_to(ROOT)
        print(f"[{idx}/{len(algorithm_folders)}] Обработка: {relative_path}")
        
        if process_algorithm_folder(folder_path):
            print(f"  [OK] Создан school.ru.md")
            generated_count += 1
        else:
            print(f"  [SKIP] Пропущено")
            skipped_count += 1
        
        if (idx % 50 == 0):
            print(f"\nПрогресс: {idx}/{len(algorithm_folders)} обработано\n")
    
    print()
    print("=" * 70)
    print(f"Итоги:")
    print(f"  Всего папок: {len(algorithm_folders)}")
    print(f"  Создано файлов: {generated_count}")
    print(f"  Пропущено: {skipped_count}")
    print(f"  Ошибок: {error_count}")
    print("=" * 70)


if __name__ == "__main__":
    main()

