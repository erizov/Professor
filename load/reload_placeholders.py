"""
Reload all entries that have placeholders in specific columns:
- Algorithm Definition
- Simple Explanation
- Technical Description
- Example
"""
from algo_fetcher import (
    init_db, Session, enrich_description_from_web, 
    Algorithm, AlgorithmDescription, get_db_statistics, print_status,
    contains_placeholder, clear_placeholder_fields
)
from pathlib import Path
from datetime import datetime

def has_placeholders_in_target_fields(desc):
    """Check if entry has placeholders in target fields."""
    fields = [
        desc.simple_explanation,
        desc.algorithm_definition,
        desc.technical_description,
        desc.example,
        desc.where_its_used,
        desc.application,
        desc.step_by_step,
        desc.long_description,
        desc.short_description,
    ]
    return any(contains_placeholder(field) for field in fields)

def reload_all_placeholders(base_path: Path = None, status_interval: int = 300):
    """Reload all entries with placeholders in target columns."""
    init_db()
    session = Session()
    
    # Get all descriptions
    all_descriptions = session.query(AlgorithmDescription).all()
    
    # Filter entries that have placeholders in target fields
    entries_to_reload = []
    for desc in all_descriptions:
        if has_placeholders_in_target_fields(desc):
            entries_to_reload.append(desc)
    
    total_entries = len(entries_to_reload)
    total_web_success = 0
    total_web_failed = 0
    total_web_skipped = 0
    
    last_status_time = datetime.now()
    start_time = datetime.now()
    
    print("="*60)
    print("RELOADING ENTRIES WITH PLACEHOLDERS")
    print("="*60)
    print("Target columns: Algorithm Definition, Simple Explanation,")
    print("                 Technical Description, Example")
    print("="*60)
    print(f"Total entries to process: {total_entries}")
    print(f"Status updates every {status_interval} seconds")
    print("="*60)
    print()
    
    if total_entries == 0:
        print("No entries with placeholders found!")
        return
    
    for idx, desc in enumerate(entries_to_reload, 1):
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
        
        # Show which fields have placeholders
        placeholder_fields = []
        
        def field_has_placeholder(field_text):
            return contains_placeholder(field_text)
        
        if desc.simple_explanation and field_has_placeholder(desc.simple_explanation):
            placeholder_fields.append("Simple Explanation")
        if desc.algorithm_definition and field_has_placeholder(desc.algorithm_definition):
            placeholder_fields.append("Algorithm Definition")
        if desc.technical_description and field_has_placeholder(desc.technical_description):
            placeholder_fields.append("Technical Description")
        if desc.example and field_has_placeholder(desc.example):
            placeholder_fields.append("Example")
        
        fields_note = f" [{', '.join(placeholder_fields)}]" if placeholder_fields else ""
        
        print(f"[{idx}/{total_entries}] Reloading: {algorithm_name} ({desc.language.value}, {desc.level.value}){fields_note}")
        
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
        
        # Refresh description and clear any remaining placeholders
        session.refresh(desc)
        if clear_placeholder_fields(desc):
            session.add(desc)
            session.commit()
            print("  ∘ Removed placeholder-only sections after enrichment")
        
        # Rate limiting
        import time
        time.sleep(1.0)  # 1 second between requests
    
    # Final status
    print("\n" + "="*60)
    print("FINAL STATUS")
    print("="*60)
    print(f"Reload stats:")
    print(f"  - Success: {total_web_success}")
    print(f"  - Failed: {total_web_failed}")
    print(f"  - Skipped (no answer): {total_web_skipped}")
    print(f"  - Total processed: {total_entries}")
    print_status(session, "Final")

if __name__ == "__main__":
    import sys
    base_path = Path("..") if len(sys.argv) < 2 else Path(sys.argv[1])
    status_interval = 300 if len(sys.argv) < 3 else int(sys.argv[2])
    
    reload_all_placeholders(base_path=base_path, status_interval=status_interval)

