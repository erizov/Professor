#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete workflow script for algorithm content generation.

This script orchestrates the full pipeline:
1. Enhance READMEs and populate database with 4 records per algorithm
2. Generate school.en.md and univer.en.md from database
3. Generate school.ru.md from database
4. Generate univer.ru.md from database
"""

import sys
import argparse
import subprocess
import time
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"


def print_header(title: str) -> None:
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def print_step(step_num: int, total: int, description: str) -> None:
    """Print step information."""
    print(f"\n{'=' * 70}")
    print(f"STEP {step_num}/{total}: {description}")
    print(f"{'=' * 70}\n")


def run_script(script_name: str, description: str) -> bool:
    """Run a Python script and return success status."""
    script_path = SCRIPTS_DIR / script_name
    
    if not script_path.exists():
        print(f"ERROR: Script not found: {script_path}")
        return False
    
    print(f"Running: python {script_name}")
    print(f"Description: {description}\n")
    
    start_time = time.time()
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(ROOT),
            check=False,
            capture_output=False,
        )
        
        elapsed = time.time() - start_time
        
        if result.returncode == 0:
            print(f"\n✓ Completed in {elapsed:.1f} seconds")
            return True
        else:
            print(f"\n✗ Failed with exit code {result.returncode} after {elapsed:.1f} seconds")
            return False
            
    except KeyboardInterrupt:
        print("\n\n⚠ Interrupted by user")
        return False
    except Exception as e:
        print(f"\n✗ Error running script: {e}")
        return False


def main(run_all: bool = False):
    """Run the complete workflow.
    
    Args:
        run_all: If True, automatically continue all steps without prompting.
    """
    print_header("ALGORITHM CONTENT GENERATION WORKFLOW")
    
    print("This workflow will:")
    print("  1. Enhance READMEs and populate database (4 records per algorithm)")
    print("  2. Generate school.en.md and univer.en.md files")
    print("  3. Generate school.ru.md files")
    print("  4. Generate univer.ru.md files")
    
    if run_all:
        print("\n⚠ Running in automatic mode: all steps will continue even if errors occur")
    
    print("\nStarting workflow...")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    steps = [
        (
            "enhance_readmes_improved.py",
            "Enhance READMEs and populate database with 4 records per algorithm",
        ),
        (
            "generate_english_md_files.py",
            "Generate school.en.md and univer.en.md from database",
        ),
        (
            "generate_school_ru_md_improved.py",
            "Generate school.ru.md from database",
        ),
        (
            "generate_univer_ru_md.py",
            "Generate univer.ru.md from database",
        ),
    ]
    
    total_steps = len(steps)
    success_count = 0
    failed_steps = []
    
    for step_num, (script_name, description) in enumerate(steps, 1):
        print_step(step_num, total_steps, description)
        
        success = run_script(script_name, description)
        
        if success:
            success_count += 1
        else:
            failed_steps.append((step_num, script_name, description))
            if run_all:
                print("\n⚠ Step failed, but continuing automatically (--run-all mode)")
            else:
                print("\n⚠ Workflow will continue to next step...")
                response = input("\nContinue to next step? (y/n): ").strip().lower()
                if response != 'y':
                    print("\n⚠ Workflow stopped by user")
                    break
    
    # Summary
    print_header("WORKFLOW SUMMARY")
    
    print(f"Completed steps: {success_count}/{total_steps}")
    
    if failed_steps:
        print("\nFailed steps:")
        for step_num, script_name, description in failed_steps:
            print(f"  {step_num}. {script_name} - {description}")
    else:
        print("\n✓ All steps completed successfully!")
    
    print(f"\nWorkflow finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70 + "\n")
    
    return success_count == total_steps


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run complete algorithm content generation workflow"
    )
    parser.add_argument(
        "--run-all",
        action="store_true",
        help="Automatically continue all steps even if errors occur (no user prompts)",
    )
    
    args = parser.parse_args()
    
    try:
        success = main(run_all=args.run_all)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠ Workflow interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

