#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Improve all sections in school.ru.md files with specific examples, questions, and tasks.
Remove ethical notes from non-AI/ML algorithms.
"""

import json
import re
import sys
import io
import time
from pathlib import Path
from typing import Dict, List, Optional
import urllib.request
from urllib.error import URLError, HTTPError

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parents[1]


def is_ai_ml_algorithm(english_name: str, folder_path: Path) -> bool:
    """Check if algorithm is AI/ML related."""
    lower_name = english_name.lower()
    
    ai_ml_keywords = [
        'machine learning', 'ml', 'neural', 'deep learning', 'ai', 'artificial intelligence',
        'reinforcement', 'supervised', 'unsupervised', 'classification', 'regression',
        'clustering', 'recommendation', 'natural language', 'nlp', 'computer vision',
        'pattern recognition', 'prediction', 'model', 'training', 'inference'
    ]
    
    for keyword in ai_ml_keywords:
        if keyword in lower_name:
            return True
    
    # Check metadata
    metadata_file = folder_path / "metadata.json"
    if metadata_file.exists():
        try:
            metadata = json.loads(metadata_file.read_text(encoding='utf-8'))
            category = metadata.get('category', '').lower()
            algo_type = metadata.get('algorithm_type', '').lower()
            if any(keyword in category or keyword in algo_type for keyword in ai_ml_keywords):
                return True
        except:
            pass
    
    return False


def get_specific_example(english_name: str, russian_name: str, folder_path: Path) -> str:
    """Generate specific example for the algorithm."""
    lower_name = english_name.lower()
    
    # Batch processing
    if 'batch' in lower_name and 'process' in lower_name:
        return """Представим, что банк обрабатывает миллионы транзакций за день:

Исходные данные: 5 миллионов транзакций

Шаг 1: Разделяем на батчи по 10,000 транзакций → 500 батчей
Шаг 2: Обрабатываем батч 1: проверяем балансы, обновляем счета
Шаг 3: Обрабатываем батч 2: проверяем балансы, обновляем счета
...
Шаг 4: После обработки всех батчей формируем итоговый отчёт

Преимущество: вместо обработки 5 миллионов записей по одной (очень медленно), 
обрабатываем порциями (быстро и эффективно).

"""
    
    # Data monitoring
    elif 'monitoring' in lower_name:
        return """Мониторим температуру сервера каждую минуту:

Установлен порог: 80°C

Минута 1: Температура 65°C → норма, продолжаем
Минута 2: Температура 68°C → норма, продолжаем
Минута 3: Температура 75°C → норма, но близко к порогу
Минута 4: Температура 82°C → превышен порог! Отправляем предупреждение администратору
Минута 5: Администратор принял меры, температура 70°C → норма

Алгоритм помог вовремя обнаружить проблему и предотвратить перегрев.

"""
    
    # Data quality
    elif 'quality' in lower_name and 'data' in lower_name:
        return """Проверяем список учеников в классе:

Исходные данные: ["Иван Петров", "", "Мария Сидорова", "null", "Пётр Иванов", "Анна"]

Шаг 1: Проверяем каждый элемент
Шаг 2: "Иван Петров" → корректно
Шаг 3: "" → ошибка: пустая строка
Шаг 4: "Мария Сидорова" → корректно
Шаг 5: "null" → ошибка: недопустимое значение
Шаг 6: "Пётр Иванов" → корректно
Шаг 7: "Анна" → предупреждение: неполное имя

Результат: найдено 2 ошибки, 1 предупреждение. Данные требуют исправления.

"""
    
    # Bubble sort
    elif 'bubble' in lower_name and 'sort' in lower_name:
        return """Сортируем оценки учеников: [5, 2, 4, 1, 3]

Проход 1:
Сравниваем 5 и 2 → 5 > 2, меняем → [2, 5, 4, 1, 3]
Сравниваем 5 и 4 → 5 > 4, меняем → [2, 4, 5, 1, 3]
Сравниваем 5 и 1 → 5 > 1, меняем → [2, 4, 1, 5, 3]
Сравниваем 5 и 3 → 5 > 3, меняем → [2, 4, 1, 3, 5]

Проход 2:
Сравниваем 2 и 4 → 2 < 4, не меняем → [2, 4, 1, 3, 5]
Сравниваем 4 и 1 → 4 > 1, меняем → [2, 1, 4, 3, 5]
Сравниваем 4 и 3 → 4 > 3, меняем → [2, 1, 3, 4, 5]

Проход 3:
Сравниваем 2 и 1 → 2 > 1, меняем → [1, 2, 3, 4, 5]
Сравниваем 2 и 3 → 2 < 3, не меняем → [1, 2, 3, 4, 5]

