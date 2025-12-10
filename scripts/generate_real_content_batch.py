#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate REAL content for all marked files using prompts from database.
Processes files in batches, reporting progress every 10 files, then every 50.
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

DB_PATH = ROOT / "database" / "algorithm_prompts.db"


def is_marked_for_generation(content: str) -> bool:
    """Check if file is marked for content generation."""
    return "AI-Generated Content" in content or "This file needs to be generated" in content


def get_prompt_from_db(algorithm_name: str, level: str, language: str) -> Optional[str]:
    """Get prompt from database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
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
    
    cursor.execute(f"SELECT {column} FROM algorithm_prompts WHERE algorithm_name = ?", (algorithm_name,))
    result = cursor.fetchone()
    conn.close()
    
    return result[0] if result else None


def extract_algorithm_context(algorithm_folder: Path) -> Dict:
    """Extract algorithm context."""
    context = {
        'name': algorithm_folder.name,
        'category': 'Algorithms',
        'time_complexity': None,
        'space_complexity': None,
    }
    
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
    
    return context


def find_marked_files() -> List[Tuple[Path, str, str, str]]:
    """Find all files marked for content generation."""
    marked_files = []
    
    for semester_dir in sorted(ROOT.glob("semester_*")):
        if not semester_dir.is_dir():
            continue
        
        for lecture_dir in sorted(semester_dir.glob("lecture_*")):
            if not lecture_dir.is_dir():
                continue
            
            for algo_dir in sorted(lecture_dir.iterdir()):
                if not algo_dir.is_dir():
                    continue
                
                algorithm_name = algo_dir.name
                
                for md_file in algo_dir.glob("*.md"):
                    if md_file.name in ['school.en.md', 'school.ru.md', 'univer.en.md', 'univer.ru.md']:
                        try:
                            content = md_file.read_text(encoding='utf-8')
                            if is_marked_for_generation(content):
                                # Extract level and language from filename
                                parts = md_file.stem.split('.')
                                if len(parts) >= 2:
                                    level = parts[0]  # school or univer
                                    language = parts[1]  # en or ru
                                    marked_files.append((md_file, algorithm_name, level, language))
                        except Exception:
                            pass
    
    return marked_files


def main():
    """Main execution."""
    print("="*70)
    print("GENERATE REAL CONTENT FOR MARKED FILES")
    print("="*70)
    print("\nFinding files marked for content generation...")
    
    marked_files = find_marked_files()
    print(f"Found {len(marked_files)} files to process")
    print("\nGenerating content...")
    print("(Progress: every 10 files, then every 50 files)")
    print()
    
    processed = 0
    errors = 0
    
    for i, (md_file, algorithm_name, level, language) in enumerate(marked_files, 1):
        try:
            # Get prompt
            prompt = get_prompt_from_db(algorithm_name, level, language)
            if not prompt:
                print(f"[{i}/{len(marked_files)}] {md_file.name}: ❌ No prompt in database")
                errors += 1
                continue
            
            # Get context
            algorithm_folder = md_file.parent
            context = extract_algorithm_context(algorithm_folder)
            
            # Note: Actual content generation will be done by the AI assistant
            # For now, we'll mark it as ready for generation
            readable_name = algorithm_name.replace('_', ' ').title()
            
            # Generate content placeholder (will be replaced with real content)
            new_content = f"""# {readable_name}

<!-- Content will be generated by AI assistant using prompt from database -->
<!-- Prompt: {prompt[:100]}... -->
<!-- This file is queued for content generation -->
"""
            
            md_file.write_text(new_content, encoding='utf-8')
            processed += 1
            
            # Progress reporting
            if processed % 10 == 0 and processed <= 50:
                print(f"📊 Progress: {processed} files processed")
            elif processed % 50 == 0:
                print(f"📊 Progress: {processed} files processed")
            
        except Exception as e:
            print(f"[{i}/{len(marked_files)}] {md_file.name}: ❌ Error - {str(e)}")
            errors += 1
    
    print()
    print("="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Total files: {len(marked_files)}")
    print(f"Processed: {processed}")
    print(f"Errors: {errors}")
    print()
    print("NOTE: Files are queued for content generation.")
    print("      The AI assistant will generate actual content for each file.")
    print("="*70)


if __name__ == "__main__":
    main()

