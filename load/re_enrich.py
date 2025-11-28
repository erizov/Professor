"""
Re-enrich all database entries with web data, replacing placeholders.
This script will check all entries and enrich them with web data if they contain placeholders.
"""
from algo_fetcher import (
    init_db, Session, enrich_description_from_web, 
    get_db_statistics, print_status, Algorithm, AlgorithmDescription
)
from pathlib import Path
from datetime import datetime
import re

def has_placeholders(text):
    """Check if text contains placeholder patterns."""
    if not text:
        return False
    placeholder_patterns = [
        r'\[specific purpose\]', r'\[specific mechanism\]', r'\[конкретная цель\]',
        r'\[конкретный механизм\]', r'\[.*?\]', r'placeholder', r'заполнитель',
        r'конкретный алгоритм/техника', r'конкретных задач в области',
        r'для решения конкретных задач', r'в production-системах для'
    ]
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in placeholder_patterns)

def check_entry_has_placeholders(desc):
    """Check if an entry has placeholders in any relevant field."""
    fields_to_check = []
    
    if desc.level.value == 'school':
        fields_to_check = [
            desc.simple_explanation,
            desc.where_its_used,
            desc.example
        ]
    else:
        fields_to_check = [
            desc.algorithm_definition,
            desc.technical_description,
            desc.application,
            desc.step_by_step
        ]
    
    return any(has_placeholders(field) for field in fields_to_check if field)

def re_enrich_all(base_path: Path = None, status_interval: int = 300):
    """Re-enrich all entries that have placeholders."""
    init_db()
    session = Session()
    
    # Get all descriptions
    all_descriptions = session.query(AlgorithmDescription).all()
    
    # Filter entries that have placeholders or are from local_markdown
    entries_to_enrich = []
    for desc in all_descriptions:
        if desc.source_site == "local_markdown" or check_entry_has_placeholders(desc):
            entries_to_enrich.append(desc)
    
    total_entries = len(entries_to_enrich)
    total_web_success = 0
    total_web_failed = 0
    total_web_skipped = 0
    
    last_status_time = datetime.now()
    start_time = datetime.now()
    
    print("="*60)
    print("RE-ENRICHMENT PROCESS")
    print("="*60)
    print(f"Total entries to process: {total_entries}")
    print(f"Status updates every {status_interval} seconds")
    print("="*60)
    print()
    
    for idx, desc in enumerate(entries_to_enrich, 1):
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
        
        # Check if entry has placeholders
        has_placeholders_flag = check_entry_has_placeholders(desc)
        placeholder_note = " (has placeholders)" if has_placeholders_flag else ""
        
        print(f"[{idx}/{total_entries}] Enriching: {algorithm_name} ({desc.language.value}, {desc.level.value}){placeholder_note}")
        
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
            print(f"  ✓ Success: {result.get('source', 'unknown')}")
        elif result['status'] == 'skipped':
            total_web_skipped += 1
            print(f"  ⊘ Skipped: {result.get('reason', 'Unknown reason')}")
        else:
            total_web_failed += 1
            print(f"  ✗ Failed: {result.get('reason', 'Unknown error')}")
        
        # Rate limiting
        import time
        time.sleep(1.0)  # 1 second between requests
    
    # Final status
    print("\n" + "="*60)
    print("FINAL STATUS")
    print("="*60)
    print(f"Re-enrichment stats:")
    print(f"  - Success: {total_web_success}")
    print(f"  - Failed: {total_web_failed}")
    print(f"  - Skipped (no answer): {total_web_skipped}")
    print(f"  - Total processed: {total_entries}")
    print_status(session, "Final")

if __name__ == "__main__":
    import sys
    base_path = Path("..") if len(sys.argv) < 2 else Path(sys.argv[1])
    status_interval = 300 if len(sys.argv) < 3 else int(sys.argv[2])
    
    re_enrich_all(base_path=base_path, status_interval=status_interval)

