#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Monitor enhancement progress and report every 5 minutes.
"""

import time
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Optional

LOG_FILE = Path(__file__).resolve().parents[1] / "logs" / "enhancement_progress.log"
LOG_FILE.parent.mkdir(exist_ok=True)


def parse_log_line(line: str) -> Optional[Dict]:
    """Parse a log line to extract progress information."""
    # Pattern: [123/693] ✓ Enhanced: algorithm_name (Section1, Section2)
    enhanced_pattern = r"\[(\d+)/(\d+)\].*✓ Enhanced: (\w+).*\(([^)]+)\)"
    match = re.search(enhanced_pattern, line)
    
    if match:
        return {
            "type": "enhanced",
            "current": int(match.group(1)),
            "total": int(match.group(2)),
            "algorithm": match.group(3),
            "sections": [s.strip() for s in match.group(4).split(",")],
        }
    
    # Pattern: [PROGRESS] Enhanced 50/100 README files (50%)
    progress_pattern = r"\[PROGRESS\].*Enhanced (\d+)/(\d+).*\((\d+)%\)"
    match = re.search(progress_pattern, line)
    
    if match:
        return {
            "type": "progress",
            "enhanced": int(match.group(1)),
            "processed": int(match.group(2)),
            "percentage": int(match.group(3)),
        }
    
    # Pattern: [COMPLETE] Enhanced 350/693 README files
    complete_pattern = r"\[COMPLETE\].*Enhanced (\d+)/(\d+)"
    match = re.search(complete_pattern, line)
    
    if match:
        return {
            "type": "complete",
            "enhanced": int(match.group(1)),
            "total": int(match.group(2)),
        }
    
    return None


def get_latest_stats(log_file: Path) -> Dict:
    """Get latest statistics from log file."""
    stats = {
        "last_enhanced": None,
        "last_progress": None,
        "complete": False,
        "total_enhanced": 0,
        "total_processed": 0,
        "percentage": 0,
        "section_counts": {},
        "recent_enhancements": [],
    }
    
    if not log_file.exists():
        return stats
    
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        # Process lines in reverse to get latest stats
        for line in reversed(lines):
            parsed = parse_log_line(line)
            
            if parsed:
                if parsed["type"] == "complete":
                    stats["complete"] = True
                    stats["total_enhanced"] = parsed["enhanced"]
                    stats["total_processed"] = parsed["total"]
                    stats["percentage"] = (
                        parsed["enhanced"] * 100 // parsed["total"]
                        if parsed["total"] > 0
                        else 0
                    )
                    break
                
                elif parsed["type"] == "progress":
                    if not stats["last_progress"]:
                        stats["last_progress"] = parsed
                        stats["total_enhanced"] = parsed["enhanced"]
                        stats["total_processed"] = parsed["processed"]
                        stats["percentage"] = parsed["percentage"]
                
                elif parsed["type"] == "enhanced":
                    if not stats["last_enhanced"]:
                        stats["last_enhanced"] = parsed
                    
                    # Track recent enhancements (last 10)
                    if len(stats["recent_enhancements"]) < 10:
                        stats["recent_enhancements"].insert(0, parsed)
                    
                    # Count sections
                    for section in parsed["sections"]:
                        stats["section_counts"][section] = (
                            stats["section_counts"].get(section, 0) + 1
                        )
        
        # If we have last_enhanced but no progress, estimate
        if stats["last_enhanced"] and not stats["last_progress"]:
            stats["total_processed"] = stats["last_enhanced"]["current"]
            stats["total_enhanced"] = sum(
                1 for e in stats["recent_enhancements"]
                if e["type"] == "enhanced"
            )
            if stats["total_processed"] > 0:
                stats["percentage"] = (
                    stats["total_enhanced"] * 100 // stats["total_processed"]
                )
    
    except Exception as e:
        print(f"Error reading log file: {e}")
    
    return stats


def format_progress_report(stats: Dict, elapsed: timedelta) -> str:
    """Format a progress report."""
    report = []
    report.append("=" * 70)
    report.append(f"Enhancement Progress Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("=" * 70)
    report.append("")
    
    if stats["complete"]:
        report.append("✅ PROCESS COMPLETE")
        report.append("")
        report.append(f"Total Enhanced: {stats['total_enhanced']}/{stats['total_processed']}")
        report.append(f"Success Rate: {stats['percentage']}%")
    else:
        report.append("📊 CURRENT STATUS")
        report.append("")
        if stats["last_progress"]:
            report.append(
                f"Processed: {stats['total_processed']} files "
                f"({stats['percentage']}% success rate)"
            )
            report.append(f"Enhanced: {stats['total_enhanced']} files")
        elif stats["last_enhanced"]:
            report.append(
                f"Processed: {stats['last_enhanced']['current']}/{stats['last_enhanced']['total']} files"
            )
            report.append(f"Enhanced: {stats['total_enhanced']} files")
        else:
            report.append("Status: Starting up...")
        
        report.append("")
        report.append(f"⏱️  Elapsed Time: {elapsed}")
        
        # Estimate remaining time
        if stats["last_enhanced"] and stats["total_enhanced"] > 0:
            total = stats["last_enhanced"]["total"]
            processed = stats["last_enhanced"]["current"]
            remaining = total - processed
            
            if processed > 0 and elapsed.total_seconds() > 0:
                rate = processed / elapsed.total_seconds()  # files per second
                if rate > 0:
                    remaining_seconds = remaining / rate
                    remaining_time = timedelta(seconds=int(remaining_seconds))
                    report.append(f"⏳ Estimated Remaining: {remaining_time}")
    
    report.append("")
    
    # Section statistics
    if stats["section_counts"]:
        report.append("📈 Section Enhancement Statistics:")
        for section, count in sorted(
            stats["section_counts"].items(), key=lambda x: -x[1]
        )[:5]
        ):
            report.append(f"   - {section}: {count} files")
        report.append("")
    
    # Recent enhancements
    if stats["recent_enhancements"]:
        report.append("🔄 Recent Enhancements (last 5):")
        for enh in stats["recent_enhancements"][:5]:
            sections = ", ".join(enh["sections"])
            report.append(
                f"   - {enh['algorithm']} ({sections}) "
                f"[{enh['current']}/{enh['total']}]"
            )
        report.append("")
    
    report.append("=" * 70)
    
    return "\n".join(report)


def main():
    """Monitor enhancement progress and report every 5 minutes."""
    print("Starting enhancement progress monitor...")
    print(f"Log file: {LOG_FILE}")
    print("Reports will be generated every 5 minutes.\n")
    
    start_time = datetime.now()
    last_report_time = start_time
    report_interval = timedelta(minutes=5)
    
    while True:
        current_time = datetime.now()
        elapsed = current_time - start_time
        
        # Check if it's time for a report
        if current_time - last_report_time >= report_interval:
            stats = get_latest_stats(LOG_FILE)
            report = format_progress_report(stats, elapsed)
            
            print(report)
            print()
            
            # Save report to file
            report_file = LOG_FILE.parent / "enhancement_reports.log"
            with open(report_file, "a", encoding="utf-8") as f:
                f.write(report + "\n\n")
            
            last_report_time = current_time
            
            # If complete, exit
            if stats["complete"]:
                print("Enhancement process completed. Exiting monitor.")
                break
        
        # Check if process is still running (simple check)
        # In a real scenario, you'd check the process ID
        time.sleep(30)  # Check every 30 seconds


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nMonitor stopped by user.")


