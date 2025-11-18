#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto commit and push script - runs without confirmation.

Usage: python scripts/auto_commit_push.py [commit_message]
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: list, check: bool = True) -> tuple[int, str, str]:
    """Run a shell command and return exit code, stdout, stderr."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=check
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return e.returncode, e.stdout, e.stderr


def auto_commit_push(commit_message: str = None) -> None:
    """Auto commit and push changes."""
    if commit_message is None:
        commit_message = "Auto commit: Update algorithm implementations"
    
    print("Staging all changes...")
    exit_code, stdout, stderr = run_command(['git', 'add', '-A'], check=False)
    if exit_code != 0:
        print(f"Error staging: {stderr}")
        return
    
    print("Checking for changes...")
    exit_code, stdout, stderr = run_command(['git', 'status', '--short'], check=False)
    if not stdout.strip():
        print("No changes to commit.")
        return
    
    print(f"Committing with message: {commit_message}")
    exit_code, stdout, stderr = run_command(
        ['git', 'commit', '-m', commit_message],
        check=False
    )
    if exit_code != 0:
        print(f"Error committing: {stderr}")
        return
    
    print("Pushing to remote...")
    exit_code, stdout, stderr = run_command(['git', 'push'], check=False)
    if exit_code != 0:
        print(f"Error pushing: {stderr}")
        return
    
    print("Successfully committed and pushed!")


if __name__ == "__main__":
    commit_msg = sys.argv[1] if len(sys.argv) > 1 else None
    auto_commit_push(commit_msg)

