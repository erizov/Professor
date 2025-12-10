#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Translate English MD files to Russian for files that have placeholders.
Uses the fixed English files as source and creates/updates Russian files.
"""

import sys
import re
from pathlib import Path
from typing import Dict, Optional

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding='utf-8', errors='replace'
    )


def has_placeholders(content: str) -> bool:
    """Check if content has placeholder patterns."""
    placeholder_patterns = [
        r'systematically processing data according to a specific strategy',
        r'step 1, step 2, step 3',
        r'\[example',
        r'\[Answer based on',
        r'\[List 3-5 key steps\]',
        r'\[related algorithms\]',
        r'\[other algorithms\]',
        r'\[algorithm family\]',
        r'General algorithmic problem solving',
        r'Complementary algorithms for preprocessing',
    ]
    
    for pattern in placeholder_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            return True
    
    return False


def translate_section_to_russian(en_text: str, section_name: str) -> str:
    """
    Basic translation - in production use proper translation API.
    For now, this keeps the structure and marks for translation.
    """
    # This is a placeholder - in production, use translation service
    # For now, we'll create a structure-preserving version
    
    # Simple keyword translations
    translations = {
        'Quick Summary': 'Краткое резюме',
        'Purpose': 'Назначение',
        'Complexity': 'Сложность',
        'Category': 'Категория',
        'Key Idea': 'Ключевая идея',
        'Where It\'s Used': 'Где применяется',
        'Real-World Applications': 'Применение в реальных системах',
        'Related Algorithms': 'Связанные алгоритмы',
        'Common Application Errors': 'Частые ошибки применения',
        'Key Implementation Details': 'Ключевые детали реализации',
        'Practice Exercise': 'Практическое упражнение',
        'Check Your Understanding': 'Проверьте понимание',
        'Step-by-Step Execution': 'Пошаговое выполнение',
        'Try It Yourself': 'Попробуйте сами',
    }
    
    # For now, return English with note that translation is needed
    # In production, use proper translation API
    return en_text  # Placeholder - needs actual translation


def translate_english_to_russian(en_file: Path, ru_file: Path) -> bool:
    """Translate English file to Russian."""
    try:
        en_content = en_file.read_text(encoding='utf-8')
        
        # Check if English has placeholders
        if has_placeholders(en_content):
            return False  # Don't translate if English still has placeholders
        
        # Check if Russian file exists and has placeholders
        if ru_file.exists():
            ru_content = ru_file.read_text(encoding='utf-8')
            if not has_placeholders(ru_content):
                return False  # Russian is already good
        
        # For now, we'll just mark that translation is needed
        # In production, use translation API here
        # For this script, we'll create a simple structure-preserving version
        
        # Simple approach: Copy structure but keep English for now
        # Mark sections that need translation
        translated = en_content
        
        # Replace section headers with Russian equivalents
        header_translations = {
            '## 📋 Quick Summary': '## 📋 Краткое резюме',
            '## Where It\'s Used': '## Где применяется',
            '## Real-World Applications': '## Применение в реальных системах',
            '## Related Algorithms': '## Связанные алгоритмы',
            '## Common Application Errors': '## Частые ошибки применения',
            '## Key Implementation Details': '## Ключевые детали реализации',
            '## ✏️ Practice Exercise': '## ✏️ Практическое упражнение',
            '## ✅ Check Your Understanding': '## ✅ Проверьте понимание',
            '## 🔍 Step-by-Step Execution': '## 🔍 Пошаговое выполнение',
            '## 🎯 Try It Yourself': '## 🎯 Попробуйте сами',
        }
        
        for en_header, ru_header in header_translations.items():
            translated = translated.replace(en_header, ru_header)
        
        # Replace common English phrases (basic translation)
        phrase_translations = {
            '- **Purpose:**': '- **Назначение:**',
            '- **Complexity:**': '- **Сложность:**',
            '- **Category:**': '- **Категория:**',
            '- **Key Idea:**': '- **Ключевая идея:**',
            '**Exercise 1 (Easy):**': '**Упражнение 1 (Легкое):**',
            '**Exercise 2 (Medium):**': '**Упражнение 2 (Среднее):**',
            '**Exercise 3 (Hard):**': '**Упражнение 3 (Сложное):**',
            '**Q1:**': '**В1:**',
            '**Q2:**': '**В2:**',
            '**Q3:**': '**В3:**',
            '**Q4:**': '**В4:**',
            '**A:**': '**О:**',
        }
        
        for en_phrase, ru_phrase in phrase_translations.items():
            translated = translated.replace(en_phrase, ru_phrase)
        
        # Note: This is a basic structure translation
        # Full content translation requires proper translation API
        # For now, we'll add a note at the top
        if '<!-- TRANSLATION NEEDED -->' not in translated:
            translated = '<!-- TRANSLATION NEEDED: This file was auto-generated from English version. Full translation required. -->\n\n' + translated
        
        ru_file.write_text(translated, encoding='utf-8')
        return True
    except Exception as e:
        print(f"  [ERROR] {ru_file.name}: {e}")
        return False


def process_semester(semester_num: int) -> Dict:
    """Process all files in a semester."""
    semester_path = ROOT / f"semester_{semester_num:02d}"
    
    if not semester_path.exists():
        return {'translated': 0, 'ru_total': 0, 'ru_with_placeholders': 0}
    
    ru_files = list(semester_path.glob("lecture_*/*/school.ru.md"))
    ru_files.extend(semester_path.glob("lecture_*/*/univer.ru.md"))
    
    translated = 0
    ru_with_placeholders = 0
    
    print(f"  Processing {len(ru_files)} Russian files...")
    for ru_file in sorted(ru_files):
        try:
            # Find corresponding English file
            en_file = ru_file.parent / ru_file.name.replace('.ru.', '.en.')
            
            if en_file.exists():
                ru_content = ru_file.read_text(encoding='utf-8')
                if has_placeholders(ru_content):
                    ru_with_placeholders += 1
                    # Translate from English
                    if translate_english_to_russian(en_file, ru_file):
                        translated += 1
        except Exception as e:
            print(f"    [ERROR] {ru_file.name}: {e}")
    
    return {
        'translated': translated,
        'ru_total': len(ru_files),
        'ru_with_placeholders': ru_with_placeholders
    }


def main() -> int:
    """Main execution."""
    print("="*70)
    print("TRANSLATE ENGLISH TO RUSSIAN FOR FILES WITH PLACEHOLDERS")
    print("="*70)
    print("\nStrategy:")
    print("  1. Find Russian files with placeholders")
    print("  2. Use corresponding fixed English files as source")
    print("  3. Translate structure and basic content")
    print("  4. Note: Full translation requires proper translation API")
    print()
    
    total_translated = 0
    total_ru = 0
    total_ru_placeholders = 0
    
    for semester in range(1, 17):
        print(f"\n{'='*70}")
        print(f"Semester {semester:02d}")
        print(f"{'='*70}")
        
        result = process_semester(semester)
        total_translated += result['translated']
        total_ru += result['ru_total']
        total_ru_placeholders += result['ru_with_placeholders']
        
        print(f"  Translated: {result['translated']}/{result['ru_with_placeholders']} (out of {result['ru_total']} total)")
    
    print(f"\n{'='*70}")
    print("FINAL SUMMARY")
    print(f"{'='*70}")
    print(f"Total Russian files: {total_ru}")
    print(f"Russian files with placeholders: {total_ru_placeholders}")
    print(f"Russian files translated: {total_translated}")
    print()
    print(f"Note: This is basic structure translation.")
    print(f"      Full content translation requires proper translation API.")
    print(f"{'='*70}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