Результат: [1, 2, 3, 4, 5] — все оценки отсортированы по возрастанию!

"""
    
    # Binary search
    elif 'binary' in lower_name and 'search' in lower_name:
        return """Ищем оценку "4" в отсортированном списке: [1, 2, 3, 4, 5, 6, 7]

Шаг 1: Смотрим середину → индекс 3, значение 4 → найдено!

Если бы искали "2":
Шаг 1: Середина → индекс 3, значение 4, ищем слева → [1, 2, 3]
Шаг 2: Середина левой части → индекс 1, значение 2 → найдено!

Если бы искали "6":
Шаг 1: Середина → индекс 3, значение 4, ищем справа → [5, 6, 7]
Шаг 2: Середина правой части → индекс 1, значение 6 → найдено!

Бинарный поиск очень эффективен: за 1-2 шага находит элемент в списке из 7 чисел!

"""
    
    # Quick sort
    elif 'quick' in lower_name and 'sort' in lower_name:
        return """Сортируем список: [64, 34, 25, 12, 22, 11, 90]

Шаг 1: Выбираем опорный элемент (pivot) → 64
Шаг 2: Разделяем: меньше 64 → [34, 25, 12, 22, 11], больше 64 → [90]
Шаг 3: Рекурсивно сортируем левую часть [34, 25, 12, 22, 11]
  - Pivot: 34
  - Меньше: [25, 12, 22, 11], Больше: []
  - Сортируем [25, 12, 22, 11] → [11, 12, 22, 25]
Шаг 4: Объединяем: [11, 12, 22, 25, 34] + [64] + [90]

Результат: [11, 12, 22, 25, 34, 64, 90]

"""
    
    # Hash table
    elif 'hash' in lower_name:
        return """Храним контакты в телефонной книге:

Имя: "Иван" → хеш-функция → индекс 5 → храним номер "123-456"
Имя: "Мария" → хеш-функция → индекс 2 → храним номер "789-012"
Имя: "Пётр" → хеш-функция → индекс 5 → коллизия! Используем цепочку

Поиск "Иван":
Шаг 1: Хеш "Иван" → индекс 5
Шаг 2: Проверяем элемент по индексу 5 → найдено "Иван" с номером "123-456"

Поиск очень быстрый — O(1) в среднем случае!

"""
    
    # Graph traversal (DFS/BFS)
    elif 'graph' in lower_name and ('traversal' in lower_name or 'dfs' in lower_name or 'bfs' in lower_name):
        if 'dfs' in lower_name or 'depth' in lower_name:
            return """Обходим граф друзей в социальной сети:

Граф: Иван → [Мария, Пётр], Мария → [Анна], Пётр → [Анна]

DFS (в глубину):
Шаг 1: Начинаем с "Иван"
Шаг 2: Идём к "Мария" (первый друг)
Шаг 3: От "Мария" идём к "Анна"
Шаг 4: Возвращаемся к "Иван", идём к "Пётр"
Шаг 5: От "Пётр" идём к "Анна" (уже посещена, пропускаем)

Порядок обхода: Иван → Мария → Анна → Пётр

"""
        else:
            return """Обходим граф друзей в социальной сети:

Граф: Иван → [Мария, Пётр], Мария → [Анна], Пётр → [Анна]

BFS (в ширину):
Шаг 1: Начинаем с "Иван" (уровень 0)
Шаг 2: Посещаем всех друзей "Иван": "Мария", "Пётр" (уровень 1)
Шаг 3: Посещаем друзей "Мария" и "Пётр": "Анна" (уровень 2)

Порядок обхода: Иван → Мария, Пётр → Анна

"""
    
    # Default - try to make it more specific
    else:
        return f"""Рассмотрим конкретный пример работы {russian_name.lower()}:

1. Подготовка данных: [конкретные входные данные]
2. Применение алгоритма: [конкретные шаги]
3. Получение результата: [конкретный результат]

Алгоритм выполняет операции последовательно, обрабатывая данные по определённым правилам.

