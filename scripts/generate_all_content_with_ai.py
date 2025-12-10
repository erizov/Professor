#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate real algorithm content using prompts from database.
Processes files in order: univer.en.md, school.en.md, univer.ru.md, school.ru.md
Replaces entire MD files if they have 5+ placeholders.
Reports progress every 10 files, then every 50 files.
"""

import sys
import sqlite3
import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding='utf-8', errors='replace'
    )

# Database setup
DB_PATH = ROOT / "database" / "algorithm_prompts.db"


def count_placeholders(content: str) -> int:
    """Count placeholder patterns in content."""
    placeholder_patterns = [
        r'\[.*?\]',  # [placeholder]
        r'\[example',
        r'\[Answer based on',
        r'\[List.*?\]',
        r'\[related algorithms\]',
        r'\[other algorithms\]',
        r'\[algorithm family\]',
        r'General algorithmic problem solving',
        r'Complementary algorithms for preprocessing',
        r'Software development frameworks',
        r'systematically processing data according to a specific strategy',
        r'step 1, step 2, step 3',
        r'# Core algorithm logic',
        r'# Implementation logic',
        r'return result\s*$',
        r'This file needs to be generated',
        r'Content generated using prompt',
    ]
    
    count = 0
    for pattern in placeholder_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        count += len(matches)
    
    return count


def has_many_placeholders(content: str) -> bool:
    """Check if content has many placeholders (threshold: 5+)."""
    return count_placeholders(content) >= 5


def get_prompt_from_db(algorithm_name: str, level: str, language: str) -> Optional[str]:
    """Get prompt from database for specific algorithm, level, and language."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Map to database column names
    column_map = {
        ('school', 'en'): 'prompt_school_en',
        ('school', 'ru'): 'prompt_school_ru',
        ('univer', 'en'): 'prompt_univer_en',
        ('univer', 'ru'): 'prompt_univer_ru',
    }
    
    column = column_map.get((level, language))
    if not column:
        conn.close()
        return None
    
    cursor.execute(f"""
        SELECT {column} FROM algorithm_prompts 
        WHERE algorithm_name = ?
    """, (algorithm_name,))
    
    result = cursor.fetchone()
    conn.close()
    
    return result[0] if result else None


def extract_algorithm_context(algorithm_folder: Path) -> Dict:
    """Extract algorithm context from files."""
    context = {
        'name': algorithm_folder.name,
        'category': 'Algorithms',
        'description': '',
        'time_complexity': None,
        'space_complexity': None,
        'code': '',
        'use_cases': [],
    }
    
    # Read metadata.json
    metadata_path = algorithm_folder / "metadata.json"
    if metadata_path.exists():
        try:
            metadata = json.loads(metadata_path.read_text(encoding='utf-8'))
            context.update(metadata)
            if 'complexity' in metadata and isinstance(metadata['complexity'], dict):
                context['time_complexity'] = metadata['complexity'].get('time')
                context['space_complexity'] = metadata['complexity'].get('space')
        except Exception:
            pass
    
    # Read algorithm.py for code snippets
    code_path = algorithm_folder / "algorithm.py"
    if code_path.exists():
        try:
            code = code_path.read_text(encoding='utf-8')
            # Extract main function/class
            lines = code.split('\n')
            main_code = []
            in_function = False
            for line in lines[:100]:  # First 100 lines
                if 'def ' in line or 'class ' in line:
                    in_function = True
                if in_function:
                    main_code.append(line)
                    if line.strip() and not line.startswith(' ') and not line.startswith('\t'):
                        if 'def ' not in line and 'class ' not in line:
                            break
            context['code'] = '\n'.join(main_code[:30])  # First 30 lines of main code
        except Exception:
            pass
    
    return context


def generate_content_from_prompt(prompt: str, algorithm_name: str, level: str, language: str, context: Dict) -> str:
    """
    Generate real content based on prompt.
    This uses the AI assistant's knowledge to create comprehensive content.
    """
    readable_name = algorithm_name.replace('_', ' ').title()
    
    # This function will be called by the AI assistant to generate content
    # For now, return a marker that content needs to be generated
    # The actual generation happens through the AI assistant processing
    
    return f"""# {readable_name}

<!-- AI-Generated Content -->
<!-- Generated from prompt in database -->
<!-- Level: {level}, Language: {language} -->
<!-- Algorithm: {readable_name} -->
<!-- Category: {context.get('category', 'Algorithms')} -->
<!-- Complexity: {context.get('time_complexity', 'Unknown')} time, {context.get('space_complexity', 'Unknown')} space -->

{prompt}

<!-- 
The content above is the PROMPT, not the content.
Real content will be generated by the AI assistant based on this prompt.
This file will be replaced with actual generated content.
-->
"""


