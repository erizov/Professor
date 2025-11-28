#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shared text utilities for placeholder detection, sanitization, and duplicate checks.
"""

from __future__ import annotations

import re
from typing import Optional

from bs4 import BeautifulSoup

PLACEHOLDER_PATTERNS = [
    r"\[specific purpose\]", r"\[specific mechanism\]", r"\[конкретная цель\]",
    r"\[конкретный механизм\]", r"\[.*?\]", r"placeholder", r"заполнитель",
    r"конкретный алгоритм/техника", r"конкретных задач в области",
    r"используемая для \[", r"работает путем \[", r"применение .* для решения конкретных задач",
]


def contains_placeholder(text: Optional[str]) -> bool:
    """Return True if text contains any known placeholder pattern."""
    if not text:
        return False
    for pattern in PLACEHOLDER_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


def sanitize_text_field(text: Optional[str]) -> Optional[str]:
    """Trim text and remove placeholder content."""
    if text is None:
        return None
    cleaned = text.strip()
    if not cleaned:
        return None
    return None if contains_placeholder(cleaned) else cleaned


def html_to_plain_text(html: str) -> str:
    """Convert Wikipedia HTML fragment into readable plain text."""
    if not html:
        return ""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all(["sup", "table", "span"], {"class": ["reference", "mw-editsection"]}):
        tag.decompose()
    text = soup.get_text("\n")
    text = re.sub(r"\n{2,}", "\n\n", text)
    return text.strip()


def normalize_text(text: str) -> str:
    """Normalize text for duplicate comparison."""
    cleaned = text.strip().lower()
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = re.sub(r"[^\w\s]", "", cleaned)
    return cleaned


def is_content_duplicate(text1: Optional[str], text2: Optional[str], threshold: float = 0.8) -> bool:
    """Return True if two text fields contain substantially the same content."""
    if not text1 or not text2:
        return False

    t1 = normalize_text(text1)
    t2 = normalize_text(text2)

    if not t1 or not t2:
        return False

    if t1 == t2:
        return True

    if len(t1) > 50 and len(t2) > 50:
        if len(t1) > len(t2):
            if t2 in t1 and len(t2) / len(t1) > threshold:
                return True
        else:
            if t1 in t2 and len(t1) / len(t2) > threshold:
                return True

    words1 = set(t1.split())
    words2 = set(t2.split())
    if words1 and words2:
        overlap = len(words1 & words2)
        union = len(words1 | words2)
        similarity = overlap / union if union > 0 else 0
        if similarity > threshold:
            return True

    return False


def validate_algorithm_match(algorithm_name: str, fetched_title: str, extract: str) -> bool:
    """Validate that the fetched content matches the algorithm name."""
    algo_lower = algorithm_name.lower()
    title_lower = fetched_title.lower()
    extract_lower = extract.lower()

    algo_normalized = re.sub(r"\s+(algorithm|алгоритм)$", "", algo_lower)
    algo_normalized = re.sub(r"^(the|a|an)\s+", "", algo_normalized)

    if algo_normalized in title_lower or algo_normalized in extract_lower:
        return True

    algo_words = set(re.findall(r"\w+", algo_normalized))
    title_words = set(re.findall(r"\w+", title_lower))
    extract_words = set(re.findall(r"\w+", extract_lower[:500]))

    if len(algo_words) >= 2:
        common_title = len(algo_words & title_words)
        common_extract = len(algo_words & extract_words)
        if common_title >= len(algo_words) * 0.5 or common_extract >= len(algo_words) * 0.5:
            return True

    if len(algo_words) <= 2:
        if any(word in title_lower or word in extract_lower for word in algo_words if len(word) > 3):
            return True

    return False

