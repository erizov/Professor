#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Continuous progress reporter - reports every 5 minutes.
This script will keep running and report progress automatically.
"""

import time
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict

ROOT = Path(__file__).resolve().parents[1]
LOG_FILE = ROOT / "logs" / "enhancement_progress.log"


def get_progress_stats() -> Dict:
    """Get current progress statistics from log file."""
    stats = {
        "total_enhanced": 0,
        "total_processed": 0,
        "section_counts": {},
        "recent_enhancements": [],
        "complete": False,
        "last_update": None,
        "has_activity": False,
    }
    
    if not LOG_FILE.exists():
        return stats
    
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        if not lines:
            return stats
        
        stats["has_activity"] = True
        
        for line in lines:
            # Enhanced line
            match = re.search(
                r"\[(\d+)/(\d+)\].*✓ Enhanced: (\w+).*\(([^)]+)\)", line
            )
            if match:
                stats["total_enhanced"] += 1
                stats["total_processed"] = int(match.group(1))
                algorithm = match.group(3)
                sections = [s.strip() for s in match.group(4).split(",")]
                
                stats["recent_enhancements"].append({
                    "algorithm": algorithm,
                    "sections": sections,
                    "index": int(match.group(1)),
                })
                if len(stats["recent_enhancements"]) > 10:
                    stats["recent_enhancements"].pop(0)
                
                for section in sections:
                    stats["section_counts"][section] = (
                        stats["section_counts"].get(section, 0) + 1
                    )
                
                stats["last_update"] = datetime.now()
                continue
            
            # Progress line
            match = re.search(
                r"\[PROGRESS\].*Enhanced (\d+)/(\d+).*\((\d+)%\)", line
            )
            if match:
                stats["total_enhanced"] = int(match.group(1))
                stats["total_processed"] = int(match.group(2))
                stats["last_update"] = datetime.now()
                continue
            
            # Complete line
            match = re.search(r"\[COMPLETE\].*Enhanced (\d+)/(\d+)", line)
            if match:
                stats["complete"] = True
                stats["total_enhanced"] = int(match.group(1))
                stats["total_processed"] = int(match.group(2))
                stats["last_update"] = datetime.now()
                break
    
    except Exception as e:
        print(f"Error reading log: {e}")
    
    return stats


def print_progress_report(stats: Dict, start_time: datetime):
    """Print formatted progress report."""
    elapsed = datetime.now() - start_time
    
    print("\n" + "=" * 70)
    print(
        f"📊 PROGRESS REPORT - "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    print("=" * 70)
    
    if stats["complete"]:
        print("✅ PROCESS COMPLETE!")
        print(
            f"Total Enhanced: {stats['total_enhanced']}/"
            f"{stats['total_processed']}"
        )
        if stats["total_processed"] > 0:
            percentage = (
                stats["total_enhanced"] * 100 // stats["total_processed"]
            )
            print(f"Success Rate: {percentage}%")
    else:
        if not stats["has_activity"]:
            print("⏳ Status: Process is starting up...")
            print("   Waiting for first enhancement to appear in log.")
        else:
            print(f"⏱️  Elapsed Time: {elapsed}")
            
            if stats["total_processed"] > 0:
                print(f"📁 Processed: {stats['total_processed']} files")
                print(f"✅ Enhanced: {stats['total_enhanced']} files")
                
                percentage = (
                    stats["total_enhanced"] * 100 // stats["total_processed"]
                )
                print(f"📈 Success Rate: {percentage}%")
                
                # Estimate remaining
                if elapsed.total_seconds() > 0:
                    rate = stats["total_processed"] / elapsed.total_seconds()
                    estimated_total = 693
                    remaining = estimated_total - stats["total_processed"]
                    if rate > 0 and remaining > 0:
                        remaining_sec = remaining / rate
                        remaining_time = timedelta(seconds=int(remaining_sec))
                        print(f"⏳ Estimated Remaining: {remaining_time}")
            else:
                print("Status: Waiting for first file to be processed...")
        
        if stats["last_update"]:
            time_since_update = datetime.now() - stats["last_update"]
            if time_since_update.total_seconds() < 60:
                print(
                    f"🔄 Last update: {time_since_update.seconds} seconds ago"
                )
            else:
                print(
                    f"🔄 Last update: "
                    f"{int(time_since_update.total_seconds() / 60)} "
                    f"minutes ago"
                )
    
    if stats["section_counts"]:
        print("\n📈 Top Enhanced Sections:")
        for section, count in sorted(
            stats["section_counts"].items(), key=lambda x: -x[1]
        )[:5]:
            print(f"   - {section}: {count} files")
    
    if stats["recent_enhancements"]:
        print("\n🔄 Recent Enhancements (last 5):")
        for enh in stats["recent_enhancements"][-5:]:
            sections = ", ".join(enh["sections"])
            print(
                f"   - {enh['algorithm']} ({sections}) "
                f"[{enh['index']}]"
            )
    
    print("=" * 70 + "\n")


def main():
    """Monitor and report progress every 5 minutes."""
    print("=" * 70)
    print("🚀 Enhancement Progress Monitor")
    print("=" * 70)
    print("Reports will be generated every 5 minutes.")
    print("Press Ctrl+C to stop monitoring.\n")
    
    start_time = datetime.now()
    report_interval = 300  # 5 minutes in seconds
    last_report_time = start_time
    
    # Initial report
    print("Initial status check...")
    stats = get_progress_stats()
    print_progress_report(stats, start_time)
    last_report_time = datetime.now()
    
    try:
        while True:
            current_time = datetime.now()
            
            # Check if it's time for a report
            elapsed_since_last = (current_time - last_report_time).total_seconds()
            if elapsed_since_last >= report_interval:
                stats = get_progress_stats()
                print_progress_report(stats, start_time)
                last_report_time = current_time
                
                # If complete, exit
                if stats["complete"]:
                    print("✅ Enhancement process completed. Exiting monitor.")
                    break
            
            # Wait 30 seconds before checking again
            time.sleep(30)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Monitor stopped by user.")
        stats = get_progress_stats()
        print_progress_report(stats, start_time)


if __name__ == "__main__":
    main()

