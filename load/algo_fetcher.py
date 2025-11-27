"""
algo_fetcher.py

Fetch bilingual (en/ru) algorithm descriptions tuned for two educational levels (school/university).
Stores results into a SQL database (SQLite by default) using SQLAlchemy.

Features implemented:
- algorithm_name normalized and used as primary key
- store aliases (redirects, raw queries, discovered titles)
- use MediaWiki API per language (disambiguation handling and redirects)
- fallback to e-maxx.ru scraping for Russian pages
- fetch_logs recording success/errors for human review
- simple rate limiting and retries

Usage:
    pip install -r requirements.txt
    python algo_fetcher.py

Configure DATABASE_URL at top to point to your Postgres or SQLite DB.
"""

from __future__ import annotations

import re
import time
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List, Dict, Tuple
from urllib.parse import urlencode, quote_plus

import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from sqlalchemy import (
    create_engine, Column, String, Text, Enum, Float, DateTime, Integer,
    ForeignKey, UniqueConstraint, func
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import enum
from datetime import datetime, timezone

from markdown_parser import parse_markdown_file, ParsedMarkdown
from text_utils import (
    PLACEHOLDER_PATTERNS,
    contains_placeholder,
    sanitize_text_field,
    html_to_plain_text,
    is_content_duplicate,
    validate_algorithm_match,
)

# -----------------------
# Config
# -----------------------
DATABASE_URL = "sqlite:///algos.db"  # replace with e.g. "postgresql+psycopg2://user:pass@host/dbname"
USER_AGENT = "AlgoEduFetcher/1.0 (https://example.org; contact@example.org)"
REQUEST_HEADERS = {"User-Agent": USER_AGENT}
WIKIPEDIA_API_URL = "https://{lang}.wikipedia.org/w/api.php"
DEFAULT_RATE_SLEEP = 1.0  # seconds between requests to avoid hammering servers

CURATED_SUMMARIES_PATH = Path(__file__).with_name("curated_summaries.json")

# -----------------------
# Enums
# -----------------------
class LangCode(enum.Enum):
    en = "en"
    ru = "ru"


class EduLevel(enum.Enum):
    school = "school"
    university = "university"


RU_SECTION_TITLES = [
    "Алгоритм",
    "Простой алгоритм",
    "Реализация",
    "Реализация на Java",
    "Анализ",
    "Пример работы алгоритма",
    "Пример реализации",
    "Ссылки",
    "См. также",
    "Примечания",
    "Литература",
]


def _match_section_index(sections: List[dict], target: str) -> Optional[str]:
    """Find section index by matching heading text."""
    target_lower = target.lower()
    for sec in sections:
        line = (sec.get("line") or "").strip()
        if not line:
            continue
        if line.lower() == target_lower:
            return sec.get("index")
    for sec in sections:
        line = (sec.get("line") or "").strip()
        if not line:
            continue
        if target_lower in line.lower():
            return sec.get("index")
    return None


def fetch_ru_wiki_sections(title: str) -> Dict[str, str]:
    """Fetch specific Russian Wikipedia sections for structured content."""
    sections_content: Dict[str, str] = {}
    try:
        meta = mediawiki_query(
            {"action": "parse", "page": title, "prop": "sections", "format": "json"},
            lang="ru",
        )
        parse_data = meta.get("parse")
        if not parse_data:
            return sections_content
        sections = parse_data.get("sections", [])
        for name in RU_SECTION_TITLES:
            idx = _match_section_index(sections, name)
            if not idx:
                continue
            section_resp = mediawiki_query(
                {
                    "action": "parse",
                    "page": title,
                    "prop": "text",
                    "format": "json",
                    "section": idx,
                    "formatversion": 2,
                },
                lang="ru",
            )
            html = section_resp.get("parse", {}).get("text", "")
            text = sanitize_text_field(html_to_plain_text(html))
            if text:
                sections_content[name] = text
    except Exception:
        # Silently ignore parsing issues; fallback to extract
        return sections_content
    return sections_content


def remove_duplicate_structured_fields(desc: "AlgorithmDescription", level: "EduLevel"):
    """Remove duplicate content across structured fields, keeping higher priority values."""
    if level == EduLevel.school:
        field_priority = {
            'simple_explanation': 5,
            'where_its_used': 4,
            'example': 3,
            'long_description': 2,
            'short_description': 1,
        }
        fields_to_check = [
            ('simple_explanation', desc.simple_explanation),
            ('where_its_used', desc.where_its_used),
            ('example', desc.example),
            ('long_description', desc.long_description),
            ('short_description', desc.short_description),
        ]
    else:
        field_priority = {
            'algorithm_definition': 6,
            'technical_description': 5,
            'application': 4,
            'step_by_step': 3,
            'example': 2,
            'long_description': 1,
            'short_description': 0,
        }
        fields_to_check = [
            ('algorithm_definition', desc.algorithm_definition),
            ('technical_description', desc.technical_description),
            ('application', desc.application),
            ('step_by_step', desc.step_by_step),
            ('example', desc.example),
            ('long_description', desc.long_description),
            ('short_description', desc.short_description),
        ]

    fields_to_check = [(name, val) for name, val in fields_to_check if val]
    to_clear = set()

    for i, (name1, val1) in enumerate(fields_to_check):
        if name1 in to_clear:
            continue
        for name2, val2 in fields_to_check[i + 1:]:
            if name2 in to_clear:
                continue
            if is_content_duplicate(val1, val2):
                priority1 = field_priority.get(name1, 0)
                priority2 = field_priority.get(name2, 0)

                if priority1 > priority2:
                    to_clear.add(name2)
                elif priority2 > priority1:
                    to_clear.add(name1)
                    break
                else:
                    if len(val1) >= len(val2):
                        to_clear.add(name2)
                    else:
                        to_clear.add(name1)
                        break

    for field_name in to_clear:
        setattr(desc, field_name, None)


def apply_source_result(desc: "AlgorithmDescription", result: SourceResult, level: EduLevel):
    """Apply adapter result to an AlgorithmDescription instance."""
    if result.title:
        desc.title = sanitize_text_field(result.title) or result.title

    long_text = result.sections.get("long_description") or result.long_summary
    short_text = result.sections.get("short_description") or result.short_summary

    if long_text:
        desc.long_description = sanitize_text_field(long_text) or long_text
    if short_text:
        desc.short_description = sanitize_text_field(short_text) or short_text

    structured_fields = {
        'simple_explanation', 'where_its_used', 'example',
        'algorithm_definition', 'technical_description',
        'application', 'step_by_step', 'discipline',
        'ethical_reasoning', 'extra_chapters',
        'self_check_basic', 'self_check_intermediate', 'self_check_advanced',
        'practical_tasks_basic', 'practical_tasks_applied', 'practical_tasks_research',
    }

    for field, value in result.sections.items():
        if field in {'long_description', 'short_description'}:
            continue
        if field not in structured_fields:
            continue
        if value:
            setattr(desc, field, sanitize_text_field(value) or value)

    desc.source_url = result.source_url
    desc.source_site = result.source_site
    desc.fetched_at = datetime.now(timezone.utc)
    desc.quality_score = 0.9

@dataclass
class SourceResult:
    title: str
    short_summary: str
    long_summary: str
    sections: Dict[str, str]
    source_url: str
    source_site: str


class BaseAdapter:
    """Base class for enrichment adapters."""

    def fetch(self, algorithm_name: str, lang: LangCode, level: EduLevel) -> Optional[SourceResult]:
        raise NotImplementedError


class CuratedSummaryAdapter(BaseAdapter):
    """Adapter that loads curated summaries from JSON."""

    _cache: Optional[Dict[str, Dict[str, Dict[str, Dict[str, str]]]]] = None

    @classmethod
    def _load_cache(cls) -> Dict[str, Dict[str, Dict[str, Dict[str, str]]]]:
        if cls._cache is not None:
            return cls._cache
        if not CURATED_SUMMARIES_PATH.exists():
            cls._cache = {}
        else:
            with CURATED_SUMMARIES_PATH.open("r", encoding="utf-8") as fp:
                cls._cache = json.load(fp)
        return cls._cache

    def fetch(self, algorithm_name: str, lang: LangCode, level: EduLevel) -> Optional[SourceResult]:
        data = self._load_cache()
        key = normalize_algorithm_name(algorithm_name)
        lang_data = data.get(key, {}).get(lang.value)
        if not lang_data:
            return None
        entry = lang_data.get(level.value)
        if not entry:
            return None

        title = entry.get("title") or algorithm_name
        sections = {k: v for k, v in entry.items() if k not in {"title", "short_summary", "long_summary"}}
        long_summary = entry.get("long_summary") or sections.get("long_description")
        short_summary = entry.get("short_summary") or sections.get("short_description")
        if not long_summary:
            return None

        return SourceResult(
            title=title,
            short_summary=short_summary or tune_summary_for_level(long_summary, level),
            long_summary=long_summary,
            sections=sections,
            source_url="curated://summaries",
            source_site="curated",
        )


class WikipediaAdapter(BaseAdapter):
    """Adapter that fetches data from Wikipedia."""

    def fetch(self, algorithm_name: str, lang: LangCode, level: EduLevel) -> Optional[SourceResult]:
        resolved = resolve_wiki_for_query(algorithm_name, lang=lang.value)
        if not resolved:
            return None

        title, extract, fullurl = resolved
        if not extract or len(extract.strip()) < 50:
            return None
        if contains_placeholder(extract):
            return None
        if not validate_algorithm_match(algorithm_name, title, extract):
            return None

        short = tune_summary_for_level(extract, level)
        sections: Dict[str, str] = {
            "long_description": extract,
            "short_description": short,
        }

        if lang == LangCode.ru:
            ru_sections = fetch_ru_wiki_sections(title)
        else:
            ru_sections = {}

        def pick_ru_section(*names: str) -> Optional[str]:
            for name in names:
                value = ru_sections.get(name)
                if value and not contains_placeholder(value):
                    return value
            return None

        if level == EduLevel.school:
            ru_simple = pick_ru_section("Простой алгоритм", "Алгоритм")
            if ru_simple:
                sections["simple_explanation"] = ru_simple
            ru_usage = pick_ru_section("Анализ")
            if ru_usage:
                sections["where_its_used"] = ru_usage
            ru_example = pick_ru_section("Пример работы алгоритма", "Пример реализации")
            if ru_example:
                sections["example"] = ru_example
        else:
            ru_definition = pick_ru_section("Алгоритм")
            if ru_definition:
                sections["algorithm_definition"] = ru_definition
            ru_realization = [pick_ru_section("Реализация"), pick_ru_section("Реализация на Java")]
            realization_text = "\n\n".join([part for part in ru_realization if part])
            if realization_text:
                sections["technical_description"] = realization_text
            ru_application = pick_ru_section("Анализ")
            if ru_application:
                sections["application"] = ru_application
            ru_steps = pick_ru_section("Пример работы алгоритма")
            if ru_steps:
                sections["step_by_step"] = ru_steps
            ru_example_uni = pick_ru_section("Пример реализации")
            if ru_example_uni:
                sections["example"] = ru_example_uni

        return SourceResult(
            title=title,
            short_summary=short,
            long_summary=extract,
            sections=sections,
            source_url=fullurl,
            source_site=f"wikipedia.{lang.value}",
        )


class EMaxxAdapter(BaseAdapter):
    """Adapter that fetches Russian summaries from e-maxx.ru."""

    def fetch(self, algorithm_name: str, lang: LangCode, level: EduLevel) -> Optional[SourceResult]:
        if lang != LangCode.ru:
            return None

        em = fetch_emaxx_page(algorithm_name)
        if not em:
            return None
        title, extract, url = em
        if not extract or len(extract.strip()) < 50:
            return None
        if contains_placeholder(extract):
            return None

        short = tune_summary_for_level(extract, level)
        sections = {
            "long_description": extract,
            "short_description": short,
        }
        return SourceResult(
            title=title,
            short_summary=short,
            long_summary=extract,
            sections=sections,
            source_url=url,
            source_site="e-maxx.ru",
        )


def get_source_adapters(lang: LangCode, prefer_ru_emaxx: bool = True) -> List[BaseAdapter]:
    adapters: List[BaseAdapter] = [
        CuratedSummaryAdapter(),
        WikipediaAdapter(),
    ]
    if lang == LangCode.ru and prefer_ru_emaxx:
        adapters.append(EMaxxAdapter())
    return adapters


def clear_placeholder_fields(desc: "AlgorithmDescription") -> bool:
    """
    Remove placeholder text from all known fields.
    Returns True if any field was modified.
    """
    target_attrs = [
        "simple_explanation",
        "where_its_used",
        "example",
        "algorithm_definition",
        "technical_description",
        "application",
        "step_by_step",
        "long_description",
        "short_description",
        "title",
        "discipline",
        "ethical_reasoning",
        "extra_chapters",
    ]
    changed = False
    for attr in target_attrs:
        value = getattr(desc, attr, None)
        if not value:
            continue
        if attr == "extra_chapters":
            try:
                data = json.loads(value) if isinstance(value, str) else value
            except Exception:
                setattr(desc, attr, None)
                changed = True
                continue
            if not isinstance(data, dict):
                setattr(desc, attr, None)
                changed = True
                continue
            filtered = {k: v for k, v in data.items() if sanitize_text_field(v)}
            if filtered:
                if filtered != data:
                    setattr(desc, attr, json.dumps(filtered, ensure_ascii=False))
                    changed = True
            else:
                setattr(desc, attr, None)
                changed = True
            continue
        sanitized = sanitize_text_field(value)
        if sanitized is None:
            setattr(desc, attr, None)
            changed = True
        elif sanitized != value:
            setattr(desc, attr, sanitized)
            changed = True
    return changed

# -----------------------
# SQLAlchemy models
# -----------------------
Base = declarative_base()

class Algorithm(Base):
    __tablename__ = "algorithms"
    algorithm_name = Column(String, primary_key=True)  # normalized key
    canonical_label = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    descriptions = relationship("AlgorithmDescription", cascade="all, delete-orphan")
    aliases = relationship("AlgorithmAlias", cascade="all, delete-orphan")

class AlgorithmDescription(Base):
    __tablename__ = "algorithm_descriptions"
    id = Column(Integer, primary_key=True)
    algorithm_name = Column(String, ForeignKey("algorithms.algorithm_name", ondelete="CASCADE"), nullable=False)
    language = Column(Enum(LangCode), nullable=False)
    level = Column(Enum(EduLevel), nullable=False)
    title = Column(String)
    short_description = Column(Text)
    long_description = Column(Text)
    example_snippet = Column(Text)
    source_url = Column(Text)
    source_site = Column(String)
    fetched_at = Column(DateTime(timezone=True), server_default=func.now())
    quality_score = Column(Float, default=0.0)
    
    # University level fields
    discipline = Column(Text)
    algorithm_definition = Column(Text)
    technical_description = Column(Text)
    application = Column(Text)
    step_by_step = Column(Text)
    self_check_basic = Column(Text)
    self_check_intermediate = Column(Text)
    self_check_advanced = Column(Text)
    practical_tasks_basic = Column(Text)
    practical_tasks_applied = Column(Text)
    practical_tasks_research = Column(Text)
    ethical_reasoning = Column(Text)
    example_result = Column(Text)
    
    # School level specific fields
    simple_explanation = Column(Text)
    where_its_used = Column(Text)
    example = Column(Text)
    
    # Extra content as JSON
    extra_chapters = Column(Text)  # Stored as JSON string (SQLite) or JSONB (PostgreSQL)
    
    __table_args__ = (UniqueConstraint('algorithm_name', 'language', 'level', name='uix_algo_lang_level'),)

class AlgorithmAlias(Base):
    __tablename__ = "algorithm_aliases"
    id = Column(Integer, primary_key=True)
    algorithm_name = Column(String, ForeignKey("algorithms.algorithm_name", ondelete="CASCADE"), nullable=False)
    alias = Column(String, nullable=False)
    language = Column(Enum(LangCode))
    source_url = Column(Text)

class FetchLog(Base):
    __tablename__ = "fetch_logs"
    id = Column(Integer, primary_key=True)
    algorithm_name = Column(String)
    language = Column(Enum(LangCode))
    level = Column(Enum(EduLevel))
    status = Column(String)
    message = Column(Text)
    fetched_at = Column(DateTime(timezone=True), server_default=func.now())

# -----------------------
# DB init
# -----------------------
engine = create_engine(DATABASE_URL, echo=False, future=True)
Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)

