#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate school.ru.md files for each algorithm folder with specific, concrete explanations.
Creates Russian educational content for school students (grades 6-9).
"""

import json
import re
import sys
import io
from pathlib import Path
from typing import Dict, Optional, Tuple

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parents[1]


def extract_readme_info(readme_path: Path) -> Dict[str, str]:
    """Extract information from README.md."""
    info = {}
    if not readme_path.exists():
        return info
    
    try:
        content = readme_path.read_text(encoding='utf-8')
        
        # Extract description from Introduction or Overview
        intro_match = re.search(
            r'(?:## Introduction|## Overview|## Description)\s*\n\n(.+?)(?:\n\n##|\n## |\Z)',
            content, re.DOTALL
        )
        if intro_match:
            desc = intro_match.group(1).strip()
            # Clean up markdown formatting
            desc = re.sub(r'\*\*([^*]+)\*\*', r'\1', desc)
            desc = re.sub(r'`([^`]+)`', r'\1', desc)
            info['description'] = desc[:500]  # Limit length
        
        # Extract short description
        short_match = re.search(
            r'### Short Description\s*\n\n(.+?)(?:\n\n|\n##|\Z)',
            content, re.DOTALL
        )
        if short_match:
            info['short_description'] = short_match.group(1).strip()[:200]
        
        # Extract real-world applications
        apps_match = re.search(
            r'(?:## Real-World Applications|## Use Cases|## Applications)\s*\n\n(.+?)(?:\n\n##|\Z)',
            content, re.DOTALL
        )
        if apps_match:
            apps_text = apps_match.group(1)
            # Extract list items
            apps = re.findall(r'[-*]\s*(.+?)(?:\n|$)', apps_text)
            info['applications'] = [app.strip() for app in apps[:5]]
        
        # Extract algorithm steps
        steps_match = re.search(
            r'(?:## Algorithm Steps|## Steps|## How It Works)\s*\n\n(.+?)(?:\n\n##|\Z)',
            content, re.DOTALL
        )
        if steps_match:
            steps_text = steps_match.group(1)
            # Extract numbered or bulleted steps
            steps = re.findall(r'(?:^\d+\.|^[-*])\s*(.+?)(?:\n|$)', steps_text, re.MULTILINE)
            info['steps'] = [step.strip() for step in steps[:10]]
        
    except Exception as e:
        pass
    
    return info


def extract_code_info(algorithm_path: Path) -> Dict[str, str]:
    """Extract information from algorithm code."""
    info = {}
    
    # Try Python first
    py_file = algorithm_path / "algorithm.py"
    if py_file.exists():
        try:
            content = py_file.read_text(encoding='utf-8')
            
            # Extract class or function docstring
            docstring_match = re.search(
                r'"""(.*?)"""',
                content, re.DOTALL
            )
            if docstring_match:
                doc = docstring_match.group(1).strip()
                info['code_description'] = doc[:300]
            
            # Extract main function logic
            main_match = re.search(
                r'def main[^{]*\{([^}]+)\}',
                content, re.DOTALL
            )
            if main_match:
                main_body = main_match.group(1)
                # Look for example data
                example_match = re.search(r'\[([^\]]+)\]', main_body)
                if example_match:
                    info['example_data'] = example_match.group(1)
        
        except:
            pass
    
    # Try Java
    java_file = algorithm_path / "Algorithm.java"
    if java_file.exists():
        try:
            content = java_file.read_text(encoding='utf-8')
            
            # Extract class comment
            comment_match = re.search(
                r'/\*\*(.*?)\*/',
                content, re.DOTALL
            )
            if comment_match:
                comment = comment_match.group(1).strip()
                info['code_description'] = comment[:300]
        
        except:
            pass
    
    return info


def get_algorithm_name(folder_path: Path) -> Tuple[str, str]:
    """Extract algorithm name in English and Russian."""
    # Try to get from metadata.json
    metadata_file = folder_path / "metadata.json"
    english_name = None
    if metadata_file.exists():
        try:
            metadata = json.loads(metadata_file.read_text(encoding='utf-8'))
            if 'name' in metadata:
                english_name = metadata['name']
            elif 'display_name' in metadata:
                english_name = metadata['display_name']
        except:
            pass
    
    # Try to get from README.md
    if not english_name:
        readme_file = folder_path / "README.md"
        if readme_file.exists():
            try:
                content = readme_file.read_text(encoding='utf-8')
                first_line = content.split('\n')[0].strip()
                if first_line.startswith('#'):
                    english_name = first_line.lstrip('#').strip()
            except:
                pass
    
    # Fallback: convert folder name
    if not english_name:
        folder_name = folder_path.name
        english_name = folder_name.replace('_', ' ').title()
    
    # Translate to Russian
    translations = {
        'bubble sort': 'Пузырьковая сортировка',
        'insertion sort': 'Сортировка вставками',
        'selection sort': 'Сортировка выбором',
        'merge sort': 'Сортировка слиянием',
        'quick sort': 'Быстрая сортировка',
        'heap sort': 'Сортировка кучей',
        'binary search': 'Бинарный поиск',
        'linear search': 'Линейный поиск',
        'binary tree': 'Бинарное дерево',
        'hash table': 'Хеш-таблица',
        'data monitoring': 'Мониторинг данных',
        'data quality': 'Качество данных',
        'graph traversal': 'Обход графа',
        'depth first search': 'Поиск в глубину',
        'breadth first search': 'Поиск в ширину',
    }
    
    # Try exact match first
    russian_name = translations.get(english_name.lower(), None)
    
    # If not found, try partial matches
    if not russian_name:
        for key, value in translations.items():
            if key in english_name.lower() or english_name.lower() in key:
                russian_name = value
                break
    
    # If still not found, convert to readable Russian
    if not russian_name:
        # Convert snake_case or Title Case to readable Russian
        words = re.split(r'[_\s]+', english_name)
        # Simple translation of common words with proper Russian word order
        word_translations = {
            'data': 'данных',
            'monitoring': 'мониторинг',
            'quality': 'качество',
            'search': 'поиск',
            'sort': 'сортировка',
            'tree': 'дерево',
            'graph': 'граф',
            'algorithm': 'алгоритм',
        }
        
        # Special handling for common patterns
        lower_name = english_name.lower()
        if 'data monitoring' in lower_name or 'monitoring' in lower_name and 'data' in lower_name:
            russian_name = 'Мониторинг данных'
        elif 'data quality' in lower_name or 'quality' in lower_name and 'data' in lower_name:
            russian_name = 'Качество данных'
        else:
            translated_words = []
            for word in words:
                lower_word = word.lower()
                if lower_word in word_translations:
                    translated_words.append(word_translations[lower_word])
                else:
                    translated_words.append(word)
            russian_name = ' '.join(translated_words).title()
    
    return english_name, russian_name


def generate_specific_explanation(english_name: str, russian_name: str, 
                                  folder_path: Path, readme_info: Dict,
                                  code_info: Dict) -> str:
    """Generate algorithm-specific explanation."""
    
    # Build explanation from available information
    explanation_parts = []
    
    # Use short description if available and meaningful
    if 'short_description' in readme_info and len(readme_info['short_description']) > 20:
        desc = readme_info['short_description']
        # Clean up
        desc = re.sub(r'\*\*([^*]+)\*\*', r'\1', desc)
        desc = re.sub(r'`([^`]+)`', r'\1', desc)
        if not desc.startswith('*') and not desc.startswith('Data Monitoring implementation'):
            explanation_parts.append(desc[:300])
    
    # Use description if available
    if 'description' in readme_info and len(readme_info['description']) > 20:
        desc = readme_info['description']
        # Clean up
        desc = re.sub(r'\*\*([^*]+)\*\*', r'\1', desc)
        desc = re.sub(r'`([^`]+)`', r'\1', desc)
        # Take first sentence or first 200 chars
        first_sentence = desc.split('.')[0] if '.' in desc else desc[:200]
        if not first_sentence.startswith('*') and 'implementation' not in first_sentence.lower():
            explanation_parts.append(first_sentence)
    
    # Only use code description if it's meaningful
    if 'code_description' in code_info:
        desc = code_info['code_description']
        # Skip generic descriptions
        if desc and len(desc) > 30 and 'implementation' not in desc.lower()[:50]:
            desc = re.sub(r'Time Complexity.*', '', desc, flags=re.IGNORECASE)
            desc = re.sub(r'Space Complexity.*', '', desc, flags=re.IGNORECASE)
            desc = re.sub(r'\*\*([^*]+)\*\*', r'\1', desc)
            if not desc.strip().startswith('*'):
                explanation_parts.append(desc[:200])
    
    # If we have a good explanation, use it
    if explanation_parts:
        return ' '.join(explanation_parts) + '.'
    
    # Otherwise generate based on algorithm name
    if False:  # This will be handled below
        pass
    else:
        # Generate based on algorithm name
        if 'monitoring' in english_name.lower():
            explanation_parts.append(
                f"{russian_name} — это способ отслеживать состояние данных и "
                "обнаруживать проблемы. Алгоритм постоянно проверяет метрики "
                "(например, скорость обработки, количество ошибок) и предупреждает, "
                "если что-то идёт не так."
            )
        elif 'quality' in english_name.lower():
            explanation_parts.append(
                f"{russian_name} — это способ проверять, насколько хороши данные. "
                "Алгоритм анализирует данные и находит ошибки, пропуски или "
                "несоответствия, чтобы убедиться, что информация правильная."
            )
        elif 'sort' in english_name.lower():
            if 'bubble' in english_name.lower():
                explanation_parts.append(
                    f"{russian_name} работает как пузырьки в воде — более лёгкие "
                    "элементы 'всплывают' наверх. Алгоритм сравнивает соседние "
                    "элементы и меняет их местами, если они в неправильном порядке, "
                    "пока весь список не будет отсортирован."
                )
            elif 'quick' in english_name.lower():
                explanation_parts.append(
                    f"{russian_name} использует стратегию 'разделяй и властвуй'. "
                    "Алгоритм выбирает опорный элемент, разделяет список на части "
                    "(меньше и больше опорного) и рекурсивно сортирует каждую часть."
                )
            else:
                explanation_parts.append(
                    f"{russian_name} упорядочивает элементы списка по возрастанию "
                    "или убыванию, используя специальную стратегию сравнения и "
                    "перестановки элементов."
                )
        elif 'search' in english_name.lower():
            if 'binary' in english_name.lower():
                explanation_parts.append(
                    f"{russian_name} работает как поиск слова в словаре — мы открываем "
                    "середину, смотрим, нужно ли нам искать раньше или позже, и "
                    "продолжаем в нужной половине. Это очень быстро для упорядоченных списков."
                )
            else:
                explanation_parts.append(
                    f"{russian_name} просматривает элементы списка один за другим, "
                    "сравнивая каждый с искомым значением, пока не найдёт нужный элемент."
                )
        else:
            explanation_parts.append(
                f"{russian_name} — это алгоритм для решения конкретной задачи. "
                "Он выполняет последовательность шагов, чтобы получить нужный результат."
            )
    
    return ' '.join(explanation_parts)


def generate_specific_applications(english_name: str, russian_name: str,
                                   readme_info: Dict) -> list:
    """Generate algorithm-specific real-world applications."""
    
    if 'applications' in readme_info:
        return readme_info['applications']
    
    # Generate based on algorithm type
    apps = []
    
    if 'monitoring' in english_name.lower():
        apps = [
            "отслеживание работы серверов и приложений",
            "контроль качества данных в базе данных",
            "мониторинг производительности веб-сайта",
            "отслеживание ошибок в программах"
        ]
    elif 'quality' in english_name.lower():
        apps = [
            "проверка правильности данных в таблицах",
            "поиск ошибок в больших файлах",
            "валидация информации перед использованием",
            "контроль качества данных в системах"
        ]
    elif 'sort' in english_name.lower():
        apps = [
            "упорядочивание оценок в журнале",
            "сортировка товаров по цене в магазине",
            "организация списка друзей по алфавиту",
            "упорядочивание файлов по дате"
        ]
    elif 'search' in english_name.lower():
        apps = [
            "поиск ученика в списке класса",
            "поиск нужного файла в папке",
            "поиск слова в тексте",
            "поиск контакта в телефонной книге"
        ]
    elif 'tree' in english_name.lower():
        apps = [
            "организация файлов и папок на компьютере",
            "структура меню в программах",
            "организация категорий товаров",
            "построение генеалогического дерева"
        ]
    else:
        apps = [
            "решение практических задач в программировании",
            "оптимизация работы приложений",
            "обработка данных",
            "автоматизация процессов"
        ]
    
    return apps[:4]


def generate_specific_example(english_name: str, russian_name: str,
                             folder_path: Path, readme_info: Dict,
                             code_info: Dict) -> str:
    """Generate algorithm-specific example."""
    
    if 'monitoring' in english_name.lower():
        return """Представим, что мы следим за температурой сервера:

