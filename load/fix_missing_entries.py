"""Fix missing entries for modelregistry and conditionalexecution."""
from algo_fetcher import (
    init_db, Session, Algorithm, AlgorithmDescription,
    load_from_markdown_files, find_all_algorithm_folders
)
from pathlib import Path

init_db()
session = Session()

# Find algorithm folders
base_path = Path("..")
algorithm_folders = find_all_algorithm_folders(base_path)

# Find the specific algorithm folders
modelregistry_folder = None
conditionalexecution_folder = None

for folder in algorithm_folders:
    if 'model_registry' in folder.name.lower() or 'modelregistry' in folder.name.lower():
        if 'advanced' not in folder.name.lower():
            modelregistry_folder = folder
    if 'conditional' in folder.name.lower() and 'execution' in folder.name.lower():
        conditionalexecution_folder = folder

print("Found algorithm folders:")
if modelregistry_folder:
    print(f"  Model Registry: {modelregistry_folder}")
    load_from_markdown_files(session, modelregistry_folder)
    print("  ✓ Loaded modelregistry")
else:
    print("  ✗ Model Registry folder not found")

if conditionalexecution_folder:
    print(f"  Conditional Execution: {conditionalexecution_folder}")
    load_from_markdown_files(session, conditionalexecution_folder)
    print("  ✓ Loaded conditionalexecution")
else:
    print("  ✗ Conditional Execution folder not found")

# Now re-enrich
from algo_fetcher import enrich_description_from_web, LangCode, EduLevel

algorithms_to_fix = []
if modelregistry_folder:
    algorithms_to_fix.append(('modelregistry', 'Model Registry'))
if conditionalexecution_folder:
    algorithms_to_fix.append(('conditionalexecution', 'Conditional Execution'))

for algo_name, canonical in algorithms_to_fix:
    print(f"\nRe-enriching {canonical}...")
    algo = session.get(Algorithm, algo_name)
    if not algo:
        print(f"  Algorithm {algo_name} not found after loading")
        continue
    
    descriptions = session.query(AlgorithmDescription).filter_by(
        algorithm_name=algo_name
    ).all()
    
    print(f"  Found {len(descriptions)} descriptions")
    
    for desc in descriptions:
        result = enrich_description_from_web(
            session,
            desc.algorithm_name,
            desc.language,
            desc.level,
            algo.canonical_label
        )
        status_icon = "✓" if result['status'] == 'success' else "⊘" if result['status'] == 'skipped' else "✗"
        print(f"  {status_icon} {desc.language.value}/{desc.level.value}: {result.get('reason', result['status'])}")
        import time
        time.sleep(1.0)

print("\nDone!")