# -----------------------
# Utilities
# -----------------------
def normalize_algorithm_name(name: str) -> str:
    """Normalize a user-provided algorithm name to a DB key."""
    if not name:
        return ""
    name = name.strip().lower()
    name = name.replace("–", "-").replace("—", "-")
    # remove many punctuation characters but keep hyphens and cyrillic letters
    name = re.sub(r"[’'`\"]", "", name)
    name = re.sub(r"\s+", "-", name)
    name = re.sub(r"[^a-z0-9а-яё\-]", "", name, flags=re.IGNORECASE)
    return name

def sentence_split(text: str) -> List[str]:
    return re.split(r'(?<=[.!?])\s+', text.strip())

def tune_summary_for_level(extract_text: str, level: EduLevel) -> str:
    sents = sentence_split(extract_text)
    if level == EduLevel.school:
        chosen = " ".join(sents[:1])
        chosen = re.sub(r'\([^)]*\)', '', chosen)  # remove parentheticals
        return chosen.strip()
    else:
        return " ".join(sents[:3]).strip()

# -----------------------
# MediaWiki helpers (Wikipedia)
# -----------------------
@retry(wait=wait_exponential(min=1, max=10), stop=stop_after_attempt(3), retry=retry_if_exception_type(Exception))
def mediawiki_query(params: dict, lang: str = "en") -> dict:
    """Generic MediaWiki API GET helper with retries."""
    url = WIKIPEDIA_API_URL.format(lang=lang)
    headers = REQUEST_HEADERS
    resp = requests.get(url, params=params, headers=headers, timeout=15)
    resp.raise_for_status()
    return resp.json()