"""


def get_specific_questions(english_name: str, russian_name: str) -> Dict[str, List[str]]:
    """Generate algorithm-specific questions."""
    lower_name = english_name.lower()
    
    questions = {
        'basic': [],
        'medium': [],
        'advanced': []
    }
    
    # Batch processing
    if 'batch' in lower_name and 'process' in lower_name:
        questions['basic'] = [
            "Что такое батч (порция) в обработке данных?",
            "Почему батч-обработка быстрее обработки по одному элементу?",
            "В каких случаях лучше использовать батч-обработку?"
        ]
        questions['medium'] = [
            "Как определить оптимальный размер батча?",
            "Что происходит, если один элемент в батче обрабатывается с ошибкой?",
            "Можно ли обрабатывать батчи параллельно?"
        ]
        questions['advanced'] = [
            "Как обрабатывать батчи разного размера?",
            "Как обеспечить надёжность при обработке больших батчей?",
            "Как оптимизировать батч-обработку для экономии памяти?"
        ]
    
    # Data monitoring
    elif 'monitoring' in lower_name:
        questions['basic'] = [
            "Что такое метрика в мониторинге данных?",
            "Зачем нужны пороги (thresholds) в мониторинге?",
            "Что происходит, когда метрика превышает порог?"
        ]
        questions['medium'] = [
            "Как выбрать правильные пороги для разных метрик?",
            "Что делать, если система отправляет слишком много предупреждений?",
            "Как обрабатывать временные всплески метрик?"
        ]
        questions['advanced'] = [
            "Как обрабатывать тысячи метрик одновременно?",
            "Как использовать машинное обучение для определения аномалий?",
            "Как создать систему автоматического реагирования на проблемы?"
        ]
    
    # Sorting
    elif 'sort' in lower_name:
        if 'bubble' in lower_name:
            questions['basic'] = [
                "Почему алгоритм называется 'пузырьковой' сортировкой?",
                "Сколько проходов нужно для сортировки n элементов?",
                "В каком случае пузырьковая сортировка работает быстрее всего?"
            ]
            questions['medium'] = [
                "Почему пузырьковая сортировка медленная для больших списков?",
                "Можно ли оптимизировать пузырьковую сортировку?",
                "Когда имеет смысл использовать пузырьковую сортировку?"
            ]
            questions['advanced'] = [
                "Какова временная сложность пузырьковой сортировки?",
                "Является ли пузырьковая сортировка стабильной?",
                "Как сравнить эффективность разных алгоритмов сортировки?"
            ]
        else:
            questions['basic'] = [
                "Что делает алгоритм сортировки?",
                "В каких случаях нужна сортировка данных?",
                "Можно ли отсортировать список за один проход?"
            ]
            questions['medium'] = [
                "Как работает алгоритм, если элементы уже отсортированы?",
                "Почему некоторые алгоритмы сортировки быстрее других?",
                "Что такое стабильная сортировка?"
            ]
            questions['advanced'] = [
                "Какова временная сложность этого алгоритма сортировки?",
                "Как алгоритм работает с очень большими списками?",
                "Можно ли отсортировать данные параллельно?"
            ]
    
    # Search
    elif 'search' in lower_name:
        if 'binary' in lower_name:
            questions['basic'] = [
                "Почему бинарный поиск работает только с отсортированными списками?",
                "Сколько шагов нужно для поиска в списке из 1000 элементов?",
                "Что происходит, если искомый элемент отсутствует?"
            ]
            questions['medium'] = [
                "Почему бинарный поиск быстрее линейного?",
                "Как найти первое или последнее вхождение элемента?",
                "Можно ли использовать бинарный поиск для нечисловых данных?"
            ]
            questions['advanced'] = [
                "Какова временная сложность бинарного поиска?",
                "Как работает бинарный поиск в многомерных массивах?",
                "Как оптимизировать бинарный поиск для очень больших данных?"
            ]
        else:
            questions['basic'] = [
                "Как работает алгоритм поиска?",
                "Сколько элементов нужно проверить в худшем случае?",
                "Что происходит, если элемент не найден?"
            ]
            questions['medium'] = [
                "Можно ли ускорить линейный поиск?",
                "Как работает поиск в неупорядоченном списке?",
                "Когда линейный поиск предпочтительнее бинарного?"
            ]
            questions['advanced'] = [
                "Какова временная сложность линейного поиска?",
                "Как организовать поиск в очень больших данных?",
                "Можно ли распараллелить поиск?"
            ]
    
    # Default
    else:
        questions['basic'] = [
            f"Что делает алгоритм {russian_name.lower()}?",
            f"В каких ситуациях используется {russian_name.lower()}?",
            f"Какие данные нужны для работы алгоритма?"
        ]
        questions['medium'] = [
            f"Как {russian_name.lower()} обрабатывает граничные случаи?",
            f"Какие преимущества и недостатки у {russian_name.lower()}?",
            f"Можно ли улучшить работу {russian_name.lower()}?"
        ]
        questions['advanced'] = [
            f"Какова временная сложность {russian_name.lower()}?",
            f"Как {russian_name.lower()} работает с большими объёмами данных?",
            f"Как можно оптимизировать {russian_name.lower()}?"
        ]
    
    return questions


def get_specific_tasks(english_name: str, russian_name: str) -> Dict[str, str]:
    """Generate algorithm-specific practical tasks."""
    lower_name = english_name.lower()
    
    tasks = {}
    
    # Batch processing
    if 'batch' in lower_name and 'process' in lower_name:
        tasks['level1'] = """Обработай список из 10 чисел порциями по 3 элемента. 
