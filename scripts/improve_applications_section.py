#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Improve "Где применяется" section in school.ru.md files with concrete examples from internet sources.
"""

import json
import re
import sys
import io
import time
from pathlib import Path
from typing import Dict, List, Optional
import urllib.request
import urllib.parse
from urllib.error import URLError, HTTPError

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parents[1]


def get_wikipedia_applications(algorithm_name: str) -> List[str]:
    """Get real-world applications from Wikipedia."""
    applications = []
    
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
        }
        
        clean_name = algorithm_name.replace('_', ' ').strip()
        wiki_name = name_mappings.get(clean_name.lower())
        
        if not wiki_name:
            wiki_name = clean_name.title().replace(' ', '_')
        
        # Try to get full Wikipedia page
        variations = [
            wiki_name,
            clean_name.replace(' ', '_'),
            clean_name.replace(' ', '_').title(),
        ]
        
        for variation in variations:
            try:
                url = f"https://en.wikipedia.org/api/rest_v1/page/html/{variation}"
                with urllib.request.urlopen(url, timeout=5) as response:
                    html = response.read().decode('utf-8')
                    
                    # Look for "Applications" or "Uses" section
                    # Extract list items that might be applications
                    # This is a simplified extraction
                    if 'application' in html.lower() or 'use' in html.lower():
                        # Try to extract from summary first
                        summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{variation}"
                        with urllib.request.urlopen(summary_url, timeout=5) as summary_response:
                            summary_data = json.loads(summary_response.read().decode('utf-8'))
                            if 'extract' in summary_data:
                                extract = summary_data['extract']
                                # Look for application-related sentences
                                sentences = re.split(r'[.!?]+', extract)
                                for sentence in sentences:
                                    if any(word in sentence.lower() for word in ['use', 'application', 'applied', 'used in']):
                                        if len(sentence) > 20 and len(sentence) < 150:
                                            applications.append(sentence.strip())
                                            if len(applications) >= 3:
                                                break
                
                if applications:
                    break
            except (URLError, HTTPError, KeyError):
                continue
            except Exception:
                continue
        
    except Exception:
        pass
    
    return applications[:4]  # Return up to 4 applications


def get_specific_applications(english_name: str, russian_name: str, 
                             folder_path: Path) -> List[str]:
    """Get specific applications for an algorithm."""
    applications = []
    
    # Try Wikipedia first
    wiki_apps = get_wikipedia_applications(english_name)
    if wiki_apps:
        # Clean and translate
        for app in wiki_apps:
            app = re.sub(r'\[\d+\]', '', app)  # Remove citations
            app = app.strip()
            if app and len(app) > 15:
                # Simple translation of common terms
                app = app.replace('is used', 'используется')
                app = app.replace('used in', 'используется в')
                app = app.replace('for', 'для')
                applications.append(app)
    
    # If we have good applications, return them
    if len(applications) >= 3:
        return applications[:4]
    
    # Otherwise, generate based on algorithm type
    lower_name = english_name.lower()
    
    # Batch processing
    if 'batch' in lower_name and 'process' in lower_name:
        return [
            "обработка больших объёмов данных в банковских системах (обработка транзакций за день)",
            "генерация отчётов в корпоративных системах (ежедневные, еженедельные отчёты)",
            "обработка изображений и видео в социальных сетях (загрузка и обработка фотографий)",
            "анализ логов серверов (обработка миллионов записей за раз)"
        ]
    
    # Data monitoring
    elif 'monitoring' in lower_name:
        return [
            "отслеживание производительности веб-сайтов и приложений в реальном времени",
            "мониторинг состояния серверов и дата-центров (температура, нагрузка, память)",
            "контроль качества данных в базах данных (обнаружение ошибок и аномалий)",
            "отслеживание бизнес-метрик в аналитических системах (продажи, трафик, конверсии)"
        ]
    
    # Data quality
    elif 'quality' in lower_name and 'data' in lower_name:
        return [
            "проверка корректности данных перед загрузкой в базу данных",
            "обнаружение дубликатов и ошибок в больших таблицах",
            "валидация данных в формах и приложениях",
            "контроль качества данных в системах аналитики и отчётности"
        ]
    
    # Sorting algorithms
    elif 'sort' in lower_name:
        if 'bubble' in lower_name:
            return [
                "обучение программированию (простой пример для понимания сортировки)",
                "сортировка небольших списков в образовательных целях",
                "демонстрация базовых алгоритмов в учебниках"
            ]
        elif 'quick' in lower_name:
            return [
                "сортировка больших массивов данных в библиотеках программирования",
                "упорядочивание результатов поиска в поисковых системах",
                "сортировка товаров в интернет-магазинах (по цене, рейтингу, дате)",
                "организация файлов в файловых системах"
            ]
        elif 'merge' in lower_name:
            return [
                "сортировка больших файлов, которые не помещаются в память",
                "объединение отсортированных списков в базах данных",
                "сортировка в системах распределённой обработки данных",
                "упорядочивание данных в системах аналитики"
            ]
        else:
            return [
                "упорядочивание оценок в электронных журналах",
                "сортировка товаров по цене в интернет-магазинах",
                "организация списка контактов по алфавиту",
                "упорядочивание файлов по дате создания или размеру"
            ]
    
    # Search algorithms
    elif 'search' in lower_name:
        if 'binary' in lower_name:
            return [
                "поиск слова в словаре или энциклопедии",
                "поиск элемента в отсортированном массиве в программировании",
                "поиск записи в телефонной книге (если она отсортирована)",
                "поиск значения в отсортированных базах данных"
            ]
        else:
            return [
                "поиск ученика в списке класса",
                "поиск нужного файла в папке",
                "поиск слова в текстовом документе",
                "поиск контакта в списке телефонных номеров"
            ]
    
    # Graph algorithms
    elif 'graph' in lower_name:
        if 'traversal' in lower_name or 'dfs' in lower_name or 'bfs' in lower_name:
            return [
                "поиск пути в лабиринте или на карте",
                "анализ социальных сетей (поиск друзей, рекомендации)",
                "поиск кратчайшего пути в навигационных системах",
                "анализ связей между веб-страницами в поисковых системах"
            ]
        else:
            return [
                "анализ сетей и связей в социальных медиа",
                "оптимизация маршрутов в логистике и доставке",
                "поиск зависимостей в системах управления проектами",
                "анализ структуры веб-сайтов и интернет-связей"
            ]
    
    # Hash tables
    elif 'hash' in lower_name:
        return [
            "быстрый поиск контактов в телефонной книге по имени",
            "хранение паролей в безопасном виде (хеширование)",
            "индексация страниц в поисковых системах",
            "кэширование данных для ускорения работы приложений"
        ]
    
    # Trees
    elif 'tree' in lower_name:
        return [
            "организация файлов и папок на компьютере",
            "структура меню в программах и веб-сайтах",
            "организация категорий товаров в интернет-магазинах",
            "построение генеалогических деревьев и иерархий"
        ]
    
    # Stream processing
    elif 'stream' in lower_name and 'process' in lower_name:
        return [
            "обработка данных в реальном времени в финансовых системах (биржи, трейдинг)",
            "мониторинг событий в системах безопасности (обнаружение вторжений)",
            "обработка логов веб-серверов в реальном времени",
            "анализ данных с датчиков IoT (интернет вещей) устройств"
        ]
    
    # Machine learning
    elif 'machine learning' in lower_name or 'ml' in lower_name or 'neural' in lower_name:
        return [
            "распознавание изображений в приложениях (фото, медицинская диагностика)",
            "рекомендательные системы в интернет-магазинах и стриминговых сервисах",
            "обработка естественного языка (переводчики, чат-боты)",
            "предсказание и прогнозирование в различных областях (погода, финансы)"
        ]
    
    # Database
    elif 'database' in lower_name or 'index' in lower_name:
        return [
            "ускорение поиска данных в больших базах данных",
            "оптимизация запросов в системах управления базами данных",
            "организация хранения информации для быстрого доступа",
            "улучшение производительности веб-приложений"
        ]
    
    # Data engineering
    elif 'data engineering' in lower_name or 'pipeline' in lower_name:
        return [
            "автоматизация сбора данных из различных источников",
            "преобразование и очистка данных для аналитики",
            "загрузка данных в хранилища и базы данных",
            "создание инфраструктуры для работы с большими данными"
        ]
    
    # Default fallback
    else:
        return [
            "решение практических задач в программировании",
            "оптимизация работы приложений и систем",
            "обработка и анализ данных",
            "автоматизация процессов в различных областях"
        ]


def improve_applications_section(school_file: Path, folder_path: Path) -> bool:
    """Improve the applications section in a school.ru.md file."""
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
        
        # Get specific applications
        applications = get_specific_applications(english_name, russian_name, folder_path)
        
        # Build new applications section
        new_section = "## Где применяется\n\n"
        for app in applications:
            new_section += f"- {app};\n"
        new_section += "\n"
        
        # Replace the applications section
        applications_pattern = r'(## Где применяется\s*\n\n)(.+?)(\n\n## )'
        match = re.search(applications_pattern, content, re.DOTALL)
        
        if match:
            new_content = (
                content[:match.start()] +
                new_section +
                content[match.end(2):]
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
    print("УЛУЧШЕНИЕ РАЗДЕЛА 'ГДЕ ПРИМЕНЯЕТСЯ' В school.ru.md")
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
        
        if improve_applications_section(school_file, folder_path):
            print(f"  [OK] Раздел улучшен")
            improved_count += 1
        else:
            print(f"  [SKIP] Не удалось улучшить")
            error_count += 1
        
        # Rate limiting for web requests
        if idx % 10 == 0:
            time.sleep(1)
        
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