def wiki_search_titles(query: str, lang: str = "en", limit: int = 10) -> List[str]:
    """Use MediaWiki search to retrieve suggested titles for a query."""
    params = {"action": "query", "list": "search", "srsearch": query, "format": "json", "srlimit": limit}
    j = mediawiki_query(params, lang=lang)
    hits = j.get("query", {}).get("search", [])
    return [h["title"] for h in hits]

def wiki_get_page_by_title(title: str, lang: str = "en") -> Optional[dict]:
    """
    Get page extracts and metadata. Also returns pageprops (for disambiguation) and redirects.
    Returns dict {pageid,title,extract,fullurl,pageprops,redirects?}
    """
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts|info|pageprops|links|categories|revisions",
        "rvprop": "content",
        "inprop": "url",
        "exintro": 1,
        "explaintext": 1,
        "titles": title,
        "redirects": 1,
        "pllimit": 50,
        "cllimit": 50
    }
    j = mediawiki_query(params, lang=lang)
    pages = j.get("query", {}).get("pages", {})
    for pid, p in pages.items():
        if pid == "-1":
            return None
        return p
    return None

def is_disambiguation_page(page: dict) -> bool:
    """Detect disambiguation pages using pageprops or categories."""
    pageprops = page.get("pageprops", {})
    if pageprops.get("disambiguation"):
        return True
    # look for categories that indicate disambiguation
    cats = page.get("categories", [])
    for c in cats:
        title = c.get("title", "").lower()
        if "disambiguation" in title or "значения" in title:  # ru hint
            return True
    return False

