#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate algorithm briefs using OpenAI API proxy.

For each algorithm folder:
- Creates 4 prompts (school/en, school/ru, univer/en, univer/ru)
- Calls OpenAI API to generate briefs
- Saves results to appropriate MD files
- Stores prompts in database for future reports
"""

import os
import sys
import sqlite3
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from openai import OpenAI

# Fix Windows console encoding
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding='utf-8', errors='replace'
    )
    sys.stderr = io.TextIOWrapper(
        sys.stderr.buffer, encoding='utf-8', errors='replace'
    )

# Add project root to path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.config import OPENAI_API_KEY, OPENAI_API_BASE


# Database setup
DB_PATH = ROOT / "database" / "algorithm_prompts.db"


def init_database() -> None:
    """Initialize database with prompts table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS algorithm_prompts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            algorithm_name TEXT NOT NULL,
            prompt_school_en TEXT NOT NULL,
            prompt_school_ru TEXT NOT NULL,
            prompt_univer_en TEXT NOT NULL,
            prompt_univer_ru TEXT NOT NULL,
            date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(algorithm_name)
        )
    """)
    
    conn.commit()
    conn.close()


def find_all_algorithm_folders() -> List[Path]:
    """Find all algorithm folders in the repository."""
    algorithm_folders = []
    
    for semester_dir in ROOT.glob("semester_*"):
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


def generate_prompts(algorithm_name: str) -> Dict[str, str]:
    """Generate 4 prompts for an algorithm."""
    # Convert snake_case to readable name
    readable_name = algorithm_name.replace("_", " ").title()
    
    prompts = {
        "school_en": f"""Create a brief about the "{readable_name}" algorithm for school students:

- Explain the principle of operation in very simple language.
- Specify the algorithm complexity in O-notation.
- Where is it used in practice.
- What can the algorithm be compared to.
- Minimal code example (only important parts).
- Common mistakes.
- Recommended literature.

Structure the brief using subheadings, lists, and short examples.""",
        
        "school_ru": f"""Составь бриф для школьников об алгоритме "{readable_name}" (простыми словами):

- Объясни принцип работы очень простым языком.
- Укажи сложность алгоритма в O-нотации.
- Где применяется на практике.
- С чем можно сравнить алгоритм.
- Минимальный пример кода (только важное).
- Частые ошибки.
- Рекомендуемая литература.

Структурируй бриф, используй подзаголовки, списки и короткие примеры.""",
        
        "univer_en": f"""Create a brief about the "{readable_name}" algorithm for college students:

- Specify convergence speed and complexity estimate in O-notation.
- Where the algorithm is used in real frameworks and software.
- What it's similar to in concept.
- Which algorithms it's often used with.
- Key code (only important parts).
- Common application errors.
- Recommended literature.

Structure the brief using subheadings, lists, and short examples.""",
        
        "univer_ru": f"""Составь бриф для студентов колледжа об алгоритме "{readable_name}":

- Укажи скорость схождения и оценку сложности по O-нотации.
- Где применяется алгоритм в реальных фреймворках и ПО.
- На что похож по идее.
- С какими алгоритмами часто используется.
- Приведи ключевой код (только важные части).
- Распространённые ошибки применения.
- Рекомендуемая литература.

Структурируй бриф, используй подзаголовки, списки и короткие примеры."""
    }
    
    return prompts


def save_prompts_to_db(
    algorithm_name: str,
    prompts: Dict[str, str]
) -> None:
    """Save prompts to database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT OR REPLACE INTO algorithm_prompts 
        (algorithm_name, prompt_school_en, prompt_school_ru, 
         prompt_univer_en, prompt_univer_ru, date_updated)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        algorithm_name,
        prompts["school_en"],
        prompts["school_ru"],
        prompts["univer_en"],
        prompts["univer_ru"],
        datetime.now().isoformat()
    ))
    
    conn.commit()
    conn.close()


def call_openai_api(prompt: str) -> Optional[str]:
    """Call OpenAI API with the prompt."""
    try:
        client = OpenAI(
            api_key=OPENAI_API_KEY,
            base_url=OPENAI_API_BASE
        )
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"  [ERROR] API Error: {e}")
        return None


def save_brief_to_file(
    algorithm_folder: Path,
    level: str,
    language: str,
    content: str
) -> bool:
    """Save brief content to appropriate MD file."""
    filename = f"{level}.{language}.md"
    filepath = algorithm_folder / filename
    
    try:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"  [ERROR] Failed to save {filepath}: {e}")
        return False