Найди сумму каждого батча и выведи результаты."""
        tasks['level2'] = """Создай систему батч-обработки для списка из 1000 транзакций. 
Раздели на батчи по 50 транзакций, обработай каждый батч (например, проверь баланс), 
и собери итоговую статистику."""
        tasks['level3'] = """Реализуй полноценную систему батч-обработки на языке программирования. 
Добавь обработку ошибок, логирование, возможность настройки размера батча и 
обработку батчей разного размера."""
    
    # Data monitoring
    elif 'monitoring' in lower_name:
        tasks['level1'] = """Создай простой мониторинг температуры: если температура выше 25°C, 
выводи предупреждение. Используй список температур: [20, 22, 26, 24, 28, 30]."""
        tasks['level2'] = """Создай систему мониторинга с несколькими метриками (температура, память, скорость). 
Установи разные пороги для каждой метрики, отслеживай нарушения и веди журнал событий."""
        tasks['level3'] = """Реализуй полноценную систему мониторинга с возможностью настройки порогов, 
хранением истории метрик, отправкой уведомлений и визуализацией данных на графиках."""
    
    # Bubble sort
    elif 'bubble' in lower_name and 'sort' in lower_name:
        tasks['level1'] = """Отсортируй список фруктов по алфавиту: ["яблоко", "банан", "апельсин", "груша"]. 
Выведи каждый шаг сортировки."""
        tasks['level2'] = """Отсортируй список из 10 чисел: [64, 34, 25, 12, 22, 11, 90, 5, 77, 1]. 
Подсчитай количество сравнений и перестановок."""
        tasks['level3'] = """Напиши программу пузырьковой сортировки, которая выводит каждый шаг процесса. 
Сравни время работы с разными размерами списков (10, 100, 1000 элементов) и 
визуализируй результаты на графике."""
    
    # Binary search
    elif 'binary' in lower_name and 'search' in lower_name:
        tasks['level1'] = """Найди число 7 в отсортированном списке: [1, 3, 5, 7, 9, 11, 13]. 
Выведи каждый шаг поиска."""
        tasks['level2'] = """Найди все вхождения числа 5 в отсортированном списке: [1, 3, 5, 5, 5, 7, 9]. 
Определи первое и последнее вхождение."""
        tasks['level3'] = """Реализуй бинарный поиск с подсчётом сравнений. Сравни время работы 
с линейным поиском на списках разного размера (100, 1000, 10000 элементов) и 
построй график сравнения."""
    
    # Default
    else:
        tasks['level1'] = f"""Выполни простую операцию с алгоритмом {russian_name.lower()}. 
Используй небольшой набор данных (3-5 элементов) и выведи результат."""
        tasks['level2'] = f"""Примени алгоритм {russian_name.lower()} к более сложному набору данных. 
Проанализируй результат, объясни каждый шаг работы алгоритма."""
        tasks['level3'] = f"""Напиши реализацию алгоритма {russian_name.lower()} на языке программирования. 