def is_algorithm_related(page: dict, extract: str) -> bool:
    """
    Check if a Wikipedia page is algorithm-related.
    Filters out cars, organizations, people, etc.
    """
    title = page.get("title", "").lower()
    extract_lower = extract.lower()
    
    # Non-algorithm keywords to filter out
    non_algorithm_keywords = [
        # Vehicles
        'jaguar', 'xk140', 'car', 'automobile', 'автомобиль', 'машина',
        # Organizations/Politics
        'taliban', 'талибан', 'pakistan', 'пакистан', 'organization', 'организация',
        'political', 'политический', 'party', 'партия',
        # People
        'person', 'человек', 'biography', 'биография',
        # Medical terms
        'инфаркт', 'миокарда', 'myocardial', 'infarction', 'медицин', 'medical',
        'болезнь', 'disease', 'лечение', 'treatment', 'терапия', 'therapy',
        'хирургия', 'surgery', 'диагностика', 'diagnosis', 'сердце', 'heart',
        'кровь', 'blood', 'артерия', 'artery', 'вена', 'vein',
        # Other non-algorithm topics
        'movie', 'фильм', 'song', 'песня', 'book', 'книга',
        'история', 'history', 'география', 'geography', 'философия', 'philosophy'
    ]
    
    # Check title for non-algorithm terms
    if any(keyword in title for keyword in non_algorithm_keywords):
        # Allow only if it's clearly about algorithms (e.g., "algorithm for medical diagnosis")
        if 'алгоритм' not in title and 'algorithm' not in title:
            return False
    
    # Check extract for algorithm-related terms
    algorithm_keywords = [
        'algorithm', 'алгоритм', 'computing', 'вычисление', 'data structure',
        'структура данных', 'programming', 'программирование', 'complexity',
        'сложность', 'sort', 'сортировка', 'search', 'поиск', 'graph',
        'граф', 'tree', 'дерево', 'array', 'массив'
    ]
    
    # Must have at least one algorithm-related keyword
    has_algorithm_keyword = any(keyword in extract_lower for keyword in algorithm_keywords)
    
    # Check for medical/health terms in extract - if present without algorithm context, reject
    medical_terms = ['инфаркт', 'миокарда', 'myocardial', 'infarction', 'сердце', 'heart',
                     'кровь', 'blood', 'артерия', 'artery', 'вена', 'vein', 'болезнь', 'disease']
    has_medical_terms = any(term in extract_lower for term in medical_terms)
    
    if has_medical_terms and not has_algorithm_keyword:
        return False
    
    # Check categories if available
    categories = page.get("categories", [])
    category_titles = [cat.get("title", "").lower() for cat in categories]
    
    algorithm_categories = [
        'algorithm', 'алгоритм', 'computer science', 'информатика',
        'data structure', 'структура данных', 'computing', 'вычисление',
        'programming', 'программирование'
    ]
    
    non_algorithm_categories = [
        'medicine', 'медицина', 'health', 'здоровье', 'disease', 'болезнь',
        'biology', 'биология', 'anatomy', 'анатомия', 'physiology', 'физиология',
        'cardiology', 'кардиология', 'pathology', 'патология'
    ]
    
    has_algorithm_category = any(
        any(alg_cat in cat_title for alg_cat in algorithm_categories)
        for cat_title in category_titles
    )
    
    has_non_algorithm_category = any(
        any(non_cat in cat_title for non_cat in non_algorithm_categories)
        for cat_title in category_titles
    )
    
    # If it has non-algorithm category and no algorithm category, reject
    if has_non_algorithm_category and not has_algorithm_category:
        return False
    
    # If it has algorithm category, it's likely an algorithm
    if has_algorithm_category:
        return True
    
    # If no algorithm keywords, reject
    if not has_algorithm_keyword:
        return False
    
    return True


def extract_from_wiki_title(candidate_title: str, lang: str = "en") -> Optional[Tuple[str,str,str]]:
    """
    Try to get extract and URL for a candidate title in a given language.
    Returns (title, extract, fullurl) or None.
    """
    page = wiki_get_page_by_title(candidate_title, lang=lang)
    if not page:
        return None
    if is_disambiguation_page(page):
        return {"disambiguation": True, "page": page}
    title = page.get("title")
    extract = page.get("extract", "") or ""
    
    # Check if this is algorithm-related
    if not is_algorithm_related(page, extract):
        return None  # Skip non-algorithm pages
    
    fullurl = page.get("fullurl", f"https://{lang}.wikipedia.org/wiki/{quote_plus(title.replace(' ', '_'))}")
    return (title, extract, fullurl)

def resolve_wiki_for_query(query: str, lang: str = "en") -> Optional[Tuple[str,str,str]]:
    """
    Resolve the best page for a query:
    - try the query as-is,
    - if disambiguation page returned, parse links and prefer pages in algorithm-related categories,
    - fall back to first search hit.
    """
    # try exact first
    try:
        first = extract_from_wiki_title(query, lang=lang)
        if first:
            if isinstance(first, dict) and first.get("disambiguation"):
                # disambiguation: get links and pick best candidate
                page = first["page"]
                # fetch links from the page (already requested via pllimit)
                links = page.get("links", [])
                # prefer links whose title contains algorithm-related words (heuristic)
                alg_candidates = [l["title"] for l in links if re.search(r"algorithm|algorith|алгоритм|алгоритмы", l["title"], re.IGNORECASE)]
                if alg_candidates:
                    # try top candidates
                    for cand in alg_candidates[:6]:
                        resolved = extract_from_wiki_title(cand, lang=lang)
                        if resolved and not (isinstance(resolved, dict) and resolved.get("disambiguation")):
                            return resolved
                # as fallback, search
            else:
                return first
    except Exception:
        pass

    # fallback: search
    try:
        titles = wiki_search_titles(query, lang=lang, limit=8)
        for t in titles:
            resolved = extract_from_wiki_title(t, lang=lang)
            if resolved and not (isinstance(resolved, dict) and resolved.get("disambiguation")):
                return resolved
    except Exception:
        pass
    return None