Шаг 1: Устанавливаем порог — если температура выше 80°C, это проблема
Шаг 2: Каждую минуту проверяем текущую температуру
Шаг 3: Если температура 75°C → всё нормально, продолжаем
Шаг 4: Если температура 85°C → отправляем предупреждение администратору
Шаг 5: Продолжаем мониторинг

Так алгоритм помогает вовремя обнаружить перегрев и предотвратить поломку.

"""
    elif 'quality' in english_name.lower():
        return """Проверяем список учеников в классе:

Исходные данные: ["Иван", "", "Мария", "null", "Пётр"]

Шаг 1: Проверяем каждый элемент
Шаг 2: Находим пустую строку "" → ошибка качества
Шаг 3: Находим "null" → ошибка качества
Шаг 4: Составляем отчёт: найдено 2 проблемы

Алгоритм помог найти и исправить ошибки в данных.

"""
    elif 'bubble' in english_name.lower():
        return """Нужно отсортировать числа: 5, 2, 8, 1, 9

Проход 1:
Сравниваем 5 и 2 → 5 > 2, меняем → [2, 5, 8, 1, 9]
Сравниваем 5 и 8 → 5 < 8, не меняем → [2, 5, 8, 1, 9]
Сравниваем 8 и 1 → 8 > 1, меняем → [2, 5, 1, 8, 9]
Сравниваем 8 и 9 → 8 < 9, не меняем → [2, 5, 1, 8, 9]

