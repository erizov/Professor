#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remove duplicate algorithm folders, keeping the first occurrence.
"""

import sys
import shutil
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]


def find_duplicate_folders() -> dict:
    """Find duplicate algorithm folder names with their paths."""
    algorithm_folders = []
    
    for semester_dir in sorted(ROOT.glob("semester_*")):
        if not semester_dir.is_dir():
            continue
        if any(x in str(semester_dir) for x in ["__pycache__", ".git"]):
            continue
        
        semester_num = int(semester_dir.name.split("_")[1])
        
        for lecture_dir in sorted(semester_dir.iterdir()):
            if not lecture_dir.is_dir():
                continue
            if "lecture_" not in lecture_dir.name:
                continue
            
            lecture_num = int(lecture_dir.name.split("_")[1])
            
            for algo_dir in sorted(lecture_dir.iterdir()):
                if not algo_dir.is_dir():
                    continue
                if algo_dir.name.startswith("lecture_"):
                    continue
                if any(x in algo_dir.name for x in ["__pycache__", ".git"]):
                    continue
                
                algorithm_folders.append({
                    'name': algo_dir.name,
                    'path': algo_dir,
                    'semester': semester_num,
                    'lecture': lecture_num,
                    'full_path': str(algo_dir)
                })
    
    # Group by name
    folders_by_name = defaultdict(list)
    for folder_info in algorithm_folders:
        folders_by_name[folder_info['name']].append(folder_info)
    
    # Find duplicates
    duplicates = {}
    for name, folders in folders_by_name.items():
        if len(folders) > 1:
            # Sort by semester, then lecture
            folders.sort(key=lambda x: (x['semester'], x['lecture']))
            duplicates[name] = folders
    
    return duplicates


def remove_duplicates(dry_run: bool = True) -> None:
    """Remove duplicate folders, keeping the first occurrence."""
    duplicates = find_duplicate_folders()
    
    print("="*70)
    print("REMOVING DUPLICATE ALGORITHM FOLDERS")
    print("="*70)
    print(f"\nFound {len(duplicates)} duplicate algorithm names")
    print(f"Mode: {'DRY RUN' if dry_run else 'DELETE'}\n")
    
    total_to_remove = 0
    
    for name, folders in sorted(duplicates.items()):
        keep = folders[0]
        to_remove = folders[1:]
        
        print(f"\n{name}:")
        print(f"  KEEP: {keep['full_path']} (semester {keep['semester']}, lecture {keep['lecture']})")
        
        for folder in to_remove:
            print(f"  REMOVE: {folder['full_path']} (semester {folder['semester']}, lecture {folder['lecture']})")
            total_to_remove += 1
            
            if not dry_run:
                try:
                    shutil.rmtree(folder['path'])
                    print(f"    [DELETED]")
                except Exception as e:
                    print(f"    [ERROR] Failed to delete: {e}")
    
    print(f"\n{'='*70}")
    print(f"Summary:")
    print(f"  Duplicate algorithms: {len(duplicates)}")
    print(f"  Folders to remove: {total_to_remove}")
    print(f"  Mode: {'DRY RUN - No files deleted' if dry_run else 'DELETED'}")
    print(f"{'='*70}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Remove duplicate algorithm folders")
    parser.add_argument("--execute", action="store_true", help="Actually delete files (default is dry run)")
    args = parser.parse_args()
    
    remove_duplicates(dry_run=not args.execute)