# -----------------------
# e-maxx.ru scraper (minimal HTML parsing)
# -----------------------
@retry(wait=wait_exponential(min=1, max=6), stop=stop_after_attempt(3), retry=retry_if_exception_type(Exception))
def fetch_emaxx_page(query: str) -> Optional[Tuple[str,str,str]]:
    """
    Try to find and fetch a page from e-maxx.ru related to the query.
    Strategy:
      - perform a site search using DuckDuckGo's HTML endpoint (lightweight,
        not ideal for production; better: use curated URL mapping or search engine API).
      - fetch first result from e-maxx.ru and return title + first paragraph.
    NOTE: In production consider using a search API or maintain a curated mapping.
    """
    # Build a search query for e-maxx
    q = f"site:e-maxx.ru {query}"
    ddg_url = "https://duckduckgo.com/html/"
    headers = REQUEST_HEADERS
    resp = requests.post(ddg_url, data={"q": q}, headers=headers, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    # find first result link that points to e-maxx.ru
    for a in soup.select("a.result__a"):
        href = a.get("href", "")
        # DuckDuckGo may wrap URLs; try to extract uddg= param
        if href.startswith("/l/?kh=") and "uddg=" in href:
            m = re.search(r"uddg=(http.*?)(&|$)", href)
            if m:
                href = requests.utils.unquote(m.group(1))
        if "e-maxx.ru" in href:
            # fetch page
            r2 = requests.get(href, headers=headers, timeout=15)
            r2.raise_for_status()
            p_soup = BeautifulSoup(r2.text, "html.parser")
            # Try to get H1 or title and first <p>
            title_node = p_soup.find("h1") or p_soup.find("title")
            title = title_node.get_text(strip=True) if title_node else "e-maxx article"
            p = p_soup.find("p")
            extract = p.get_text(strip=True) if p else ""
            return (title, extract, href)
    return None

# -----------------------
# Upsert helpers (DB)
# -----------------------
def upsert_algorithm(session, canonical_label: str) -> str:
    key = normalize_algorithm_name(canonical_label)
    obj = session.get(Algorithm, key)
    if obj:
        # update canonical_label if changed
        if obj.canonical_label != canonical_label:
            obj.canonical_label = canonical_label
            session.add(obj)
            session.commit()
        return key
    obj = Algorithm(algorithm_name=key, canonical_label=canonical_label)
    session.add(obj)
    session.commit()
    return key

def add_alias(session, algo_key: str, alias: str, lang: Optional[LangCode]=None, source_url: Optional[str]=None):
    # ensure no duplicate
    q = session.query(AlgorithmAlias).filter_by(algorithm_name=algo_key, alias=alias, language=lang)
    if q.first():
        return
    alias_obj = AlgorithmAlias(algorithm_name=algo_key, alias=alias, language=lang, source_url=source_url)
    session.add(alias_obj)
    session.commit()

def upsert_description(session, algo_key: str, lang: LangCode, level: EduLevel, title: str,
                       short: str, long_desc: str, source_url: str, source_site: str, quality: float=0.8,
                       parsed_md: Optional[ParsedMarkdown] = None, prefer_web: bool = False):
    """
    Upsert algorithm description with optional parsed markdown content.
    
    Args:
        session: Database session
        algo_key: Normalized algorithm name
        lang: Language code
        level: Education level
        title: Title
        short: Short description
        long_desc: Long description
        source_url: Source URL
        source_site: Source site name
        quality: Quality score
        parsed_md: Optional parsed markdown content
        prefer_web: If True, only update if source is web (not local_markdown)
    """
    existing = session.query(AlgorithmDescription).filter_by(algorithm_name=algo_key, language=lang, level=level).one_or_none()
    
    # If prefer_web is True and existing record is from web, don't overwrite with local
    if prefer_web and existing and existing.source_site and existing.source_site != "local_markdown":
        # Web source already exists, skip local update
        return
    
    # If existing is local and we're adding web, always update
    if existing and existing.source_site == "local_markdown" and source_site != "local_markdown":
        # Web source takes preference over local
        existing.title = title
        existing.short_description = short
        existing.long_description = long_desc
        existing.source_url = source_url
        existing.source_site = source_site
        existing.fetched_at = datetime.now(timezone.utc)
        existing.quality_score = quality
        
        # Update parsed markdown fields if provided
        if parsed_md:
            _update_description_from_parsed(existing, parsed_md, level)
        
        session.add(existing)
    elif existing:
        # Update existing (local to local, or web to web)
        existing.title = title
        existing.short_description = short
        existing.long_description = long_desc
        existing.source_url = source_url
        existing.source_site = source_site
        existing.fetched_at = datetime.now(timezone.utc)
        existing.quality_score = quality
        
        # Update parsed markdown fields if provided
        if parsed_md:
            _update_description_from_parsed(existing, parsed_md, level)
        
        session.add(existing)
    else:
        # Create new
        new = AlgorithmDescription(
            algorithm_name=algo_key,
            language=lang,
            level=level,
            title=title,
            short_description=short,
            long_description=long_desc,
            source_url=source_url,
            source_site=source_site,
            quality_score=quality
        )
        
        # Set parsed markdown fields if provided
        if parsed_md:
            _update_description_from_parsed(new, parsed_md, level)
        
        session.add(new)
    session.commit()


def _update_description_from_parsed(desc: AlgorithmDescription, parsed: ParsedMarkdown, level: EduLevel):
    """Update description object with parsed markdown content."""
    # Common fields
    desc.self_check_basic = parsed.self_check_basic
    desc.self_check_intermediate = parsed.self_check_intermediate
    desc.self_check_advanced = parsed.self_check_advanced
    desc.practical_tasks_basic = parsed.practical_tasks_basic
    desc.practical_tasks_applied = parsed.practical_tasks_applied
    desc.practical_tasks_research = parsed.practical_tasks_research
    
    if level == EduLevel.school:
        # School level fields
        desc.simple_explanation = parsed.simple_explanation
        desc.where_its_used = parsed.where_its_used
        desc.example = parsed.example
        desc.ethical_reasoning = parsed.ethical_note  # school uses ethical_note
    else:
        # University level fields
        desc.discipline = parsed.discipline
        desc.algorithm_definition = parsed.algorithm_definition
        desc.technical_description = parsed.technical_description
        desc.application = parsed.application
        desc.step_by_step = parsed.step_by_step
        desc.ethical_reasoning = parsed.ethical_reasoning
    
    # Store extra content as JSON
    if parsed.extra:
        desc.extra_chapters = json.dumps(parsed.extra, ensure_ascii=False)

def log_fetch(session, algo_key: str, lang: Optional[LangCode], level: Optional[EduLevel], status: str, message: str):
    fl = FetchLog(algorithm_name=algo_key, language=lang, level=level, status=status, message=message)
    session.add(fl)
    session.commit()

# -----------------------
# Local markdown file loading
# -----------------------
def find_all_algorithm_folders(base_path: Path = None) -> List[Path]:
    """
    Find all algorithm folders in the repository.
    
    Structure: semester_*/lecture_*/algorithm_name/
    """
    if base_path is None:
        base_path = Path(".")
    
    algorithm_folders = []
    
    for semester_dir in base_path.glob("semester_*"):
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


def load_from_markdown_files(session, algorithm_folder: Path, 
                             algorithm_name: Optional[str] = None) -> bool:
    """
    Load algorithm descriptions from local markdown files.
    Ensures all 4 combinations (2 languages × 2 levels) are created for each algorithm.
    
    Args:
        session: Database session
        algorithm_folder: Path to algorithm folder containing markdown files
        algorithm_name: Optional algorithm name (if None, uses folder name or metadata.json)
    
    Returns:
        True if at least one file was loaded successfully
    """
    if not algorithm_folder.exists() or not algorithm_folder.is_dir():
        return False
    
    # Try to get algorithm name from metadata.json
    metadata_path = algorithm_folder / "metadata.json"
    if metadata_path.exists():
        try:
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
                if not algorithm_name:
                    algorithm_name = metadata.get("name") or metadata.get("display_name")
        except Exception:
            pass
    
    # Fallback to folder name
    if not algorithm_name:
        algorithm_name = algorithm_folder.name
    
    algo_key = upsert_algorithm(session, algorithm_name)
    
    # Map of file patterns to (level, language) - ALL 4 combinations required
    file_patterns = [
        ("school.en.md", EduLevel.school, LangCode.en),
        ("school.ru.md", EduLevel.school, LangCode.ru),
        ("univer.en.md", EduLevel.university, LangCode.en),
        ("univer.ru.md", EduLevel.university, LangCode.ru),
    ]
    
    loaded_count = 0
    created_count = 0
    
    # Process all 4 combinations - create entry even if file doesn't exist
    for filename, level, lang in file_patterns:
        markdown_path = algorithm_folder / filename
        parsed = None
        title = algorithm_name
        short_desc = ""
        long_desc = ""
        source_url = None
        source_site = "local_markdown"
        quality = 0.5  # Lower quality if file doesn't exist
        
        # Try to load and parse if file exists
        if markdown_path.exists():
            try:
                parsed = parse_markdown_file(markdown_path)
                if parsed:
                    # Use parsed title or algorithm name
                    title = parsed.title or algorithm_name
                    
                    # Create short and long descriptions
                    if level == EduLevel.school:
                        short_desc = parsed.simple_explanation[:200] if parsed.simple_explanation else ""
                        long_desc = parsed.simple_explanation or ""
                    else:
                        short_desc = parsed.algorithm_definition[:200] if parsed.algorithm_definition else ""
                        long_desc = parsed.algorithm_definition or ""
                    
                    source_url = f"file://{markdown_path.absolute()}"
                    quality = 1.0  # High quality for existing files
                    loaded_count += 1
                else:
                    log_fetch(session, algo_key, lang, level, "error", 
                             f"Failed to parse {filename}")
            except Exception as e:
                log_fetch(session, algo_key, lang, level, "error", 
                         f"Error loading {filename}: {str(e)}")
        
        # Always create/update the entry (even if file doesn't exist)
        try:
            upsert_description(
                session=session,
                algo_key=algo_key,
                lang=lang,
                level=level,
                title=title,
                short=short_desc,
                long_desc=long_desc,
                source_url=source_url,
                source_site=source_site,
                quality=quality,
                parsed_md=parsed
            )
            
            if markdown_path.exists() and parsed:
                log_fetch(session, algo_key, lang, level, "ok", 
                         f"Loaded from {filename}")
            else:
                log_fetch(session, algo_key, lang, level, "created", 
                         f"Created entry for {filename} (file not found)")
                created_count += 1
        except Exception as e:
            log_fetch(session, algo_key, lang, level, "error", 
                     f"Error creating entry for {filename}: {str(e)}")
            continue
    
    # Return True if at least one file was loaded, or if all 4 entries were created
    return loaded_count > 0 or created_count == 4


def load_all_from_markdown_files(session, base_path: Path = None, 
                                 algorithm_folders: Optional[List[Path]] = None) -> Dict[str, int]:
    """
    Load all algorithms from markdown files in the repository.
    
    Args:
        session: Database session
        base_path: Base path to search (defaults to current directory)
        algorithm_folders: Optional list of specific folders to process
    
    Returns:
        Dictionary with stats: {'loaded': count, 'failed': count, 'total': count}
    """
    if algorithm_folders is None:
        algorithm_folders = find_all_algorithm_folders(base_path)
    
    stats = {'loaded': 0, 'failed': 0, 'total': len(algorithm_folders)}
    
    for algo_folder in algorithm_folders:
        try:
            if load_from_markdown_files(session, algo_folder):
                stats['loaded'] += 1
            else:
                stats['failed'] += 1
        except Exception as e:
            print(f"Error processing {algo_folder}: {e}")
            stats['failed'] += 1
    
    return stats


# -----------------------
# High-level orchestrator
# -----------------------
def fetch_and_store(session, algorithm_query: str,
                    languages: List[str] = ("en", "ru"),
                    levels: List[str] = ("school", "university"),
                    prefer_ru_emaxx: bool = True) -> Dict[str, int]:
    """
    Given an arbitrary query (user-supplied name), resolve canonical pages and store descriptions
    for requested languages and levels.
    
    Returns:
        Dictionary with stats: {'success': count, 'failed': count, 'skipped': count}
    """
    stats = {'success': 0, 'failed': 0, 'skipped': 0}
    algo_key = upsert_algorithm(session, algorithm_query)
    
    # store query as alias in both languages
    for lang in languages:
        try:
            add_alias(session, algo_key, algorithm_query, LangCode(lang))
        except Exception:
            pass

    for lang in languages:
        for lvl in levels:
            lang_enum = LangCode(lang)
            lvl_enum = EduLevel(lvl)
            
            # Check if extract is empty or placeholder - skip if so
            extract = None
            title = None
            fullurl = None
            source = None
            
            try:
                # 1) try Wikipedia resolve in target language
                resolved = resolve_wiki_for_query(algorithm_query, lang=lang)
                if resolved:
                    title, extract, fullurl = resolved
                    source = f"wikipedia.{lang}"
                    # Check if extract is meaningful (not empty, not placeholder)
                    if not extract or len(extract.strip()) < 50:
                        stats['skipped'] += 1
                        log_fetch(session, algo_key, lang_enum, lvl_enum, "skipped", 
                                 f"Extract too short or empty from {source}")
                        continue
                else:
                    # 2) fallback: if RU, try e-maxx.ru first if enabled
                    if lang == "ru" and prefer_ru_emaxx:
                        em = fetch_emaxx_page(algorithm_query)
                        if em:
                            title, extract, fullurl = em
                            source = "e-maxx.ru"
                            # Check if extract is meaningful
                            if not extract or len(extract.strip()) < 50:
                                stats['skipped'] += 1
                                log_fetch(session, algo_key, lang_enum, lvl_enum, "skipped", 
                                         f"Extract too short from {source}")
                                continue
                        else:
                            stats['skipped'] += 1
                            log_fetch(session, algo_key, lang_enum, lvl_enum, "skipped", 
                                     f"No source found for {lang}")
                            continue
                    else:
                        stats['skipped'] += 1
                        log_fetch(session, algo_key, lang_enum, lvl_enum, "skipped", 
                                 f"No source found in language {lang} for query {algorithm_query}")
                        continue
                
                # Check for placeholder text - skip if found
                if contains_placeholder(extract):
                    stats['skipped'] += 1
                    log_fetch(session, algo_key, lang_enum, lvl_enum, "skipped", 
                             f"Placeholder text detected in extract")
                    continue
                
                # tune summary per level
                short = tune_summary_for_level(extract, lvl_enum)
                # Web takes preference - use prefer_web=False since we're adding web data
                upsert_description(session, algo_key, lang_enum, lvl_enum, title, short, extract, 
                                  fullurl, source, quality=0.9, prefer_web=False)
                add_alias(session, algo_key, title, lang_enum, source_url=fullurl)
                log_fetch(session, algo_key, lang_enum, lvl_enum, "ok", f"Fetched from {source}: {fullurl}")
                stats['success'] += 1
                time.sleep(DEFAULT_RATE_SLEEP)
            except Exception as e:
                # record failure
                stats['failed'] += 1
                log_fetch(session, algo_key, LangCode(lang) if lang in LangCode.__members__ else None,
                          EduLevel(lvl) if lvl in EduLevel.__members__ else None,
                          "error", str(e))
                continue
    
    return stats

# -----------------------
# Status reporting
# -----------------------
def get_db_statistics(session) -> Dict[str, int]:
    """Get current database statistics."""
    total_algorithms = session.query(Algorithm).count()
    total_descriptions = session.query(AlgorithmDescription).count()
    web_descriptions = session.query(AlgorithmDescription).filter(
        AlgorithmDescription.source_site != "local_markdown"
    ).count()
    local_descriptions = session.query(AlgorithmDescription).filter(
        AlgorithmDescription.source_site == "local_markdown"
    ).count()
    
    return {
        'total_algorithms': total_algorithms,
        'total_descriptions': total_descriptions,
        'web_descriptions': web_descriptions,
        'local_descriptions': local_descriptions
    }


def print_status(session, stats_label: str = ""):
    """Print current status."""
    db_stats = get_db_statistics(session)
    print(f"\n{'='*60}")
    print(f"STATUS {stats_label}")
    print(f"{'='*60}")
    print(f"Total algorithms in DB: {db_stats['total_algorithms']}")
    print(f"Total descriptions: {db_stats['total_descriptions']}")
    print(f"  - From web sources: {db_stats['web_descriptions']}")
    print(f"  - From local markdown: {db_stats['local_descriptions']}")
    print(f"{'='*60}\n")


# -----------------------
# Web enrichment for existing database entries
# -----------------------
def has_main_description_without_placeholders(desc: "AlgorithmDescription", level: EduLevel) -> bool:
    """
    Check if at least one main description field is present and no placeholders exist.
    
    Args:
        desc: AlgorithmDescription instance
        level: Education level (school or university)
    
    Returns:
        True if at least one main description field is filled and no placeholders exist
    """
    # Main description fields for school level
    if level == EduLevel.school:
        main_fields = [
            'simple_explanation',
            'where_its_used',
            'example',
            'long_description',
            'short_description',
        ]
    else:
        # Main description fields for university level
        main_fields = [
            'algorithm_definition',
            'technical_description',
            'application',
            'step_by_step',
            'example',
            'long_description',
            'short_description',
        ]
    
    # Check if at least one main field is filled
    has_main_field = False
    for field_name in main_fields:
        value = getattr(desc, field_name, None)
        if value and value.strip():
            has_main_field = True
            break
    
    if not has_main_field:
        return False
    
    # Check ALL text fields for placeholders (comprehensive check)
    all_text_fields = [
        'title', 'short_description', 'long_description',
        'simple_explanation', 'where_its_used', 'example',
        'algorithm_definition', 'technical_description',
        'application', 'step_by_step', 'discipline',
        'ethical_reasoning', 'example_result', 'example_snippet',
        'self_check_basic', 'self_check_intermediate', 'self_check_advanced',
        'practical_tasks_basic', 'practical_tasks_applied', 'practical_tasks_research',
    ]
    
    for field_name in all_text_fields:
        value = getattr(desc, field_name, None)
        if value and contains_placeholder(value):
            return False
    
    # Also check extra_chapters if it's a JSON string
    if desc.extra_chapters:
        try:
            extra_data = json.loads(desc.extra_chapters) if isinstance(desc.extra_chapters, str) else desc.extra_chapters
            if isinstance(extra_data, dict):
                for key, value in extra_data.items():
                    if isinstance(value, str) and contains_placeholder(value):
                        return False
        except Exception:
            # If parsing fails, check as string
            if isinstance(desc.extra_chapters, str) and contains_placeholder(desc.extra_chapters):
                return False
    
    return True


def enrich_description_from_web(session, algo_key: str, lang: LangCode, level: EduLevel,
                                algorithm_name: str, prefer_ru_emaxx: bool = True) -> Dict[str, any]:
    """
    Enrich a specific (algorithm, language, level) entry with web data.
    Uses adapter pipeline to gather candidate content.
    Skips enrichment if at least one main description is already present and contains no placeholders.
    """
    # First, check if description already exists and is complete
    existing = session.query(AlgorithmDescription).filter_by(
        algorithm_name=algo_key, language=lang, level=level
    ).one_or_none()

    if not existing:
        return {'status': 'failed', 'reason': 'Description not found in database'}
    
    # Skip if already enriched from web (not local_markdown)
    if existing.source_site and existing.source_site != "local_markdown":
        # Check if it has main description and no placeholders
        if has_main_description_without_placeholders(existing, level):
            return {
                'status': 'skipped', 
                'reason': f'Already enriched from {existing.source_site} and no placeholders for {algorithm_name} ({lang.value}, {level.value})'
            }
    
    # Check if at least one main description is present and no placeholders exist
    should_skip = has_main_description_without_placeholders(existing, level)
    if should_skip:
        return {
            'status': 'skipped', 
            'reason': f'Main description already present and no placeholders for {algorithm_name} ({lang.value}, {level.value})'
        }
    
    # Debug: if not skipping, log why (for troubleshooting)
    # This helps understand why certain algorithms aren't being skipped
    if existing.source_site == "local_markdown":
        # Check which main fields are missing
        if level == EduLevel.school:
            main_fields = ['simple_explanation', 'where_its_used', 'example', 'long_description', 'short_description']
        else:
            main_fields = ['algorithm_definition', 'technical_description', 'application', 'step_by_step', 'example', 'long_description', 'short_description']
        
        filled_fields = [f for f in main_fields if getattr(existing, f, None) and getattr(existing, f, '').strip()]
        if not filled_fields:
            log_fetch(session, algo_key, lang, level, "debug", 
                     f"Not skipping: No main fields filled for {algorithm_name}")
        else:
            # Check for placeholders in filled fields
            placeholder_fields = []
            for f in filled_fields:
                val = getattr(existing, f, None)
                if val and contains_placeholder(val):
                    placeholder_fields.append(f)
            if placeholder_fields:
                log_fetch(session, algo_key, lang, level, "debug", 
                         f"Not skipping: Placeholders found in {', '.join(placeholder_fields)} for {algorithm_name}")
    
    try:
        adapters = get_source_adapters(lang, prefer_ru_emaxx=prefer_ru_emaxx)
        result: Optional[SourceResult] = None
        for adapter in adapters:
            try:
                result = adapter.fetch(algorithm_name, lang, level)
            except Exception as adapter_error:
                continue
            if result:
                break

        if not result:
            return {'status': 'skipped', 'reason': f'No source found for {algorithm_name} ({lang.value})'}

        apply_source_result(existing, result, level)
        remove_duplicate_structured_fields(existing, level)
        clear_placeholder_fields(existing)

        session.add(existing)
        session.commit()

        add_alias(session, algo_key, result.title, lang, source_url=result.source_url)

        log_fetch(session, algo_key, lang, level, "ok", f"Enriched from {result.source_site}: {result.source_url}")
        return {'status': 'success', 'source': result.source_site, 'url': result.source_url}

    except Exception as e:
        log_fetch(session, algo_key, lang, level, "error", str(e))
        return {'status': 'failed', 'reason': str(e)}


# -----------------------
# Main processing function
# -----------------------
def process_all_algorithms(base_path: Path = None, status_interval: int = 300, 
                           target_algorithm_count: int = 700):
    """
    Process all algorithms: load from markdown, then enhance with web data.
    
    Args:
        base_path: Base path to search for algorithms
        status_interval: Status update interval in seconds (default 300 = 5 minutes)
        target_algorithm_count: Expected number of algorithms (default 700)
    """
    from datetime import datetime
    
    init_db()
    session = Session()
    
    # Find all algorithm folders
    algorithm_folders = find_all_algorithm_folders(base_path)
    print(f"Found {len(algorithm_folders)} algorithm folders")
    
    # Step 1: Load from markdown files
    print("\n" + "="*60)
    print("STEP 1: Loading from local markdown files...")
    print("="*60)
    markdown_stats = load_all_from_markdown_files(session, algorithm_folders=algorithm_folders)
    print(f"Loaded: {markdown_stats['loaded']}, Failed: {markdown_stats['failed']}, Total: {markdown_stats['total']}")
    print_status(session, "After loading from markdown")
    
    # Wait until all algorithms are loaded (check for target count)
    db_stats = get_db_statistics(session)
    print(f"\nWaiting for all algorithms to be loaded...")
    print(f"Current: {db_stats['total_algorithms']} algorithms, {db_stats['total_descriptions']} descriptions")
    print(f"Expected: ~{target_algorithm_count} algorithms, ~{target_algorithm_count * 4} descriptions (4 per algorithm)")
    
    if db_stats['total_algorithms'] < target_algorithm_count * 0.9:  # Allow 10% variance
        print(f"Warning: Only {db_stats['total_algorithms']} algorithms loaded, expected ~{target_algorithm_count}")
        response = input("Continue with web enrichment anyway? (y/n): ")
        if response.lower() != 'y':
            print("Aborted.")
            return
    
    # Step 2: Enhance existing database entries with web data
    print("\n" + "="*60)
    print("STEP 2: Enriching existing database with web data...")
    print("="*60)
    print("Using original English/Russian websites (no translation)")
    print("Web data takes priority over local data")
    print("Skipping if website doesn't answer (no generic placeholders)")
    print("="*60)
    
    # Get all existing descriptions from database
    all_descriptions = session.query(AlgorithmDescription).filter_by(
        source_site="local_markdown"
    ).all()
    
    total_entries = len(all_descriptions)
    total_web_success = 0
    total_web_failed = 0
    total_web_skipped = 0
    
    last_status_time = datetime.now()
    start_time = datetime.now()
    
    print(f"\nProcessing {total_entries} database entries for web enrichment...")
    
    for idx, desc in enumerate(all_descriptions, 1):
        # Check if we need to print status
        current_time = datetime.now()
        if (current_time - last_status_time).total_seconds() >= status_interval:
            elapsed = current_time - start_time
            print_status(session, f"Progress: {idx}/{total_entries} entries processed (Elapsed: {elapsed})")
            last_status_time = current_time
        
        # Get algorithm name
        algo = session.get(Algorithm, desc.algorithm_name)
        if not algo:
            continue
        
        algorithm_name = algo.canonical_label
        
        print(f"[{idx}/{total_entries}] Enriching: {algorithm_name} ({desc.language.value}, {desc.level.value})")
        
        # Enrich this specific entry
        result = enrich_description_from_web(
            session, 
            desc.algorithm_name, 
            desc.language, 
            desc.level,
            algorithm_name
        )
        
        if result['status'] == 'success':
            total_web_success += 1
        elif result['status'] == 'skipped':
            total_web_skipped += 1
            print(f"  Skipped: {result.get('reason', 'Unknown reason')}")
        else:
            total_web_failed += 1
            print(f"  Failed: {result.get('reason', 'Unknown error')}")
        
        # Rate limiting
        time.sleep(DEFAULT_RATE_SLEEP)
    
    # Final status
    print("\n" + "="*60)
    print("FINAL STATUS")
    print("="*60)
    print(f"Web enrichment stats:")
    print(f"  - Success: {total_web_success}")
    print(f"  - Failed: {total_web_failed}")
    print(f"  - Skipped (no answer): {total_web_skipped}")
    print(f"  - Total processed: {total_entries}")
    print_status(session, "Final")


# -----------------------
# CLI example: test 20 canonical algorithms
# -----------------------
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Fetch algorithm descriptions from web or local markdown files")
    parser.add_argument("--mode", choices=["web", "local", "both", "full"], default="full",
                       help="Fetch mode: web, local, both, or full (local then web enhancement)")
    parser.add_argument("--base-path", type=str, default="..",
                       help="Base path to search for algorithm folders (default: parent directory)")
    parser.add_argument("--algorithm", type=str, nargs="+",
                       help="Specific algorithm names to fetch (for web mode)")
    parser.add_argument("--status-interval", type=int, default=300,
                       help="Status update interval in seconds (default: 300 = 5 minutes)")
    args = parser.parse_args()
    
    base_path = Path(args.base_path).resolve()
    
    if args.mode == "full":
        # Full processing: load from markdown, then enhance with web
        process_all_algorithms(base_path=base_path, status_interval=args.status_interval)
    else:
        init_db()
        s = Session()
        
        if args.mode in ["local", "both"]:
            print("Loading from local markdown files...")
            stats = load_all_from_markdown_files(s, base_path=base_path)
            print(f"Loaded: {stats['loaded']}, Failed: {stats['failed']}, Total: {stats['total']}")
            print_status(s, "After loading from markdown")
        
        if args.mode in ["web", "both"]:
            if args.algorithm:
                algorithms_to_fetch = args.algorithm
            else:
                algorithms_to_fetch = [
                    "Dijkstra's algorithm", "Breadth-First Search", "Depth-First Search", 
                    "QuickSort", "MergeSort", "Binary Search", "Bellman-Ford algorithm", 
                    "Floyd-Warshall", "Kruskal's algorithm", "Prim's algorithm",
                    "A* search", "HeapSort", "Radix Sort", "Counting Sort", 
                    "Ford-Fulkerson algorithm", "Johnson", "Topological Sort", 
                    "Knuth-Morris-Pratt", "Rabin-Karp", "Binary Search Tree"
                ]
            
            print(f"Fetching {len(algorithms_to_fetch)} algorithms from web...")
            for q in algorithms_to_fetch:
                print(f"Fetching: {q}")
                fetch_and_store(s, q, languages=("en", "ru"), levels=("school", "university"))
                time.sleep(DEFAULT_RATE_SLEEP)
            
            print_status(s, "After web fetching")
    
    print(f"Done. See DB: {DATABASE_URL}")
