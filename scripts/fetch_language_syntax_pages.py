#!/usr/bin/env python3
"""
Fetch programming language syntax pages from learnxinyminutes.com.

This script:
1. Fetches the main page to extract language links
2. Downloads English and Russian versions of each language page
3. Saves them to static_pages/language_syntax/ directory
4. Generates an appendix markdown file with links
"""

import os
import re
import json
import time
import urllib.parse
from pathlib import Path
from typing import List, Dict, Set, Optional
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError


BASE_URL = "https://learnxinyminutes.com"
MAIN_PAGE = f"{BASE_URL}/"
STATIC_DIR = Path("static_pages/language_syntax")
EN_DIR = STATIC_DIR / "en"
RU_DIR = STATIC_DIR / "ru"
DELAY = 0.5  # Delay between requests to be polite


def fetch_url(url: str, retries: int = 3) -> Optional[str]:
    """Fetch content from URL with retries."""
    for attempt in range(retries):
        try:
            req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urlopen(req, timeout=10) as response:
                return response.read().decode("utf-8", errors="ignore")
        except (URLError, HTTPError) as e:
            if attempt < retries - 1:
                time.sleep(1)
                continue
            print(f"  ⚠ Failed to fetch {url}: {e}")
            return None
        except Exception as e:
            print(f"  ⚠ Error fetching {url}: {e}")
            return None
    return None


def extract_language_links(html: str) -> List[Dict[str, str]]:
    """Extract language links from the main page."""
    languages = []
    seen = set()
    
    # Known language codes to exclude from language list
    translation_codes = {
        "en", "ru", "de", "es", "fr", "it", "pt-br", "pt-pt", "ja", "ko",
        "zh-cn", "zh-tw", "hi", "ar", "be", "bg", "ca", "cs", "da", "el",
        "fa", "fi", "he", "hu", "id", "lt", "ms", "nl", "no", "pl", "ro",
        "sk", "sl", "sv", "ta", "th", "tr", "uk", "vi"
    }
    
    # Pattern to match links in table cells
    # Look for <a href="/lang/">Language Name</a> patterns
    pattern = r'<a\s+href="([^"]+)"[^>]*>([^<]+)</a>'
    matches = re.findall(pattern, html)
    
    for href, name in matches:
        if not href.startswith("/"):
            continue
        
        # Remove leading/trailing slashes
        path_parts = [p for p in href.strip("/").split("/") if p]
        
        # We want single-level paths that are not translation codes
        if len(path_parts) == 1:
            lang_key = path_parts[0]
            
            # Skip if it's a translation code or common non-language paths
            if lang_key in translation_codes:
                continue
            if lang_key in ["docs", "about", "contribute", "github"]:
                continue
            
            # Skip if already seen
            if lang_key in seen:
                continue
            
            seen.add(lang_key)
            languages.append({
                "key": lang_key,
                "name": name.strip() or lang_key.title(),
                "path": href
            })
    
    # If we didn't find many, use a comprehensive list of common languages
    if len(languages) < 20:
        common_langs = {
            "python", "java", "javascript", "c", "cpp", "csharp", "go",
            "rust", "ruby", "php", "swift", "kotlin", "scala", "r",
            "matlab", "sql", "html", "css", "bash", "powershell",
            "perl", "lua", "haskell", "clojure", "elixir", "erlang",
            "ocaml", "fsharp", "dart", "typescript", "coffeescript",
            "d", "nim", "crystal", "zig", "v", "julia", "racket",
            "scheme", "prolog", "fortran", "cobol", "pascal", "ada",
            "assembly", "forth", "tcl", "smalltalk", "objective-c",
            "groovy", "julia", "mathematica", "wolfram", "octave"
        }
        
        for lang_key in common_langs:
            if lang_key not in seen:
                seen.add(lang_key)
                languages.append({
                    "key": lang_key,
                    "name": lang_key.replace("-", " ").title(),
                    "path": f"/{lang_key}/"
                })
    
    return sorted(languages, key=lambda x: x["name"].lower())


def save_page(content: str, filepath: Path) -> bool:
    """Save page content to file."""
    try:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"  ⚠ Failed to save {filepath}: {e}")
        return False


def fetch_language_page(lang_key: str, lang_code: str = "") -> Optional[str]:
    """Fetch a language page (English or Russian)."""
    if lang_code:
        url = f"{BASE_URL}/{lang_code}/{lang_key}/"
    else:
        url = f"{BASE_URL}/{lang_key}/"
    
    return fetch_url(url)