Проход 2:
Сравниваем 2 и 5 → 2 < 5, не меняем → [2, 5, 1, 8, 9]
Сравниваем 5 и 1 → 5 > 1, меняем → [2, 1, 5, 8, 9]

Продолжаем, пока не получим: [1, 2, 5, 8, 9]

"""
    elif 'binary' in english_name.lower() and 'search' in english_name.lower():
        return """Ищем число 7 в упорядоченном списке: [1, 3, 5, 7, 9, 11, 13]

Шаг 1: Смотрим середину → индекс 3, значение 7 → найдено!

Если бы искали 5:
Шаг 1: Середина → 7, ищем слева → [1, 3, 5]
Шаг 2: Середина левой части → 3, ищем справа → [5]
Шаг 3: Находим 5

Бинарный поиск очень быстрый — за 3 шага нашли элемент в списке из 7 чисел!

"""
    elif 'linear_search' in english_name.lower():
        return """Ищем число 25 в списке: [10, 7, 25, 3]

Шаг 1: Смотрим первый элемент → 10, не то
Шаг 2: Смотрим второй элемент → 7, не то
Шаг 3: Смотрим третий элемент → 25, найдено!
Останавливаемся.

Алгоритм проверил 3 элемента и нашёл нужный.

"""
    else:
        # Try to extract from code or generate generic
        if 'example_data' in code_info:
            return f"""Пример работы алгоритма:

Исходные данные: {code_info['example_data']}

Алгоритм обрабатывает данные по шагам и получает результат.
Подробности можно увидеть, запустив программу.

"""
        else:
            return f"""Рассмотрим пример работы {russian_name.lower()}:

1. Подготовка: получаем входные данные
2. Обработка: применяем алгоритм
3. Результат: получаем ответ

Алгоритм работает последовательно, выполняя необходимые операции.

"""


def generate_russian_content(algorithm_name: str, folder_name: str, 
                           category: str, folder_path: Path) -> str:
    """Generate Russian educational content for the algorithm."""
    
    # Get names
    english_name, russian_name = get_algorithm_name(folder_path)
    
    # Extract information
    readme_info = extract_readme_info(folder_path / "README.md")
    code_info = extract_code_info(folder_path)
    
    # Generate content
    content = f"""# {russian_name}

## Простое объяснение

{generate_specific_explanation(english_name, russian_name, folder_path, readme_info, code_info)}

## Где применяется

"""
    
    # Add applications
    applications = generate_specific_applications(english_name, russian_name, readme_info)
    for app in applications:
        content += f"- {app};\n"
    content += "\n"
    
    # Add example
    content += "## Пример\n\n"
    content += generate_specific_example(english_name, russian_name, folder_path, readme_info, code_info)
    
    # Add questions (keep existing structure but make them more specific)
    content += """## Вопросы для самопроверки

