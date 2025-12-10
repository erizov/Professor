#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Find duplicate algorithms in database and folders.
"""

import sys
import sqlite3
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "database" / "algorithm_prompts.db"


def find_duplicates_in_database() -> dict:
    """Find duplicate algorithm names in database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT algorithm_name FROM algorithm_prompts ORDER BY algorithm_name")
    all_names = [row[0] for row in cursor.fetchall()]
    
    # Count occurrences
    name_counts = defaultdict(int)
    for name in all_names:
        name_counts[name] += 1
    
    duplicates = {name: count for name, count in name_counts.items() if count > 1}
    
    conn.close()
    return duplicates, all_names


def find_duplicates_in_folders() -> dict:
    """Find duplicate algorithm folder names."""
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
                
                algorithm_folders.append((algo_dir.name, algo_dir))
    
    # Group by name
    folders_by_name = defaultdict(list)
    for name, path in algorithm_folders:
        folders_by_name[name].append(path)
    
    duplicates = {name: paths for name, paths in folders_by_name.items() if len(paths) > 1}
    
    return duplicates, algorithm_folders


def main():
    """Main execution."""
    print("="*70)
    print("FINDING DUPLICATE ALGORITHMS")
    print("="*70)
    
    # Check database
    print("\n[1] Checking database...")
    db_duplicates, db_all_names = find_duplicates_in_database()
    
    if db_duplicates:
        print(f"Found {len(db_duplicates)} duplicate names in database:")
        for name, count in sorted(db_duplicates.items()):
            print(f"  {name}: {count} entries")
    else:
        print("No duplicates found in database (all unique)")
    
    print(f"\nTotal algorithms in database: {len(db_all_names)}")
    print(f"Unique algorithms in database: {len(set(db_all_names))}")
    
    # Check folders
    print("\n[2] Checking folders...")
    folder_duplicates, folder_list = find_duplicates_in_folders()
    
    if folder_duplicates:
        print(f"\nFound {len(folder_duplicates)} duplicate folder names:")
        for name, paths in sorted(folder_duplicates.items()):
            print(f"\n  {name} ({len(paths)} folders):")
            for path in paths:
                print(f"    - {path}")
    else:
        print("No duplicate folder names found")
    
    folder_names = [name for name, _ in folder_list]
    print(f"\nTotal algorithm folders: {len(folder_names)}")
    print(f"Unique algorithm folder names: {len(set(folder_names))}")
    
    # Compare
    print("\n[3] Comparing database vs folders...")
    db_unique = set(db_all_names)
    folder_unique = set(folder_names)
    
    only_in_db = db_unique - folder_unique
    only_in_folders = folder_unique - db_unique
    in_both = db_unique & folder_unique
    
    print(f"\nAlgorithms only in database: {len(only_in_db)}")
    if only_in_db:
        for name in sorted(only_in_db)[:10]:
            print(f"  - {name}")
        if len(only_in_db) > 10:
            print(f"  ... and {len(only_in_db) - 10} more")
    
    print(f"\nAlgorithms only in folders: {len(only_in_folders)}")
    if only_in_folders:
        for name in sorted(only_in_folders)[:10]:
            print(f"  - {name}")
        if len(only_in_folders) > 10:
            print(f"  ... and {len(only_in_folders) - 10} more")
    
    print(f"\nAlgorithms in both: {len(in_both)}")
    
    return db_duplicates, folder_duplicates, only_in_db, only_in_folders


if __name__ == "__main__":
    main()

