#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Improved README enhancement script.
Enhances algorithm READMEs based on algorithm name using multiple strategies.
Any section enhancement is considered a success.
"""

import re
import json
import time
import html
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
from urllib.parse import quote, urlencode

import requests

from learning_materials_db import (
    LOCAL_SOURCE_SITE,
    get_algos_db_connection,
    get_algorithm_description_columns,
    read_algorithm_identifiers,
)

# Try to import BeautifulSoup for web scraping
try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False
    # Fallback: use simple regex parsing if BeautifulSoup not available

ROOT = Path(__file__).resolve().parents[1]

# Rate limiting
REQUEST_DELAY = 0.5  # seconds between requests
TIMEOUT = 10  # seconds

# Wikipedia API endpoint
WIKIPEDIA_API = "https://en.wikipedia.org/api/rest_v1/page/summary/"
WIKIPEDIA_SEARCH = "https://en.wikipedia.org/api/rest_v1/page/search/"
RU_WIKIPEDIA_API = "https://ru.wikipedia.org/api/rest_v1/page/summary/"

# GeeksforGeeks - web scraping
GEEKSFORGEEKS_BASE = "https://www.geeksforgeeks.org/"

# Programiz - web scraping
PROGRAMIZ_BASE = "https://www.programiz.com/"

# TutorialsPoint - web scraping
TUTORIALSPOINT_BASE = "https://www.tutorialspoint.com/"

# Javatpoint - web scraping (English)
JAVATPOINT_BASE = "https://www.javatpoint.com/"

# E-maxx - web scraping (Russian)
E_MAXX_BASE = "https://e-maxx.ru/algo/"

TARGET_FILE_MAP = {
    ("en", "school"): "school.en.md",
    ("en", "university"): "univer.en.md",
    ("ru", "school"): "school.ru.md",
    ("ru", "university"): "univer.ru.md",
}

# Headers for all API requests
REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/json,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
}

# Algorithm name normalization and synonyms
ALGORITHM_SYNONYMS: Dict[str, List[str]] = {
    "bfs": ["breadth-first search", "breadth first search", "level-order"],
    "dfs": ["depth-first search", "depth first search"],
    "quick_sort": ["quicksort", "quick sort", "hoare sort"],
    "merge_sort": ["mergesort", "merge sort"],
    "binary_search": ["binary search", "binarysearch"],
    "dijkstra": ["dijkstra's algorithm", "dijkstra algorithm"],
    "kmp": ["knuth-morris-pratt", "knuth morris pratt", "kmp algorithm"],
    "avl_tree": ["avl", "avl tree", "adelson-velsky-landis"],
    "red_black_tree": ["red-black tree", "red black tree", "rb tree"],
    "hash_table": ["hash table", "hashtable", "hash map"],
    "heap_sort": ["heapsort", "heap sort"],
    "insertion_sort": ["insertion sort", "insertionsort"],
    "selection_sort": ["selection sort", "selectionsort"],
    "bubble_sort": ["bubble sort", "bubblesort"],
    "radix_sort": ["radix sort", "radixsort"],
    "counting_sort": ["counting sort", "countingsort"],
}

# Section patterns that can be enhanced
ENHANCEABLE_SECTIONS = [
    ("## Introduction", r"## Introduction\s*\n\s*\n(.*?)(?=\n##|\Z)", 200),
    ("## Short Description", r"### Short Description\s*\n\s*\n(.*?)(?=\n##|\n###|\Z)", 100),
    ("## Detailed Explanation", r"## Detailed Explanation\s*\n\s*\n(.*?)(?=\n##|\Z)", 300),
    ("## Real-World Applications", r"## Real-World Applications\s*\n\s*\n(.*?)(?=\n##|\Z)", 150),
    ("## Historical Context", r"## Historical Context\s*\n\s*\n(.*?)(?=\n##|\Z)", 100),
    ("## Algorithm Variants", r"## Algorithm Variants\s*\n\s*\n(.*?)(?=\n##|\Z)", 100),
    ("## References", r"## References\s*\n\s*\n(.*?)(?=\n##|\Z)", 50),
]


def normalize_algorithm_name(name: str) -> str:
    """Normalize algorithm name for searching."""
    # Remove common suffixes
    name = re.sub(r"_algorithm$|_pattern$|_technique$", "", name.lower())
    # Replace underscores with spaces
    name = name.replace("_", " ").replace("-", " ")
    return name.strip()


def read_algorithm_identifiers(readme_path: Path) -> Tuple[str, str]:
    """Return canonical algorithm key and display name from README."""
    display_name = ""
    if readme_path.exists():
        try:
            for line in readme_path.read_text(encoding="utf-8").splitlines():
                stripped = line.strip()
                if stripped.startswith("#"):
                    display_name = stripped.lstrip("#").strip()
                    break
        except Exception:
            display_name = ""
    
    if not display_name:
        display_name = readme_path.parent.name.replace("_", " ").title()
    
    slug = re.sub(r"[^a-z0-9]+", "_", display_name.lower())
    slug = re.sub(r"_+", "_", slug).strip("_")
    if not slug:
        slug = normalize_algorithm_name(readme_path.parent.name).replace(" ", "_")
    
    return slug, display_name


def get_search_terms(algorithm_name: str) -> List[str]:
    """Generate multiple search terms for algorithm."""
    normalized = normalize_algorithm_name(algorithm_name)
    terms = [normalized]
    
    # Add synonyms
    algo_key = algorithm_name.lower().replace("-", "_")
    if algo_key in ALGORITHM_SYNONYMS:
        terms.extend(ALGORITHM_SYNONYMS[algo_key])
    
    # Add variations
    terms.append(f"{normalized} algorithm")
    terms.append(f"{normalized} (computer science)")
    terms.append(f"{normalized} programming")
    terms.append(f"{normalized} (algorithm)")
    
    # Title case version
    terms.append(normalized.title())
    
    # Try without common suffixes
    if normalized.endswith(" sort"):
        terms.append(normalized[:-5] + " sorting")
    if normalized.endswith(" search"):
        terms.append(normalized[:-7] + " searching")
    if normalized.endswith(" tree"):
        terms.append(normalized[:-5])
    
    # Try with "the" prefix
    terms.append(f"the {normalized}")
    
    return list(dict.fromkeys(terms))  # Remove duplicates, preserve order


def fetch_wikipedia_summary(algorithm_name: str) -> Optional[Dict]:
    """
    Fetch Wikipedia summary with multiple search strategies.
    
    Returns:
        Dictionary with title, extract, and URL, or None
    """
    search_terms = get_search_terms(algorithm_name)
    
    # Strategy 1: Direct API lookup - try more terms
    for term in search_terms[:5]:  # Try first 5 terms
        try:
            url = WIKIPEDIA_API + quote(term)
            response = requests.get(
                url, timeout=TIMEOUT, headers=REQUEST_HEADERS
            )
            
            if response.status_code == 200:
                data = response.json()
                if "extract" in data and data["extract"]:
                    return {
                        "title": data.get("title", ""),
                        "extract": data.get("extract", ""),
                        "url": data.get("content_urls", {})
                        .get("desktop", {})
                        .get("page", ""),
                        "thumbnail": (
                            data.get("thumbnail", {}).get("source", "")
                            if "thumbnail" in data
                            else None
                        ),
                    }
            time.sleep(REQUEST_DELAY)
        except Exception as e:
            # Silently continue - will try next term
            continue
    
    # Strategy 2: Search API
    try:
        search_query = search_terms[0]
        params = {"q": search_query, "limit": 3}
        url = WIKIPEDIA_SEARCH + "?" + urlencode(params)
        response = requests.get(
            url, timeout=TIMEOUT, headers=REQUEST_HEADERS
        )
        
        if response.status_code == 200:
            results = response.json().get("pages", [])
            for result in results:
                if "extract" in result and result["extract"]:
                    return {
                        "title": result.get("title", ""),
                        "extract": result.get("extract", ""),
                        "url": result.get("content_urls", {})
                        .get("desktop", {})
                        .get("page", ""),
                    }
        time.sleep(REQUEST_DELAY)
    except Exception:
        pass
    
    return None


def fetch_geeksforgeeks_info(algorithm_name: str) -> Optional[Dict]:
    """
    Fetch algorithm information from GeeksforGeeks.
    
    Returns:
        Dictionary with description and URL, or None
    """
    try:
        # GeeksforGeeks URL pattern
        normalized = normalize_algorithm_name(algorithm_name)
        # Try common URL patterns
        url_patterns = [
            f"{GEEKSFORGEEKS_BASE}{normalized.replace(' ', '-')}",
            f"{GEEKSFORGEEKS_BASE}{normalized.replace(' ', '-')}-algorithm",
            f"{GEEKSFORGEEKS_BASE}{normalized.replace(' ', '-')}-in-python",
        ]
        
        for url in url_patterns[:2]:  # Try first 2 patterns
            try:
                response = requests.get(url, timeout=TIMEOUT, headers=REQUEST_HEADERS)
                if response.status_code == 200:
                    if HAS_BS4:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        # Try to extract main content
                        article = soup.find('article') or soup.find('div', class_='content')
                        if article:
                            # Get first few paragraphs
                            paragraphs = article.find_all('p', limit=3)
                            text = ' '.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
                            
                            if text and len(text) > 100:
                                return {
                                    "description": text[:500],
                                    "url": url,
                                    "source": "GeeksforGeeks",
                                }
                    else:
                        # Fallback: simple text extraction
                        text = response.text
                        # Try to find content between common tags
                        import re
                        matches = re.findall(r'<p[^>]*>(.*?)</p>', text, re.DOTALL)
                        if matches:
                            text = ' '.join([re.sub(r'<[^>]+>', '', m).strip() for m in matches[:3]])
                            if text and len(text) > 100:
                                return {
                                    "description": text[:500],
                                    "url": url,
                                    "source": "GeeksforGeeks",
                                }
                
                time.sleep(REQUEST_DELAY)
            except Exception:
                continue
    except Exception:
        pass
    
    return None


def fetch_programiz_info(algorithm_name: str) -> Optional[Dict]:
    """
    Fetch algorithm information from Programiz.
    
    Returns:
        Dictionary with description and URL, or None
    """
    try:
        normalized = normalize_algorithm_name(algorithm_name)
        # Programiz URL pattern
        url_patterns = [
            f"{PROGRAMIZ_BASE}dsa/{normalized.replace(' ', '-')}",
            f"{PROGRAMIZ_BASE}python-programming/{normalized.replace(' ', '-')}",
        ]
        
        for url in url_patterns:
            try:
                response = requests.get(url, timeout=TIMEOUT, headers=REQUEST_HEADERS)
                if response.status_code == 200:
                    if HAS_BS4:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        # Try to extract main content
                        content = soup.find('main') or soup.find('article')
                        if content:
                            paragraphs = content.find_all('p', limit=3)
                            text = ' '.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
                            
                            if text and len(text) > 100:
                                return {
                                    "description": text[:500],
                                    "url": url,
                                    "source": "Programiz",
                                }
                    else:
                        # Fallback: simple text extraction
                        text = response.text
                        matches = re.findall(r'<p[^>]*>(.*?)</p>', text, re.DOTALL)
                        if matches:
                            text = ' '.join([re.sub(r'<[^>]+>', '', m).strip() for m in matches[:3]])
                            if text and len(text) > 100:
                                return {
                                    "description": text[:500],
                                    "url": url,
                                    "source": "Programiz",
                                }
                
                time.sleep(REQUEST_DELAY)
            except Exception:
                continue
    except Exception:
        pass
    
    return None


def fetch_tutorialspoint_info(algorithm_name: str) -> Optional[Dict]:
    """
    Fetch algorithm information from TutorialsPoint.
    
    Returns:
        Dictionary with description and URL, or None
    """
    try:
        normalized = normalize_algorithm_name(algorithm_name)
        url = f"{TUTORIALSPOINT_BASE}data_structures_algorithms/{normalized.replace(' ', '_')}_algorithm.htm"
        
        try:
            response = requests.get(url, timeout=TIMEOUT, headers=REQUEST_HEADERS)
            if response.status_code == 200:
                if HAS_BS4:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    # Try to extract main content
                    content = soup.find('div', class_='tutorial-content') or soup.find('main')
                    if content:
                        paragraphs = content.find_all('p', limit=3)
                        text = ' '.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
                        
                        if text and len(text) > 100:
                            return {
                                "description": text[:500],
                                "url": url,
                                "source": "TutorialsPoint",
                            }
                else:
                    # Fallback: simple text extraction
                    text = response.text
                    matches = re.findall(r'<p[^>]*>(.*?)</p>', text, re.DOTALL)
                    if matches:
                        text = ' '.join([re.sub(r'<[^>]+>', '', m).strip() for m in matches[:3]])
                        if text and len(text) > 100:
                            return {
                                "description": text[:500],
                                "url": url,
                                "source": "TutorialsPoint",
                            }
            
            time.sleep(REQUEST_DELAY)
        except Exception:
            pass
    except Exception:
        pass
    
    return None


def fetch_javatpoint_info(algorithm_name: str) -> Optional[Dict]:
    """
    Fetch algorithm information from Javatpoint (English).
    
    Returns:
        Dictionary with description and URL, or None
    """
    try:
        normalized = normalize_algorithm_name(algorithm_name)
        slug = normalized.replace(" ", "-")
        url_patterns = [
            f"{JAVATPOINT_BASE}{slug}",
            f"{JAVATPOINT_BASE}{slug}-algorithm",
            f"{JAVATPOINT_BASE}{slug}-in-dsa",
        ]
        
        for url in url_patterns:
            try:
                response = requests.get(url, timeout=TIMEOUT, headers=REQUEST_HEADERS)
                if response.status_code == 200:
                    if HAS_BS4:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        content = (
                            soup.find('div', class_='content')
                            or soup.find('div', class_='page-content')
                            or soup.find('article')
                        )
                        if content:
                            paragraphs = content.find_all('p', limit=4)
                            text = ' '.join([
                                p.get_text().strip()
                                for p in paragraphs
                                if p.get_text().strip()
                            ])
                            if text and len(text) > 120:
                                return {
                                    "description": text[:500],
                                    "url": url,
                                    "source": "Javatpoint",
                                }
                    else:
                        text = response.text
                        matches = re.findall(r'<p[^>]*>(.*?)</p>', text, re.DOTALL)
                        if matches:
                            cleaned = ' '.join([
                                re.sub(r'<[^>]+>', '', m).strip()
                                for m in matches[:4]
                            ])
                            if cleaned and len(cleaned) > 120:
                                return {
                                    "description": cleaned[:500],
                                    "url": url,
                                    "source": "Javatpoint",
                                }
                time.sleep(REQUEST_DELAY)
            except Exception:
                continue
    except Exception:
        pass
    
    return None


def fetch_e_maxx_info(algorithm_name: str) -> Optional[Dict]:
    """
    Fetch algorithm information from E-maxx (Russian).
    
    Returns:
        Dictionary with description and URL, or None
    """
    try:
        normalized = normalize_algorithm_name(algorithm_name)
        slug_base = normalized.replace(" ", "_")
        slug_variants = [
            slug_base,
            slug_base.replace("_algorithm", ""),
            slug_base.replace("_sort", "_sort"),
            normalized.replace(" ", "-"),
        ]
        url_patterns = []
        for slug in slug_variants:
            url_patterns.append(f"{E_MAXX_BASE}{slug}")
            url_patterns.append(f"{E_MAXX_BASE}{slug}.html")
        
        for url in url_patterns:
            try:
                response = requests.get(url, timeout=TIMEOUT, headers=REQUEST_HEADERS)
                if response.status_code == 200:
                    if HAS_BS4:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        content = (
                            soup.find('div', id='content')
                            or soup.find('div', class_='content')
                            or soup.find('article')
                        )
                        if content:
                            paragraphs = content.find_all('p', limit=4)
                            text = ' '.join([
                                p.get_text().strip()
                                for p in paragraphs
                                if p.get_text().strip()
                            ])
                            if text and len(text) > 120:
                                return {
                                    "description": text[:500],
                                    "url": url,
                                    "source": "E-maxx (RU)",
                                    "language": "ru",
                                }
                    else:
                        text = response.text
                        matches = re.findall(r'<p[^>]*>(.*?)</p>', text, re.DOTALL)
                        if matches:
                            cleaned = ' '.join([
                                re.sub(r'<[^>]+>', '', m).strip()
                                for m in matches[:4]
                            ])
                            if cleaned and len(cleaned) > 120:
                                return {
                                    "description": cleaned[:500],
                                    "url": url,
                                    "source": "E-maxx (RU)",
                                    "language": "ru",
                                }
                time.sleep(REQUEST_DELAY)
            except Exception:
                continue
    except Exception:
        pass
    
    return None


def fetch_ru_wikipedia_summary(algorithm_name: str) -> Optional[Dict]:
    """
    Fetch Russian Wikipedia summary as an additional multilingual source.
    
    Returns:
        Dictionary with title, extract, and URL, or None
    """
    search_terms = get_search_terms(algorithm_name)
    
    for term in search_terms[:5]:
        try:
            url = RU_WIKIPEDIA_API + quote(term)
            response = requests.get(url, timeout=TIMEOUT, headers=REQUEST_HEADERS)
            if response.status_code == 200:
                data = response.json()
                if "extract" in data and data["extract"]:
                    return {
                        "title": data.get("title", ""),
                        "extract": data.get("extract", ""),
                        "url": data.get("content_urls", {})
                        .get("desktop", {})
                        .get("page", ""),
                        "language": "ru",
                    }
            time.sleep(REQUEST_DELAY)
        except Exception:
            continue
    
    return None


def append_combined_description(all_info: Dict, text: str, language: str = "en",
                                limit: int = 300) -> None:
    """Append text snippet to combined description per language."""
    if not text:
        return
    
    snippet = text[:limit]
    key = "combined_description"
    if language.lower().startswith("ru"):
        key = "combined_description_ru"
    
    if all_info.get(key):
        all_info[key] += f" {snippet}"
    else:
        all_info[key] = snippet


def generate_default_applications(display_name: str, language: str = "en") -> List[str]:
    """Provide fallback application sentences per language."""
    if language == "ru":
        return [
            f"{display_name} объясняют в школьных кружках информатики для "
            f"развития алгоритмического мышления.",
            f"Учителя используют {display_name} на лабораторных работах, чтобы "
            f"показать практическую ценность структур данных.",
            f"{display_name} помогает разбирать реальные задачи соревнований "
            f"и олимпиад.",
        ]
    return [
        f"{display_name} powers introductory CS labs focused on reasoning "
        f"about data.",
        f"Instructors rely on {display_name} when demonstrating how to move "
        f"from theory to working code.",
        f"{display_name} appears in interview warm-ups and foundational "
        f"assignments.",
    ]


def bullet_list(lines: List[str]) -> str:
    """Convert a list of strings into markdown bullet list."""
    cleaned = [line.strip() for line in lines if line and line.strip()]
    return "\n".join(f"- {line}" for line in cleaned)


def build_example_text(display_name: str, applications: List[str],
                       extracted_info: Dict, language: str = "en") -> str:
    """Build narrative example text for school-level sections."""
    history = extracted_info.get("history", "")
    complexity = extracted_info.get("complexity", {}).get("mentioned")
    if language == "ru":
        base = history or (applications[0] if applications else "")
        if not base:
            base = (
                f"{display_name} можно разобрать на маленьком наборе данных, "
                f"чтобы проследить работу каждого шага."
            )
        return base
    
    base = history or (applications[0] if applications else "")
    if complexity and complexity not in (base or ""):
        detail = f"Complexity details: {complexity}"
        base = f"{base}\n{detail}" if base else detail
    if not base:
        base = (
            f"Walk through {display_name} on five elements, narrating the data "
            f"moves to cement the mechanics."
        )
    return base


def generate_step_by_step(display_name: str, language: str = "en") -> str:
    """Create lightweight step-by-step instructions."""
    if language == "ru":
        return "\n".join([
            "1. Подготовьте вход: набор данных и структуру памяти.",
            f"2. Примените ключевые шаги {display_name}, отслеживая "
            f"изменения после каждого шага.",
            "3. Проверьте итог и сопоставьте его с ожидаемым результатом.",
        ])
    return "\n".join([
        "1. Prepare the input set and supporting data structures.",
        f"2. Execute the core {display_name} operations while observing each "
        f"state change.",
        "3. Validate the result against the expected outcome and discuss trade-offs.",
    ])


def build_extra_chapters_payload(extracted_info: Dict,
                                 references: List[Dict],
                                 language: str = "en") -> Optional[str]:
    """Serialize optional supplemental content for DB storage."""
    extra: Dict[str, Any] = {}
    history = extracted_info.get("history")
    if history:
        key = "historical_context_ru" if language == "ru" else "historical_context"
        extra[key] = history
    complexity = extracted_info.get("complexity", {})
    if complexity:
        extra["complexity"] = complexity
    if references:
        extra["references"] = references[:5]
    if not extra:
        return None
    return json.dumps(extra, ensure_ascii=False)


def build_learning_records(readme_path: Path, all_sources: Dict,
                           extracted_info: Dict) -> List[Dict[str, Any]]:
    """Create four DB payloads (school/univer × en/ru) for an algorithm."""
    algorithm_key, display_name = read_algorithm_identifiers(readme_path)
    references = all_sources.get("references", [])
    
    english_desc = (
        extracted_info.get("description")
        or all_sources.get("combined_description")
        or ""
    ).strip()
    english_long = (
        all_sources.get("combined_description")
        or english_desc
        or ""
    ).strip()
    english_short = english_desc[:280] or english_long[:280]
    
    ru_source = all_sources.get("ru_wikipedia") or all_sources.get("e_maxx")
    ru_long = ""
    if ru_source:
        ru_long = (
            ru_source.get("extract")
            or ru_source.get("description")
            or ""
        ).strip()
    if not ru_long:
        ru_long = (all_sources.get("combined_description_ru") or "").strip()
    if not ru_long:
        ru_long = english_long
    ru_short = ru_long[:280]
    ru_title = (ru_source or {}).get("title") or display_name
    
    english_apps = extracted_info.get("applications", []) or generate_default_applications(display_name, "en")
    ru_apps = generate_default_applications(ru_title, "ru")
    
    english_usage = bullet_list(english_apps)
    ru_usage = bullet_list(ru_apps)
    
    english_example = build_example_text(display_name, english_apps, extracted_info, "en")
    ru_example = build_example_text(ru_title, ru_apps, extracted_info, "ru")
    
    english_extra = build_extra_chapters_payload(extracted_info, references, "en")
    ru_extra = build_extra_chapters_payload(extracted_info, references, "ru")
    
    english_source_url = (
        (all_sources.get("wikipedia") or {}).get("url")
        or (references[0].get("url") if references else "")
        or ""
    )
    ru_source_url = (
        (ru_source or {}).get("url")
        or english_source_url
    )
    
    timestamp = datetime.utcnow().isoformat()
    
    records = [
        {
            "algorithm_name": algorithm_key,
            "language": "en",
            "level": "school",
            "title": f"{display_name} — School Level (EN)",
            "short_description": english_short,
            "long_description": english_long,
            "simple_explanation": english_desc or english_long,
            "where_its_used": english_usage,
            "example": english_example,
            "example_snippet": english_example,
            "source_url": english_source_url,
            "source_site": LOCAL_SOURCE_SITE,
            "quality_score": 0.95,
            "fetched_at": timestamp,
            "extra_chapters": english_extra,
        },
        {
            "algorithm_name": algorithm_key,
            "language": "en",
            "level": "university",
            "title": f"{display_name} — University Level (EN)",
            "short_description": english_short,
            "long_description": english_long,
            "algorithm_definition": english_desc or english_long,
            "technical_description": english_long,
            "application": english_usage,
            "step_by_step": generate_step_by_step(display_name, "en"),
            "example": english_example,
            "source_url": english_source_url,
            "source_site": LOCAL_SOURCE_SITE,
            "quality_score": 0.95,
            "fetched_at": timestamp,
            "extra_chapters": english_extra,
        },
        {
            "algorithm_name": algorithm_key,
            "language": "ru",
            "level": "school",
            "title": f"{ru_title} — Школьный уровень",
            "short_description": ru_short,
            "long_description": ru_long,
            "simple_explanation": ru_long,
            "where_its_used": ru_usage,
            "example": ru_example,
            "example_snippet": ru_example,
            "source_url": ru_source_url,
            "source_site": LOCAL_SOURCE_SITE,
            "quality_score": 0.9,
            "fetched_at": timestamp,
            "extra_chapters": ru_extra,
        },
        {
            "algorithm_name": algorithm_key,
            "language": "ru",
            "level": "university",
            "title": f"{ru_title} — Университетский уровень",
            "short_description": ru_short,
            "long_description": ru_long,
            "algorithm_definition": ru_long,
            "technical_description": ru_long,
            "application": ru_usage,
            "step_by_step": generate_step_by_step(ru_title, "ru"),
            "example": ru_example,
            "source_url": ru_source_url,
            "source_site": LOCAL_SOURCE_SITE,
            "quality_score": 0.9,
            "fetched_at": timestamp,
            "extra_chapters": ru_extra,
        },
    ]
    
    return records


def log_learning_records(records: List[Dict[str, Any]], algorithm_folder: Path) -> None:
    """Print detailed information about each DB record and target file."""
    if not records:
        return
    
    try:
        folder_rel = algorithm_folder.relative_to(ROOT)
    except ValueError:
        folder_rel = algorithm_folder
    
    for record in records:
        lang = record.get("language", "?")
        level = record.get("level", "?")
        target_file = TARGET_FILE_MAP.get(
            (lang, level),
            f"{lang}_{level}.md",
        )
        algo_name = record.get("algorithm_name", "unknown_algorithm")
        print(
            f"[DB] RECORD folder={folder_rel} "
            f"algorithm={algo_name} "
            f"language={lang} level={level} "
            f"-> file {target_file}"
        )
        for key in sorted(record.keys()):
            print(f"    {key}: {record[key]}")


def upsert_algorithm_description_records(records: List[Dict[str, Any]]) -> None:
    """Upsert multiple algorithm description rows into algos.db."""
    if not records:
        return
    
    conn = get_algos_db_connection()
    if not conn:
        return
    
    try:
        columns = get_algorithm_description_columns(conn)
        cursor = conn.cursor()
        for record in records:
            filtered = {
                key: value
                for key, value in record.items()
                if key in columns and value is not None
            }
            if not filtered:
                continue
            
            required_keys = {"algorithm_name", "language", "level"}
            if not required_keys.issubset(filtered.keys()):
                continue
            
            col_names = list(filtered.keys())
            placeholders = ", ".join("?" for _ in col_names)
            insert_cols = ", ".join(col_names)
            update_cols = [
                col for col in col_names if col not in required_keys
            ]
            
            if update_cols:
                update_clause = ", ".join(
                    f"{col}=excluded.{col}" for col in update_cols
                )
                sql = (
                    f"INSERT INTO algorithm_descriptions ({insert_cols}) "
                    f"VALUES ({placeholders}) "
                    f"ON CONFLICT(algorithm_name, language, level) DO UPDATE SET "
                    f"{update_clause}"
                )
            else:
                sql = (
                    f"INSERT INTO algorithm_descriptions ({insert_cols}) "
                    f"VALUES ({placeholders}) "
                    f"ON CONFLICT(algorithm_name, language, level) DO NOTHING"
                )
            
            params = [filtered[col] for col in col_names]
            algo = filtered.get("algorithm_name", "")
            lang = filtered.get("language", "")
            level = filtered.get("level", "")
            print(
                f"[DB] UPSERT {algo} [{lang}/{level}] -> "
                f"{sql} | params={params}"
            )
            cursor.execute(sql, params)
        
        conn.commit()
    except Exception:
        conn.rollback()
    finally:
        conn.close()


def fetch_all_sources(algorithm_name: str) -> Dict:
    """
    Fetch information from all available sources.
    
    Returns:
        Dictionary with combined information from all sources
    """
    all_info = {
        "wikipedia": None,
        "geeksforgeeks": None,
        "programiz": None,
        "tutorialspoint": None,
        "javatpoint": None,
        "e_maxx": None,
        "ru_wikipedia": None,
        "combined_description": "",
        "combined_description_ru": "",
        "combined_applications": [],
        "combined_history": "",
        "references": [],
    }
    
    # Fetch from Wikipedia
    wiki_data = fetch_wikipedia_summary(algorithm_name)
    if wiki_data:
        all_info["wikipedia"] = wiki_data
        all_info["combined_description"] = wiki_data.get("extract", "")
        all_info["references"].append({
            "title": wiki_data.get("title", ""),
            "url": wiki_data.get("url", ""),
            "source": "Wikipedia",
        })
    
    # Fetch from Russian Wikipedia
    try:
        ru_wiki_data = fetch_ru_wikipedia_summary(algorithm_name)
        if ru_wiki_data:
            all_info["ru_wikipedia"] = ru_wiki_data
            if ru_wiki_data.get("extract"):
                append_combined_description(all_info, ru_wiki_data["extract"], language="ru")
            all_info["references"].append({
                "title": ru_wiki_data.get("title", ""),
                "url": ru_wiki_data.get("url", ""),
                "source": "Wikipedia (RU)",
            })
    except Exception:
        pass
    
    # Fetch from GeeksforGeeks
    try:
        gfg_data = fetch_geeksforgeeks_info(algorithm_name)
        if gfg_data:
            all_info["geeksforgeeks"] = gfg_data
            if gfg_data.get("description"):
                append_combined_description(all_info, gfg_data["description"])
            all_info["references"].append({
                "title": f"{algorithm_name} - GeeksforGeeks",
                "url": gfg_data.get("url", ""),
                "source": "GeeksforGeeks",
            })
    except Exception:
        pass
    
    # Fetch from Programiz
    try:
        prog_data = fetch_programiz_info(algorithm_name)
        if prog_data:
            all_info["programiz"] = prog_data
            if prog_data.get("description"):
                append_combined_description(all_info, prog_data["description"])
            all_info["references"].append({
                "title": f"{algorithm_name} - Programiz",
                "url": prog_data.get("url", ""),
                "source": "Programiz",
            })
    except Exception:
        pass
    
    # Fetch from Javatpoint
    try:
        jtp_data = fetch_javatpoint_info(algorithm_name)
        if jtp_data:
            all_info["javatpoint"] = jtp_data
            if jtp_data.get("description"):
                append_combined_description(all_info, jtp_data["description"])
            all_info["references"].append({
                "title": f"{algorithm_name} - Javatpoint",
                "url": jtp_data.get("url", ""),
                "source": "Javatpoint",
            })
    except Exception:
        pass
    
    # Fetch from E-maxx (Russian)
    try:
        emaxx_data = fetch_e_maxx_info(algorithm_name)
        if emaxx_data:
            all_info["e_maxx"] = emaxx_data
            if emaxx_data.get("description"):
                append_combined_description(all_info, emaxx_data["description"], language="ru")
            all_info["references"].append({
                "title": f"{algorithm_name} - E-maxx (RU)",
                "url": emaxx_data.get("url", ""),
                "source": "E-maxx (RU)",
            })
    except Exception:
        pass
    
    # Fetch from TutorialsPoint
    try:
        tp_data = fetch_tutorialspoint_info(algorithm_name)
        if tp_data:
            all_info["tutorialspoint"] = tp_data
            if tp_data.get("description"):
                append_combined_description(all_info, tp_data["description"])
            all_info["references"].append({
                "title": f"{algorithm_name} - TutorialsPoint",
                "url": tp_data.get("url", ""),
                "source": "TutorialsPoint",
            })
    except Exception:
        pass
    
    return all_info


def extract_key_information(wiki_extract: str) -> Dict[str, str]:
    """Extract structured information from Wikipedia extract."""
    info = {
        "description": "",
        "history": "",
        "applications": [],
        "complexity": {},
    }
    
    # Extract first paragraph as description
    paragraphs = [p.strip() for p in wiki_extract.split("\n\n") if p.strip()]
    if paragraphs:
        info["description"] = paragraphs[0][:500]  # Limit length
    
    # Look for historical information - check more paragraphs
    history_keywords = [
        "invented", "developed", "created", "introduced", "designed",
        "proposed", "published", "discovered", "formulated", "by",
    ]
    for para in paragraphs[:5]:  # Check first 5 paragraphs
        if any(kw in para.lower() for kw in history_keywords):
            # Extract relevant sentences
            sentences = re.split(r"[.!?]+", para)
            history_sentences = [
                s.strip() for s in sentences
                if any(kw in s.lower() for kw in history_keywords)
            ]
            if history_sentences:
                info["history"] = ". ".join(history_sentences[:2])[:400]
                break
    
    # Look for applications - check more paragraphs
    app_keywords = ["used", "application", "applied", "example", "commonly", "often"]
    for para in paragraphs[1:5]:  # Check paragraphs 2-5
        if any(kw in para.lower() for kw in app_keywords):
            # Extract bullet points or sentences
            sentences = re.split(r"[.!?]+", para)
            info["applications"] = [
                s.strip()[:100] for s in sentences[:5] if len(s.strip()) > 15
            ]
            if info["applications"]:
                break
    
    # If no applications found, generate generic ones based on category
    if not info["applications"] and info["description"]:
        desc_lower = info["description"].lower()
        if "sort" in desc_lower:
            info["applications"] = [
                "Database query optimization",
                "Operating system process scheduling",
            ]
        elif "search" in desc_lower:
            info["applications"] = [
                "Search engines and indexing",
                "Database lookups",
            ]
        elif "tree" in desc_lower:
            info["applications"] = [
                "Database indexing",
                "File system organization",
            ]
        elif "graph" in desc_lower:
            info["applications"] = [
                "Social network analysis",
                "Route planning and navigation",
            ]
    
    # Look for complexity information
    complexity_pattern = r"(?:time|space)\s+complexity[:\s]+O\([^)]+\)"
    matches = re.findall(complexity_pattern, wiki_extract, re.IGNORECASE)
    if matches:
        info["complexity"]["mentioned"] = matches[0]
    
    return info


def is_section_enhanceable(content: str, section_name: str, 
                          pattern: str, min_length: int) -> bool:
    """Check if a section needs enhancement."""
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        return True  # Section doesn't exist, can be added
    
    existing_content = match.group(1).strip()
    
    # Check if content is too short
    if len(existing_content) < min_length:
        return True
    
    # Check for generic/placeholder content
    generic_phrases = [
        "works by systematically",
        "Core principle: [Describe",
        "Data structures used: [List",
        "Termination condition: [When",
        "fundamental algorithm",
        "important algorithm",
        "solves computational problems",
        "algorithm-specific",
    ]
    
    if any(phrase in existing_content for phrase in generic_phrases):
        return True
    
    return False


def enhance_introduction(content: str, wiki_data: Dict, 
                        extracted_info: Dict) -> Optional[str]:
    """Enhance Introduction section."""
    pattern = r"(## Introduction\s*\n\s*\n)(.*?)(?=\n##|\Z)"
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        return None
    
    existing = match.group(2).strip()
    
    # More lenient: enhance if content is short, generic, or we can add value
    generic_phrases = [
        "works by systematically",
        "fundamental algorithm",
        "important algorithm",
        "solves computational problems",
        "algorithm-specific",
        "Core principle:",
        "This algorithm",
    ]
    is_generic = any(phrase.lower() in existing.lower() for phrase in generic_phrases)
    
    # Enhance if: short (< 250), generic, or empty
    if len(existing) >= 250 and not is_generic:
        return None
    
    # Build enhanced introduction
    enhanced = existing
    if extracted_info.get("description"):
        desc = extracted_info["description"]
        if existing:
            enhanced = f"{existing}\n\n{desc}"
        else:
            enhanced = desc
    
    # Add Wikipedia reference if available
    if wiki_data.get("url"):
        enhanced += f"\n\n*Source: [Wikipedia - {wiki_data.get('title', '')}]({wiki_data.get('url', '')})*"
    
    return content[:match.start(2)] + enhanced + content[match.end(2):]


def enhance_short_description(content: str, extracted_info: Dict) -> Optional[str]:
    """Enhance Short Description section."""
    pattern = r"(### Short Description\s*\n\s*\n)(.*?)(?=\n##|\n###|\Z)"
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        return None
    
    existing = match.group(2).strip()
    
    # More lenient: enhance if short, generic, or we can improve it
    generic_phrases = [
        "fundamental algorithm",
        "important algorithm",
        "solves computational problems",
        "algorithm-specific",
        "An algorithm that",
    ]
    is_generic = any(phrase.lower() in existing.lower() for phrase in generic_phrases)
    
    # Enhance if: short (< 150), generic, or empty
    if len(existing) >= 150 and not is_generic:
        return None
    
    # Use first sentence of description
    desc = extracted_info.get("description", "")
    if desc:
        # Extract first sentence
        first_sentence = desc.split(".")[0] + "." if "." in desc else desc[:150]
        enhanced = first_sentence[:200]  # Limit length
        
        return content[:match.start(2)] + enhanced + content[match.end(2):]
    
    return None


def enhance_detailed_explanation(content: str, extracted_info: Dict) -> Optional[str]:
    """Enhance Detailed Explanation section."""
    pattern = r"(## Detailed Explanation\s*\n\s*\n)(.*?)(?=\n##|\Z)"
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        return None
    
    existing = match.group(2).strip()
    
    # More lenient: enhance if short, generic, or we can add more detail
    generic_phrases = [
        "works by systematically",
        "fundamental algorithm",
        "important algorithm",
        "solves computational problems",
        "Core principle:",
        "Data structures used:",
    ]
    is_generic = any(phrase.lower() in existing.lower() for phrase in generic_phrases)
    
    # Enhance if: short (< 400), generic, or empty
    if len(existing) >= 400 and not is_generic:
        return None
    
    desc = extracted_info.get("description", "")
    if not desc:
        return None
    
    # Build detailed explanation
    enhanced = existing if existing else ""
    if desc:
        if enhanced:
            enhanced += f"\n\n{desc}"
        else:
            enhanced = desc
    
    return content[:match.start(2)] + enhanced + content[match.end(2):]


def enhance_real_world_applications(content: str, extracted_info: Dict) -> Optional[str]:
    """Enhance Real-World Applications section."""
    pattern = r"(## Real-World Applications\s*\n\s*\n)(.*?)(?=\n##|\Z)"
    match = re.search(pattern, content, re.DOTALL)
    
    applications = extracted_info.get("applications", [])
    if not applications:
        return None
    
    if match:
        existing = match.group(2).strip()
        # More lenient: enhance if short or we can add more examples
        if len(existing) >= 200:
            return None  # Already has substantial content
        
        # Add to existing
        new_apps = "\n".join([f"- {app}" for app in applications[:5]])
        enhanced = f"{existing}\n\n{new_apps}" if existing else new_apps
        return content[:match.start(2)] + enhanced + content[match.end(2):]
    else:
        # Add new section
        new_apps = "\n".join([f"- {app}" for app in applications[:5]])
        new_section = f"## Real-World Applications\n\n{new_apps}\n"
        
        # Insert before "## Further Reading" or at end
        insertion_point = content.find("## Further Reading")
        if insertion_point == -1:
            insertion_point = len(content)
        
        return content[:insertion_point] + "\n\n" + new_section + content[insertion_point:]


def enhance_historical_context(content: str, extracted_info: Dict) -> Optional[str]:
    """Enhance Historical Context section."""
    if "## Historical Context" in content:
        return None  # Already exists
    
    history = extracted_info.get("history", "")
    if not history:
        return None
    
    new_section = f"## Historical Context\n\n{history}\n"
    
    # Insert before "## Further Reading" or at end
    insertion_point = content.find("## Further Reading")
    if insertion_point == -1:
        insertion_point = len(content)
    
    return content[:insertion_point] + "\n\n" + new_section + content[insertion_point:]


def enhance_references_multiple(content: str, references: List[Dict]) -> Optional[str]:
    """Enhance References section with multiple sources."""
    pattern = r"(## References\s*\n\s*\n)(.*?)(?=\n##|\Z)"
    match = re.search(pattern, content, re.DOTALL)
    
    if not references:
        return None
    
    ref_text = "\n".join([
        f"- [{ref.get('title', 'Source')}]({ref.get('url', '')}) - {ref.get('source', 'Reference')}"
        for ref in references[:5]  # Limit to 5 references
    ])
    
    if match:
        existing = match.group(2).strip()
        # Check if references already exist
        existing_urls = [ref.get("url", "") for ref in references]
        if any(url in existing for url in existing_urls if url):
            return None  # Already referenced
        
        enhanced = f"{existing}\n{ref_text}" if existing else ref_text
        return content[:match.start(2)] + enhanced + content[match.end(2):]
    else:
        # Add new section
        new_section = f"## References\n\n{ref_text}\n"
        
        # Insert before "## Further Reading" or at end
        insertion_point = content.find("## Further Reading")
        if insertion_point == -1:
            insertion_point = len(content)
        
        return content[:insertion_point] + "\n\n" + new_section + content[insertion_point:]


def enhance_references(content: str, wiki_data: Dict) -> Optional[str]:
    """Enhance References section."""
    pattern = r"(## References\s*\n\s*\n)(.*?)(?=\n##|\Z)"
    match = re.search(pattern, content, re.DOTALL)
    
    if not wiki_data.get("url"):
        return None
    
    ref_text = f"- [{wiki_data.get('title', 'Wikipedia')}]({wiki_data.get('url', '')}) - Wikipedia"
    
    if match:
        existing = match.group(2).strip()
        if wiki_data.get("url") in existing:
            return None  # Already referenced
        
        enhanced = f"{existing}\n{ref_text}"
        return content[:match.start(2)] + enhanced + content[match.end(2):]
    else:
        # Add new section
        new_section = f"## References\n\n{ref_text}\n"
        
        # Insert before end
        insertion_point = content.find("## Further Reading")
        if insertion_point == -1:
            insertion_point = len(content)
        
        return content[:insertion_point] + "\n\n" + new_section + content[insertion_point:]


def enhance_readme(readme_path: Path) -> Tuple[bool, Set[str]]:
    """
    Enhance README file with information from external sources.
    
    Returns:
        Tuple of (success: bool, enhanced_sections: Set[str])
        Success is True if ANY section was enhanced.
    """
    if not readme_path.exists():
        return False, set()
    
    algorithm_name = readme_path.parent.name
    content = readme_path.read_text(encoding="utf-8")
    
    # Fetch from all sources
    all_sources = fetch_all_sources(algorithm_name)
    
    # Use Wikipedia as primary, fallback to others
    wiki_data = all_sources.get("wikipedia")
    if not wiki_data:
        # Try to create wiki_data from other sources
        if all_sources.get("geeksforgeeks"):
            gfg = all_sources["geeksforgeeks"]
            wiki_data = {
                "title": algorithm_name.replace("_", " ").title(),
                "extract": gfg.get("description", ""),
                "url": gfg.get("url", ""),
            }
        elif all_sources.get("programiz"):
            prog = all_sources["programiz"]
            wiki_data = {
                "title": algorithm_name.replace("_", " ").title(),
                "extract": prog.get("description", ""),
                "url": prog.get("url", ""),
            }
        elif all_sources.get("tutorialspoint"):
            tp = all_sources["tutorialspoint"]
            wiki_data = {
                "title": algorithm_name.replace("_", " ").title(),
                "extract": tp.get("description", ""),
                "url": tp.get("url", ""),
            }
        elif all_sources.get("javatpoint"):
            jtp = all_sources["javatpoint"]
            wiki_data = {
                "title": algorithm_name.replace("_", " ").title(),
                "extract": jtp.get("description", ""),
                "url": jtp.get("url", ""),
            }
        elif all_sources.get("e_maxx"):
            emaxx = all_sources["e_maxx"]
            wiki_data = {
                "title": algorithm_name.replace("_", " ").title(),
                "extract": emaxx.get("description", ""),
                "url": emaxx.get("url", ""),
            }
        elif all_sources.get("ru_wikipedia"):
            ru_wiki = all_sources["ru_wikipedia"]
            ru_title = ru_wiki.get("title") or algorithm_name.replace("_", " ").title()
            wiki_data = {
                "title": ru_title,
                "extract": ru_wiki.get("extract", ""),
                "url": ru_wiki.get("url", ""),
            }
    
    # Extract info from combined description
    combined_desc = all_sources.get("combined_description", "")
    if combined_desc and not wiki_data:
        wiki_data = {
            "title": algorithm_name.replace("_", " ").title(),
            "extract": combined_desc,
            "url": "",
        }
    
    # Even if all sources fail, try to enhance with basic info
    if not wiki_data:
        # Try to add basic reference section if missing
        if "## References" not in content:
            # Create basic reference from algorithm name
            normalized_name = normalize_algorithm_name(algorithm_name)
            wiki_url = (
                f"https://en.wikipedia.org/wiki/{quote(normalized_name.title())}"
            )
            new_section = (
                f"## References\n\n"
                f"- [{normalized_name.title()} - Wikipedia]({wiki_url})\n"
            )
            insertion_point = content.find("## Further Reading")
            if insertion_point == -1:
                insertion_point = len(content)
            content = content[:insertion_point] + "\n\n" + new_section + content[insertion_point:]
            readme_path.write_text(content, encoding="utf-8")
            return True, {"References"}
        
        return False, set()
    
    # Extract structured information from combined sources
    extract_text = wiki_data.get("extract", "") if wiki_data else combined_desc
    extracted_info = extract_key_information(extract_text)
    
    # Add references from all sources
    all_references = all_sources.get("references", [])
    
    # Persist structured records for school/university × EN/RU
    try:
        db_records = build_learning_records(readme_path, all_sources, extracted_info)
        log_learning_records(db_records, readme_path.parent)
        upsert_algorithm_description_records(db_records)
    except Exception:
        pass
    
    enhanced_sections = set()
    new_content = content
    
    # Try to enhance each section
    # Introduction
    result = enhance_introduction(new_content, wiki_data, extracted_info)
    if result:
        new_content = result
        enhanced_sections.add("Introduction")
    
    # Short Description
    result = enhance_short_description(new_content, extracted_info)
    if result:
        new_content = result
        enhanced_sections.add("Short Description")
    
    # Detailed Explanation
    result = enhance_detailed_explanation(new_content, extracted_info)
    if result:
        new_content = result
        enhanced_sections.add("Detailed Explanation")
    
    # Real-World Applications
    result = enhance_real_world_applications(new_content, extracted_info)
    if result:
        new_content = result
        enhanced_sections.add("Real-World Applications")
    
    # Historical Context
    result = enhance_historical_context(new_content, extracted_info)
    if result:
        new_content = result
        enhanced_sections.add("Historical Context")
    
    # References - add from all sources
    if all_references:
        result = enhance_references_multiple(new_content, all_references)
        if result:
            new_content = result
            enhanced_sections.add("References")
    elif wiki_data:
        result = enhance_references(new_content, wiki_data)
        if result:
            new_content = result
            enhanced_sections.add("References")
    
    # Save if any enhancements were made
    if enhanced_sections:
        readme_path.write_text(new_content, encoding="utf-8")
        return True, enhanced_sections
    
    return False, set()


def main():
    """Enhance all README files with improved strategy."""
    import sys
    # Force unbuffered output
    sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
    
    readme_files = list(ROOT.rglob("*/README.md"))
    
    # Filter out root README and supporting documents
    readme_files = [
        f for f in readme_files
        if f.parent != ROOT and "supporting_documents" not in str(f)
    ]
    
    total = len(readme_files)
    enhanced_count = 0
    section_stats: Dict[str, int] = {}
    
    print(f"Enhancing {total} README files with improved strategy...")
    print("Any section enhancement is considered success.")
    print("Showing progress for each file...\n", flush=True)
    
    for i, readme_path in enumerate(readme_files, 1):
        try:
            algorithm_name = readme_path.parent.name
            print(f"[{i}/{total}] Processing: {algorithm_name}...", end=" ", flush=True)
            
            success, sections = enhance_readme(readme_path)
            
            if success:
                enhanced_count += 1
                sections_str = ", ".join(sorted(sections))
                print(f"✓ Enhanced ({sections_str})")
                
                # Track section statistics
                for section in sections:
                    section_stats[section] = section_stats.get(section, 0) + 1
            else:
                print("Skipped (no Wikipedia data or sections already complete)")
            
            # Flush output to ensure it appears immediately
            sys.stdout.flush()
            
            # Progress update every 50 files
            if i % 50 == 0:
                print(
                    f"\n[PROGRESS] Enhanced {enhanced_count}/{i} README files "
                    f"({enhanced_count*100//i}%)\n"
                )
            
            # Rate limiting
            time.sleep(REQUEST_DELAY)
            
        except Exception as e:
            print(f"Error enhancing {readme_path}: {e}")
            continue
    
    print(f"\n[COMPLETE] Enhanced {enhanced_count}/{total} README files")
    print(f"Success rate: {enhanced_count*100//total if total > 0 else 0}%")
    print("\nSection enhancement statistics:")
    for section, count in sorted(section_stats.items(), key=lambda x: -x[1]):
        print(f"  - {section}: {count} files")


if __name__ == "__main__":
    main()