### Базовые

"""
    
    if 'monitoring' in english_name.lower():
        content += """1. Что делает алгоритм мониторинга данных?
2. Зачем нужно отслеживать метрики?
3. Что происходит, когда значение превышает порог?

"""
    elif 'quality' in english_name.lower():
        content += """1. Что проверяет алгоритм качества данных?
2. Какие ошибки он может найти?
3. Почему важно проверять данные перед использованием?

"""
    elif 'sort' in english_name.lower():
        content += """1. Что делает алгоритм сортировки?
2. В каких случаях нужна сортировка?
3. Сколько элементов можно отсортировать этим способом?

"""
    elif 'search' in english_name.lower():
        content += """1. Что делает алгоритм поиска?
2. В каких случаях он подходит?
3. Что происходит, если элемент не найден?

"""
    else:
        content += f"""1. Что делает алгоритм {russian_name.lower()}?
2. В каких ситуациях его используют?
3. Какие данные нужны для работы алгоритма?

"""
    
    content += """### Средние

"""
    
    if 'monitoring' in english_name.lower():
        content += """4. Как алгоритм определяет, что что-то не так?
5. Что делать, если получено предупреждение?
6. Можно ли настроить разные пороги для разных метрик?

"""
    elif 'quality' in english_name.lower():
        content += """4. Как алгоритм обрабатывает разные типы ошибок?
5. Можно ли автоматически исправлять найденные проблемы?
6. Как часто нужно проверять качество данных?

"""
    elif 'sort' in english_name.lower():
        content += """4. Как работает алгоритм, если элементы уже отсортированы?
5. Почему некоторые алгоритмы сортировки быстрее других?
6. Сколько сравнений нужно для сортировки n элементов?

"""
    elif 'search' in english_name.lower():
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
    
    if 'monitoring' in english_name.lower():
        content += """7. Как обрабатывать большое количество метрик одновременно?
8. Что делать, если система отправляет слишком много предупреждений?
9. Как оптимизировать мониторинг для экономии ресурсов?

"""
    elif 'quality' in english_name.lower():
        content += """7. Как алгоритм работает с очень большими объёмами данных?
8. Можно ли использовать машинное обучение для улучшения проверки?
9. Как создать правила проверки для специфических типов данных?

"""
    elif 'sort' in english_name.lower():
        content += """7. Что изменится, если список очень большой?
8. Как оценить эффективность алгоритма?
9. Можно ли отсортировать данные за один проход?

"""
    elif 'search' in english_name.lower():
        content += """7. Что изменится, если список упорядочен?
8. Как улучшить время поиска?
9. Как работает поиск в неупорядоченном списке?

"""
    else:
        content += """7. Как алгоритм работает с большими объёмами данных?
8. Какая сложность у этого алгоритма?
9. Как можно оптимизировать алгоритм?

"""
    
    # Add practical tasks (make them more specific)
    content += """## Практические задания

### Уровень 1 (Лёгкий)

"""
    
    if 'monitoring' in english_name.lower():
        content += """Создай простую систему мониторинга температуры: если температура выше 25°C, выводи предупреждение. Используй список температур: [20, 22, 26, 24, 28].

"""
    elif 'quality' in english_name.lower():
        content += """Проверь список имён на пустые значения: ["Иван", "", "Мария", "Пётр", ""]. Найди все ошибки.

