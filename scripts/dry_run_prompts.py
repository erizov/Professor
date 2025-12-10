#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dry run: Generate prompts for all algorithms and save to database.
No actual OpenAI API calls - just prompt generation and database storage.
"""

import sys
import sqlite3
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict

# Add project root to path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Fix Windows console encoding
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding='utf-8', errors='replace'
    )


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


def process_algorithm(
    algorithm_folder: Path,
    algorithm_name: str
) -> bool:
    """Process one algorithm: generate prompts and save to database."""
    # Generate prompts
    prompts = generate_prompts(algorithm_name)
    
    # Save prompts to database
    save_prompts_to_db(algorithm_name, prompts)
    
    return True


def main() -> int:
    """Main execution."""
    print("="*70)
    print("DRY RUN: PROMPT GENERATION (NO API CALLS)")
    print("="*70)
    
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
    print("GENERATING PROMPTS")
    print("="*70)
    
    start_time = time.time()
    processed_count = 0
    last_report_time = start_time
    
    for i, algo_folder in enumerate(algorithm_folders, 1):
        algorithm_name = algo_folder.name
        
        # Process algorithm
        success = process_algorithm(algo_folder, algorithm_name)
        
        if success:
            processed_count += 1
        
        # Progress reporting every 100 algorithms or every 30 seconds
        current_time = time.time()
        if processed_count % 100 == 0 or (current_time - last_report_time) >= 30:
            elapsed = current_time - start_time
            rate = processed_count / elapsed if elapsed > 0 else 0
            remaining = len(algorithm_folders) - processed_count
            eta = remaining / rate if rate > 0 else 0
            
            print(f"\nProgress: {processed_count}/{len(algorithm_folders)} "
                  f"({processed_count/len(algorithm_folders)*100:.1f}%) | "
                  f"Rate: {rate:.1f} alg/sec | "
                  f"ETA: {eta:.0f}s")
            last_report_time = current_time
    
    # Final summary
    total_time = time.time() - start_time
    
    # Get database stats
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM algorithm_prompts")
    db_count = cursor.fetchone()[0]
    conn.close()
    
    print("\n" + "="*70)
    print("DRY RUN COMPLETE")
    print("="*70)
    print(f"\nAlgorithms processed: {processed_count}")
    print(f"Prompts generated: {processed_count * 4}")
    print(f"Prompts in database: {db_count}")
    print(f"\nTotal time: {total_time:.2f} seconds")
    print(f"Average time per algorithm: {total_time/processed_count*1000:.2f} ms")
    print(f"Processing rate: {processed_count/total_time:.1f} algorithms/second")
    print(f"Prompts per second: {processed_count*4/total_time:.1f}")
    print("\n" + "="*70)
    print("\n[OK] All prompts generated and saved to database.")
    print("Ready for actual API calls when balance is available.")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

