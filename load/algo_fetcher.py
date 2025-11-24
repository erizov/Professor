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

import re
import time
import json
from pathlib import Path
from typing import Optional, List, Dict, Tuple
from urllib.parse import urlencode, quote_plus

import requests
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from sqlalchemy import (
    create_engine, Column, String, Text, Enum, Float, DateTime, Integer,
    ForeignKey, UniqueConstraint, func
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import enum
from datetime import datetime

from markdown_parser import parse_markdown_file, ParsedMarkdown

# -----------------------
# Config
# -----------------------
DATABASE_URL = "sqlite:///algos.db"  # replace with e.g. "postgresql+psycopg2://user:pass@host/dbname"
USER_AGENT = "AlgoEduFetcher/1.0 (https://example.org; contact@example.org)"
REQUEST_HEADERS = {"User-Agent": USER_AGENT}
WIKIPEDIA_API_URL = "https://{lang}.wikipedia.org/w/api.php"
DEFAULT_RATE_SLEEP = 1.0  # seconds between requests to avoid hammering servers

# -----------------------
# SQLAlchemy models
# -----------------------
Base = declarative_base()

class LangCode(enum.Enum):
    en = "en"
    ru = "ru"

class EduLevel(enum.Enum):
    school = "school"
    university = "university"

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
        existing.fetched_at = datetime.utcnow()
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
        existing.fetched_at = datetime.utcnow()
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
    
    # Map of file patterns to (level, language)
    file_patterns = [
        ("school.en.md", EduLevel.school, LangCode.en),
        ("school.ru.md", EduLevel.school, LangCode.ru),
        ("univer.en.md", EduLevel.university, LangCode.en),
        ("univer.ru.md", EduLevel.university, LangCode.ru),
    ]
    
    loaded_count = 0
    
    for filename, level, lang in file_patterns:
        markdown_path = algorithm_folder / filename
        if not markdown_path.exists():
            continue
        
        try:
            parsed = parse_markdown_file(markdown_path)
            if not parsed:
                log_fetch(session, algo_key, lang, level, "error", 
                         f"Failed to parse {filename}")
                continue
            
            # Use parsed title or algorithm name
            title = parsed.title or algorithm_name
            
            # Create short and long descriptions
            if level == EduLevel.school:
                short_desc = parsed.simple_explanation[:200] if parsed.simple_explanation else ""
                long_desc = parsed.simple_explanation or ""
            else:
                short_desc = parsed.algorithm_definition[:200] if parsed.algorithm_definition else ""
                long_desc = parsed.algorithm_definition or ""
            
            # Store description
            upsert_description(
                session=session,
                algo_key=algo_key,
                lang=lang,
                level=level,
                title=title,
                short=short_desc,
                long_desc=long_desc,
                source_url=f"file://{markdown_path.absolute()}",
                source_site="local_markdown",
                quality=1.0,  # Local files are high quality
                parsed_md=parsed
            )
            
            log_fetch(session, algo_key, lang, level, "ok", 
                     f"Loaded from {filename}")
            loaded_count += 1
            
        except Exception as e:
            log_fetch(session, algo_key, lang, level, "error", 
                     f"Error loading {filename}: {str(e)}")
            continue
    
    return loaded_count > 0


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
                placeholder_patterns = [
                    r'\[specific purpose\]', r'\[specific mechanism\]', r'\[конкретная цель\]',
                    r'\[конкретный механизм\]', r'placeholder', r'заполнитель'
                ]
                if any(re.search(pattern, extract, re.IGNORECASE) for pattern in placeholder_patterns):
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
# Main processing function
# -----------------------
def process_all_algorithms(base_path: Path = None, status_interval: int = 300):
    """
    Process all algorithms: load from markdown, then enhance with web data.
    
    Args:
        base_path: Base path to search for algorithms
        status_interval: Status update interval in seconds (default 300 = 5 minutes)
    """
    import threading
    from datetime import datetime, timedelta
    
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
    
    # Step 2: Enhance with web data
    print("\n" + "="*60)
    print("STEP 2: Enhancing with web data...")
    print("="*60)
    
    # Get algorithm names from database (those loaded from markdown)
    algorithms_to_enhance = session.query(Algorithm).all()
    total_web_success = 0
    total_web_failed = 0
    total_web_skipped = 0
    
    last_status_time = datetime.now()
    start_time = datetime.now()
    
    for idx, algo in enumerate(algorithms_to_enhance, 1):
        # Check if we need to print status
        current_time = datetime.now()
        if (current_time - last_status_time).total_seconds() >= status_interval:
            elapsed = current_time - start_time
            print_status(session, f"Progress: {idx}/{len(algorithms_to_enhance)} algorithms processed (Elapsed: {elapsed})")
            last_status_time = current_time
        
        print(f"[{idx}/{len(algorithms_to_enhance)}] Enhancing: {algo.canonical_label}")
        
        try:
            web_stats = fetch_and_store(session, algo.canonical_label, 
                                       languages=("en", "ru"), 
                                       levels=("school", "university"))
            total_web_success += web_stats['success']
            total_web_failed += web_stats['failed']
            total_web_skipped += web_stats['skipped']
        except Exception as e:
            print(f"  Error: {e}")
            total_web_failed += 1
            continue
    
    # Final status
    print("\n" + "="*60)
    print("FINAL STATUS")
    print("="*60)
    print(f"Web enhancement stats:")
    print(f"  - Success: {total_web_success}")
    print(f"  - Failed: {total_web_failed}")
    print(f"  - Skipped (no answer): {total_web_skipped}")
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