"""
    elif 'sort' in english_name.lower():
        content += """Отсортируй список фруктов по алфавиту: ["яблоко", "банан", "апельсин", "груша"].

"""
    elif 'search' in english_name.lower():
        content += """Найди слово "яблоко" в списке фруктов: ["банан", "яблоко", "апельсин", "груша"].

"""
    else:
        content += f"""Выполни простую операцию с алгоритмом {russian_name.lower()}. Используй небольшой набор данных (3-5 элементов).

"""
    
    content += """### Уровень 2 (Средний)

"""
    
    if 'monitoring' in english_name.lower():
        content += """Создай систему мониторинга с несколькими метриками (температура, память, скорость). Установи разные пороги для каждой метрики и отслеживай нарушения.

"""
    elif 'quality' in english_name.lower():
        content += """Проверь большой список данных на несколько типов ошибок: пустые значения, неправильный формат, дубликаты. Составь отчёт о найденных проблемах.

"""
    elif 'sort' in english_name.lower():
        content += """Определи, сколько шагов сделает алгоритм при сортировке списка из 10 элементов. Отсортируй список чисел: [64, 34, 25, 12, 22, 11, 90, 5, 77, 1].

"""
    elif 'search' in english_name.lower():
        content += """Определи, сколько шагов сделает алгоритм при поиске числа 18 в списке из 20 элементов. Найди все вхождения числа 5 в списке: [1, 5, 3, 5, 7, 5, 9, 2, 5, 4].

"""
    else:
        content += f"""Примени алгоритм {russian_name.lower()} к более сложному набору данных. Проанализируй результат и объясни, как работает алгоритм.

"""
    
    content += """### Уровень 3 (Продвинутый)

"""
    
    if 'monitoring' in english_name.lower():
        content += """Напиши полноценную систему мониторинга на языке программирования. Добавь возможность настройки порогов, хранение истории метрик и отправку уведомлений при проблемах.

"""
    elif 'quality' in english_name.lower():
        content += """Создай систему проверки качества данных с правилами валидации. Добавь автоматическое исправление простых ошибок и генерацию подробных отчётов.

"""
    elif 'sort' in english_name.lower():
        content += """Напиши простую программу сортировки на любом языке программирования, которая выводит каждый шаг процесса сортировки. Сравни время работы с разными размерами списков.

"""
    elif 'search' in english_name.lower():
        content += """Напиши простой алгоритм поиска на любом языке программирования, который выводит номер найденного элемента и количество выполненных сравнений. Реализуй поиск для упорядоченного и неупорядоченного списка.

"""
    else:
        content += f"""Напиши реализацию алгоритма {russian_name.lower()} на языке программирования. Добавь обработку ошибок и проверку входных данных. Протестируй алгоритм на разных наборах данных.

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
        # Check if this is an algorithm folder
        has_java = (folder_path / "Algorithm.java").exists()
        has_python = (folder_path / "algorithm.py").exists()
        
        if not (has_java or has_python):
            return False
        
        # Get algorithm information
        algorithm_name = get_algorithm_name(folder_path)[1]  # Russian name
        category = get_algorithm_category(folder_path)
        folder_name = folder_path.name
        
        # Generate content
        content = generate_russian_content(algorithm_name, folder_name, category, folder_path)
        
        # Write file
        school_file = folder_path / "school.ru.md"
        school_file.write_text(content, encoding='utf-8')
        return True
        
    except Exception as e:
        print(f"  [ERROR] Failed to process {folder_path}: {e}")
        return False


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


def main():
    """Main function to generate school.ru.md for all algorithm folders."""
    print("=" * 70)
    print("ГЕНЕРАЦИЯ ФАЙЛОВ school.ru.md (УЛУЧШЕННАЯ ВЕРСИЯ)")
    print("=" * 70)
    print()
    
    # Find all algorithm folders
    algorithm_folders = []
    
    for java_file in ROOT.rglob("Algorithm.java"):
        folder = java_file.parent
        if folder not in algorithm_folders:
            algorithm_folders.append(folder)
    
    for py_file in ROOT.rglob("algorithm.py"):
        folder = py_file.parent
        if folder not in algorithm_folders:
            algorithm_folders.append(folder)
    
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