def process_algorithm(
    algorithm_folder: Path,
    algorithm_name: str
) -> Tuple[bool, int]:
    """
    Process one algorithm: generate prompts, call API, save results.
    
    Returns: (success, prompts_processed)
    """
    print(f"\n{'='*70}")
    print(f"Processing: {algorithm_name}")
    print(f"Folder: {algorithm_folder}")
    print(f"{'='*70}")
    
    # Generate prompts
    prompts = generate_prompts(algorithm_name)
    
    # Save prompts to database
    save_prompts_to_db(algorithm_name, prompts)
    
    # Process each prompt
    prompt_configs = [
        ("school", "en", prompts["school_en"]),
        ("school", "ru", prompts["school_ru"]),
        ("univer", "en", prompts["univer_en"]),
        ("univer", "ru", prompts["univer_ru"])
    ]
    
    success_count = 0
    total_prompts = len(prompt_configs)
    
    for level, lang, prompt_text in prompt_configs:
        print(f"\n  [{level}.{lang}] Calling OpenAI API...")
        
        # Call API
        result = call_openai_api(prompt_text)
        
        if result is None:
            print(f"  [FAIL] Failed to get response for {level}.{lang}")
            # If API call fails, quit immediately as requested
            print("\n[FAIL] API call failed. Stopping immediately.")
            return False, success_count
        
        # Save to file
        if save_brief_to_file(algorithm_folder, level, lang, result):
            print(f"  [OK] Saved {level}.{lang}.md")
            success_count += 1
        else:
            print(f"  [FAIL] Failed to save {level}.{lang}.md")
            return False, success_count
        
        # Small delay to avoid rate limiting
        time.sleep(0.5)
    
    print(f"\n[OK] Completed: {success_count}/{total_prompts} prompts processed")
    return True, success_count


def main() -> int:
    """Main execution."""
    print("="*70)
    print("ALGORITHM BRIEF GENERATOR")
    print("="*70)
    
    # Check API configuration
    if not OPENAI_API_KEY:
        print("[ERROR] OPENAI_API_KEY not found in .env file")
        return 1
    
    if not OPENAI_API_BASE:
        print("[ERROR] OPENAI_API_BASE not found in .env file")
        return 1
    
    print(f"\nAPI Configuration:")
    print(f"  Base URL: {OPENAI_API_BASE}")
    print(f"  API Key: {OPENAI_API_KEY[:7]}...{OPENAI_API_KEY[-4:]}")
    
    # Initialize database
    print("\nInitializing database...")
    init_database()
    print("[OK] Database initialized")
    
    # Find all algorithm folders
    print("\nFinding algorithm folders...")
    algorithm_folders = find_all_algorithm_folders()
    print(f"[OK] Found {len(algorithm_folders)} algorithm folders")
    
    if not algorithm_folders:
        print("[ERROR] No algorithm folders found")
        return 1
    
    # Process algorithms
    print("\n" + "="*70)
    print("STARTING PROCESSING")
    print("="*70)
    
    start_time = time.time()
    last_report_time = start_time
    processed_count = 0
    total_success = 0
    total_prompts = 0
    
    for i, algo_folder in enumerate(algorithm_folders, 1):
        algorithm_name = algo_folder.name
        
        # Process algorithm
        success, prompts_processed = process_algorithm(
            algo_folder,
            algorithm_name
        )
        
        if not success:
            print(f"\n[FAIL] Failed processing {algorithm_name}. Stopping.")
            return 1
        
        processed_count += 1
        total_success += 1
        total_prompts += prompts_processed
        
        # Progress reporting
        current_time = time.time()
        elapsed = current_time - start_time
        
        # Report every 10 prompts for first hour, then every 100
        should_report = False
        if elapsed < 3600:  # First hour
            if processed_count % 10 == 0:
                should_report = True
            elif current_time - last_report_time >= 600:  # 10 minutes
                should_report = True
        else:  # After first hour
            if processed_count % 100 == 0:
                should_report = True
            elif current_time - last_report_time >= 1800:  # 30 minutes
                should_report = True
        
        if should_report:
            print(f"\n{'='*70}")
            print(f"PROGRESS REPORT")
            print(f"{'='*70}")
            print(f"Algorithms processed: {processed_count}/{len(algorithm_folders)}")
            print(f"Total prompts: {total_prompts}")
            print(f"Time elapsed: {elapsed/60:.1f} minutes")
            print(f"Average time per algorithm: {elapsed/processed_count:.1f} seconds")
            print(f"{'='*70}\n")
            last_report_time = current_time
    
    # Final summary
    total_time = time.time() - start_time
    print("\n" + "="*70)
    print("FINAL SUMMARY")
    print("="*70)
    print(f"Total algorithms processed: {total_success}")
    print(f"Total prompts generated: {total_prompts}")
    print(f"Total time: {total_time/60:.1f} minutes")
    print(f"Average time per algorithm: {total_time/total_success:.1f} seconds")
    print("="*70)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