Добавь обработку ошибок, проверку входных данных, тесты и документацию."""
    
    return tasks


def improve_school_file(school_file: Path, folder_path: Path) -> bool:
    """Improve all sections in a school.ru.md file."""
    try:
        content = school_file.read_text(encoding='utf-8')
        
        # Extract algorithm names
        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        if not title_match:
            return False
        
        russian_name = title_match.group(1).strip()
        
        # Get English name
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
        
        # Check if AI/ML
        is_ai_ml = is_ai_ml_algorithm(english_name, folder_path)
        
        # Get specific content
        example = get_specific_example(english_name, russian_name, folder_path)
        questions = get_specific_questions(english_name, russian_name)
        tasks = get_specific_tasks(english_name, russian_name)
        
        # Replace Example section
        example_pattern = r'(## Пример\s*\n\n)(.+?)(\n\n## )'
        example_match = re.search(example_pattern, content, re.DOTALL)
        if example_match:
            content = content[:example_match.start()] + example_match.group(1) + example + example_match.group(3) + content[example_match.end():]
        
        # Replace Questions section
        questions_pattern = r'(## Вопросы для самопроверки\s*\n\n### Базовые\s*\n\n)(.+?)(\n\n## |\n\n---|\Z)'
        questions_match = re.search(questions_pattern, content, re.DOTALL)
        if questions_match:
            new_questions = "## Вопросы для самопроверки\n\n### Базовые\n\n"
            for i, q in enumerate(questions['basic'], 1):
                new_questions += f"{i}. {q}\n"
            new_questions += "\n### Средние\n\n"
            for i, q in enumerate(questions['medium'], 1):
                new_questions += f"{i + len(questions['basic'])}. {q}\n"
            new_questions += "\n### Сложные\n\n"
            for i, q in enumerate(questions['advanced'], 1):
                new_questions += f"{i + len(questions['basic']) + len(questions['medium'])}. {q}\n"
            new_questions += "\n"
            
            # Replace from start of questions to before next section or end
            next_section_start = questions_match.end(2)
            content = content[:questions_match.start()] + new_questions + content[next_section_start:]
        
        # Replace or add Tasks section
        tasks_pattern = r'(## Практические задания\s*\n\n)(.+?)(?:\n\n---|\Z)'
        tasks_match = re.search(tasks_pattern, content, re.DOTALL)
        
        new_tasks = "## Практические задания\n\n### Уровень 1 (Лёгкий)\n\n"
        new_tasks += tasks['level1'] + "\n\n"
        new_tasks += "### Уровень 2 (Средний)\n\n"
        new_tasks += tasks['level2'] + "\n\n"
        new_tasks += "### Уровень 3 (Продвинутый)\n\n"
        new_tasks += tasks['level3'] + "\n\n"
        
        if tasks_match:
            # Replace existing section
            insert_pos = tasks_match.end(2)
            # Check what comes after
            if insert_pos < len(content):
                remaining = content[insert_pos:].lstrip()
                if remaining.startswith('\n\n---'):
                    content = content[:tasks_match.start()] + new_tasks + content[insert_pos:]
                elif remaining.startswith('\n\n##'):
                    content = content[:tasks_match.start()] + new_tasks + content[insert_pos:]
                else:
                    content = content[:tasks_match.start()] + new_tasks
            else:
                content = content[:tasks_match.start()] + new_tasks
        else:
            # Add new section after questions
            questions_end_pattern = r'(## Вопросы для самопроверки.+?### Сложные\s*\n\n\d+\..+?\n\n)'
            questions_end_match = re.search(questions_end_pattern, content, re.DOTALL)
            if questions_end_match:
                insert_pos = questions_end_match.end()
                content = content[:insert_pos] + '\n\n' + new_tasks + content[insert_pos:]
            else:
                # Add at the end
                content = content.rstrip() + '\n\n' + new_tasks
        
        # Remove or keep ethical note
        ethical_pattern = r'(\n\n---\s*\n\n\*\*Этическое замечание:\*\*\s*\n\n)(.+?)(?:\n\n|\Z)'
        ethical_match = re.search(ethical_pattern, content, re.DOTALL)
        
        if ethical_match:
            if not is_ai_ml:
                # Remove ethical note and the --- separator for non-AI/ML algorithms
                ethical_start = content.rfind('\n\n---', 0, ethical_match.start())
                if ethical_start != -1:
                    # Remove from --- to end of ethical note
                    content = content[:ethical_start] + content[ethical_match.end():]
                else:
                    # If no --- found, just remove the ethical note part
                    content = content[:ethical_match.start()] + content[ethical_match.end(2):]
        else:
            # No ethical note found
            if is_ai_ml:
                # Add ethical note for AI/ML algorithms
                ethical_note = """---

**Этическое замечание:**

Помни, что алгоритмы машинного обучения и искусственного интеллекта — это мощные инструменты, 
которые могут влиять на жизнь людей. Важно использовать их ответственно, учитывая этические 
принципы, справедливость, прозрачность и уважение к приватности. Всегда думай о последствиях 
своих решений и используй технологии для блага общества.

"""
                content = content.rstrip() + '\n\n' + ethical_note
        
        school_file.write_text(content, encoding='utf-8')
        return True
        
    except Exception as e:
        print(f"  [ERROR] {e}")
        return False


def main():
    """Main function to improve all school.ru.md files."""
    print("=" * 70)
    print("УЛУЧШЕНИЕ ВСЕХ РАЗДЕЛОВ В school.ru.md")
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
            print(f"  [OK] Файл улучшен")
            improved_count += 1
        else:
            print(f"  [SKIP] Не удалось улучшить")
            error_count += 1
        
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