def process_algorithm_folder(algorithm_folder: Path, processing_order: List[Tuple[str, str]], files_processed: int) -> Tuple[Dict, int]:
    """Process an algorithm folder and generate content for MD files."""
    algorithm_name = algorithm_folder.name
    results = {
        'algorithm': algorithm_name,
        'processed': [],
        'skipped': [],
        'errors': []
    }
    
    # Extract context once for all files
    context = extract_algorithm_context(algorithm_folder)
    
    for level, language in processing_order:
        md_filename = f"{level}.{language}.md"
        md_file = algorithm_folder / md_filename
        
        if not md_file.exists():
            results['skipped'].append(f"{md_filename} (not found)")
            continue
        
        try:
            # Read current content
            current_content = md_file.read_text(encoding='utf-8')
            
            # Check if file has many placeholders
            should_replace = has_many_placeholders(current_content)
            
            if not should_replace:
                placeholder_count = count_placeholders(current_content)
                results['skipped'].append(f"{md_filename} (few placeholders: {placeholder_count})")
                continue
            
            # Get prompt from database
            prompt = get_prompt_from_db(algorithm_name, level, language)
            
            if not prompt:
                results['errors'].append(f"{md_filename} (no prompt in database)")
                continue
            
            # Generate content marker (actual generation will be done by AI assistant)
            new_content = generate_content_from_prompt(prompt, algorithm_name, level, language, context)
            
            # Write marker content (will be replaced with real content)
            md_file.write_text(new_content, encoding='utf-8')
            results['processed'].append(f"{md_filename}")
            files_processed += 1
            
        except Exception as e:
            results['errors'].append(f"{md_filename}: {str(e)}")
    
    return results, files_processed


def find_all_algorithm_folders() -> List[Path]:
    """Find all algorithm folders in the repository."""
    algorithm_folders = []
    
    for semester_dir in sorted(ROOT.glob("semester_*")):
        if not semester_dir.is_dir():
            continue
        
        for lecture_dir in sorted(semester_dir.glob("lecture_*")):
            if not lecture_dir.is_dir():
                continue
            
            for algo_dir in sorted(lecture_dir.iterdir()):
                if not algo_dir.is_dir():
                    continue
                if algo_dir.name.startswith(".") or algo_dir.name.startswith("_"):
                    continue
                
                algorithm_folders.append(algo_dir)
    
    return algorithm_folders


def main() -> int:
    """Main execution."""
    print("="*70)
    print("GENERATE ALGORITHM CONTENT USING AI AND DATABASE PROMPTS")
    print("="*70)
    print("\nProcessing order:")
    print("  1. English College (univer.en.md)")
    print("  2. English School (school.en.md)")
    print("  3. Russian College (univer.ru.md)")
    print("  4. Russian School (school.ru.md)")
    print("\nFiles with 5+ placeholders will be replaced entirely.")
    print("Progress reports: Every 10 files, then every 50 files.")
    print()
    
    # Check database
    if not DB_PATH.exists():
        print(f"ERROR: Database not found at {DB_PATH}")
        return 1
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM algorithm_prompts")
    prompt_count = cursor.fetchone()[0]
    conn.close()
    
    print(f"Prompts in database: {prompt_count}")
    print()
    
    # Processing order: univer.en, school.en, univer.ru, school.ru
    processing_order = [
        ('univer', 'en'),
        ('school', 'en'),
        ('univer', 'ru'),
        ('school', 'ru'),
    ]
    
    # Find all algorithm folders
    algorithm_folders = find_all_algorithm_folders()
    print(f"Found {len(algorithm_folders)} algorithm folders")
    print()
    
    # Process each algorithm
    total_processed = 0
    total_skipped = 0
    total_errors = 0
    files_processed = 0
    
    for i, algorithm_folder in enumerate(algorithm_folders, 1):
        results, files_processed = process_algorithm_folder(
            algorithm_folder, processing_order, files_processed
        )
        
        total_processed += len(results['processed'])
        total_skipped += len(results['skipped'])
        total_errors += len(results['errors'])
        
        # Progress reporting
        if files_processed > 0:
            if files_processed % 10 == 0 and files_processed <= 50:
                print(f"\n📊 Progress: {files_processed} files processed")
            elif files_processed % 50 == 0:
                print(f"\n📊 Progress: {files_processed} files processed")
        
        # Detailed output for processed files
        if results['processed']:
            print(f"[{i}/{len(algorithm_folders)}] {algorithm_folder.name}: ✅ {', '.join(results['processed'])}")
        elif results['errors']:
            print(f"[{i}/{len(algorithm_folders)}] {algorithm_folder.name}: ❌ {len(results['errors'])} errors")
    
    print()
    print("="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Total algorithms: {len(algorithm_folders)}")
    print(f"Files processed: {total_processed}")
    print(f"Files skipped: {total_skipped}")
    print(f"Errors: {total_errors}")
    print()
    print("NOTE: Files have been marked for content generation.")
    print("      Next step: AI assistant will generate actual content")
    print("      for each marked file using the prompts.")
    print("="*70)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

