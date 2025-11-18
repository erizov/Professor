#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rename semester folders from semester_01 to semester_01, etc.

This script:
1. Renames all semester folders to use zero-padded numbers
2. Updates all references in files (markdown, Python, etc.)
"""

from pathlib import Path
from typing import List, Dict
import re
import shutil


def get_semester_folders(base_path: Path) -> List[Path]:
    """Get all semester folders."""
    folders = []
    for item in base_path.iterdir():
        if item.is_dir() and item.name.startswith('semester_'):
            try:
                num = int(item.name.split('_')[1])
                if 1 <= num <= 16:
                    folders.append((num, item))
            except (ValueError, IndexError):
                pass
    return sorted(folders, key=lambda x: x[0])


def rename_semester_folders(base_path: Path) -> Dict[str, str]:
    """Rename semester folders and return mapping of old to new names."""
    folders = get_semester_folders(base_path)
    rename_map = {}
    
    for num, folder in folders:
        old_name = folder.name
        new_name = f"semester_{num:02d}"
        
        if old_name != new_name:
            new_path = folder.parent / new_name
            if new_path.exists():
                print(f"Warning: {new_path} already exists, skipping {old_name}")
                continue
            
            print(f"Renaming {old_name} -> {new_name}")
            folder.rename(new_path)
            rename_map[old_name] = new_name
    
    return rename_map


def update_file_references(file_path: Path, rename_map: Dict[str, str]) -> bool:
    """Update references to semester folders in a file."""
    try:
        content = file_path.read_text(encoding='utf-8')
        original_content = content
        
        # Update all references
        for old_name, new_name in rename_map.items():
            # Replace in paths: semester_01/ -> semester_01/
            content = re.sub(
                rf'\b{re.escape(old_name)}\b',
                new_name,
                content
            )
        
        if content != original_content:
            file_path.write_text(content, encoding='utf-8')
            return True
        return False
    except Exception as e:
        print(f"Error updating {file_path}: {e}")
        return False


def find_files_to_update(base_path: Path) -> List[Path]:
    """Find all files that might contain semester references."""
    files_to_update = []
    
    # File extensions to check
    extensions = {'.md', '.py', '.html', '.txt', '.yml', '.yaml', '.json', '.java'}
    
    # Directories to skip
    skip_dirs = {'.git', '__pycache__', 'target', 'node_modules', '.pytest_cache'}
    
    for file_path in base_path.rglob('*'):
        if file_path.is_file():
            # Skip files in skip directories
            if any(skip in file_path.parts for skip in skip_dirs):
                continue
            
            # Check if file has relevant extension
            if file_path.suffix in extensions:
                files_to_update.append(file_path)
    
    return files_to_update


def main():
    """Main function to rename folders and update references."""
    base_path = Path('.')
    
    print("Step 1: Renaming semester folders...")
    rename_map = rename_semester_folders(base_path)
    
    if not rename_map:
        print("No folders to rename.")
        return
    
    print(f"\nRenamed {len(rename_map)} folders:")
    for old, new in sorted(rename_map.items()):
        print(f"  {old} -> {new}")
    
    print("\nStep 2: Finding files to update...")
    files_to_update = find_files_to_update(base_path)
    print(f"Found {len(files_to_update)} files to check")
    
    print("\nStep 3: Updating file references...")
    updated_count = 0
    for file_path in files_to_update:
        if update_file_references(file_path, rename_map):
            updated_count += 1
            if updated_count % 50 == 0:
                print(f"  Updated {updated_count} files...")
    
    print(f"\nCompleted!")
    print(f"  Folders renamed: {len(rename_map)}")
    print(f"  Files updated: {updated_count}")


if __name__ == "__main__":
    main()

