#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sandbox management utilities.
Handles file system operations for sandboxes.
"""

from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
SANDBOXES_DIR = ROOT / "sandboxes"


def create_user_sandbox_dir(user_id: int) -> Path:
    """
    Create sandbox directory for user if it doesn't exist.
    
    Args:
        user_id: User ID
        
    Returns:
        Path to user's sandbox directory
    """
    user_dir = SANDBOXES_DIR / str(user_id)
    user_dir.mkdir(parents=True, exist_ok=True)
    return user_dir


def get_sandbox_path(
    user_id: int, 
    algorithm_path: str, 
    language: str
) -> Path:
    """
    Get path to sandbox for specific algorithm.
    
    Args:
        user_id: User ID
        algorithm_path: Path to original algorithm (e.g., 
                       "semester_01/lecture_01/bubble_sort/algorithm.py")
        language: 'python' or 'java'
        
    Returns:
        Path to sandbox directory
    """
    user_dir = create_user_sandbox_dir(user_id)
    
    # Normalize algorithm path (replace slashes with underscores)
    # Remove file extension and path separators
    safe_path = algorithm_path.replace('/', '_').replace('\\', '_')
    safe_path = safe_path.replace('.py', '').replace('.java', '')
    
    sandbox_dir = user_dir / f"{safe_path}_{language}"
    sandbox_dir.mkdir(parents=True, exist_ok=True)
    return sandbox_dir


def get_sandbox_dir(user_id: int, sandbox_id: int) -> Path:
    """
    Get path to sandbox directory by sandbox ID.
    This is used when we only have the sandbox_id from the database.
    
    Args:
        user_id: User ID
        sandbox_id: Sandbox ID from database
        
    Returns:
        Path to sandbox directory
    """
    user_dir = create_user_sandbox_dir(user_id)
    sandbox_dir = user_dir / str(sandbox_id)
    return sandbox_dir


def get_version_path(
    user_id: int,
    algorithm_path: str,
    language: str,
    version_number: int
) -> Path:
    """
    Get path to specific version directory.
    
    Args:
        user_id: User ID
        algorithm_path: Path to original algorithm
        language: 'python' or 'java'
        version_number: Version number
        
    Returns:
        Path to version directory
    """
    sandbox_dir = get_sandbox_path(user_id, algorithm_path, language)
    version_dir = sandbox_dir / f"version_{version_number}"
    version_dir.mkdir(parents=True, exist_ok=True)
    return version_dir


def save_version_code(
    user_id: int,
    algorithm_path: str,
    language: str,
    version_number: int,
    code_content: str
) -> Path:
    """
    Save code to version directory.
    
    Args:
        user_id: User ID
        algorithm_path: Path to original algorithm
        language: 'python' or 'java'
        version_number: Version number
        code_content: Code content to save
        
    Returns:
        Path to saved file
    """
    version_dir = get_version_path(user_id, algorithm_path, language, 
                                   version_number)
    
    file_name = "algorithm.py" if language == "python" else "Algorithm.java"
    file_path = version_dir / file_name
    
    file_path.write_text(code_content, encoding='utf-8')
    return file_path


def load_version_code(
    user_id: int,
    algorithm_path: str,
    language: str,
    version_number: int
) -> Optional[str]:
    """
    Load code from version directory.
    
    Args:
        user_id: User ID
        algorithm_path: Path to original algorithm
        language: 'python' or 'java'
        version_number: Version number
        
    Returns:
        Code content or None if not found
    """
    version_dir = get_version_path(user_id, algorithm_path, language, 
                                   version_number)
    
    file_name = "algorithm.py" if language == "python" else "Algorithm.java"
    file_path = version_dir / file_name
    
    if file_path.exists():
        return file_path.read_text(encoding='utf-8')
    return None


def list_user_sandboxes(user_id: int) -> list:
    """
    List all sandboxes for a user.
    
    Args:
        user_id: User ID
        
    Returns:
        List of sandbox directory paths
    """
    user_dir = SANDBOXES_DIR / str(user_id)
    if not user_dir.exists():
        return []
    
    sandboxes = []
    for item in user_dir.iterdir():
        if item.is_dir():
            sandboxes.append(item)
    
    return sorted(sandboxes)