def main():
    """Main execution."""
    print("=" * 70)
    print("FETCHING LANGUAGE SYNTAX PAGES")
    print("=" * 70)
    print()
    
    # Fetch main page
    print("1. Fetching main page...")
    main_html = fetch_url(MAIN_PAGE)
    if not main_html:
        print("❌ Failed to fetch main page")
        return 1
    
    print("   ✓ Main page fetched")
    
    # Extract language links
    print("\n2. Extracting language links...")
    languages = extract_language_links(main_html)
    print(f"   ✓ Found {len(languages)} languages")
    
    if not languages:
        print("   ⚠ No languages found, trying alternative extraction...")
        # Fallback: use common languages
        common_langs = [
            "python", "java", "javascript", "c", "cpp", "csharp", "go",
            "rust", "ruby", "php", "swift", "kotlin", "scala", "r",
            "matlab", "r", "sql", "html", "css", "bash", "powershell",
            "perl", "lua", "haskell", "clojure", "elixir", "erlang",
            "ocaml", "fsharp", "dart", "typescript", "coffeescript"
        ]
        languages = [{"key": lang, "name": lang.title(), "path": f"/{lang}/"} 
                     for lang in common_langs]
        print(f"   ✓ Using {len(languages)} common languages")
    
    # Create directories
    EN_DIR.mkdir(parents=True, exist_ok=True)
    RU_DIR.mkdir(parents=True, exist_ok=True)
    
    # Fetch pages
    print("\n3. Fetching language pages...")
    fetched = {"en": 0, "ru": 0}
    failed = {"en": 0, "ru": 0}
    
    for i, lang in enumerate(languages, 1):
        lang_key = lang["key"]
        lang_name = lang["name"]
        print(f"\n   [{i}/{len(languages)}] {lang_name} ({lang_key})")
        
        # Fetch English version
        print("      EN: ", end="", flush=True)
        en_content = fetch_language_page(lang_key, "")
        if en_content:
            en_path = EN_DIR / f"{lang_key}.html"
            if save_page(en_content, en_path):
                print("✓", end="")
                fetched["en"] += 1
            else:
                print("✗", end="")
                failed["en"] += 1
        else:
            print("✗", end="")
            failed["en"] += 1
        
        time.sleep(DELAY)
        
        # Fetch Russian version
        print(" | RU: ", end="", flush=True)
        ru_content = fetch_language_page(lang_key, "ru")
        if ru_content:
            ru_path = RU_DIR / f"{lang_key}.html"
            if save_page(ru_content, ru_path):
                print("✓", end="")
                fetched["ru"] += 1
            else:
                print("✗", end="")
                failed["ru"] += 1
        else:
            print("✗", end="")
            failed["ru"] += 1
        
        time.sleep(DELAY)
    
    # Save language list as JSON
    lang_list_path = STATIC_DIR / "languages.json"
    with open(lang_list_path, "w", encoding="utf-8") as f:
        json.dump(languages, f, indent=2, ensure_ascii=False)
    print(f"\n\n   ✓ Saved language list to {lang_list_path}")
    
    # Generate appendix
    print("\n4. Generating appendix...")
    appendix_path = Path("APPENDIX_LANGUAGE_SYNTAX.md")
    stats = {"en": fetched["en"], "ru": fetched["ru"]}
    generate_appendix(languages, appendix_path, stats)
    print(f"   ✓ Appendix generated: {appendix_path}")
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total languages: {len(languages)}")
    print(f"English pages: {fetched['en']} fetched, {failed['en']} failed")
    print(f"Russian pages: {fetched['ru']} fetched, {failed['ru']} failed")
    print(f"Static pages saved to: {STATIC_DIR}")
    print("=" * 70)
    
    return 0


def generate_appendix(
    languages: List[Dict[str, str]], 
    output_path: Path,
    stats: Dict[str, int]
) -> None:
    """Generate appendix markdown file."""
    content = f"""# Appendix: Syntax of Programming Languages

This appendix provides quick reference guides for programming language syntax, 
based on content from [Learn X in Y Minutes](https://learnxinyminutes.com/).

**Source**: [Learn X in Y Minutes](https://learnxinyminutes.com/) - Community-driven programming language quick references

**Pages Available**: 
- English: {stats['en']} languages
- Russian: {stats['ru']} languages

**Note**: Static copies of these pages are stored in `static_pages/language_syntax/` 
for offline access. Original pages are available at learnxinyminutes.com.

---

## Languages

"""
    
    # Group languages alphabetically
    for lang in languages:
        lang_key = lang["key"]
        lang_name = lang["name"]
        
        en_file = EN_DIR / f"{lang_key}.html"
        ru_file = RU_DIR / f"{lang_key}.html"
        
        content += f"### {lang_name}\n\n"
        
        # English link
        if en_file.exists():
            content += f"- **English**: [View](static_pages/language_syntax/en/{lang_key}.html) | "
            content += f"[Online]({BASE_URL}/{lang_key}/)\n"
        else:
            content += f"- **English**: [Online]({BASE_URL}/{lang_key}/)\n"
        
        # Russian link
        if ru_file.exists():
            content += f"- **Russian**: [View](static_pages/language_syntax/ru/{lang_key}.html) | "
            content += f"[Online]({BASE_URL}/ru/{lang_key}/)\n"
        else:
            content += f"- **Russian**: [Online]({BASE_URL}/ru/{lang_key}/)\n"
        
        content += "\n"
    
    content += f"""
---

## About Learn X in Y Minutes

[Learn X in Y Minutes](https://learnxinyminutes.com/) is a community-driven 
project that provides quick reference guides for programming languages, tools, 
and concepts. Each guide is designed to be read in a few minutes and covers 
the essential syntax and features of the language.

**License**: All articles are licensed under [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/)

**Contributing**: To contribute or request a language, visit the 
[GitHub repository](https://github.com/adambard/learnxinyminutes-docs)

---

*Last updated: {time.strftime("%Y-%m-%d")}*
*Total languages: {len(languages)}*
"""
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    import sys
    sys.exit(main())

