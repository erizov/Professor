#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Quick progress checker for enhancement process."""

import re
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
LOG_FILE = ROOT / "logs" / "enhancement_progress.log"


def check_progress():
    """Check current progress from log file."""
    if not LOG_FILE.exists():
        print("Log file not found. Process may not have started yet.")
        return
    
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    if not lines:
        print("Log file is empty. Process is starting...")
        return
    
    # Count enhancements
    enhanced_count = 0
    total_processed = 0
    section_counts = {}
    recent = []
    
    for line in lines:
        # Enhanced line
        match = re.search(
            r"\[(\d+)/(\d+)\].*✓ Enhanced: (\w+).*\(([^)]+)\)", line
        )
        if match:
            enhanced_count += 1
            total_processed = int(match.group(1))
            algorithm = match.group(3)
            sections = [s.strip() for s in match.group(4).split(",")]
            recent.append((algorithm, sections, total_processed))
            
            for section in sections:
                section_counts[section] = section_counts.get(section, 0) + 1
        
        # Progress line
        match = re.search(r"\[PROGRESS\].*Enhanced (\d+)/(\d+)", line)
        if match:
            enhanced_count = int(match.group(1))
            total_processed = int(match.group(2))
        
        # Complete line
        match = re.search(r"\[COMPLETE\].*Enhanced (\d+)/(\d+)", line)
        if match:
            enhanced_count = int(match.group(1))
            total_processed = int(match.group(2))
            print("✅ PROCESS COMPLETE!")
            break
    
    # Print status
    print(f"\n📊 Enhancement Progress - {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 60)
    print(f"Processed: {total_processed} files")
    print(f"Enhanced: {enhanced_count} files")
    if total_processed > 0:
        percentage = (enhanced_count * 100) // total_processed
        print(f"Success Rate: {percentage}%")
    
    if section_counts:
        print("\nTop Enhanced Sections:")
        for section, count in sorted(
            section_counts.items(), key=lambda x: -x[1]
        )[:5]:
            print(f"  - {section}: {count}")
    
    if recent:
        print("\nRecent Enhancements (last 5):")
        for algo, sections, idx in recent[-5:]:
            print(f"  - {algo} ({', '.join(sections)}) [{idx}]")
    
    print("=" * 60)


if __name__ == "__main__":
    check_progress()


