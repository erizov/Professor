"""
Re-enrich specific algorithms that had incorrect entries deleted.
"""
from algo_fetcher import (
    init_db, Session, enrich_description_from_web, 
    Algorithm, AlgorithmDescription
)
from pathlib import Path
from datetime import datetime

def re_enrich_algorithm(algorithm_name: str):
    """Re-enrich a specific algorithm."""
    from algo_fetcher import normalize_algorithm_name
    
    init_db()
    session = Session()
    
    # Normalize the algorithm name
    normalized_name = normalize_algorithm_name(algorithm_name)
    
    # Find the algorithm
    algo = session.get(Algorithm, normalized_name)
    if not algo:
        # Try searching by canonical label
        algo = session.query(Algorithm).filter(
            Algorithm.canonical_label.ilike(f"%{algorithm_name}%")
        ).first()
        if not algo:
            print(f"Algorithm '{algorithm_name}' (normalized: '{normalized_name}') not found")
            return
    
    # Get all descriptions for this algorithm using the found algorithm's name
    algo_key = algo.algorithm_name
    descriptions = session.query(AlgorithmDescription).filter_by(
        algorithm_name=algo_key
    ).all()
    
    print(f"Re-enriching algorithm: {algo.canonical_label}")
    print(f"Found {len(descriptions)} descriptions\n")
    
    success_count = 0
    skipped_count = 0
    failed_count = 0
    
    for desc in descriptions:
        print(f"Processing: {desc.language.value}, {desc.level.value}")
        
        result = enrich_description_from_web(
            session,
            desc.algorithm_name,
            desc.language,
            desc.level,
            algo.canonical_label
        )
        
        if result['status'] == 'success':
            success_count += 1
            print(f"  ✓ Success: {result.get('source', 'unknown')}")
        elif result['status'] == 'skipped':
            skipped_count += 1
            print(f"  ⊘ Skipped: {result.get('reason', 'Unknown')}")
        else:
            failed_count += 1
            print(f"  ✗ Failed: {result.get('reason', 'Unknown')}")
        
        import time
        time.sleep(1.0)
    
    print(f"\nSummary:")
    print(f"  Success: {success_count}")
    print(f"  Skipped: {skipped_count}")
    print(f"  Failed: {failed_count}")

if __name__ == "__main__":
    import sys
    
    # Algorithms that had incorrect entries
    algorithms_to_fix = ['conditionalexecution', 'modelregistry']
    
    if len(sys.argv) > 1:
        algorithms_to_fix = sys.argv[1:]
    
    for algo_name in algorithms_to_fix:
        print(f"\n{'='*60}")
        re_enrich_algorithm(algo_name)
        print(f"{'='*60}\n")

